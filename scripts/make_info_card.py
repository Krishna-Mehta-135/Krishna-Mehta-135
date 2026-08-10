"""Hand-authored neofetch-style info card SVG with a fade-in-line stagger."""
import os

WIDTH = 700
HEIGHT = 400
BG = "#0d1117"
BORDER = "#30363d"
TITLE_BAR = "#161b22"
LABEL_COLOR = "#39d353"
TEXT_COLOR = "#c9d1d9"
DIM_COLOR = "#8b949e"
STAGGER = 0.15
DUR = 0.5
STATIC = os.environ.get("STATIC") == "1"

USER_HOST = "krishna@github"

FIELDS = [
    ("Now", "Full Stack AI Software Engineer"),
    ("Prev", "Full Stack Eng Intern @ AVAJet Aviation Consultants"),
    ("Stack", "TypeScript, Node.js, React/Next.js, PostgreSQL"),
    ("", "Redis, RabbitMQ, Docker, GCP"),
    ("Highlights", "CanvasSync - Redis CRDT whiteboard, ~60% latency cut"),
    ("", "Knowdex - binary WS codec, ~90% less traffic"),
    ("", "CAMO - compliance ledger for 70+ component types"),
]


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">'
    )
    parts.append(
        f'<rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>'
    )
    # title bar
    parts.append(f'<rect x="1" y="1" width="{WIDTH-2}" height="34" rx="10" fill="{TITLE_BAR}"/>')
    parts.append(f'<rect x="1" y="24" width="{WIDTH-2}" height="11" fill="{TITLE_BAR}"/>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{22 + i*18}" cy="17" r="6" fill="{c}"/>')
    parts.append(
        f'<text x="{WIDTH/2}" y="21" text-anchor="middle" font-size="12" fill="{DIM_COLOR}">'
        f'neofetch</text>'
    )

    if not STATIC:
        parts.append("<style>")
        parts.append(
            ".ln{opacity:0;animation:fadein %.2fs ease-out forwards;}" % DUR
        )
        parts.append(
            "@keyframes fadein{from{opacity:0;transform:translateX(-8px);}"
            "to{opacity:1;transform:translateX(0);}}"
        )
        n = 1 + len(FIELDS)
        for i in range(n):
            delay = 0.3 + i * STAGGER
            parts.append(f".d{i}{{animation-delay:{delay:.2f}s;}}")
        parts.append("</style>")

    def cls(i):
        return "ln" if STATIC else f"ln d{i}"

    y = 70
    parts.append(
        f'<text x="30" y="{y}" font-size="16" font-weight="bold" fill="{LABEL_COLOR}" class="{cls(0)}">'
        f'{escape(USER_HOST)}</text>'
    )
    y += 14
    parts.append(f'<line x1="30" y1="{y}" x2="{WIDTH-30}" y2="{y}" stroke="{BORDER}" stroke-width="1" class="{cls(0)}"/>')
    y += 30

    for i, (label, value) in enumerate(FIELDS, start=1):
        if label:
            parts.append(
                f'<text x="30" y="{y}" font-size="14" font-weight="bold" fill="{LABEL_COLOR}" class="{cls(i)}">'
                f'{escape(label)}</text>'
            )
            parts.append(
                f'<text x="150" y="{y}" font-size="13.5" fill="{TEXT_COLOR}" class="{cls(i)}">'
                f'{escape(value)}</text>'
            )
        else:
            parts.append(
                f'<text x="150" y="{y}" font-size="13.5" fill="{TEXT_COLOR}" class="{cls(i)}">'
                f'{escape(value)}</text>'
            )
        y += 30

    parts.append("</svg>")
    out = "info-card.svg"
    with open(out, "w") as f:
        f.write("\n".join(parts))
    print(f"wrote {out}")


if __name__ == "__main__":
    build()
