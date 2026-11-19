#!/usr/bin/env python3
"""Local Claude Code spend audit. Reads the session logs Claude Code keeps in ~/.claude/projects
and prices them at Anthropic list prices. Reads files only; sends nothing anywhere. Standard library only.

Usage: spend_audit.py [days]   (default 7)
"""
import glob, json, os, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

# $ per million tokens: (input, 5m cache write, 1h cache write, cache read, output). List prices, checked 2026-11-19.
PRICES = {
    "claude-fable-5-2": (8.0, 10.0, 16.0, 0.20, 40.0), "claude-fable-5-1": (10.0, 12.5, 20.0, 0.25, 50.0),
    "claude-fable-5": (10.0, 12.5, 20.0, 1.0, 50.0),
    "claude-opus-5-5": (4.0, 5.0, 8.0, 0.20, 20.0), "claude-opus-5": (5.0, 6.25, 10.0, 0.50, 25.0),
    "claude-opus-4-8": (5.0, 6.25, 10.0, 0.50, 25.0), "claude-opus-4-7": (5.0, 6.25, 10.0, 0.50, 25.0),
    "claude-opus-4-6": (5.0, 6.25, 10.0, 0.50, 25.0), "claude-opus-4-5": (5.0, 6.25, 10.0, 0.50, 25.0),
    "claude-opus-4-1": (15.0, 18.75, 30.0, 1.50, 75.0), "claude-opus-4": (15.0, 18.75, 30.0, 1.50, 75.0),
    "claude-sonnet-5-5": (2.0, 2.5, 4.0, 0.10, 10.0), "claude-sonnet-5": (2.0, 2.5, 4.0, 0.20, 10.0),
    "claude-sonnet-4-6": (3.0, 3.75, 6.0, 0.30, 15.0), "claude-sonnet-4-5": (3.0, 3.75, 6.0, 0.30, 15.0),
    "claude-sonnet-4": (3.0, 3.75, 6.0, 0.30, 15.0),
    "claude-haiku-5-5": (0.10, 0.125, 0.20, 0.01, 0.50), "claude-haiku-4-5": (1.0, 1.25, 2.0, 0.10, 5.0),
    "claude-3-5-haiku": (0.80, 1.0, 1.60, 0.08, 4.0),
}
CHEAPER = {"opus": "claude-sonnet-5-5", "fable": "claude-opus-5-5"}


def rates(model):
    for k in sorted(PRICES, key=len, reverse=True):
        if model.startswith(k):
            return k, PRICES[k]
    return None, None


def tokens(u):
    parts = u.get("iterations") or [u]
    t = defaultdict(int)
    for p in parts:
        cc = p.get("cache_creation") or {}
        w1h = cc.get("ephemeral_1h_input_tokens", 0) or 0
        w5m = cc.get("ephemeral_5m_input_tokens", (p.get("cache_creation_input_tokens") or 0) - w1h) or 0
        t["in"] += p.get("input_tokens") or 0
        t["w5m"] += w5m
        t["w1h"] += w1h
        t["read"] += p.get("cache_read_input_tokens") or 0
        t["out"] += p.get("output_tokens") or 0
    return t


def price(t, r):
    return (t["in"] * r[0] + t["w5m"] * r[1] + t["w1h"] * r[2] + t["read"] * r[3] + t["out"] * r[4]) / 1e6


def main():
    days = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
    since = datetime.now(timezone.utc) - timedelta(days=days)
    root = os.path.join(os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"), "projects")
    seen, by_model, by_project, by_session, by_day = set(), defaultdict(float), defaultdict(float), {}, defaultdict(float)
    tok, unknown, cheaper = defaultdict(int), set(), 0.0
    for path in glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True):
        if datetime.fromtimestamp(os.path.getmtime(path), timezone.utc) < since:
            continue
        try:
            f = open(path, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with f:
            for line in f:
                if '"usage"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                m = d.get("message") or {}
                u, model = m.get("usage"), m.get("model") or ""
                if not u or model.startswith("<"):
                    continue
                key = (m.get("id"), d.get("requestId"))
                if key in seen:
                    continue
                seen.add(key)
                try:
                    ts = datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00"))
                except (KeyError, ValueError):
                    continue
                if ts < since:
                    continue
                fam, r = rates(model)
                if not r:
                    unknown.add(model)
                    continue
                t = tokens(u)
                c = price(t, r)
                for k, v in t.items():
                    tok[k] += v
                by_model[fam] += c
                proj = os.path.basename(d.get("cwd") or "") or "?"
                by_project[proj] += c
                sid = d.get("sessionId") or path
                s = by_session.setdefault(sid, {"cost": 0.0, "project": proj, "start": ts, "msgs": 0})
                s["cost"] += c
                s["msgs"] += 1
                s["start"] = min(s["start"], ts)
                by_day[ts.astimezone().strftime("%a %b %d")] += c
                for word, alt in CHEAPER.items():
                    if word in fam:
                        cheaper += c - price(t, PRICES[alt])
    total = sum(by_model.values())
    print(f"Claude Code spend, last {days} days, at API list prices: ${total:,.2f}")
    if not total:
        print("No Claude Code usage found in", root)
        return
    print(f"About ${total / days:,.2f} a day, or ${total / days * 30:,.0f} a month at this pace.")
    print("If you're on a Pro or Max plan you pay a flat price; this is what the same work would cost through the API.\n")
    print("By model:")
    for k, v in sorted(by_model.items(), key=lambda x: -x[1]):
        print(f"  {k:<22} ${v:>10,.2f}  {v / total:5.0%}")
    print("\nBy project:")
    for k, v in sorted(by_project.items(), key=lambda x: -x[1])[:8]:
        print(f"  {k[:30]:<30} ${v:>10,.2f}")
    print("\nBy day:")
    for k, v in sorted(by_day.items(), key=lambda x: datetime.strptime(x[0] + f" {datetime.now().year}", "%a %b %d %Y")):
        print(f"  {k}  ${v:>9,.2f}  " + "#" * max(1, int(30 * v / max(by_day.values()))))
    print("\nMost expensive sessions:")
    for sid, s in sorted(by_session.items(), key=lambda x: -x[1]["cost"])[:5]:
        print(f"  ${s['cost']:>9,.2f}  {s['start'].astimezone():%b %d %H:%M}  {s['project'][:28]:<28} {s['msgs']} responses  ({sid[:8]})")
    reads = tok["read"]
    fresh = tok["in"] + tok["w5m"] + tok["w1h"]
    hit = reads / (reads + fresh) if reads + fresh else 0
    print(f"\nCache hit rate: {hit:.0%} of input tokens came from cache ({reads / 1e6:,.1f}M read, {fresh / 1e6:,.1f}M fresh or written).")
    print(f"Output tokens: {tok['out'] / 1e6:,.2f}M.")
    if cheaper > 1:
        print(f"Same work on one model tier down (Opus->Sonnet 5.5, Fable->Opus 5.5) would have cost ${cheaper:,.2f} less.")
    if unknown:
        print("Not priced (unknown model): " + ", ".join(sorted(unknown)))


if __name__ == "__main__":
    main()
