# Pendulum Simulation

Real-time simulation of rigid and elastic pendulums in a gravitational field, derived from first principles using polar coordinates and Newton's equations of motion.

## Physics

The complete derivation of the equations of motion — polar coordinate acceleration, force decomposition, rigid and elastic cases, and the breaking condition — is documented in:

- [`derivation.pdf`](derivation.pdf) — English version
- [`Herleitung.pdf`](Herleitung.pdf) — German version (handwritten)

## Project Structure

```
einfaches-pendel/
├── rigid_pendulum.py      # Rigid (mathematical) pendulum — single nonlinear ODE
├── elastic_pendulum.py    # Elastic (spring) pendulum — coupled nonlinear ODEs
├── derivation.pdf         # Derivation of the equations of motion (English)
├── Herleitung.pdf         # Herleitung der Bewegungsgleichungen (Deutsch)
├── README.md
└── .gitignore
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install numpy scipy matplotlib
```

## Usage

```bash
python3 rigid_pendulum.py
python3 elastic_pendulum.py
```

## Controls

| Key | Action |
|-----|--------|
| `H` | Toggle sliders and input fields |
| `D` | Toggle data display |
| `F` | Toggle fullscreen |

## Parameters

### Sliders

| Slider | Description | Range |
|--------|-------------|-------|
| Zoom | Zoom level | 1.0 – 20.0 |
| g (m/s²) | Gravitational acceleration | 0.1 – 20.0 |
| L (m) | Rest length | 0.5 – 10.0 |

### Material Inputs (Elastic Pendulum)

| Field | Description | Default |
|-------|-------------|---------|
| A | Cross-sectional area (m²) | 1e-4 |
| E | Young's modulus (Pa) | 2e6 |
| σ_b | Ultimate tensile strength (Pa) | 500e3 |

Click **Check Breaking** to recalculate the spring constant k = EA/L and check whether the pendulum breaks.

## Live Data

| Symbol | Quantity |
|--------|----------|
| F | Radial force (N) |
| θ | Angular displacement (rad) |
| θ̇ | Angular velocity (rad/s) |
| r | Radial distance (m) |
| ṙ | Radial velocity (m/s) |
| Δr/L | Relative extension |

## Dependencies

- Python 3.x
- NumPy
- SciPy
- Matplotlib