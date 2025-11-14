import numpy as np
from math import *
import time


def generate_hexagon_centers(diagonal_angle_degrees=7.5):
    """
    Generate hexagon centers for tessellating a sphere.
    Uses a fibonacci sphere or icosahedron-based approach.

    For 7.5° diagonal, we need approximately:
    - Sphere surface area = 4π
    - Hexagon area ≈ (diagonal/2)^2 * 3*sqrt(3)/2 in steradians
    - Number of hexagons ≈ 4π / hexagon_area
    """

    # Convert diagonal angle to radians
    diagonal_rad = np.radians(diagonal_angle_degrees)

    # Estimate number of points needed
    # For hexagon with diagonal d, area ≈ 0.65 * d^2 (in steradians for small angles)
    hexagon_area = 0.65 * diagonal_rad**2
    n_points = int(4 * np.pi / hexagon_area)

    print(f"Generating approximately {n_points} hexagon centers")
    print(f"Diagonal angle: {diagonal_angle_degrees}°")

    # Use Fibonacci sphere algorithm for uniform distribution
    centers = []
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio

    for i in range(n_points):
        # Fibonacci sphere algorithm
        y = 1 - (2 * i / (n_points - 1))  # y goes from 1 to -1
        radius = np.sqrt(1 - y**2)

        theta = 2 * np.pi * i / phi

        x = np.cos(theta) * radius
        z = np.sin(theta) * radius

        centers.append([x, y, z])

    return np.array(centers)


def find_neighbors(centers, max_distance_factor=1.5):
    """
    Find neighboring points for each center.
    Two points are neighbors if their angular distance is within max_distance_factor times the average.
    """
    n = len(centers)

    # Calculate average nearest neighbor distance
    min_distances = []
    for i in range(min(100, n)):  # Sample first 100 points
        distances = []
        for j in range(n):
            if i != j:
                # Angular distance between unit vectors
                cos_angle = np.clip(np.dot(centers[i], centers[j]), -1, 1)
                angle = np.arccos(cos_angle)
                distances.append(angle)
        min_distances.append(min(distances))

    avg_min_distance = np.mean(min_distances)
    threshold = avg_min_distance * max_distance_factor

    print(
        f"Average nearest neighbor distance: {np.degrees(avg_min_distance):.2f}°")
    print(f"Neighbor threshold: {np.degrees(threshold):.2f}°")

    # Find all neighbors
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            cos_angle = np.clip(np.dot(centers[i], centers[j]), -1, 1)
            angle = np.arccos(cos_angle)

            if angle <= threshold:
                edges.append((i, j))

    print(f"Total edges: {len(edges)}")
    return edges


def find_edges(ps):

    lmt = 0.954555620192181
    res = []
    # ylmt=0.3026311666666667
    for i in range(0, len(ps)-1):
        theta = acos(1-abs(ps[i][1]))
        ylmt = max(abs(sin(0.3+theta)), sin(theta))*0.3 + ps[i][1]
        j = i+1
        while ps[j][1] < ylmt:
            if np.dot(ps[i], ps[j]) > lmt:
                res.append((i, j))
            j += 1
            if j>=len(ps):
                break
    return res


def get_pNe():
    ps = generate_hexagon_centers(diagonal_angle_degrees=15)
    ps = ps[2:-2]
    
    start = time.perf_counter()
    es = find_edges([np.array(i) for i in ps])
    end = time.perf_counter()
    elapsed_us = (end - start) * 1_000_000
    print(f"Execution time: {elapsed_us:.2f} µs")
    
    # start = time.perf_counter()
    # find_neighbors(ps)
    # end = time.perf_counter()
    # elapsed_us = (end - start) * 1_000_000
    # print(f"Execution time: {elapsed_us:.2f} µs")
    
    # print(len(es))
    return ps, es

if __name__ == "__main__":
    get_pNe()
