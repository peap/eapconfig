#!/bin/bash
#
# Convert a string argument containing LaTeX markup to a PNG image
#
# Example: latex2png.sh '$$F_G = \frac{Gm_1 m_2}{r^2}$$'
# Example: latex2png.sh '\LaTeX'
#

if ! TEST=$(which latex) ; then
  echo "You must install latex."
  exit 1
fi

if ! TEST=$(which dvipng) ; then
  echo "You must install dvipng."
  exit 2
fi

_OUT_FILE_=latex_out.png
_TEMP_BASE_=_latex_temp_

# create temporary LaTeX file
cat > $_TEMP_BASE_.tex <<_end_LaTeX_
\documentclass{article}
  \begin{document}
  \pagestyle{empty}
  $1
\end{document}
_end_LaTeX_

# typeset LaTeX file to DVI
latex $_TEMP_BASE_.tex

# convert DVI to PNG
dvipng -T tight -bg Transparent -D 500 -o $_OUT_FILE_ $_TEMP_BASE_.dvi

# clean-up
rm $_TEMP_BASE_.*

