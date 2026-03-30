from numpy import sin, cos, pi, linspace
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

g, L, m = 9.81, 4.0, 1.0   # Acceleration due to gravity (m/s^2), length of the pendulum (m), and mass of the bob (kg)
initial_conditions = [pi / 4, 0]  # Initial angle and initial angular velocity
t_span = (0, 100)  # Time span for the simulation (0 to 100 seconds)
t_eval = linspace(t_span[0], t_span[1], 10000)  # Time points to evaluate the solution

def pendulum(t, y):
    return [y[1], -(g/L) * sin(y[0])]

# Solving the differential equation using solve_ivp
solution = solve_ivp(pendulum, t_span, initial_conditions, t_eval=t_eval)

# Extracting the results
theta = solution.y[0]  

"""
# Plotting the results
plt.figure(figsize=(10, 5))
plt.plot(solution.t, theta, label='Angular Displacement (theta)', color='blue')
plt.title('Simple Pendulum Simulation')
plt.xlabel('Time (s)')
plt.ylabel('Angular Displacement (radians)')
plt.grid()
plt.legend()
plt.show()  
"""

x = L * sin(theta)  # x-coordinate of the pendulum bob
y = -L * cos(theta)  # y-coordinate of the pendulum bob

# Setting up the figure and axis for animation
fig = plt.figure(facecolor='black', figsize=(8, 6))
ax = fig.add_axes((0.1, 0.25, 0.8, 0.7))

def calculate_tension(theta, theta_dot):
    return m * (L * theta_dot**2 + g * cos(theta))

tension = calculate_tension(theta, solution.y[1])

# Animation of the pendulum
def update(frame):
    ax.cla()
    pivot = ax.plot([0], [0], 'o', color='cyan', markersize=5)
    rod = ax.plot([0, x[frame]], [0, y[frame]], '-', color='cyan')
    bob = ax.plot([x[frame]], [y[frame]], 'o', color='cyan', markersize=15)
    trace = ax.plot(x[:frame], y[:frame], '-', color='cyan', alpha=0.3, linewidth=0.5)
    ax.text(0.02, 0.98, f'Tension = {tension[frame]:.2f} N', color='white', fontsize=12,
        transform=ax.transAxes, verticalalignment='top')
    ax.set_xlim(-slider_L.val-0.5, slider_L.val+0.5)
    ax.set_ylim(-slider_L.val-0.5, slider_L.val+0.5)
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    ax.axis('off')
    return pivot + rod + bob + trace

# Update function for gravity slider
def update_g(val):
    global g, solution, theta, x, y, tension
    g = slider_g.val
    solution = solve_ivp(pendulum, t_span, initial_conditions, t_eval=t_eval) 
    theta = solution.y[0]
    x = L * sin(theta)
    y = -L * cos(theta)
    tension = calculate_tension(theta, solution.y[1])  # Update tension based on new gravity

# Update function for length slider
def update_L(val):
    global L, solution, theta, x, y, tension
    L = slider_L.val
    solution = solve_ivp(pendulum, t_span, initial_conditions, t_eval=t_eval) 
    theta = solution.y[0]
    x = L * sin(theta)
    y = -L * cos(theta)
    tension = calculate_tension(theta, solution.y[1])  # Update tension based on new length

# Creating sliders for length and gravity
ax_L = plt.axes((0.2, 0.1, 0.6, 0.03))
ax_L.set_facecolor('white')
slider_L = Slider(ax_L, 'Length (m)', 0.5, 10.0, valinit=4.0, valfmt='%.1f m')
slider_L.on_changed(update_L)

# Set slider text color to white for better visibility on black background
slider_L.label.set_color('white')
slider_L.valtext.set_color('white')

# Slider for gravity
ax_g = plt.axes((0.2, 0.04, 0.6, 0.03))
ax_g.set_facecolor('white')
slider_g = Slider(ax_g, 'Gravity (m/s²)', 0.1, 20.0, valinit=9.81, valfmt='%.2f m/s²')
slider_g.on_changed(update_g)

# Set slider text color to white for better visibility on black background
slider_g.label.set_color('white')
slider_g.valtext.set_color('white')

# Creating the animation    
dt = (t_span[1] - t_span[0]) / len(t_eval) * 1000
pendulum_animation = FuncAnimation(fig, update, interval=dt, frames=len(solution.t), repeat=True)
plt.show()