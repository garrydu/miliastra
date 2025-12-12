import numpy as np
import plotly.graph_objects as go

def create_sphere_with_circle(points):
    """
    Create a blue sphere with a green circular region.
    
    Parameters:
    - center_vector: tuple (x, y, z) - unit vector pointing to circle center
    - arc_angle_degrees: float - angular radius of the green circle in degrees
    """
    
    # Create sphere coordinates
    u = np.linspace(0, 2 * np.pi, 200)
    v = np.linspace(0, np.pi, 200)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Initialize colors - all blue
    colors = np.zeros_like(x)
    
    for center_vector, arc_angle_degrees in points:
        # Normalize the center vector to ensure it's a unit vector
        center = np.array(center_vector)
        center = center / np.linalg.norm(center)
    
        # Convert arc angle to radians
        arc_angle_rad = np.radians(arc_angle_degrees)
        
        # Calculate angular distance from center point for each point on sphere
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                # Current point on sphere
                point = np.array([x[i, j], y[i, j], z[i, j]])
                
                # Calculate angular distance using dot product
                # cos(angle) = dot(v1, v2) for unit vectors
                cos_angle = np.dot(point, center)
                # Clamp to [-1, 1] to avoid numerical errors
                cos_angle = np.clip(cos_angle, -1, 1)
                angle = np.arccos(cos_angle)
                
                # If within the circle radius, color it green (1), else blue (0)
                if angle <= arc_angle_rad:
                    colors[i, j] = 1
        
    # Create custom colorscale: 0 = blue, 1 = green
    colorscale = [[0, 'blue'], [1, 'green']]
    
    # Create the 3D surface plot
    fig = go.Figure(data=[go.Surface(
        x=x, y=y, z=z,
        surfacecolor=colors,
        colorscale=colorscale,
        showscale=False,
        cmin=0,
        cmax=1
    )])
    
    # Add a marker at the center point for reference
    fig.add_trace(go.Scatter3d(
        x=[center[0]],
        y=[center[1]],
        z=[center[2]],
        mode='markers',
        marker=dict(size=5, color='red'),
        name='Circle Center'
    ))
    
    # Update layout
    fig.update_layout(
        title=f'Sphere with Green Circle<br>Center: ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f}), Arc Angle: {arc_angle_degrees}°',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=800,
        height=800
    )
    
    return fig