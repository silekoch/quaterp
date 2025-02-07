# Quaterp - LERP vs SLERP Visualization

<img width="1092" alt="image" src="https://github.com/user-attachments/assets/485fa162-8084-44b8-bbc3-65db5aefa760" />

`quaterp` visualizes the difference between two types of quaternion interpolation techniques: **LERP** (Linear Interpolation) and **SLERP** (Spherical Linear Interpolation). It provides an interactive 3D plot to compare how quaternions evolve through these interpolation methods.

## Features
- Input quaternions as command-line arguments.
- Visualize the path of quaternions as they interpolate between two points using both LERP and SLERP.
- Pan around to understand the interpolation path in 3D.
- Pick between different views and aspect ratios of the 3D plot.


## Background on Quaternions
This probably doesn't make a lot of sense if you are not already pretty familiar with quaternions. For a 'quick' introduction check out 3Blue1Brown on [Quaternions 1](https://www.youtube.com/watch?v=d4EgbgTm0Bg) (30 min). For a very thorough introduction also check out [Quaternions 2](https://www.youtube.com/watch?v=zjMuIxRvygQ) (6 min), Ben Eater's [interactive videos](https://eater.net/quaternions), 3Blue1Brown on [Euler's Formula 1](https://www.youtube.com/watch?v=mvmuCPvRoWQ) (24 min) and [Euler's Formula 2](https://www.youtube.com/watch?v=v0YEaeIClKY) (3 min).

Follow-up recommendations by 3Blue1Brown: 
 - [Gimbal lock](https://www.youtube.com/watch?v=zc8b2Jo7mno&t=0s) (8 min)
 - Comparing [Euler angles and quaternions 1](https://www.youtube.com/watch?v=syQnn_xuB8U&t=0s) (10 min) and [Euler angles and quaternions 2](https://www.youtube.com/watch?v=4mXL751ko0w&t=0s) (16 min) from the perspective of an animator. Contains nice mental model to interpret the orientation after an quaternion rotation as mixture of orientations, much like color is a mixture of colors. 
 - [Quanta magazine article](https://www.quantamagazine.org/the-strange-numbers-that-birthed-modern-algebra-20180906) on quaternions
 - Fun [connection with Alice in Wonderland](https://www.newscientist.com/article/mg20427391-600-alices-adventures-in-algebra-wonderland-solved)

This might seem a little bit excessive, but trust me it's worth it ;) Have fun!

### Rotations with Quaternions
You can use unit quaternions to model 3D rotations elegantly. A really nice intuition for that is to think of it as a mixture of four 180 degree rotated orientations. (See the two videos on Euler angles and quaternions above).

You have the base orientation corresponding to (1, 0, 0, 0) and then three 180 degree rotations along the three different axis corresponding to (0, 1, 0, 0), (0, 0, 1, 0) and (0, 0, 0, 1) respectively. When you mix them and normalize to unit quaternions you get a mixture of the orientations proportional to the weight you gave each.

E.g. (0, 0.71, 0.71, 0) would be an interpolation of a 180 degree rotation about the i and j axis (try it in the interactive videos above). That's a little hard to imagine, but imagine (0.57, 0.57, 0.57, 0), it's an interpolation of the base orientation and equal parts of each of the other two 180 degrees rotations. I.e. it's the interpolation of equal parts of a 180 degree rotation about the i axis and a 180 degree rotation about the j axis. The original orientation is still in the mix, but slightly dominated by the combination of the two others. This points the north pole at 45 degrees between the axis i and j and at a little bit more than 90 degrees from the original pole.

You get the exact 90 degree rotation from the pole with 45 degrees from the i and j axis, if you use (0.71, 0.5, 0.5, 0), because in this case you mix both, the i and j 180 degrees rotations equally, but rebalance for the fact that they dominate the real axis, as they are two and the real axis is just one. 

### Quaternion Interpolation
Often we want to interpolate between quaternions. E.g. when we try to simulate a transition between two orientations by showing frames of intermediate orientations in an animation. 

With LERP we define a direct path in the 4 dimensional space, but leave the unit sphere. Thus we get non-unit quaternions. One example would be t=0.5, q_1 = (0, 0.71, 0.71, 0), q_2 = (0, 0.71, 0, 0.71) and their LERP interpolation would be (0, 0.71, 0.355, 0.355) with sqrt(0.71^2 + 0.355^2 + 0.355^2)‎ = 0.87. In order to still get a valid rotation interpolation, we normalize back to the unit sphere. This results in distortions, because while we make equal sized steps in the hyperspace, projecting them back on the unit sphere makes them differently sized. 

With SLERP we make sure to stay on the hypersphere in the first place and thus can easily define equal sized partial rotation steps by defining equal sized time steps in the interpolation. We can also define arbitrary non-equal sized time steps and make the movement slower in the beginning and end and faster in the middle or something like that.


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
