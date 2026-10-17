"""Generate profile artwork from three public repositories and a public calendar.

Standard library only. No private-repository discovery, analytics, or write API calls.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

OWNER = "PKHarsimran"
PROJECTS = (
    ("SwiftIOC-Automated-Threat-Intelligence-Collector", "SwiftIOC", "ci.yml", "#43E6C5"),
    ("IOC-Inspector", "IOC Inspector", "ci.yml", "#A995FF"),
    ("website-downloader", "Website Downloader", "python-app.yml", "#F36BAA"),
)
ALLOWLIST = frozenset(p[0] for p in PROJECTS)
BG, PANEL, BORDER, TEXT, MUTED = "#0D1117", "#121A26", "#29364B", "#EFF4FC", "#A7B6CE"


def github_json(repo: str, suffix: str = "", *, missing_ok: bool = False):
    if repo not in ALLOWLIST:
        raise ValueError("Repository is outside the explicit public allowlist")
    url = f"https://api.github.com/repos/{OWNER}/{repo}{suffix}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "PKHarsimran-profile-lab", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GH_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=20) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code == 404 and missing_ok:
                return None
            if exc.code in (401, 403) and "Authorization" in headers:
                # These are public endpoints; no broader token is needed.
                headers.pop("Authorization")
                continue
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except URLError:
            if attempt == 2:
                raise
        time.sleep(attempt + 1)
    raise RuntimeError("Public GitHub request could not be completed")


def ci_state(run: dict | None) -> str:
    if not run:
        return "NO RUNS"
    if run.get("status") != "completed":
        return "RUNNING" if run.get("status") == "in_progress" else "QUEUED"
    return {"success": "PASSING", "failure": "FAILING", "timed_out": "TIMED OUT", "cancelled": "CANCELLED", "skipped": "SKIPPED", "neutral": "NEUTRAL"}.get(run.get("conclusion"), "UNKNOWN")


def collect_project(spec, fetch=github_json):
    repo, name, workflow, color = spec
    meta = fetch(repo)
    if meta.get("private") is not False:
        raise ValueError("Refusing to publish metadata for a non-public repository")
    branch = meta["default_branch"]
    commits = fetch(repo, "/commits?" + urlencode({"sha": branch, "per_page": 1}))
    latest = commits[0] if commits else None
    base_url = f"https://github.com/{OWNER}/{repo}"
    record = {"repo": repo, "name": name, "color": color, "url": base_url, "default_branch": branch, "stars": max(0, int(meta["stargazers_count"])), "latest_commit_at": latest["commit"]["committer"]["date"] if latest else None, "release": None, "release_state": "unreleased", "release_url": base_url + "/releases", "ci": "UNAVAILABLE", "ci_url": base_url + "/actions/workflows/" + workflow}
    try:
        release = fetch(repo, "/releases/latest", missing_ok=True)
        if release:
            record.update(release=str(release["tag_name"]), release_state="published", release_url=base_url + "/releases/tag/" + quote(str(release["tag_name"]), safe=""))
    except (HTTPError, URLError, RuntimeError, KeyError, ValueError):
        record["release_state"] = "unavailable"
    try:
        runs = fetch(repo, "/actions/workflows/" + workflow + "/runs?" + urlencode({"branch": branch, "per_page": 1}))["workflow_runs"]
        record["ci"] = ci_state(runs[0] if runs else None)
        if runs:
            record["ci_url"] = base_url + "/actions/runs/" + str(int(runs[0]["id"]))
    except (HTTPError, URLError, RuntimeError, KeyError, ValueError):
        pass  # An unavailable signal must never become a green status.
    return record


def txt(x, y, value, size=18, color=TEXT, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def surface(width, height, title, description):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>', '<defs><linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#152133"/><stop offset="1" stop-color="#0D1117"/></linearGradient></defs>', f'<g font-family="Segoe UI,Arial,sans-serif"><rect x="1" y="1" width="{width-2}" height="{height-2}" rx="22" fill="url(#surface)" stroke="{BORDER}"/>']


def render_radar(snapshot):
    stamp = datetime.fromisoformat(snapshot["generated_at"].replace("Z", "+00:00")).strftime("%d %b %Y · %H:%M UTC")
    desc = "; ".join(f'{p["name"]}: {p["ci"]}, release {p["release"] or p["release_state"]}, {p["stars"]} stars' for p in snapshot["projects"])
    p = surface(1000, 508, "Public build radar", desc + ". Snapshot " + stamp)
    p += ['<style>.sweep{animation:sweep 18s linear infinite}.blip{animation:blip 3s ease-in-out infinite}@keyframes sweep{to{transform:rotate(360deg)}}@keyframes blip{50%{opacity:.35}}@media(prefers-reduced-motion:reduce){.sweep,.blip{animation:none}}</style>', txt(30, 34, "PUBLIC BUILD RADAR / WORKFLOW GENERATED", 12, "#43E6C5", 600, 'letter-spacing="1.5"'), txt(30, 64, "Three projects. Real signals. One small mission control.", 22, TEXT, 600)]
    for i, item in enumerate(snapshot["projects"]):
        y = 86 + i * 116
        release = item["release"] or item["release_state"]
        display_release = release if len(release) <= 24 else release[:21] + "…"
        state_color = "#43E6C5" if item["ci"] == "PASSING" else "#F36BAA" if item["ci"] in ("FAILING", "TIMED OUT") else "#A995FF"
        last = item["latest_commit_at"][:10] if item["latest_commit_at"] else "unavailable"
        star_label = "STAR" if item["stars"] == 1 else "STARS"
        p += [f'<rect x="30" y="{y}" width="642" height="104" rx="14" fill="{PANEL}" stroke="{BORDER}"/>', f'<rect x="30" y="{y+18}" width="3" height="68" rx="1.5" fill="{item["color"]}"/>', txt(50, y+34, item["name"], 27, TEXT, 650), f'<rect x="525" y="{y+15}" width="126" height="27" rx="13" fill="{state_color}" fill-opacity=".07" stroke="{state_color}" stroke-opacity=".35"/>', txt(588, y+34, item["ci"], 12, state_color, 650, 'text-anchor="middle"'), txt(52, y+64, f'RELEASE {display_release}  ·  {item["stars"]:,} {star_label}', 16, item["color"], 500), txt(52, y+87, f'Latest {item["default_branch"]} commit: {last}', 13, MUTED)]
    p += ['<g transform="translate(824 245)"><circle r="120" fill="#43E6C5" fill-opacity=".018" stroke="#29364B"/><circle r="80" fill="none" stroke="#29364B" stroke-dasharray="3 8"/><circle r="40" fill="none" stroke="#29364B"/><path d="M-120 0H120M0-120V120" stroke="#29364B"/><g class="sweep"><path d="M0 0L-60-103A119 119 0 0 1 0-119Z" fill="#43E6C5" fill-opacity=".08"/><path d="M0 0V-119" stroke="#43E6C5" stroke-opacity=".5"/></g><path d="M-14-9L0-22L14-9V11L0 22L-14 11Z" fill="#121A26" stroke="#43E6C5" stroke-width="2"/>', '<circle class="blip" cx="-70" cy="-62" r="5" fill="#43E6C5"/><circle class="blip" cx="62" cy="-17" r="5" fill="#A995FF"/><circle class="blip" cx="-18" cy="86" r="5" fill="#F36BAA"/>', txt(-70,-77,"01",11,"#43E6C5",600,'text-anchor="middle"'),txt(62,-32,"02",11,"#A995FF",600,'text-anchor="middle"'),txt(-18,110,"03",11,"#F36BAA",600,'text-anchor="middle"'),'</g>', txt(824, 406, "PUBLIC REPOSITORIES ONLY", 11, MUTED, 500, 'text-anchor="middle" letter-spacing="1"'), txt(30, 465, "SNAPSHOT / " + stamp, 12, MUTED, 500),txt(30,487,"Daily refresh · Commit activity includes automation · Open the snapshot for source links",11,MUTED),'</g></svg>\n']
    return "\n".join(p)


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag != "td" or "ContributionCalendar-day" not in a.get("class", "").split():
            return
        day = date.fromisoformat(a["data-date"])
        level = int(a["data-level"])
        if level not in range(5):
            raise ValueError("Unexpected contribution intensity")
        if day in self.days and self.days[day] != level:
            raise ValueError("Conflicting calendar cells")
        self.days[day] = level


def parse_calendar(html, today, *, minimum=350):
    parser = CalendarParser()
    parser.feed(html)
    days = [{"date": day.isoformat(), "level": level} for day, level in sorted(parser.days.items()) if day <= today and (today-day).days < 378]
    if len(days) < minimum:
        raise ValueError("Public contribution calendar is incomplete; keeping the last good artwork")
    dates = [date.fromisoformat(d["date"]) for d in days]
    if any((b-a).days != 1 for a,b in zip(dates, dates[1:])):
        raise ValueError("Calendar contains a gap")
    return days


def render_patrol(calendar):
    days = calendar["days"]
    start = date.fromisoformat(days[0]["date"])
    start -= timedelta(days=(start.weekday()+1) % 7)
    points = []
    colors = ["#17212E", "#174B45", "#217466", "#2DAA92", "#43E6C5"]
    p = surface(1000, 340, "Contribution patrol", "A decorative pixel ship patrols active days from the public GitHub profile calendar. Colors show GitHub activity levels, not security detections. Reduced motion preserves the static calendar.")
    stamp = calendar["generated_at"][:10]
    p += [txt(30,32,"CONTRIBUTION PATROL / PUBLIC CALENDAR",12,"#43E6C5",600,'letter-spacing="1.5"'), txt(30,59,"A pixel side quest, powered by real calendar activity.",22,TEXT,600), txt(961,32,stamp,12,MUTED,400,'text-anchor="end"')]
    last_month = None
    for d in days:
        day = date.fromisoformat(d["date"])
        week = (day-start).days // 7
        row = (day.weekday()+1) % 7
        x, y = 44+week*17, 102+row*17
        if day.month != last_month:
            p += [txt(x,87,day.strftime("%b"),11,MUTED)]
            last_month = day.month
        p += [f'<rect x="{x}" y="{y}" width="13" height="13" rx="3" fill="{colors[d["level"]]}"><title>{d["date"]}: activity level {d["level"]} of 4</title></rect>']
        if d["level"]:
            points.append((x+6.5,y+6.5))
    chosen = [points[round(i*(len(points)-1)/(min(8,len(points))-1))] for i in range(min(8,len(points)))] if len(points)>1 else points
    animation = ['@keyframes ship{']
    if chosen:
        animation += [f'0%{{transform:translate({chosen[0][0]}px,267px)}}']
        for i,(x,y) in enumerate(chosen):
            lo,hi = i*100/len(chosen)+2, i*100/len(chosen)+9 if len(chosen)<=8 else i*100/len(chosen)+5
            hi = min(hi,99)
            animation += [f'{lo:.3f}%,{hi:.3f}%{{transform:translate({x}px,267px)}}']
        animation += [f'100%{{transform:translate({chosen[0][0]}px,267px)}}']
    animation += ['}']
    for i,(x,y) in enumerate(chosen):
        t = i*100/len(chosen)
        animation += [f'@keyframes shot{i}{{0%,{t+4:.3f}%,{min(t+7,99.9):.3f}%,100%{{opacity:0}}{t+5:.3f}%{{opacity:.75}}}}']
        p += [f'<g class="motion shot{i}" style="opacity:0;animation:shot{i} 32s linear infinite"><path d="M{x} 250V{y}" stroke="#43E6C5" stroke-width="2" stroke-opacity=".65"/><circle cx="{x}" cy="{y}" r="10" fill="none" stroke="#F36BAA" stroke-width="2"/></g>']
    p += ['<style>'+''.join(animation)+'.ship{transform:translate(500px,267px);animation:ship 32s linear infinite}@media(prefers-reduced-motion:reduce){.motion{display:none}.ship{animation:none}}</style>', '<g class="ship" shape-rendering="crispEdges"><path d="M-3-14H3V-8H7V-2H13V10H5V6H-5V10H-13V-2H-7V-8H-3Z" fill="#A995FF"/><path d="M-3-3H3V5H-3Z" fill="#43E6C5"/><path d="M-2 10H2V17H-2Z" fill="#F36BAA"/></g>', txt(30,315,f'{len(points)} active days in the displayed calendar · Color = GitHub activity level · Generated daily',12,MUTED),'</g></svg>\n']
    return "\n".join(p)


def report_markdown(snapshot):
    rows = ["# Public build radar", "", "Generated " + snapshot["generated_at"] + ". This is a snapshot of three explicitly selected public repositories.", "", "| Project | CI run | Latest release | Stars | Default-branch commit |", "| --- | --- | --- | ---: | --- |"]
    for p in snapshot["projects"]:
        tag = p["release"] or p["release_state"]
        safe_tag = tag.replace("|", "\\|").replace("[", "\\[").replace("]", "\\]").replace("\n", " ")
        rows.append(f'| [{p["name"]}]({p["url"]}) | [{p["ci"]}]({p["ci_url"]}) | [{safe_tag}]({p["release_url"]}) | {p["stars"]} | {p["latest_commit_at"] or "unavailable"} |')
    rows += ["", "Commit activity includes automation and all authors. A CI result describes the latest listed workflow run, not every branch or a security assessment.", "", "The radar sweep and ship are decorative. Calendar intensity comes from the unauthenticated public GitHub calendar; no private repository names or configuration are requested.", "", "[Generator](../scripts/generate_profile_lab.py) · [Daily workflow](../.github/workflows/profile-lab.yml)", ""]
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("profile"))
    args = parser.parse_args()
    now = datetime.now(timezone.utc).replace(second=0,microsecond=0)
    stamp = now.isoformat().replace("+00:00", "Z")
    projects = [collect_project(spec) for spec in PROJECTS]
    url = f"https://github.com/users/{OWNER}/contributions"
    with urlopen(Request(url, headers={"User-Agent":"PKHarsimran-profile-lab"}), timeout=25) as response:
        html = response.read().decode("utf-8")
    calendar = {"generated_at":stamp,"source":url,"days":parse_calendar(html,now.date())}
    snapshot = {"generated_at":stamp,"scope":"three selected public repositories","projects":projects}
    files = {"public-pulse.svg":render_radar(snapshot),"public-pulse.json":json.dumps(snapshot,indent=2)+"\n","public-pulse.md":report_markdown(snapshot),"contribution-patrol.svg":render_patrol(calendar),"contribution-patrol.json":json.dumps(calendar,indent=2)+"\n"}
    # No output changes until both sources have passed validation.
    args.output.mkdir(parents=True,exist_ok=True)
    for name, content in files.items():
        target=args.output/name
        tmp=target.with_suffix(target.suffix+".tmp")
        tmp.write_text(content,encoding="utf-8")
        tmp.replace(target)
    print(f"Generated {len(files)} public profile artifacts at {stamp}")


if __name__ == "__main__":
    main()
