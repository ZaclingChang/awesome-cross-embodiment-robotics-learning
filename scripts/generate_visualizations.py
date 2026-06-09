#!/usr/bin/env python3
"""
Generate lightweight SVG visualizations from `data/paper-matrix.csv`.

Outputs:
- assets/category_distribution.svg
- assets/year_distribution.svg

Usage:
    python3 scripts/generate_visualizations.py
"""

from __future__ import annotations

import csv
import html
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MATRIX = ROOT / "data" / "paper-matrix.csv"
ASSETS = ROOT / "assets"
CATEGORY_SVG = ASSETS / "category_distribution.svg"
YEAR_SVG = ASSETS / "year_distribution.svg"


def load_rows() -> list[dict[str, str]]:
    with MATRIX.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def normalize_year(year_text: str) -> str:
    text = (year_text or "").strip()
    if text.startswith("2023-2024"):
        return "2023-2024"
    return text[:4] if len(text) >= 4 else text


def nice_category(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def bar_chart_svg(
    title: str,
    subtitle: str,
    data: list[tuple[str, int]],
    output_path: Path,
    bar_color: str,
    width: int = 1500,
    height: int = 860,
) -> None:
    margin_left = 260
    margin_right = 60
    margin_top = 120
    margin_bottom = 60
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    max_value = max((value for _, value in data), default=1)
    row_gap = 18
    bar_height = max(20, int((plot_height - row_gap * max(len(data) - 1, 0)) / max(len(data), 1)))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="40" y="54" font-size="28" font-weight="700" font-family="Verdana, DejaVu Sans, Arial, sans-serif" fill="#0f172a">{html.escape(title)}</text>',
        f'<text x="40" y="84" font-size="16" font-family="Verdana, DejaVu Sans, Arial, sans-serif" fill="#475569">{html.escape(subtitle)}</text>',
    ]

    y = margin_top
    for label, value in data:
        bar_w = 0 if max_value == 0 else int(plot_width * value / max_value)
        parts.append(
            f'<text x="{margin_left - 16}" y="{y + bar_height / 2 + 6:.1f}" text-anchor="end" '
            'font-size="16" font-family="Verdana, DejaVu Sans, Arial, sans-serif" fill="#334155">'
            f'{html.escape(label)}</text>'
        )
        parts.append(
            f'<rect x="{margin_left}" y="{y}" width="{bar_w}" height="{bar_height}" rx="8" fill="{bar_color}"/>'
        )
        parts.append(
            f'<text x="{margin_left + bar_w + 12}" y="{y + bar_height / 2 + 6:.1f}" '
            'font-size="15" font-family="Verdana, DejaVu Sans, Arial, sans-serif" fill="#0f172a">'
            f'{value}</text>'
        )
        y += bar_height + row_gap

    parts.append('</svg>')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    rows = load_rows()

    category_counter = Counter(nice_category((row.get("category") or "").strip()) for row in rows if row.get("category"))
    year_counter = Counter(normalize_year(row.get("year") or "") for row in rows if row.get("year"))

    category_data = sorted(category_counter.items(), key=lambda item: (-item[1], item[0]))
    year_data = sorted(year_counter.items(), key=lambda item: item[0])

    bar_chart_svg(
        title="Paper Categories in the Seed Matrix",
        subtitle="Grouped by cross-embodiment research bucket",
        data=category_data,
        output_path=CATEGORY_SVG,
        bar_color="#0f766e",
        height=960,
    )
    bar_chart_svg(
        title="Paper Year Distribution",
        subtitle="Based on the current structured paper matrix",
        data=year_data,
        output_path=YEAR_SVG,
        bar_color="#2563eb",
        height=700,
    )

    print(f"Saved category chart: {CATEGORY_SVG}")
    print(f"Saved year chart: {YEAR_SVG}")


if __name__ == "__main__":
    main()
