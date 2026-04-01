from numpy import sin, cos, pi, linspace
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

g, L, mass = 9.81, 4.0, 1.0   
initial_conditions = [pi / 4, 0]  # Initial angle and initial angular velocity
t_span = (0, 100)  
t_eval = linspace(t_span[0], t_span[1], 10000) 

def rigidPendulum(t, y):
    return [y[1], -(g/L) * sin(y[0])]

# Solving ODE using solve_ivp
solution = solve_ivp(rigidPendulum, t_span, initial_conditions, t_eval=t_eval)

angle = solution.y[0]  

"""
# Plotting the results
plt.figure(figsize=(10, 5))
plt.plot(solution.t, angle, label='Angular Displacement (angle)', color='blue')
plt.title('Simple Pendulum Simulation')
plt.xlabel('Time (s)')
plt.ylabel('Angular Displacement (radians)')
plt.grid()
plt.legend()
plt.show()  
"""

x = L * sin(angle)  
y = -L * cos(angle) 

# Setting up the figure and axis for animation
fig = plt.figure(facecolor='black', figsize=(8, 6))
ax = fig.add_axes((0.1, 0.25, 0.8, 0.7))

def calculate_tension(theta, theta_dot):
    return mass * (L * theta_dot**2 + g * cos(theta))

tension = calculate_tension(angle, solution.y[1])

# Animation of the pendulum
def update(frame):
    ax.cla()
    center = ax.plot([0], [0], 'o', color='cyan', markersize=5)
    line = ax.plot([0, x[frame]], [0, y[frame]], '-', color='cyan')
    pendulum = ax.plot([x[frame]], [y[frame]], 'o', color='cyan', markersize=15)
    trace = ax.plot(x[:frame], y[:frame], '-', color='cyan', alpha=0.3, linewidth=0.5)
    ax.text(0.02, 0.98, f'Tension = {tension[frame]:.2f} N', color='white', fontsize=12, transform=ax.transAxes, verticalalignment='top')
    ax.set_xlim(-slider_Length.val-0.5, slider_Length.val+0.5)
    ax.set_ylim(-slider_Length.val-0.5, slider_Length.val+0.5)
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    ax.axis('off')
    return center + line + pendulum + trace


def update_g(val):
    global g, solution, angle, x, y, tension
    g = slider_gravity.val
    solution = solve_ivp(rigidPendulum, t_span, initial_conditions, t_eval=t_eval) 
    angle = solution.y[0]
    x = Length * sin(angle)
    y = -Length * cos(angle)
    tension = calculate_tension(angle, solution.y[1])  

def update_L(val):      
    global Length, solution, angle, x, y, tension
    Length = slider_Length.val
    solution = solve_ivp(rigidPendulum, t_span, initial_conditions, t_eval=t_eval) 
    angle = solution.y[0]
    x = Length * sin(angle)
    y = -Length * cos(angle)
    tension = calculate_tension(angle, solution.y[1]) 

# Slider for length
ax_Length = plt.axes((0.2, 0.1, 0.6, 0.03))
ax_Length.set_facecolor('white')
slider_Length = Slider(ax_Length, 'Length (m)', 0.5, 10.0, valinit=4.0, valfmt='%.1f m')
slider_Length.on_changed(update_L)


slider_Length.label.set_color('white')
slider_Length.valtext.set_color('white')

# Slider for gravity
ax_gravity = plt.axes((0.2, 0.04, 0.6, 0.03))
ax_gravity.set_facecolor('white')
slider_gravity = Slider(ax_gravity, 'Gravity (m/s²)', 0.1, 20.0, valinit=9.81, valfmt='%.2f m/s²')
slider_gravity.on_changed(update_g)


slider_gravity.label.set_color('white')
slider_gravity.valtext.set_color('white')

# Creating the animation    
dt = (t_span[1] - t_span[0]) / len(t_eval) * 1000
pendulum_animation = FuncAnimation(fig, update, interval=dt, frames=len(solution.t), repeat=True)
plt.show()