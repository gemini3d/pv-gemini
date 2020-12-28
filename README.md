# pv-gemini

ParaView 3-D scientific visualization for Gemini.
Use [Python with ParaView](https://www.paraview.org/python/) via:

* IPyParaview: Jupyter Notebook
* PV-Python: Python environment installed with the usual standalone ParaView installer

## IPyParaView

Setup a conda environment with the same version of Python as used by the ParaView installer.
For example, ParaView 5.9 uses Python 3.8

```sh
conda create -n pv5.9 python=3.8
conda activate pv5.9

conda install numpy ipython jupyter notebook jupyterlab traitlets
```

### get IPyParaView

```sh
git clone https://github.com/nvidia/ipyparaview

cd ipyparaview

./build.sh  # Linux / MacOS

./build.ps1  # Windows
```

On Windows, we use this script "build.ps1" for Windows PowerShell in place of build.sh:

```posh
$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

pip install -e .
jupyter nbextension install --py --symlink --sys-prefix ipyparaview
jupyter nbextension enable --py --sys-prefix ipyparaview
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install js
```

### setup PYTHONPATH

Create an **environment variable** `PARAVIEW_PYTHONPATH` pointing to ParaView's Python site-packages. The path will be like:

* Windows: `C:\Program Files\ParaView 5.9.0-MPI-Windows-Python3.8-msvc2017-64bit\bin\lib\site-packages\`
* Linux: `/opt/ParaView-5.9.0-MPI-Linux-Python3.8-64bit/bin/lib/site-packages/`

Enviroment variable `PARAVIEW_PYTHONPATH` is necessary for running IPyParaView.

## Examples

IPyParaView examples need these popular Python libraries:

```sh
conda install scikit-learn pandas matplotlib
```

### Basic examples

Environment variable PARAVIEW_PYTHONPATH points to ParaView's Python libraries.
Before starting Jupyter to use IPyParaview, each time do:

```sh
conda activate pv5.9

# Windows PowerShell
$env:PYTHONPATH=$env:PARAVIEW_PYTHONPATH

# Linux / MacOS
export PYTHONPATH=$PARAVIEW_PYTHONPATH
```

```sh
cd notebooks

jupyter notebook
```

and use the web browser Jupyter Notebook that automatically opens to browse and run the examples.
We suggest examples below, which do not require a discrete GPU (they run on a light laptop):

* Hello_Jupyter-ParaView.ipynb
* Iso-Surfaces_with_RTX.ipynb  "RTX" requires an appropriate GPU

#### Advanced examples (not for beginning user)

The example using `cuml` "UMAP MNIST Example.ipynb" requires a Linux system with GPU due to
[cuml requirements](https://rapids.ai/start.html),
which is for advanced users.
cuml is a general machine learning GPU library unrelated to IPyParaView.

Also the Dask example "Dask-MPI_Volume_Render" is for running on Dask-MPI HPC cluster, which would need to be setup by your IT staff perhaps.

## ParaView Python API

ParaView
[installer ](https://www.paraview.org/download/)
comes with a Python 3 Conda environment.
MacOS and Linux have only MPI ParaView downloads.
Windows Gemini users are already using MS-MPI, so they should also use the Windows ParaView MPI installer.

### Load NetCDF

ParaView expects
[COARDS](http://wiki.seas.harvard.edu/geos-chem/index.php/The_COARDS_netCDF_conventions_for_earth_science_data)
/ CF format NetCDF4 files.
However, non-COARDS, non-CF single variable files can be loaded with the plain NetCDF filter.
In the ParaView GUI, select "Volume" and the variable name to actually render the data.
An animated camera path can be [created](https://www.paraview.org/Wiki/Advanced_Animations#Follow_Path).

ParaView can load single-variable NetCDF4 files.
To use a grid, which is particularly important for non-uniform gridded ionospheric data, store the NetCDF4 data with the grid data embedded in the file.
For [PyGemini](https://github.com/gemini3d/pygemini),
the "convert_data" scripts store the grid in the NetCDF file.

The data needs to be filtered to display as a volume in ParaView.
In the "Pipeline Browser" right click the .nc filename, Add Filter, Resample as Image
Then, in the Properties browser, select Representation: Volume.
The data can be sampled with Property "Sampling Dimensions" at higher resolution, but this takes proportionately more GPU resources.
If your computer does not have a discrete GPU, using more than about 256 grid points in a dimension may crash ParaView, even with 16 GB RAM.
If your computer has a discrete GPU, 1024 or more points per dimension may be possible, with proportionately slower rendering.

A key feature of ParaView is that it gracefully degrades to render 3D output even on modest devices, as long as you don't select too large Sampling Dimensions.

Many of the ParaView examples use `Show(); Render()`, which generates a frozen, non-interactive window.
To make the 3D plot interactive, use `Interact()` like:

```python
from paraview.simple import *

s = Sphere()
Show()
Interact()
```

### Render a video (YouTube-compatible)

This animated path can be [saved as a movie](https://www.paraview.org/Wiki/Beginning_Pictures_and_Movies#Save_Animation_.28make_a_movie.29).
Note that saving in .ogv format can use 99.5% less disk space than AVI.

### Save ParaView state to .py

If you make a workflow in the ParaView GUI interactively, this state can be rendered to Python .py code by File &rarr; Save State and selecting Python file type output.

### Am I using CPU or GPU

This may be determined from the ParaView Help &rarr; About menu.
Scrolling to the bottom of the About windows, example the lines

* OpenGL Vendor
* OpenGL Version
* OpenGL Renderer

For example, if the OpenGL Renderer is "Intel UHD" that is using the non-discrete, low capability GPU inside the CPU, which can render small renderings, not bigger than about 256 grid points per dimension.

If you have an Nvidia GPU, the Nvidia
[System Management Interface](https://developer.nvidia.com/nvidia-system-management-interface)
is run from system Terminal like:

```sh
nvidia-smi
```

If the "Processes" section says "No running processes found" while ParaView is open, then you are probably not using the Nvidia GPU.

Detailed GPU status is obtained from

```sh
nvidia-smi -q
```

Look for lines like:

```
GPU Operation Mode
    Current                           : N/A
    Pending                           : N/A
```

"N/A" or "Compute" indicates the GPU is not active for visualization.
"All On" means the GPU is available for visualization.


## Notes

* ParaView Python API [reference](https://kitware.github.io/paraview-docs/latest/python/)
* ParaView [Guide with examples](https://www.paraview.org/paraview-guide/)
* Matlab can export data to VTK files via [vtkwrite](https://www.mathworks.com/matlabcentral/fileexchange/47814-vtkwrite-exports-various-2d-3d-data-to-paraview-in-vtk-file-format)
