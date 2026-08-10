"""Hand-authored neofetch-style info card SVG with a fade-in-line stagger."""
import os

WIDTH = 760
HEIGHT = 430
BG = "#0d1117"
BORDER = "#30363d"
TITLE_BAR = "#161b22"
LABEL_COLOR = "#39d353"
TEXT_COLOR = "#c9d1d9"
DIM_COLOR = "#8b949e"
STAGGER = 0.15
CYCLE = 8.0  # full loop per line: fade in, hold, fade out, repeat
STATIC = os.environ.get("STATIC") == "1"

USER_HOST = "krishna@github"
TAGLINE = "Full Stack AI Software Engineer"

SECTIONS = [
    ("Stack", ["TypeScript, Node.js, React/Next.js, PostgreSQL", "Redis, RabbitMQ, Docker, GCP"]),
    (
        "Highlights",
        [
            "CanvasSync - Redis CRDT whiteboard, ~60% latency cut",
            "Knowdex - binary WS codec, ~90% less traffic",
            "Compliance-ledger engine for 70+ tracked component types",
        ],
    ),
]


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    body = []
    delays = []

    def cls(i):
        if STATIC:
            return "ln"
        delays.append(0.3 + i * STAGGER)
        return f"ln d{i}"

    # title bar
    body.append(f'<rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="12" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>')
    body.append(f'<rect x="1" y="1" width="{WIDTH-2}" height="40" rx="12" fill="{TITLE_BAR}"/>')
    body.append(f'<rect x="1" y="29" width="{WIDTH-2}" height="12" fill="{TITLE_BAR}"/>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        body.append(f'<circle cx="{26 + i*20}" cy="20" r="7" fill="{c}"/>')
    body.append(f'<text x="{WIDTH/2}" y="25" text-anchor="middle" font-size="14" fill="{DIM_COLOR}">neofetch</text>')

    idx = 0
    y = 92

    body.append(
        f'<text x="34" y="{y}" font-size="26" font-weight="bold" fill="{LABEL_COLOR}" class="{cls(idx)}">'
        f'{escape(USER_HOST)}</text>'
    )
    idx += 1
    y += 34
    body.append(
        f'<text x="34" y="{y}" font-size="19" fill="{TEXT_COLOR}" class="{cls(idx)}">{escape(TAGLINE)}</text>'
    )
    idx += 1
    y += 22
    body.append(f'<line x1="34" y1="{y}" x2="{WIDTH-34}" y2="{y}" stroke="{BORDER}" stroke-width="1"/>')
    y += 42

    for label, values in SECTIONS:
        body.append(
            f'<text x="34" y="{y}" font-size="18" font-weight="bold" fill="{LABEL_COLOR}" class="{cls(idx)}">'
            f'{escape(label)}</text>'
        )
        idx += 1
        y += 30
        for v in values:
            body.append(
                f'<text x="52" y="{y}" font-size="16.5" fill="{TEXT_COLOR}" class="{cls(idx)}">{escape(v)}</text>'
            )
            idx += 1
            y += 28
        y += 14

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">'
    ]

    if not STATIC:
        parts.append("<style>")
        parts.append(f".ln{{opacity:0;animation:fadein {CYCLE}s ease-in-out infinite;}}")
        parts.append(
            "@keyframes fadein{0%{opacity:0;transform:translateX(-10px);}"
            "6%{opacity:1;transform:translateX(0);}"
            "88%{opacity:1;transform:translateX(0);}"
            "100%{opacity:0;transform:translateX(-10px);}}"
        )
        for i, d in enumerate(delays):
            parts.append(f".d{i}{{animation-delay:{d:.2f}s;}}")
        parts.append("</style>")

    parts.extend(body)
    parts.append("</svg>")

    out = "info-card.svg"
    with open(out, "w") as f:
        f.write("\n".join(parts))
    print(f"wrote {out}")


if __name__ == "__main__":
    build()
