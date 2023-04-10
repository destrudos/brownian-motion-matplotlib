import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Define the simulation parameters
n_particles = 13
n_steps = 1000
vessel_width = 150
vessel_height = 150
particle_width = 2
particle_length = 8
dt = 0.1

# Set up the initial particle positions, velocities, and angles
positions = np.random.rand(n_particles, 2) * (vessel_width - 2 * particle_width) + particle_width
velocities = np.zeros((n_particles, 2))
angles = np.random.rand(n_particles) * 360

# Define a function to update the particle positions and angles
def update_positions(positions, velocities, angles, dt):
    # Add a random displacement to each particle based on the Brownian motion model
    displacements = np.random.normal(loc=0, scale=np.sqrt(2*dt), size=(n_particles, 2))
    positions += displacements

    # Apply damping to the velocities
    velocities *= 0.01

    # Check for collisions with the walls of the vessel
    positions = np.where(positions < particle_width, 2 * particle_width - positions, positions)
    positions = np.where(positions > vessel_width - particle_width, 2 * (vessel_width - particle_width) - positions, positions)
    positions = np.where(positions < particle_width, 2 * particle_width - positions, positions)
    positions = np.where(positions > vessel_height - particle_width, 2 * (vessel_height - particle_width) - positions, positions)

    # Check for collisions between particles
    for i in range(n_particles):
        for j in range(i+1, n_particles):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < particle_length:
                overlap = particle_length - dist
                direction = (positions[i] - positions[j]) / dist
                positions[i] += overlap / 2 * direction
                positions[j] -= overlap / 2 * direction
                velocities[i] -= overlap / 2 * direction
                velocities[j] += overlap / 2 * direction

    # Add a random rotation to each particle around its center
    angles += np.random.normal(loc=0, scale=5, size=n_particles)

    # Update the positions with the velocities
    positions += velocities * dt

    return positions, angles

# Create a plot to display the simulation results
fig, ax = plt.subplots()
ax.set_xlim(0, vessel_width)
ax.set_ylim(0, vessel_height)

# Generate random colors for the particles
colors = np.random.rand(n_particles, 3)

# Create a list of particle rectangles with random colors and angles
particles = [Rectangle((0, 0), particle_length, particle_width, angle=angles[i], color=colors[i]) for i in range(n_particles)]

# Add the particle rectangles to the plot
for p in particles:
    ax.add_artist(p)

# Define the animation function to update the plot with new particle positions and angles
def animate(frame):
    global positions, velocities, angles
    positions, angles = update_positions(positions, velocities, angles, dt)
    for i, p in enumerate(particles):
        p.set_xy(positions[i] - np.array([particle_length / 2, particle_width / 2]))
        p.set_angle(angles[i])
    return particles

# Animate the plot
from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, animate, frames=n_steps, interval=50, blit=True)
plt.show()
