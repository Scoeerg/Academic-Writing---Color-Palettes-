#!/usr/bin/env python3
"""
Parse colorbrewer_schemes.js and generate LaTeX color definitions.

Usage:
    python colorbrewer_to_tex.py colorbrewer_schemes.js output.tex
"""

import re
import sys
import json5
import ast               
from pathlib import Path


def parse_js_object(js_content: str) -> dict:
    """Parse colorbrewer_schemes.js using json5 after quoting numeric keys"""
    import re
    import json5

    # 1. Remove multi-line comments /* ... */
    content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL | re.MULTILINE)

    # 2. Remove single-line comments //
    content = re.sub(r'//.*', '', content)

    # 3. Strip var colorbrewer = and trailing ;
    content = re.sub(r'^\s*var\s+colorbrewer\s*=\s*', '', content.strip())
    content = re.sub(r'\s*;\s*$', '', content)

    # 4. Extract the core object { ... }
    start_idx = content.find('{')
    if start_idx == -1:
        raise ValueError("No { found")
    end_idx = content.rfind('}')
    if end_idx == -1:
        raise ValueError("No } found")
    content = content[start_idx : end_idx + 1]

    # 5. CRITICAL: Quote all unquoted numeric keys like 3: 4: 5: ... 11:
    #    We look for patterns like , 3:  or {3:  or , 11: etc.
    content = re.sub(r'([,\{\s])(\d+):', r'\1"\2":', content)

    # 6. Also quote scheme names if still unquoted (Spectral: → "Spectral":)
    content = re.sub(r'([,\{\s])([A-Za-z][A-Za-z0-9]*):', r'\1"\2":', content)

    # 7. Remove trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content, flags=re.DOTALL)

    # 8. Single quotes → double quotes (safe here since no escapes in this file)
    content = content.replace("'", '"')

    # Debug: optional, comment out later
    # print("Cleaned & quoted preview:\n", content[:800])

    try:
        data = json5.loads(content)
        if not isinstance(data, dict):
            raise ValueError("Not a dict after parsing")
        return data
    except Exception as e:
        print("Final json5 error:", e)
        print("Problematic content preview (first 800 chars):")
        print(content[:800])
        raise


def rgb_str_to_tuple(rgb_str: str) -> tuple[int, int, int]:
    """Convert 'rgb(241,163,64)' → (241, 163, 64)"""
    m = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', rgb_str.strip())
    if not m:
        raise ValueError(f"Cannot parse RGB string: {rgb_str}")
    return tuple(int(x) for x in m.groups())


def get_safety_flags(properties: dict, n: int) -> str:
    """
    Mimic the logic from checkColorblind / checkPrint / checkCopy
    Returns parts like: blindSafe_PhotoCopySafe (or empty)
    """
    parts = []

    # colorblind-safe
    blind = properties.get("blind", [])
    if blind:
        idx = 0 if len(blind) == 1 else max(0, n - 3)
        idx = min(idx, len(blind) - 1)
        if blind[idx] >= 1:  # usually 1 or 2 means safe
            parts.append("blindSafe")

    # print-safe
    pr = properties.get("print", [])
    if pr:
        idx = 0 if len(pr) == 1 else max(0, n - 3)
        idx = min(idx, len(pr) - 1)
        if pr[idx] >= 1:
            parts.append("PrintSafe")

    # photocopy-safe
    cp = properties.get("copy", [])
    if cp:
        idx = 0 if len(cp) == 1 else max(0, n - 3)
        idx = min(idx, len(cp) - 1)
        if cp[idx] >= 1:
            parts.append("PhotoCopySafe")

    # You can add "ScreenSafe" if you want using properties.screen

    if parts:
        return "_" + "_".join(parts)
    return ""


def main():
    if len(sys.argv) != 3:
        print("Usage: python colorbrewer_to_tex.py <input.js> <output.tex>")
        sys.exit(1)

    infile = Path(sys.argv[1])
    outfile = Path(sys.argv[2])

    if not infile.is_file():
        print(f"File not found: {infile}")
        sys.exit(1)

    js_text = infile.read_text(encoding="utf-8")
    schemes = parse_js_object(js_text)

    lines = []
    lines.append("% Generated from ColorBrewer schemes")
    lines.append("% https://github.com/axismaps/colorbrewer")
    lines.append("")

    for scheme, data in schemes.items():
        if scheme == "properties":  # unlikely but skip
            continue
        if not isinstance(data, dict):
            continue

        properties = data.get("properties", {})
        scheme_type = properties.get("type", "unknown")  # seq, div, qual

        for n_str, colors in data.items():
            if not (isinstance(n_str, str) and n_str.isdigit()):
                continue
            n = int(n_str)

            safe_suffix = get_safety_flags(properties, n)

            comment = f"% {n}-class {scheme_type} – {scheme.lower()}"
            lines.append(comment)

            for i, rgb_str in enumerate(colors, 1):
                try:
                    r, g, b = rgb_str_to_tuple(rgb_str)
                except ValueError:
                    print(f"Skipping invalid color in {scheme} {n}: {rgb_str}")
                    continue

                name = f"{n}_{scheme.lower()}_{scheme_type}{safe_suffix}_{i}"
                line = f"\\definecolor{{{name}}}{{RGB}}{{{r},{g},{b}}}"
                lines.append(line)

            lines.append("")  # empty line between schemes

    outfile.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} lines to {outfile}")


if __name__ == "__main__":
    main()
