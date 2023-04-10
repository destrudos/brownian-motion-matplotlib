import matplotlib.pyplot as plt
import numpy as np

# Define the simulation parameters
n_particles = 13
n_steps = 1000
vessel_width = 150
vessel_height = 150
particle_radius = 2
dt = 0.1

# Set up the initial particle positions and velocities
positions = np.random.rand(n_particles, 2) * (vessel_width - 2 * particle_radius) + particle_radius
velocities = np.zeros((n_particles, 2))

# Define a function to update the particle positions
def update_positions(positions, velocities, dt):
    # Add a random displacement to each particle based on the Brownian motion model
    displacements = np.random.normal(loc=0, scale=np.sqrt(2*dt), size=(n_particles, 2))
    positions += displacements

    # Check for collisions with the walls of the vessel
    positions = np.where(positions < particle_radius, 2 * particle_radius - positions, positions)
    positions = np.where(positions > vessel_width - particle_radius, 2 * (vessel_width - particle_radius) - positions, positions)
    positions = np.where(positions < particle_radius, 2 * particle_radius - positions, positions)
    positions = np.where(positions > vessel_height - particle_radius, 2 * (vessel_height - particle_radius) - positions, positions)

    # Check for collisions between particles
    for i in range(n_particles):
        for j in range(i+1, n_particles):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < 2 * particle_radius:
                overlap = 2 * particle_radius - dist
                direction = (positions[i] - positions[j]) / dist
                positions[i] += overlap / 2 * direction
                positions[j] -= overlap / 2 * direction

    return positions

# Create a plot to display the simulation results
fig, ax = plt.subplots()
ax.set_xlim(0, vessel_width)
ax.set_ylim(0, vessel_height)

# Generate random colors for the particles
colors = np.random.rand(n_particles, 3)

# Create a list of particle circles with random colors
particles = [plt.Circle((0, 0), particle_radius, color=colors[i]) for i in range(n_particles)]

# Add the particle circles to the plot
for p in particles:
    ax.add_artist(p)

# Define the animation function to update the plot with new particle positions
def animate(frame):
    global positions, velocities
    positions = update_positions(positions, velocities, dt)
    for i, p in enumerate(particles):
        p.center = positions[i]
    return particles

# Animate the plot
from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, frames=n_steps, interval=50, blit=True)
plt.show()
