#!/usr/bin/env python3
"""
Generate a denser SVG topic cloud and word frequency CSV from the repository.

This script is inspired by the reference project's `generate_wordcloud.py`,
but it avoids heavyweight plotting dependencies so it can run in a minimal
environment.

Outputs:
- assets/wordcloud.svg
- assets/word_frequency.csv

Usage:
    python3 scripts/generate_wordcloud.py
"""

from __future__ import annotations

import colorsys
import csv
import html
import math
import random
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
MATRIX = ROOT / "data" / "paper-matrix.csv"
ASSETS = ROOT / "assets"
WORDCLOUD_SVG = ASSETS / "wordcloud.svg"
WORD_FREQ_CSV = ASSETS / "word_frequency.csv"


STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "of", "to", "is", "it",
    "at", "by", "as", "be", "we", "do", "no", "so", "if", "up", "are", "was",
    "not", "can", "has", "had", "its", "all", "any", "our", "out", "own", "how",
    "few", "new", "one", "two", "more", "most", "each", "some", "than", "that",
    "this", "them", "they", "then", "very", "also", "been", "from", "have",
    "here", "just", "like", "into", "over", "such", "what", "when", "will",
    "with", "both", "only", "does", "done", "same", "much", "many", "well",
    "back", "even", "take", "make", "made", "need", "used", "while", "about",
    "after", "being", "could", "every", "first", "given", "other", "since",
    "still", "their", "there", "these", "those", "under", "until", "where",
    "which", "would", "your", "between", "through", "during", "before",
    "for", "via", "based", "using", "towards", "toward", "without", "beyond",
    "across", "against", "within", "whether", "approach", "approaches",
    "method", "methods", "framework", "model", "models", "system", "systems",
    "novel", "simple", "efficient", "effective", "learning", "robot", "robots",
    "robotic", "cross", "embodiment", "embodied", "humanoid", "humanoids",
    "control", "general", "toward", "towards",
}


README_LINK_RE = re.compile(r"- \[([^\]]+)\]\([^)]+\)")
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9-]*")


def load_records() -> list[dict[str, str]]:
    if not MATRIX.exists():
        return []
    with MATRIX.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def extract_titles_from_matrix() -> list[str]:
    titles: list[str] = []
    for row in load_records():
        title = (row.get("title") or "").strip()
        if title:
            titles.append(title)
    return titles


def extract_titles_from_readme() -> list[str]:
    if not README.exists():
        return []
    text = README.read_text(encoding="utf-8")
    titles: list[str] = []
    for match in README_LINK_RE.finditer(text):
        title = match.group(1).strip()
        if len(title) > 3 and "Awesome Cross-Embodiment" not in title:
            titles.append(title)
    return titles


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def normalize_token(word: str) -> str | None:
    token = word.lower().strip("-")
    if len(token) <= 2:
        return None
    if token in STOP_WORDS:
        return None
    if token.isdigit():
        return None
    return token


def tokenize_text(text: str) -> list[str]:
    tokens: list[str] = []
    for word in TOKEN_RE.findall(text):
        token = normalize_token(word)
        if token:
            tokens.append(token)
    return tokens


def weighted_counter(records: list[dict[str, str]], titles: list[str]) -> Counter:
    counts: Counter = Counter()

    # Titles get the highest weight.
    for title in titles:
        tokens = tokenize_text(title)
        counts.update(tokens)

        # Add common 2-gram phrases from titles.
        for i in range(len(tokens) - 1):
            phrase = f"{tokens[i]} {tokens[i + 1]}"
            counts[phrase] += 2
        for i in range(len(tokens) - 2):
            phrase = f"{tokens[i]} {tokens[i + 1]} {tokens[i + 2]}"
            counts[phrase] += 1

    # Categories and "why it matters" add extra context and density.
    for row in records:
        category = (row.get("category") or "").replace("-", " ")
        why = row.get("why_it_matters") or ""
        task = row.get("task") or ""
        interface = row.get("interface") or ""

        for token in tokenize_text(category):
            counts[token] += 2
        for token in tokenize_text(task):
            counts[token] += 2
        for token in tokenize_text(interface):
            counts[token] += 1
        for token in tokenize_text(why):
            counts[token] += 1

    # Remove low-information phrases that can dominate.
    phrase_stop = {
        "shared policy",
        "real robot",
        "robot data",
        "human video",
        "human videos",
        "robot policy",
        "policy learning",
        "multi robot",
        "real world",
        "cross robot",
    }
    for phrase in phrase_stop:
        counts.pop(phrase, None)

    return counts


