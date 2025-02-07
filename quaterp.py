import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.spatial.transform import Rotation as R
from mpl_toolkits.mplot3d import Axes3D

def plot_lerp_vs_slerp(q1, q2, n_points=50, birds_eye=False, aligned_view=False, equal_aspect=False):
    # Normalize input quaternions
    q1 /= np.linalg.norm(q1)
    q2 /= np.linalg.norm(q2)

    # Compute dot product and correct sign for shortest path
    dot_product = np.dot(q1, q2)
    if dot_product < 0.0:
        q2 = -q2
        dot_product = -dot_product

    theta_0 = np.arccos(dot_product)  # Angle between q1 and q2
    sin_theta_0 = np.sin(theta_0)

    quaternions_lerp = []
    quaternions_slerp = []

    for t in np.linspace(0, 1, n_points):
        # LERP (Linear interpolation)
        lerp = (1 - t) * q1 + t * q2
        lerp /= np.linalg.norm(lerp)  # Always normalize
        quaternions_lerp.append(lerp)

        # SLERP (Spherical interpolation)
        if sin_theta_0 > 1e-6:
            factor1 = np.sin((1 - t) * theta_0) / sin_theta_0
            factor2 = np.sin(t * theta_0) / sin_theta_0
        else:  # Nearly identical case
            factor1 = 1 - t
            factor2 = t
        slerp = factor1 * q1 + factor2 * q2
        slerp /= np.linalg.norm(slerp)  # Always normalize
        quaternions_slerp.append(slerp)

    # Plot setup
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')

    if equal_aspect:
        # Ensure equal aspect ratio
        for axis in [ax, ax2]:
            axis.set_box_aspect([1,1,1])

    if birds_eye:
        # Set bird's-eye view (looking down the Z-axis)
        for axis in [ax, ax2]:
            axis.view_init(elev=90, azim=0)  # Top-down view
    elif aligned_view:
        # Compute relative rotation quaternion q_rel = q1⁻¹ * q2
        q_rel = R.from_quat(q2) * R.from_quat(q1).inv()
        axis_angle = q_rel.as_rotvec()
        rotation_axis = axis_angle / np.linalg.norm(axis_angle)
        
        # Convert to azimuth and elevation angles
        azim = np.degrees(np.arctan2(rotation_axis[1], rotation_axis[0]))
        elev = np.degrees(np.arcsin(rotation_axis[2]))
        
        for axis in [ax, ax2]:
            axis.view_init(elev=elev, azim=azim)

    # Plot unit sphere for both plots
    for axis in [ax, ax2]:
        axis.set_xlim([-1, 1])
        axis.set_ylim([-1, 1])
        axis.set_zlim([-1, 1])
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        axis.plot_surface(x, y, z, color='lightgrey', alpha=0.1, edgecolor='none')

    # Plot LERP path
    ax.set_title("LERP (Linear Interpolation) Path")
    for i, q in enumerate(quaternions_lerp):
        rotation_vector = R.from_quat(q).apply([1, 0, 0])
        ax.quiver(0, 0, 0, *rotation_vector, color=plt.cm.plasma(i / n_points), length=0.7)
        ax.scatter(rotation_vector[0], rotation_vector[1], rotation_vector[2], color='red', s=50)  # Sphere intersection

    # Plot SLERP path
    ax2.set_title("SLERP (Spherical Interpolation) Path")
    for i, q in enumerate(quaternions_slerp):
        rotation_vector = R.from_quat(q).apply([1, 0, 0])
        ax2.quiver(0, 0, 0, *rotation_vector, color=plt.cm.viridis(i / n_points), length=0.7)
        ax2.scatter(rotation_vector[0], rotation_vector[1], rotation_vector[2], color='red', s=50)  # Sphere intersection

    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Visualize LERP vs SLERP interpolation between quaternions.")
    parser.add_argument("--q1", type=float, nargs=4, default=[1, 0, 0, 0], help="First quaternion (4 values). Default: Identity quaternion [1, 0, 0, 0]")
    parser.add_argument("--q2", type=float, nargs=4, default=[0, 0.7071, 0.7071, 0], help="Second quaternion (4 values). Default: 180 degrees around Y+ axis [0, 0.7071, 0.7071, 0]")
    parser.add_argument("--n_points", type=int, default=8, help="Number of interpolation points. Default: 8")
    parser.add_argument("--birds_eye", action='store_true', help="Show bird's-eye view (default: False).")
    parser.add_argument("--aligned_view", action='store_true', help="View aligned with the rotation plane (default: False).")
    parser.add_argument("--equal_aspect", action='store_true', help="Visualize with equally scaled axes for all three dimensions. More intuitive to pan around, but the default view is not as neat.")
    args = parser.parse_args()
    
    q1 = np.array(args.q1, dtype=np.float64)
    q2 = np.array(args.q2, dtype=np.float64)
    
    plot_lerp_vs_slerp(q1, q2, n_points=args.n_points, birds_eye=args.birds_eye, aligned_view=args.aligned_view, equal_aspect=args.equal_aspect)


if __name__ == "__main__":
    main()

