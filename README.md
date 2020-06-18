# pv-gemini

ParaView visualizations for Gemini.

## Quick Start

ParaView 5.8
[install](https://www.paraview.org/download/)
comes with a Python 3.7 Conda environment.
MacOS and Linux have only MPI ParaView downloads.
Windows Gemini users are already using MS-MPI, so they should also use the Windows ParaView MPI installer.

### Minimal example

Many of the ParaView examples use `Show(); Render()`, which generates a frozen, non-interactive window.
To make the 3D plot interactive, use `Interact()` like:

```python
from paraview.simple import *

s = Sphere()
Show()
Interact()
```

## Notes

* ParaView Python API [reference](https://kitware.github.io/paraview-docs/latest/python/)
* ParaView [Guide with examples](https://www.paraview.org/paraview-guide/)
