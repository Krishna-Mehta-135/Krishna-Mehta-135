"""Convert source-prepped.png into a monochrome, self-typing ASCII SVG."""
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)
COLS = 100
ROWS = 53
CHAR_W = 6.2
CHAR_H = 11
FILL = "#8b949e"
BG = "#0d1117"
STAGGER = 0.028  # seconds between row starts
CYCLE = 6.0  # full loop duration per row: wipe in, hold, wipe out, repeat


def brightness_to_char(v: float) -> str:
    idx = int((1 - v / 255) * (len(RAMP) - 1))
    idx = max(0, min(len(RAMP) - 1, idx))
    return RAMP[idx]


def build_grid(path: str):
    img = Image.open(path).convert("L")
    img = img.resize((COLS, ROWS * 2))  # 2x vertical sampling, chars are taller than wide
    px = img.load()
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            # average the two sampled rows per character row
            v = (px[c, r * 2] + px[c, r * 2 + 1]) / 2
            row.append(brightness_to_char(v))
        grid.append(row)
    return grid


def escape(ch: str) -> str:
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(ch, ch)


def render_svg(grid, out_path: str):
    width = COLS * CHAR_W
    height = ROWS * CHAR_H
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="{BG}"/>')
    parts.append("<style>")
    parts.append(f".row{{font-size:{CHAR_H}px;fill:{FILL};white-space:pre;}}")
    parts.append(
        "@keyframes wiperow{0%{clip-path:inset(0 100% 0 0);}6%{clip-path:inset(0 0 0 0);}"
        "88%{clip-path:inset(0 0 0 0);}100%{clip-path:inset(0 100% 0 0);}}"
    )
    for r in range(ROWS):
        start = r * STAGGER
        parts.append(
            f".r{r}{{animation:wiperow {CYCLE}s steps(30) {start:.3f}s infinite;}}"
        )
    parts.append("</style>")

    for r, row in enumerate(grid):
        line = "".join(escape(ch) for ch in row)
        y = (r + 1) * CHAR_H - 2
        parts.append(f'<text class="row r{r}" x="0" y="{y:.1f}" xml:space="preserve">{line}</text>')

    parts.append("</svg>")
    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    grid = build_grid("source-prepped.png")
    render_svg(grid, "avi-ascii.svg")
