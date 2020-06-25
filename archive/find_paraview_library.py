#!/usr/bin/env python3
r"""
find ParaView Python library directory

NOTE: due to complexity of ParaView + VTK + Python, this technique doesn't work, kept as "null result"

Traceback (most recent call last):
  File "find_paraview_library.py", line 25, in <module>
    import paraview.simple
  File "C:\Program Files\ParaView 5.8.0-MPI-Windows-Python3.7-msvc2015-64bit\bin\Lib\site-packages\paraview\simple.py", line 41, in <module>
    from paraview import servermanager
  File "C:\Program Files\ParaView 5.8.0-MPI-Windows-Python3.7-msvc2015-64bit\bin\Lib\site-packages\paraview\servermanager.py", line 3264, in <module>
    vtkProcessModule.PROCESS_CLIENT, pvoptions)
TypeError: Initialize argument %Id: %V

File formats ParaView can read:
https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_readers
"""
import os
import sys
import shutil
from pathlib import Path

binpath = ""

if os.name == "nt":
    binpath = shutil.which("pvpython")
    if not binpath:
        pv = list(Path("C:/Program Files/").rglob("Paraview*/bin/pvpython.exe"))
        if not pv:
            raise ImportError("could not find Paraview Python libraries")
        binpath = Path(pv[0]).parent / "Lib/site-packages"

if binpath:
    sys.path.append(str(binpath))
print(sys.path)

import paraview.simple

print(binpath)
