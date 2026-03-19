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



