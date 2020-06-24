# pv-gemini

ParaView visualizations for Gemini.

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


## Notes

* ParaView Python API [reference](https://kitware.github.io/paraview-docs/latest/python/)
* ParaView [Guide with examples](https://www.paraview.org/paraview-guide/)
* Matlab can export data to VTK files via [vtkwrite](https://www.mathworks.com/matlabcentral/fileexchange/47814-vtkwrite-exports-various-2d-3d-data-to-paraview-in-vtk-file-format)
