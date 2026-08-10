"""Render data/contributions.json as an animated 53x7 contribution heatmap SVG."""
import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BG = "#0d1117"
TEXT = "#8b949e"
BOX = 11
GAP = 3
CELL = BOX + GAP
LEFT_PAD = 30
TOP_PAD = 24
BOTTOM_PAD = 46
STAGGER = 0.012
CYCLE = 10.0  # full loop per box: pop in, hold, fade out, repeat

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load():
    with open("data/contributions.json") as f:
        return json.load(f)


def build_weeks(days):
    parsed = [
        {"date": datetime.strptime(d["date"], "%Y-%m-%d").date(), "level": d["level"]}
        for d in days
    ]
    parsed.sort(key=lambda x: x["date"])
    weeks = []
    week = [None] * 7
    for d in parsed:
        wd = (d["date"].weekday() + 1) % 7  # Sunday=0
        if wd == 0 and any(week):
            weeks.append(week)
            week = [None] * 7
        week[wd] = d
    if any(week):
        weeks.append(week)
    return weeks


def month_labels(weeks):
    labels = []
    last_month = None
    for i, week in enumerate(weeks):
        first_day = next((d for d in week if d), None)
        if not first_day:
            continue
        m = first_day["date"].month
        if m != last_month:
            labels.append((i, MONTH_NAMES[m - 1]))
            last_month = m
    return labels


def render(data, out_path="contrib-heatmap.svg"):
    weeks = build_weeks(data["days"])
    n_weeks = len(weeks)
    width = LEFT_PAD + n_weeks * CELL + 10
    height = TOP_PAD + 7 * CELL + BOTTOM_PAD

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="{BG}"/>')

    parts.append("<style>")
    parts.append(f".box{{opacity:0;animation:pop {CYCLE}s ease-in-out infinite;}}")
    parts.append(
        "@keyframes pop{0%{opacity:0;transform:translate(-4px,-4px);}"
        "4%{opacity:1;transform:translate(0,0);}"
        "90%{opacity:1;transform:translate(0,0);}"
        "100%{opacity:0;transform:translate(-4px,-4px);}}"
    )
    idx = 0
    for w in range(n_weeks):
        for d in range(7):
            delay = (w + d) * STAGGER
            parts.append(f".b{idx}{{animation-delay:{delay:.3f}s;transform-box:fill-box;}}")
            idx += 1
    parts.append("</style>")

    for i, (wi, name) in enumerate(month_labels(weeks)):
        x = LEFT_PAD + wi * CELL
        parts.append(f'<text x="{x}" y="{TOP_PAD - 8}" font-size="10" fill="{TEXT}">{name}</text>')

    box_i = 0
    for w, week in enumerate(weeks):
        for d in range(7):
            day = week[d]
            level = day["level"] if day else 0
            color = PALETTE[min(level, len(PALETTE) - 1)]
            x = LEFT_PAD + w * CELL
            y = TOP_PAD + d * CELL
            title = f'{day["date"].isoformat()}: level {level}' if day else ""
            parts.append(
                f'<rect class="box b{box_i}" x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="2" '
                f'fill="{color}"><title>{title}</title></rect>'
            )
            box_i += 1

    legend_y = height - 28
    parts.append(f'<text x="{LEFT_PAD}" y="{legend_y+8}" font-size="11" fill="{TEXT}">Less</text>')
    lx = LEFT_PAD + 34
    for c in PALETTE:
        parts.append(f'<rect x="{lx}" y="{legend_y}" width="{BOX}" height="{BOX}" rx="2" fill="{c}"/>')
        lx += CELL
    parts.append(f'<text x="{lx+4}" y="{legend_y+8}" font-size="11" fill="{TEXT}">More</text>')

    stats = data["stats"]
    footer = (
        f'{data["total_contributions"]} contributions in the last year  ·  '
        f'current streak {stats["current_streak"]}  ·  longest streak {stats["longest_streak"]}'
    )
    parts.append(
        f'<text x="{width - LEFT_PAD}" y="{legend_y+8}" font-size="11" fill="{TEXT}" text-anchor="end">{footer}</text>'
    )

    parts.append("</svg>")
    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    render(load())
