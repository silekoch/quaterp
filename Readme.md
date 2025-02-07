# Quaterp - LERP vs SLERP Visualization

<img width="1092" alt="image" src="https://github.com/user-attachments/assets/485fa162-8084-44b8-bbc3-65db5aefa760" />

`quaterp` visualizes the difference between two types of quaternion interpolation techniques: **LERP** (Linear Interpolation) and **SLERP** (Spherical Linear Interpolation). It provides an interactive 3D plot to compare how quaternions evolve through these interpolation methods.

## Features
- Input quaternions as command-line arguments.
- Visualize the path of quaternions as they interpolate between two points using both LERP and SLERP.
- Pan around to understand the interpolation path in 3D.
- Pick between different views and aspect ratios of the 3D plot.


## Installation

Install the necessary dependencies via pip:
```
pip install numpy scipy matplotlib
```

## Usage

Run the script via the command line to visualize the LERP vs SLERP interpolation:

```
python quaterp.py --q1 1 0 0 0 --q2 0 0.7071 0.7071 0 --n_points 30
```

Command-line arguments:
- `--q1`: First quaternion (4 values, defaults to [1, 0, 0, 0] for identity quaternion).
- `--q2`: Second quaternion (4 values, defaults to [0, 0.7071, 0.7071, 0] for 180-degree rotation around the Y-axis).
- `--n_points`: Number of interpolation points (default: 50).
- `--birds_eye`: Set bird's-eye view (looking down the Z-axis).
- `--aligned_view`: Set the view aligned with the rotation plane.
- `--equal_aspect`: Set equal scaling for the axes.

<img width="1092" alt="image" src="https://github.com/user-attachments/assets/3cb01d50-f24b-4d0b-be14-82aac28a2f90" />


The script generates two side-by-side 3D plots:

LERP (Linear Interpolation): The linear path between the two quaternions.

SLERP (Spherical Interpolation): The spherical path that smoothly interpolates between the two quaternions.

Both paths are visualized on the surface of a unit sphere (red dots), with the quaternion rotation vectors shown as arrows. The path for LERP is plotted in a plasma colormap, and for SLERP in a viridis colormap.

In order to see the difference between LERP and SLERP visualize fewer points and look at the rotation from the axis perpendicular to it: 

```
python quaterp.py --q1 1 0 0 0 --q2 0 0.7071 0.7071 0 --n_points 8 --aligned_view
```

<img width="1092" alt="image" src="https://github.com/user-attachments/assets/2bd88d0d-b139-48c7-b7bf-dd247d73ebd6" />


Focus on the path indicated by the red dots on the surface of the sphere. Squint your eyes and you see that the LERP equally spaced steps are distorted by the reprojection to the unit sphere while SLERP made sure that the equally spaced steps where on the unit sphere in the first place.

Feel free to run the script yourself, pan around, look at it from different angles and experiment with different rotations (quaternions). E.g. (0.57, 0.57, 0.57, 0) might be interesting :)

## Requirements:

Python 3.x

Required libraries:
- numpy
- scipy
- matplotlib

## License:

This project is licensed under the MIT License - see the LICENSE file for details.
