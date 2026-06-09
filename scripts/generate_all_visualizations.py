#!/usr/bin/env python3
"""
Convenience entrypoint to regenerate all repository visualizations.

Usage:
    python3 scripts/generate_all_visualizations.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(script_name: str) -> None:
    script_path = ROOT / script_name
    print(f"Running {script_path.name} ...")
    subprocess.run([sys.executable, str(script_path)], check=True)


def main() -> None:
    run("generate_wordcloud.py")
    run("generate_visualizations.py")
    print("All visualizations generated successfully.")


if __name__ == "__main__":
    main()
