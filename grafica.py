import matplotlib.pyplot as plt
import numpy as np

def create_gauge(value, min_value=0, max_value=100, title="Half-Circle Gauge"):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('off')  # Turn off the axes

    # Define the segments (ranges) and their colors
    segments = [20, 20, 20, 20, 20]  # Five segments for equal spacing
    colors = ['#ff3300', '#ff6600', '#ffcc00', '#ccff66', '#66cc33']

    # Draw the colored segments (only for half-circle)
    wedges, _ = ax.pie(
        segments,
        radius=1,
        colors=colors,
        startangle=180,  # Start at the top (180 degrees)
        counterclock=False,  # Draw clockwise
        wedgeprops={"width": 0.3, "edgecolor": "white"}
    )

    # Calculate the angle for the needle
    angle = 180 - (180 * (value - min_value) / (max_value - min_value))  # Map value to angle
    angle_rad = np.radians(angle)

    # Plot the needle
    ax.plot(
        [0, 0.7 * np.cos(angle_rad)],  # X coordinates
        [0, 0.7 * np.sin(angle_rad)],  # Y coordinates
        color="black", linewidth=3
    )
    ax.plot(0, 0, 'o', color='gray', markersize=10)  # Center circle for the needle pivot

    # Add title and display the value
    plt.title(title, fontsize=14, fontweight="bold")
    plt.text(0, -0.15, f"{value}", horizontalalignment="center", fontsize=12, fontweight="bold")

    # Set limits for the half-circle display
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.1, 1.1)

    return fig

# Example usage
create_gauge(value=25, title="Performance Indicator")