def estimate_text_box(word: str, font_size: float, rotate: bool) -> tuple[float, float]:
    width = max(font_size * (0.58 * len(word)), font_size * 1.8)
    height = font_size * 1.1
    if rotate:
        return height, width
    return width, height


def intersects(rect: tuple[float, float, float, float], others: list[tuple[float, float, float, float]]) -> bool:
    x1, y1, w1, h1 = rect
    for x2, y2, w2, h2 in others:
        if not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1):
            return True
    return False


def color_for_rank(rank: int, total: int) -> str:
    hue = 0.58 - 0.42 * (rank / max(total - 1, 1))
    sat = 0.65 + 0.1 * (1 - rank / max(total - 1, 1))
    val = 0.9
    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
    return f"rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})"


def generate_svg(counter: Counter, output_path: Path) -> None:
    width = 1600
    height = 900
    margin = 24

    # Keep meaningful phrases and moderately frequent words.
    filtered_items: list[tuple[str, int]] = []
    for term, count in counter.most_common(220):
        if len(term) < 3:
            continue
        if count < 2:
            continue
        filtered_items.append((term, count))
    top_items = filtered_items[:180]

    if not top_items:
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
            '<rect width="100%" height="100%" fill="#f8fbff"/>'
            '<text x="50%" y="50%" text-anchor="middle" font-size="32" fill="#334155">'
            'No terms found'
            '</text></svg>'
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(svg, encoding="utf-8")
        return

    max_count = top_items[0][1]
    min_count = top_items[-1][1]
    placed: list[tuple[float, float, float, float]] = []
    texts: list[str] = []
    random.seed(42)

    center_x = width / 2
    center_y = height / 2 + 30

    for rank, (word, count) in enumerate(top_items):
        if max_count == min_count:
            size = 24
        else:
            scale = (count - min_count) / (max_count - min_count)
            size = 12 + scale * 64

        rotate = rank % 9 == 0 and len(word) > 7 and " " not in word
        box_w, box_h = estimate_text_box(word, size, rotate)
        placed_rect = None

        # Spiral placement.
        for step in range(1, 7000):
            angle = step * 0.29
            radius = 3.7 * math.sqrt(step)
            x = center_x + radius * math.cos(angle) - box_w / 2
            y = center_y + radius * math.sin(angle) - box_h / 2

            rect = (x, y, box_w, box_h)
            if x < margin or y < margin or x + box_w > width - margin or y + box_h > height - margin:
                continue
            if intersects(rect, placed):
                continue
            placed_rect = rect
            break

        if placed_rect is None:
            continue

        x, y, _, _ = placed_rect
        placed.append(placed_rect)
        fill = color_for_rank(rank, len(top_items))
        escaped_word = html.escape(word)
        font_weight = "700" if rank < 10 else "600" if rank < 30 else "500"

        if rotate:
            tx = x + box_w / 2
            ty = y + box_h / 2
            text = (
                f'<text x="{tx:.1f}" y="{ty:.1f}" '
                f'font-size="{size:.1f}" fill="{fill}" '
                f'font-weight="{font_weight}" '
                'font-family="Verdana, DejaVu Sans, Arial, sans-serif" '
                'text-anchor="middle" dominant-baseline="middle" '
                f'transform="rotate(-90 {tx:.1f} {ty:.1f})">{escaped_word}</text>'
            )
        else:
            tx = x + box_w / 2
            ty = y + box_h / 2
            text = (
                f'<text x="{tx:.1f}" y="{ty:.1f}" '
                f'font-size="{size:.1f}" fill="{fill}" '
                f'font-weight="{font_weight}" '
                'font-family="Verdana, DejaVu Sans, Arial, sans-serif" '
                'text-anchor="middle" dominant-baseline="middle">'
                f'{escaped_word}</text>'
            )
        texts.append(text)

    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#ffffff"/>',
            *texts,
            '</svg>',
        ]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")


def write_frequency_csv(counter: Counter, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "word", "count"])
        for idx, (word, count) in enumerate(counter.most_common(), start=1):
            writer.writerow([idx, word, count])


def main() -> None:
    records = load_records()
    titles = dedupe_keep_order(extract_titles_from_matrix() + extract_titles_from_readme())
    counter = weighted_counter(records, titles)
    generate_svg(counter, WORDCLOUD_SVG)
    write_frequency_csv(counter, WORD_FREQ_CSV)
    print(f"Processed {len(titles)} titles")
    print(f"Saved word cloud: {WORDCLOUD_SVG}")
    print(f"Saved frequency CSV: {WORD_FREQ_CSV}")


if __name__ == "__main__":
    main()
