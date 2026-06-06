#!/usr/bin/env python3
"""
Archpilot → Jira / Azure DevOps Push

Parses .specs/requirements.md and creates Epics and User Stories
in the target issue tracker. A push manifest (.specs/push_manifest.json)
tracks created IDs so re-running is idempotent — already-pushed items
are skipped.

Usage (via archpilot CLI):
  archpilot push --target jira [--dir .] [--dry-run] [--epics-only]
  archpilot push --target ado  [--dir .] [--dry-run] [--epics-only]

Jira environment variables:
  JIRA_URL           https://yourorg.atlassian.net
  JIRA_EMAIL         your Atlassian account email
  JIRA_API_TOKEN     API token (id.atlassian.com → Security → API tokens)
  JIRA_PROJECT_KEY   e.g. ARCH

ADO environment variables:
  ADO_ORG            org slug from dev.azure.com/<org>
  ADO_PROJECT        project name e.g. ArchProject
  ADO_PAT            Personal Access Token (Work Items: Read & Write)
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


# ─── Config loader ────────────────────────────────────────────────────────────

_CONFIG_SEARCH = [
    ".archpilot.env",          # project-level (gitignored)
    "archpilot.env",
    os.path.expanduser("~/.archpilot.env"),  # user-level
]

def load_config(project_dir: str = ".") -> None:
    """
    Load key=value pairs from the first .archpilot.env file found into os.environ.
    Already-set environment variables are NOT overwritten (env takes priority).

    Search order:
      1. <project_dir>/.archpilot.env
      2. <project_dir>/archpilot.env
      3. ~/.archpilot.env

    File format (shell-style, no export keyword needed):
      JIRA_URL=https://yourorg.atlassian.net
      JIRA_EMAIL=you@example.com
      JIRA_API_TOKEN=your_token_here
      JIRA_PROJECT_KEY=ARCH
      # lines starting with # are comments
    """
    candidates = [
        os.path.join(project_dir, ".archpilot.env"),
        os.path.join(project_dir, "archpilot.env"),
        os.path.expanduser("~/.archpilot.env"),
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            _parse_env_file(path)
            return


def _parse_env_file(path: Path) -> None:
    loaded = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip().lstrip("export ").strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val
            loaded.append(key)


# ─── Data model ───────────────────────────────────────────────────────────────

@dataclass
class Story:
    id: str              # EP-01-S-01
    epic_id: str         # EP-01
    title: str
    as_a: str
    i_want: str
    so_that: str
    priority: str        # Must / Should / Could / Won't
    story_points: int
    nfr_tags: list
    discovery_refs: list
    acceptance_criteria: list

@dataclass
class Epic:
    id: str              # EP-01
    title: str
    category: str        # FUNCTIONAL / DATA & STORAGE / etc.
    business_value: str
    definition_of_done: list
    discovery_refs: list
    stories: list = field(default_factory=list)


# ─── Parser ───────────────────────────────────────────────────────────────────

_EPIC_HDR  = re.compile(r'^## (EP-\d+):\s+(.+)$',      re.MULTILINE)
_STORY_HDR = re.compile(r'^### (EP-\d+-S-\d+):\s+(.+)$', re.MULTILINE)
_BQ_FIELD  = re.compile(r'^>\s*\*\*(.+?):\*\*\s*(.*)')
_TBL_FIELD = re.compile(r'^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|')
_NFR_TAG   = re.compile(r'\[([^\]]+)\]')
_AC_LINE   = re.compile(r'^\d+\.\s+(.+)$')


def parse_requirements(path: Path) -> list:
    """Parse requirements.md → list of Epic (with nested Story objects)."""
    text = path.read_text(encoding="utf-8", errors="ignore")

    # Split on H2 epic headings; keep delimiter
    parts = re.split(r'(?=\n## EP-\d+:)', text)

    epics: list = []
    for chunk in parts:
        m = _EPIC_HDR.search(chunk)
        if not m:
            continue
        epic_id    = m.group(1)
        epic_title = m.group(2).strip()

        # Parse blockquote metadata (> **Key:** value)
        bq = _parse_blockquote(chunk)
        dod_raw = bq.get("Definition of Done", [])
        dod = dod_raw if isinstance(dod_raw, list) else [dod_raw]

        refs_raw = bq.get("Discovery Ref", "")
        refs = [r.strip() for r in refs_raw.split(",")] if refs_raw else []

        epic = Epic(
            id=epic_id,
            title=epic_title,
            category=bq.get("Category", "FUNCTIONAL"),
            business_value=bq.get("Business Value", ""),
            definition_of_done=[d for d in dod if d],
            discovery_refs=refs,
        )

        # Split on H3 story headings within this epic chunk
        story_parts = re.split(r'(?=\n### EP-)', chunk)
        for spart in story_parts:
            sm = _STORY_HDR.search(spart)
            if not sm:
                continue
            story = _parse_story(sm.group(1), epic_id, sm.group(2).strip(), spart)
            epic.stories.append(story)

        epics.append(epic)

    return epics


def _parse_blockquote(text: str) -> dict:
    fields: dict = {}
    current_key = None
    current_vals: list = []

    for line in text.splitlines():
        if not line.startswith(">"):
            if current_key:
                fields[current_key] = current_vals if len(current_vals) != 1 else current_vals[0]
                current_key = None
                current_vals = []
            continue

        content = line[1:].strip()
        m = _BQ_FIELD.match(line)
        if m:
            if current_key:
                fields[current_key] = current_vals if len(current_vals) != 1 else current_vals[0]
            current_key = m.group(1)
            val = m.group(2).strip()
            current_vals = [val] if val else []
        elif content.startswith("- ") and current_key:
            current_vals.append(content[2:].strip())
        elif content and current_key:
            current_vals.append(content)

    if current_key:
        fields[current_key] = current_vals if len(current_vals) != 1 else current_vals[0]
    return fields


def _parse_story(story_id: str, epic_id: str, title: str, text: str) -> Story:
    # Parse the markdown table fields
    tbl: dict = {}
    for line in text.splitlines():
        m = _TBL_FIELD.match(line)
        if m:
            tbl[m.group(1).strip()] = m.group(2).strip()

    # Acceptance Criteria — numbered list after **Acceptance Criteria:**
    ac: list = []
    in_ac = False
    for line in text.splitlines():
        if "**Acceptance Criteria:**" in line:
            in_ac = True
            continue
        if in_ac:
            m = _AC_LINE.match(line.strip())
            if m:
                ac.append(m.group(1))
            elif line.strip().startswith("#"):
                break  # next heading

    nfr_tags = _NFR_TAG.findall(tbl.get("NFR Tags", ""))
    refs = [r.strip() for r in tbl.get("Discovery Ref", "").split(",") if r.strip()]

    try:
        pts = int(tbl.get("Story Points", "3"))
    except ValueError:
        pts = 3

    return Story(
        id=story_id,
        epic_id=epic_id,
        title=title,
        as_a=tbl.get("As a", ""),
        i_want=tbl.get("I want", ""),
        so_that=tbl.get("So that", ""),
        priority=tbl.get("Priority", "Should"),
        story_points=pts,
        nfr_tags=nfr_tags,
        discovery_refs=refs,
        acceptance_criteria=ac,
    )


# ─── HTTP helper ──────────────────────────────────────────────────────────────

def _http(method: str, url: str, headers: dict, body=None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req  = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="ignore")
        raise RuntimeError(f"HTTP {e.code} {method} {url}\n{raw}") from e


# ─── Manifest (idempotency) ───────────────────────────────────────────────────

def _load_manifest(specs_dir: Path) -> dict:
    p = specs_dir / "push_manifest.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"epics": {}, "stories": {}}


def _save_manifest(specs_dir: Path, manifest: dict, target: str, project: str) -> None:
    manifest["target"]      = target
    manifest["project"]     = project
    manifest["pushed_at"]   = datetime.now(timezone.utc).isoformat()
    (specs_dir / "push_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


# ─── Jira ─────────────────────────────────────────────────────────────────────

_JIRA_PRIORITY = {"Must": "Highest", "Should": "High", "Could": "Medium", "Won't": "Low"}


def push_jira(specs_dir: Path, epics: list, dry_run: bool, epics_only: bool) -> None:
    url    = os.environ["JIRA_URL"].rstrip("/")
    email  = os.environ["JIRA_EMAIL"]
    token  = os.environ["JIRA_API_TOKEN"]
    proj   = os.environ["JIRA_PROJECT_KEY"]

    creds   = base64.b64encode(f"{email}:{token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    api = f"{url}/rest/api/2"

    manifest = _load_manifest(specs_dir)
    total_epics = total_stories = skipped = 0

    print(f"\nArchpilot → Jira  {'[DRY RUN] ' if dry_run else ''}")
    print(f"  Project  : {proj}  ({url})")
    print(f"  Epics    : {len(epics)}")
    print(f"  Stories  : {sum(len(e.stories) for e in epics)}")
    print()

    # ── Phase 1: Epics ──────────────────────────────────────────────────────
    print("Phase 1/2: Creating Epics...")
    for epic in epics:
        if epic.id in manifest["epics"]:
            print(f"  [SKIP] {epic.id}  already pushed → {manifest['epics'][epic.id]['key']}")
            skipped += 1
            continue

        desc = (
            f"Category: {epic.category}\n\n"
            f"{epic.business_value}\n\n"
            f"Discovery: {', '.join(epic.discovery_refs)}\n\n"
            f"Definition of Done:\n" + "\n".join(f"  - {d}" for d in epic.definition_of_done)
            + "\n\n_Created by Archpilot_"
        )
        payload = {
            "fields": {
                "project":     {"key": proj},
                "summary":     f"[{epic.id}] {epic.title}",
                "description": desc,
                "issuetype":   {"name": "Epic"},
                "customfield_10014": epic.title,  # Epic Name (Jira Cloud classic)
                "labels": ["archpilot", epic.category.lower().replace(" & ", "-").replace(" ", "-")],
            }
        }
        if dry_run:
            print(f"  [DRY]  {epic.id}  {epic.title}")
            manifest["epics"][epic.id] = {"key": f"{proj}-???", "dry_run": True}
            continue

        try:
            resp = _http("POST", f"{api}/issue", headers, payload)
            key  = resp["key"]
            manifest["epics"][epic.id] = {"key": key, "id": resp["id"], "url": f"{url}/browse/{key}"}
            print(f"  [OK]   {epic.id} → {key}  {epic.title}")
            total_epics += 1
        except RuntimeError as e:
            print(f"  [ERR]  {epic.id}: {str(e)[:120]}")

    if epics_only:
        if not dry_run:
            _save_manifest(specs_dir, manifest, "jira", proj)
        _summary(total_epics, 0, skipped, dry_run, specs_dir)
        return

    # ── Phase 2: Stories ────────────────────────────────────────────────────
    print("\nPhase 2/2: Creating Stories...")
    for epic in epics:
        epic_key = manifest["epics"].get(epic.id, {}).get("key")
        for story in epic.stories:
            if story.id in manifest["stories"]:
                print(f"  [SKIP] {story.id}  already pushed → {manifest['stories'][story.id]['key']}")
                skipped += 1
                continue

            ac_text = "\n".join(f"{i+1}. {c}" for i, c in enumerate(story.acceptance_criteria))
            desc = (
                f"*As a* {story.as_a},\n"
                f"*I want* {story.i_want},\n"
                f"*so that* {story.so_that}.\n\n"
                f"Discovery: {', '.join(story.discovery_refs)}\n\n"
                f"*Acceptance Criteria:*\n{ac_text}\n\n"
                f"_Created by Archpilot from requirements.md_"
            )
            payload: dict = {
                "fields": {
                    "project":     {"key": proj},
                    "summary":     f"[{story.id}] {story.title}",
                    "description": desc,
                    "issuetype":   {"name": "Story"},
                    "priority":    {"name": _JIRA_PRIORITY.get(story.priority, "Medium")},
                    "story_points": story.story_points,
                    "labels": ["archpilot"] + [t.lower() for t in story.nfr_tags],
                }
            }
            # Link to epic
            if epic_key and not epic_key.endswith("???"):
                payload["fields"]["customfield_10014"] = epic_key  # classic epic link
                payload["fields"]["parent"] = {"key": epic_key}    # next-gen parent

            if dry_run:
                print(f"  [DRY]  {story.id}  {story.title}")
                manifest["stories"][story.id] = {"key": f"{proj}-???", "dry_run": True}
                continue

            try:
                resp = _http("POST", f"{api}/issue", headers, payload)
                key  = resp["key"]
                manifest["stories"][story.id] = {"key": key, "id": resp["id"], "url": f"{url}/browse/{key}"}
                print(f"  [OK]   {story.id} → {key}  {story.title}")
                total_stories += 1
            except RuntimeError as e:
                print(f"  [ERR]  {story.id}: {str(e)[:120]}")

    if not dry_run:
        _save_manifest(specs_dir, manifest, "jira", proj)
    _summary(total_epics, total_stories, skipped, dry_run, specs_dir)


# ─── Azure DevOps ─────────────────────────────────────────────────────────────

_ADO_PRIORITY = {"Must": 1, "Should": 2, "Could": 3, "Won't": 4}


def push_ado(specs_dir: Path, epics: list, dry_run: bool, epics_only: bool) -> None:
    org     = os.environ["ADO_ORG"]
    project = urllib.parse.quote(os.environ["ADO_PROJECT"])
    pat     = os.environ["ADO_PAT"]

    import urllib.parse
    creds   = base64.b64encode(f":{pat}".encode()).decode()
    headers_patch = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json-patch+json",
    }
    base = f"https://dev.azure.com/{org}/{project}/_apis/wit/workitems"
    ver  = "?api-version=7.1"

    manifest = _load_manifest(specs_dir)
    total_epics = total_stories = skipped = 0

    print(f"\nArchpilot → Azure DevOps  {'[DRY RUN] ' if dry_run else ''}")
    print(f"  Org      : {org}")
    print(f"  Project  : {os.environ['ADO_PROJECT']}")
    print(f"  Epics    : {len(epics)}")
    print(f"  Stories  : {sum(len(e.stories) for e in epics)}")
    print()

    # ── Phase 1: Epics ──────────────────────────────────────────────────────
    print("Phase 1/2: Creating Epics...")
    for epic in epics:
        if epic.id in manifest["epics"]:
            print(f"  [SKIP] {epic.id}  already pushed → #{manifest['epics'][epic.id]['id']}")
            skipped += 1
            continue

        dod_html = "<ul>" + "".join(f"<li>{d}</li>" for d in epic.definition_of_done) + "</ul>"
        desc_html = (
            f"<p><strong>Category:</strong> {epic.category}</p>"
            f"<p>{epic.business_value}</p>"
            f"<p><strong>Discovery:</strong> {', '.join(epic.discovery_refs)}</p>"
            f"<p><strong>Definition of Done:</strong></p>{dod_html}"
            f"<p><em>Created by Archpilot</em></p>"
        )
        ops = [
            {"op": "add", "path": "/fields/System.Title",       "value": f"[{epic.id}] {epic.title}"},
            {"op": "add", "path": "/fields/System.Description", "value": desc_html},
            {"op": "add", "path": "/fields/System.Tags",        "value": f"archpilot; {epic.category.lower()}"},
        ]

        if dry_run:
            print(f"  [DRY]  {epic.id}  {epic.title}")
            manifest["epics"][epic.id] = {"id": "???", "dry_run": True}
            continue

        try:
            resp = _http("PATCH", f"{base}/$Epic{ver}", headers_patch, ops)
            eid  = resp["id"]
            manifest["epics"][epic.id] = {
                "id":  eid,
                "url": resp.get("url", ""),
                "web": f"https://dev.azure.com/{org}/{os.environ['ADO_PROJECT']}/_workitems/edit/{eid}",
            }
            print(f"  [OK]   {epic.id} → #{eid}  {epic.title}")
            total_epics += 1
        except RuntimeError as e:
            print(f"  [ERR]  {epic.id}: {str(e)[:120]}")

    if epics_only:
        if not dry_run:
            _save_manifest(specs_dir, manifest, "ado", os.environ["ADO_PROJECT"])
        _summary(total_epics, 0, skipped, dry_run, specs_dir)
        return

    # ── Phase 2: Stories ────────────────────────────────────────────────────
    print("\nPhase 2/2: Creating Stories...")
    for epic in epics:
        epic_ado_id = manifest["epics"].get(epic.id, {}).get("id")
        for story in epic.stories:
            if story.id in manifest["stories"]:
                print(f"  [SKIP] {story.id}  already pushed → #{manifest['stories'][story.id]['id']}")
                skipped += 1
                continue

            ac_html = "<ol>" + "".join(f"<li>{c}</li>" for c in story.acceptance_criteria) + "</ol>"
            desc_html = (
                f"<p><strong>As a</strong> {story.as_a},<br/>"
                f"<strong>I want</strong> {story.i_want},<br/>"
                f"<strong>so that</strong> {story.so_that}.</p>"
                f"<p><strong>Discovery:</strong> {', '.join(story.discovery_refs)}</p>"
                f"<p><em>Created by Archpilot from requirements.md</em></p>"
            )
            ops: list = [
                {"op": "add", "path": "/fields/System.Title",       "value": f"[{story.id}] {story.title}"},
                {"op": "add", "path": "/fields/System.Description", "value": desc_html},
                {"op": "add", "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria", "value": ac_html},
                {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints",   "value": story.story_points},
                {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority",          "value": _ADO_PRIORITY.get(story.priority, 2)},
                {"op": "add", "path": "/fields/System.Tags",
                 "value": "archpilot; " + "; ".join(t.lower() for t in story.nfr_tags)},
            ]
            # Parent link to epic
            if epic_ado_id and epic_ado_id != "???":
                ops.append({
                    "op":    "add",
                    "path":  "/relations/-",
                    "value": {
                        "rel": "System.LinkTypes.Hierarchy-Reverse",
                        "url": f"https://dev.azure.com/{org}/_apis/wit/workItems/{epic_ado_id}",
                        "attributes": {"comment": "Archpilot epic link"},
                    },
                })

            if dry_run:
                print(f"  [DRY]  {story.id}  {story.title}")
                manifest["stories"][story.id] = {"id": "???", "dry_run": True}
                continue

            try:
                resp = _http("PATCH", f"{base}/$User%20Story{ver}", headers_patch, ops)
                sid  = resp["id"]
                manifest["stories"][story.id] = {
                    "id":  sid,
                    "url": resp.get("url", ""),
                    "web": f"https://dev.azure.com/{org}/{os.environ['ADO_PROJECT']}/_workitems/edit/{sid}",
                }
                print(f"  [OK]   {story.id} → #{sid}  {story.title}")
                total_stories += 1
            except RuntimeError as e:
                print(f"  [ERR]  {story.id}: {str(e)[:120]}")

    if not dry_run:
        _save_manifest(specs_dir, manifest, "ado", os.environ["ADO_PROJECT"])
    _summary(total_epics, total_stories, skipped, dry_run, specs_dir)


# ─── Shared output ────────────────────────────────────────────────────────────

def _summary(epics: int, stories: int, skipped: int, dry_run: bool, specs_dir: Path) -> None:
    tag = " (dry run — nothing created)" if dry_run else ""
    print(f"\nDone{tag}")
    print(f"  Epics pushed  : {epics}")
    print(f"  Stories pushed: {stories}")
    print(f"  Skipped       : {skipped} (already in manifest)")
    if not dry_run:
        print(f"  Manifest      : {specs_dir / 'push_manifest.json'}")
    print()


# ─── Entry point ─────────────────────────────────────────────────────────────

def push(project_dir: str, target: str, dry_run: bool = False, epics_only: bool = False) -> None:
    # Load .archpilot.env before checking env vars (env always takes priority)
    load_config(project_dir)

    specs_dir = Path(project_dir) / ".specs"
    req_file  = specs_dir / "requirements.md"

    if not req_file.exists():
        print(f"Error: {req_file} not found. Run 'archpilot run' first.")
        sys.exit(1)

    # Check required env vars early
    if target == "jira":
        missing = [k for k in ("JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY")
                   if not os.environ.get(k)]
    else:
        missing = [k for k in ("ADO_ORG", "ADO_PROJECT", "ADO_PAT")
                   if not os.environ.get(k)]
    if missing:
        print(f"Error: missing environment variables: {', '.join(missing)}")
        print(f"See 'archpilot push --help' for setup instructions.")
        sys.exit(1)

    print(f"Parsing {req_file.name}...")
    epics = parse_requirements(req_file)
    if not epics:
        print("No epics found in requirements.md. Has the pipeline been run?")
        sys.exit(1)

    if target == "jira":
        push_jira(specs_dir, epics, dry_run, epics_only)
    else:
        push_ado(specs_dir, epics, dry_run, epics_only)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Push Archpilot requirements to Jira or ADO")
    p.add_argument("--target",      required=True, choices=["jira", "ado"])
    p.add_argument("--dir",         default=".", help="Project root (must contain .specs/)")
    p.add_argument("--dry-run",     action="store_true")
    p.add_argument("--epics-only",  action="store_true", help="Create epics only, skip stories")
    a = p.parse_args()
    push(a.dir, a.target, a.dry_run, a.epics_only)
