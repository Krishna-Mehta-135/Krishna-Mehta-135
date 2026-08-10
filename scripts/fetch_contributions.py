"""Fetch the public contribution calendar HTML (no token needed) and derive stats."""
import json
import re
from datetime import date, datetime, timezone

import requests
from bs4 import BeautifulSoup

USERNAME = "Krishna-Mehta-135"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_days():
    resp = requests.get(URL, headers={"User-Agent": "profile-readme-bot"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        d = td.get("data-date")
        level = td.get("data-level")
        if not d or level is None:
            continue
        days.append({"date": d, "level": int(level)})

    total_match = re.search(r"([\d,]+)\s*\n?\s*contributions", resp.text)
    total = int(total_match.group(1).replace(",", "")) if total_match else None
    days.sort(key=lambda x: x["date"])
    return days, total


def derive_stats(days):
    counts_by_level = {}
    for d in days:
        counts_by_level[d["level"]] = counts_by_level.get(d["level"], 0) + 1

    today = date.today()
    current_streak = 0
    for d in reversed(days):
        dd = datetime.strptime(d["date"], "%Y-%m-%d").date()
        if dd > today:
            continue
        if d["level"] > 0:
            current_streak += 1
        else:
            break

    longest_streak = 0
    running = 0
    for d in days:
        if d["level"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    active_days = sum(1 for d in days if d["level"] > 0)

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "active_days": active_days,
        "level_counts": counts_by_level,
    }


def main():
    days, total = fetch_days()
    stats = derive_stats(days)
    out = {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total,
        "days": days,
        "stats": stats,
    }
    with open("data/contributions.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote data/contributions.json ({len(days)} days, total={total})")


if __name__ == "__main__":
    main()
