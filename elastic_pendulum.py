from numpy import linspace, pi, sin, cos
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, TextBox, Button

# Physics parameters
g, L, m, k = 9.81, 4.0, 1.0, 50.0
initial_conditions = [L, 0, pi/4, 0]
t_span = (0, 20)
t_eval = linspace(t_span[0], t_span[1], 2000)

def pendulum(t, y):
    r, r_dot, theta, theta_dot = y
    r_ddot = g * cos(theta) - k/m * (r - L) + r * theta_dot**2
    theta_ddot = -(g/r) * sin(theta) - (2 * r_dot * theta_dot) / r
    return [r_dot, r_ddot, theta_dot, theta_ddot]

solution = solve_ivp(pendulum, t_span, initial_conditions, t_eval=t_eval)
r = solution.y[0]
theta = solution.y[2]
x = r * sin(theta)
y = -r * cos(theta)
max_range = max(max(abs(x)), max(abs(y))) + 0.5

def calculate_radial_force(r, theta, theta_dot):
    return m * (r * theta_dot**2) - m * g * cos(theta) - k * (r - L)

radial_force = calculate_radial_force(r, theta, solution.y[3])
condition = ''

# --- Figure Setup ---
fig = plt.figure(facecolor='black', figsize=(12, 10))
ax = fig.add_axes((0.05, 0.22, 0.9, 0.75))

# --- Animation ---
def update(frame):
    ax.cla()
    pivot = ax.plot([0], [0], 'o', color='white', markersize=4)
    rod = ax.plot([0, x[frame]], [0, y[frame]], '-', color='cyan', linewidth=1.5)
    bob = ax.plot([x[frame]], [y[frame]], 'o', color='cyan', markersize=12)
    trace = ax.plot(x[:frame], y[:frame], '-', color='cyan', alpha=0.2, linewidth=0.5)

    if data_visible:
        data = (
            f'F ={radial_force[frame]:>8.1f} N   '
            f'θ ={solution.y[2][frame]:>7.2f} rad   '
            f'θ̇ ={solution.y[3][frame]:>7.2f} rad/s   '
            f'r ={solution.y[0][frame]:>7.2f} m   '
            f'ṙ ={solution.y[1][frame]:>7.2f} m/s   '
            f'Δr/L ={((solution.y[0][frame] - L)/L):>8.4f}'
        )
        ax.text(0.5, 0.99, data, color='white', fontsize=9,
                transform=ax.transAxes, horizontalalignment='center',
                verticalalignment='top', family='monospace')

        try:
            a_break = float(textbox_sigma.text) * L / float(textbox_E.text)
            ax.text(0.5, 0.94, f'Break at Δr = {a_break:.4f} m  |  {condition}',
                    color='#ff6666' if 'break' in condition else '#66ff66',
                    fontsize=9, transform=ax.transAxes,
                    horizontalalignment='center', verticalalignment='top')
        except ValueError:
            pass

    ax.text(0.99, 0.01, 'H: sliders  D: data  F: fullscreen',
            color='#444444', fontsize=7, transform=ax.transAxes,
            horizontalalignment='right', verticalalignment='bottom')

    zoom = slider_zoom.val
    ax.set_xlim(-zoom, zoom)
    ax.set_ylim(-slider_L.val / 2 - zoom, -slider_L.val / 2 + zoom)
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    ax.axis('off')
    return pivot + rod + bob + trace

# --- Slider Updates ---
def update_g(val):
    global g, solution, r, theta, x, y, radial_force
    g = slider_g.val
    solution = solve_ivp(pendulum, t_span, initial_conditions, t_eval=t_eval)
    r, theta = solution.y[0], solution.y[2]
    x, y = r * sin(theta), -r * cos(theta)
    radial_force = calculate_radial_force(r, theta, solution.y[3])

def update_L(val):
    global L, solution, r, theta, x, y, radial_force
    L = slider_L.val
    solution = solve_ivp(pendulum, t_span, initial_conditions, t_eval=t_eval)
    r, theta = solution.y[0], solution.y[2]
    x, y = r * sin(theta), -r * cos(theta)
    radial_force = calculate_radial_force(r, theta, solution.y[3])

