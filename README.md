# pv-gemini

ParaView 3-D scientific visualization for Gemini.

## Quick Start

ParaView 5.8
[install](https://www.paraview.org/download/)
comes with a Python 3.7 Conda environment.
MacOS and Linux have only MPI ParaView downloads.
Windows Gemini users are already using MS-MPI, so they should also use the Windows ParaView MPI installer.

### Loading data

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

* Nvidia [GPU Tech Conference](https://www.nvidia.com/en-us/gtc/topics/high-performance-supercomputing/)
