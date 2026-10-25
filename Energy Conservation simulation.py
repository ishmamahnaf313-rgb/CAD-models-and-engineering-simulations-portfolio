import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

#Constant Variable
g = 9.81
m = float(input("Enter the mass in kg: "))
a = 0.2

h0_initial = 6.0
E_total = m*h0_initial*g
x_initial = np.sqrt(h0_initial/a)
t = 0.0
is_playing = True

fig = plt.figure()
ax_track = plt.subplot2grid((1,5), (0,0), colspan=3)
ax_bars = plt.subplot2grid((1,5), (0,3), colspan=2)
plt.subplots_adjust(bottom = 0.25, wspace = 0.4)

#The Bowl Drawing
x_bowl = np.linspace(-6, 6, 500)
y_bowl = a*x_bowl**2
ax_track.plot(x_bowl, y_bowl, color = "blue", lw = 3)
ax_track.set_xlim(-6,6)
ax_track.set_ylim(-1,8)
ax_track.set_title("Energy Conservation Simulation", fontsize = 14)
ax_track.set_xlabel("Horizontal Position/m")
ax_track.set_ylabel("Vertical Position/m")
ax_track.grid(True, linestyle = "--", alpha = 0.5)

#Ball element and height tracking line
ball, = ax_track.plot([], [], 'o', color = "red", markersize = 15)
height_line = ax_track.axhline(0, color = "grey", linestyle = ":", alpha = 0.6)
height_text = ax_track.text(0.5, 4.0, '', color = "black", fontsize = 14)

#Energy Bar Charts
bar_labels = ['PE', 'KE']
bars = ax_bars.bar(bar_labels, [0,0], color = ['pink', 'green'], width = 0.5)
ax_bars.set_ylim(0,80)
ax_bars.set_ylabel("Energy in joules")
energy_text = ax_bars.text(0.1, 72, '', fontsize = 11, fontweight = 'bold')
vel_text = ax_bars.text(0.1,6, '', fontsize = 11, color = 'black', fontweight = 'bold')

#sliders and play buttons
ax_slider = plt.axes([0.15, 0.1, 0.4, 0.03])
slider_h0 = Slider(ax_slider, 'Starting height', 1.0, 7.0, valinit = h0_initial, valfmt = '%1.1f m')
ax_btn = plt.axes([0.7, 0.1, 0.1, 0.04])
btn_play = Button(ax_btn, 'Pause')

def update_slider(val):
    global h0_initial, E_total, x_initial, t
    h0_initial = slider_h0.val
    E_total = m*h0_initial*g
    x_initial = np.sqrt(h0_initial/a)
    t = 0.0

slider_h0.on_changed(update_slider)

def toggle_play(event):
    global is_playing
    if is_playing:
        is_playing = False
        btn_play.label.set_text("Play")
    else:
        is_playing = True
        btn_play.on_clicked(toggle_play)

#Animation Loop
def animate(frame):
    global t, E_total, h0_initial, x_initial
    if is_playing:
        t +=0.01

    omega = np.sqrt(2*a*g)
    x = x_initial*np.cos(omega*t)
    y = a*x**2

    pe = m*g*y
    ke = max(0.0, E_total-pe)
    v = np.sqrt((2*ke)/m)

    #update track elements
    ball.set_data([x], [y])
    height_line.set_ydata([y])

    height_text.set_position((x+0.3, y+0.2))
    height_text.set_text(f"h={y:.1f}m")

    bars[0].set_height(pe)
    bars[1].set_height(ke)
    energy_text.set_text(f"Total Energy: {E_total:.1f} joules")
    vel_text.set_text(f'PE: {pe:.1f} joules | KE: {ke:.1f} joules\nv = {v:.1f} m/s')

    return ball, height_line, height_text, bars[0], bars[1], energy_text

ani = animation.FuncAnimation(fig, animate, interval=30, blit=False, cache_frame_data = False)
plt.show()

