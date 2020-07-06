# pv-gemini

ParaView 3-D scientific visualization for Gemini.
Two of the main ways to use Python for ParaView are via:

* IPyParaview: Jupyter Notebook
* PV-Python: Python environment installed with the usual standalone ParaView installer

## IPyParaView

Setup a Python 3.7 (or whatever the current verson of ParaView standalone installer is using) conda environment:

```sh
conda create -n pv37 python=3.7
conda activate pv37

conda install ipython jupyter notebook jupyterlab traitlets
```

### get IPyParaView

```sh
git clone https://github.com/nvidia/ipyparaview

cd ipyparaview
```

* Linux / MacOS: run "./build.sh"
* Windows: run "./build.ps1" from PowerShell, noting workarounds in next section if you get an install OSError.

### setup PYTHONPATH

Create an environment variable pointing to ParaView's Python site-packages. The path will be like:

* Windows: `PARAVIEW_PYTHONPATH=C:\Program Files\ParaView 5.8.0-MPI-Windows-Python3.7-msvc2015-64bit\bin\lib\site-packages\`
* Linux: `PARAVIEW_PYTHONPATH=/opt/ParaView-5.8.0-MPI-Linux-Python3.7-64bit/bin/lib/site-packages/`

We will use this enviroment variable PARAVIEW_PYTHONPATH when running IPyParaView.

### Run examples

The IPyParaView example use a few very widely used data science libraries also useful to geospace science.

```sh
conda install scikit-learn pandas matplotlib
```


#### Basic examples

We use the environment variable PARAVIEW_PYTHONPATH to connect to ParaView's Python libraries.
Before starting Jupyter, each time do:

```sh
conda activate pv37

# Windows only
$env:PYTHONPATH=$env:PARAVIEW_PYTHONPATH

# Linux / MacOS only
export PYTHONPATH=$PARAVIEW_PYTHONPATH
```


```sh
cd notebooks

jupyter
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


### Windows workaround for install

At the moment, there can be a slight one-time install workaround for Windows because Python 3.8 is required to make os.symlink() work correctly.
If you get an [OSError apply the Windows settings](https://www.scivision.dev/windows-symbolic-link-permission-enable/) to enable symlinks.
You may need to create this "ipyparaview" symlink in the Command Prompt like (check that the directories are the same as on your Windows PC):

```posh
mklink /d %userprofile%\miniconda3\envs\py37\share\jupyter\nbextensions\ipyparaview %userprofile%\ipyparaview\ipyparaview\static
```

and then rerun the installer.

We use this script "build.ps1" from PowerShell in place of build.sh:

```posh
$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

pip install -e .
jupyter nbextension install --py --symlink --sys-prefix ipyparaview
jupyter nbextension enable --py --sys-prefix ipyparaview
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install js
```

## ParaView Python API

ParaView 5.8
[install](https://www.paraview.org/download/)
comes with a Python 3.7 Conda environment.
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
