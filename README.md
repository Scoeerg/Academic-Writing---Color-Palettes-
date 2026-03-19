# Academic-Writing Color-Palettes

A set of color palettes for academic writing with LaTeX based on [Colorbrewer](https://colorbrewer2.org) 
and the [Colorbrewer Github Repo](https://github.com/axismaps/colorbrewer/)

```
.
  ├── colorbrewer_schemes.js
  ├── colors.tex
  └── colors_to_tex.py
```

There's three files: the `colorbrewer_schemes.js`, which stems from [github.com/axismaps/colorbrewer/blob/master/colorbrewer_schemes.js](https://github.com/axismaps/colorbrewer/blob/master/colorbrewer_schemes.js) and a python-script `colors_to_tex.py` that uses this as an input to generate the `colors.tex`. To use, simply copy `colors.tex` into your LaTeX project and `\input{colors.tex}`. Minimal example:

```
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\input{colors.tex}

\begin{document}
\textcolor{6_rdylgn_div_PrintSafe_1}{Hello world}.

\begin{tikzpicture}
\filldraw[draw=3_spectral_div_blindSafe_PrintSafe_PhotoCopySafe_1,
          fill=3_spectral_div_blindSafe_PrintSafe_PhotoCopySafe_2
](1.5,4) rectangle (3.5,4.5);
\end{tikzpicture}

\end{document}
```

which should result in

![minimal example](result.png "Minimal Example Result")


## Color Naming Convention

All colors follow this consistent naming pattern:

```
<n><scheme><type>[<safety flags>]<i>
```

- **`<n>`**          : number of classes/colors in the scheme (usually 3–11)
- **`<scheme>`**     : short ColorBrewer scheme name (e.g. `spectral`, `rdylgn`, `puor`, `blues`, `set2`, `set1`, `paired`, ...)
- **`<type>`**       : data type  
  - `sequential`  → ordered progression (low to high)  
  - `diverging`   → two opposing directions with neutral middle (good for anomalies, change, positive/negative values)  
  - `qualitative` → categorical / unordered distinct colors
- **`<safety flags>`** (optional, underscore-separated):  
  - `blindSafe`      → designed to be colorblind-friendly  
  - `PrintSafe`      → safe when printed in grayscale  
  - `PhotoCopySafe`  → remains distinguishable when photocopied  
  (not every scheme has every flag — only those indicated by ColorBrewer are included)
- **`<i>`**          : position in the scheme (1 = first/low value, …, n = last/high value)

**Examples**:
- `5_rdylgn_div_blindSafe_3`   → 5-class RdYlGn diverging scheme, colorblind-safe, middle color
- `7_spectral_div_blindSafe_PrintSafe_PhotoCopySafe_1` → first color (usually red end) of 7-class Spectral diverging scheme, with all three safety properties
- `8_set2_qual_4`              → fourth color in the 8-class qualitative Set2 palette (no safety flags)

**Quick usage tips** (also in `colors.tex` header):
- Diverging data (e.g. anomalies, change): prefer `RdYlBu`, `RdYlGn`, `Spectral`, `PuOr`, `BrBG`, ...
- Sequential/ordered data: use sequential schemes (`Blues`, `YlOrRd`, `Greens`, ...)
- Categorical/nominal data: use qualitative schemes (`Set1`, `Set2`, `Paired`, `Accent`, ...)
- Always prefer schemes with `blindSafe` when color vision deficiency matters.


