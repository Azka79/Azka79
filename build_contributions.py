#!/usr/bin/env python3
"""Generates assets/contributions-{dark,light}.svg from live GitHub contribution data.

Reads GITHUB_TOKEN and GH_USER from the environment. Uses the GitHub GraphQL API
(contributionsCollection) and renders a heatmap in the profile's blue palette with
dark/light variants that match build_assets.py.

Run locally:
    GITHUB_TOKEN=... GH_USER=Azka79 python3 build_contributions.py
In CI this is executed by .github/workflows/update-contributions.yml, which commits
the generated SVGs so the profile README can embed them.
"""
import os, sys, json, urllib.request, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
os.makedirs(A, exist_ok=True)
FONT = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

# Blue scales kept in sync with build_assets.py (index 0 = empty .. 4 = most).
T = {
    "dark": dict(ink="#e8eef7", muted="#8a97aa", line="#222b3a",
                 h=["#1a212d", "#2b4468", "#4a76ad", "#6fa3dd", "#aad2ff"]),
    "light": dict(ink="#0e1a2b", muted="#566a85", line="#d6e0ee",
                  h=["#e3e9f2", "#bcd3f1", "#86b0e6", "#4f8bd6", "#1f5fb4"]),
}

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

MN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "azka-profile-bot",
        },
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if data.get("errors"):
        sys.exit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def level(count, mx):
    if count <= 0:
        return 0
    if count <= mx * 0.25:
        return 1
    if count <= mx * 0.50:
        return 2
    if count <= mx * 0.75:
        return 3
    return 4


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONT}" role="img">{body}</svg>')


def render(cal, t):
    weeks = cal["weeks"]
    total = cal["totalContributions"]
    days = [d for w in weeks for d in w["contributionDays"]]
    mx = max((d["contributionCount"] for d in days), default=1) or 1

    left, top, cell, gap = 46, 48, 11, 3
    cols, rows = len(weeks), 7
    W = left + cols * (cell + gap) + 20
    H = top + rows * (cell + gap) + 40

    b = f'<text x="16" y="26" font-size="16" font-weight="600" fill="{t["ink"]}">{total} contributions in the last year</text>'

    # Weekday labels (Mon / Wed / Fri).
    for i, lab in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = top + i * (cell + gap) + cell - 2
        b += f'<text x="{left-8}" y="{y}" font-size="9" fill="{t["muted"]}" text-anchor="end">{lab}</text>'

    # Month labels along the top.
    last = None
    for c, w in enumerate(weeks):
        d = datetime.date.fromisoformat(w["contributionDays"][0]["date"])
        if d.day <= 7 and (last is None or d.month != last):
            x = left + c * (cell + gap)
            b += f'<text x="{x}" y="{top-10}" font-size="9" fill="{t["muted"]}">{MN[d.month-1]}</text>'
            last = d.month

    # Heatmap cells.
    for c, w in enumerate(weeks):
        for r, d in enumerate(w["contributionDays"]):
            x = left + c * (cell + gap)
            y = top + r * (cell + gap)
            b += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{t["h"][level(d["contributionCount"], mx)]}"/>'

    # Legend.
    ly = top + rows * (cell + gap) + 8
    b += f'<text x="{left}" y="{ly+10}" font-size="9" fill="{t["muted"]}">Less</text>'
    for k in range(5):
        x = left + 40 + k * 18
        b += f'<rect x="{x}" y="{ly}" width="11" height="11" rx="2" fill="{t["h"][k]}"/>'
    b += f'<text x="{left+40+5*18+6}" y="{ly+10}" font-size="9" fill="{t["muted"]}">More</text>'

    return svg(W, H, b)


def main():
    token = os.environ.get("GITHUB_TOKEN")
    login = os.environ.get("GH_USER", "Azka79")
    if not token:
        sys.exit("GITHUB_TOKEN is required")
    cal = fetch(login, token)
    for mode, t in T.items():
        with open(os.path.join(A, f"contributions-{mode}.svg"), "w", encoding="utf-8") as f:
            f.write(render(cal, t))
    print("ok", cal["totalContributions"])


if __name__ == "__main__":
    main()