def check_breaking():
    global condition, k, solution, r, theta, x, y, radial_force
    try:
        E = float(textbox_E.text)
        A = float(textbox_A.text)
        sigma = float(textbox_sigma.text)
        k = E * A / L
        solution = solve_ivp(pendulum, t_span, initial_conditions, t_eval=t_eval)
        r, theta = solution.y[0], solution.y[2]
        x, y = r * sin(theta), -r * cos(theta)
        radial_force = calculate_radial_force(r, theta, solution.y[3])
        a_break = sigma * L / E
        a_max = max(r) - L
        condition = "BREAKS" if a_max > a_break else "HOLDS"
    except ValueError:
        condition = ''

# --- Sliders ---
ax_slider_zoom = plt.axes((0.15, 0.18, 0.7, 0.02), facecolor='#333333')
slider_zoom = Slider(ax_slider_zoom, 'Zoom', 1.0, 20.0, valinit=max_range, color='cyan')
slider_zoom.label.set_color('white')
slider_zoom.valtext.set_color('white')

ax_slider_g = plt.axes((0.15, 0.14, 0.7, 0.02), facecolor='#333333')
slider_g = Slider(ax_slider_g, 'g (m/s²)', 0.1, 20.0, valinit=g, color='cyan')
slider_g.label.set_color('white')
slider_g.valtext.set_color('white')
slider_g.on_changed(update_g)

ax_slider_L = plt.axes((0.15, 0.10, 0.7, 0.02), facecolor='#333333')
slider_L = Slider(ax_slider_L, 'L (m)', 0.5, 10.0, valinit=L, color='cyan')
slider_L.label.set_color('white')
slider_L.valtext.set_color('white')
slider_L.on_changed(update_L)

# --- Text Inputs ---
ax_A = plt.axes((0.08, 0.02, 0.12, 0.025), facecolor='#333333')
textbox_A = TextBox(ax_A, 'A ', initial='1e-4', color='#444444', hovercolor='#666666')
textbox_A.label.set_color('white')
textbox_A.text_disp.set_color('white')


ax_E = plt.axes((0.27, 0.02, 0.12, 0.025), facecolor='#333333')
textbox_E = TextBox(ax_E, 'E (Pa) ', initial='2e6', color='#444444', hovercolor='#555555')
textbox_E.label.set_color('white')
textbox_E.text_disp.set_color('white')


ax_sigma = plt.axes((0.46, 0.02, 0.12, 0.025), facecolor='#333333')
textbox_sigma = TextBox(ax_sigma, 'σ_break ', initial='500e3', color='#444444', hovercolor='#555555')
textbox_sigma.label.set_color('white')
textbox_sigma.text_disp.set_color('white')


# --- Button ---
ax_btn = plt.axes((0.65, 0.02, 0.25, 0.025))
btn = Button(ax_btn, 'Check Breaking', color='#444444', hovercolor='#ff6666')
btn.label.set_color('white')
btn.on_clicked(lambda event: check_breaking())

# --- Keyboard Toggles ---
sliders_visible = True
data_visible = True

def on_key(event):
    global sliders_visible, data_visible
    if event.key == 'h':
        sliders_visible = not sliders_visible
        for a in [ax_slider_g, ax_slider_L, ax_slider_zoom, ax_E, ax_sigma, ax_A, ax_btn]:
            a.set_visible(sliders_visible)
        fig.canvas.draw_idle()
    elif event.key == 'd':
        data_visible = not data_visible
    elif event.key == 'f':
        mng = plt.get_current_fig_manager()
        if mng:
            mng.full_screen_toggle()

fig.canvas.mpl_connect('key_press_event', on_key)

check_breaking()

dt = (t_span[1] - t_span[0]) / len(t_eval) * 1000
pendulum_animation = FuncAnimation(fig, update, interval=dt, frames=len(solution.t), repeat=True)
plt.show()