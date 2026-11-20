#!/usr/bin/env python3
"""Checks run in CI on every push: manifests parse, versions match, MCP servers are HTTPS on traxagent.io,
the local audit script uses no network modules, and every skill has a name and description."""
import ast, glob, json, re, sys

errors = []
manifests = sorted(set(glob.glob("**/plugin.json", recursive=True, include_hidden=True) + glob.glob(".claude-plugin/marketplace.json", include_hidden=True) + glob.glob("**/.mcp.json", recursive=True, include_hidden=True)))
manifests = [m for m in manifests if not m.startswith(".git/")]
data = {}
for p in manifests:
    try:
        data[p] = json.load(open(p))
    except Exception as e:
        errors.append(f"{p}: not valid JSON ({e})")
versions = {p: d["version"] for p, d in data.items() if p.endswith("plugin.json") and "version" in d}
if len(set(versions.values())) > 1:
    errors.append(f"plugin versions differ: {versions}")
for p, d in data.items():
    if p.endswith(".mcp.json"):
        for name, s in (d.get("mcpServers") or {}).items():
            if not re.match(r"^https://www\.traxagent\.io/", s.get("url", "")):
                errors.append(f"{p}: server {name} is not HTTPS on www.traxagent.io")
for p in glob.glob("**/scripts/*.py", recursive=True, include_hidden=True):
    if p.startswith("scripts/"):
        continue
    tree = ast.parse(open(p).read(), p)
    mods = {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    mods |= {(n.module or "").split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    bad = mods & {"socket", "urllib", "http", "requests", "httpx", "subprocess", "ftplib", "smtplib"}
    if bad:
        errors.append(f"{p}: imports {sorted(bad)}; the local script must not use the network or run commands")
for p in glob.glob("**/SKILL.md", recursive=True, include_hidden=True):
    head = open(p).read().split("---")
    if len(head) < 3 or "name:" not in head[1] or "description:" not in head[1]:
        errors.append(f"{p}: missing name or description in front matter")
if [h for h in glob.glob("**/hooks/*", recursive=True, include_hidden=True) if not h.startswith(".git/")] or any("hooks" in d for d in data.values()):
    errors.append("hooks found; this plugin ships none")
print("\n".join(errors) or f"ok: {len(data)} manifests, version {next(iter(set(versions.values())), '?')}")
sys.exit(1 if errors else 0)
