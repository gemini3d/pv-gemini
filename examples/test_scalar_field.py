#!/usr/bin/env python3
"""
example of 3D scalar field

If you get this error, ParaView doesn't know your data file format:
TypeError: TestFileReadability argument %Id: %V
"""

from pathlib import Path
import argparse

import paraview.simple as pvs

p = argparse.ArgumentParser()
p.add_argument("fn", help="data file to load with paraview OpenDataFile()")
P = p.parse_args()

fn = Path(P.fn).expanduser()

if not fn.is_file():
    raise FileNotFoundError(fn)

pvs.OpenDataFile(fn)
