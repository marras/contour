contour
=======

Scripts for creating contour plots for Yukawa colloid phase diagrams.

Requirements:
-------------

- python 2.7 with matplotlib 1.1.1rc, and ScipPy interpolate (min 0.9)
- ruby (1.9 works fine)
- bash
- awk

Usage:
-----

./preprocess.sh x y z constraints

Parameters format: column\_name[=range]
- *column\_name* - name of column (e.g. _charge_), or its part, (_charg_)
- *range* (optional):
  - * - any values
  - 1,5 - values from 1 to 5

