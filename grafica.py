import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


def create_gauge(value, min_value=0, max_value=100):
    """
    Crea un gráfico tipo gauge con rangos de colores.

    Args:
        value (float): Valor actual a mostrar en el gauge (0-100)
        min_value (float): Valor mínimo del rango
        max_value (float): Valor máximo del rango
    Returns:
        matplotlib.figure.Figure: La figura del gráfico
    """
    # Crear la figura y el eje
    fig, ax = plt.subplots(figsize=(8, 4))

    # Configurar los límites y aspecto del eje
    ax.set_aspect('equal')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.6, 1.2)

    # Ocultar los ejes
    ax.axis('off')

    # Definir colores para cada segmento (ahora de rojo a verde)
    colors = ['#ff3232', '#ff6b32', '#ffa332', '#7ab55c', '#32b532']  # Rojo a verde

    # Definir los rangos para cada segmento (de 0 a 100)
    ranges = [
        (0, 20),  # Rojo
        (20, 40),  # Naranja rojizo
        (40, 60),  # Naranja
        (60, 80),  # Verde claro
        (80, 100)  # Verde
    ]

    # Dibujar los segmentos del arco
    radius = 1
    start_angle = 180  # Comenzar desde la izquierda

    for i, (range_min, range_max) in enumerate(ranges):
        # Calcular ángulos para cada segmento
        angle_min = start_angle * (1 - (range_min - min_value) / (max_value - min_value))
        angle_max = start_angle * (1 - (range_max - min_value) / (max_value - min_value))

        arc = Arc((0, 0), radius * 2, radius * 2,
                  theta1=angle_max, theta2=angle_min,
                  angle=0, color=colors[i], lw=20)
        ax.add_patch(arc)

    # Calcular ángulo para el valor actual
    needle_angle = start_angle * (1 - (value - min_value) / (max_value - min_value))
    needle_angle_rad = np.radians(needle_angle)

    # Dibujar la aguja
    needle_length = 0.9
    x = needle_length * np.cos(needle_angle_rad)
    y = needle_length * np.sin(needle_angle_rad)

    # Triángulo para la aguja
    ax.plot([0, x], [0, y], color='black', lw=3, zorder=5)

    # Círculo central
    circle = plt.Circle((0, 0), 0.1, color='#404040', zorder=6)
    ax.add_artist(circle)

    # Añadir el valor actual
    ax.text(0, -0.2, f'{value}', ha='center', va='center',
            fontsize=24, fontweight='bold', color='#404040')

    return fig
=======
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
