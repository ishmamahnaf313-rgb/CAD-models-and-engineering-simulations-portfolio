import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

speed = float(input("Enter Launch Speed: "))
a = float(input("Enter Launch Angle: "))
angle = math.radians(a)

vx = speed*math.cos(angle)
vy = speed*math.sin(angle)

x = 0
y = 0

g = -9.81
dt = 0.01

x_history = [x]
y_history = [y]

while y>=0:
    vy = vy + g*dt
    x = x + vx*dt
    y = y + vy*dt
    if y >= 0:
        x_history.append(x)
        y_history.append(y)

fig, ax = plt.subplots()
ax.set_xlim(0, max(x_history) * 1.1)
ax.set_ylim(0, max(y_history) * 1.2)
ax.set_title("Projectile Motion Simulation")
ax.set_xlabel("Horizontal Distance (m)")
ax.set_ylabel("Vertical Height (m)")
ax.grid(True)

# Plot elements: trajectory line and active projectile point
line, = ax.plot([], [], 'b-', lw=2, label="Trajectory")
point, = ax.plot([], [], 'ro', markersize=8, label="Projectile")
ax.legend()

# --- Animation Functions ---
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def update(frame):
    # Reveal trajectory up to current frame
    line.set_data(x_history[:frame], y_history[:frame])
    # Position of the moving projectile
    point.set_data([x_history[frame]], [y_history[frame]])
    return line, point

# Create animation (interval in milliseconds between frames)
anim = FuncAnimation(
    fig,
    update,
    frames=len(x_history),
    init_func=init,
    interval=10,
    blit=True,
    repeat=False
)

plt.show()





