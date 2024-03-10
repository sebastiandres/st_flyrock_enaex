import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

def compute_trajectory(initial_velocity, angle, floor_angle=0):
    g = 9.81  # acceleration due to gravity (m/s^2)
    angle_rad = np.radians(angle)
    time_of_flight = 2 * initial_velocity * np.sin(angle_rad) / g
    t = np.linspace(0, time_of_flight, num=100)
    x = initial_velocity * np.cos(angle_rad) * np.cos(floor_angle) * t
    y = initial_velocity * np.sin(floor_angle) * t
    z = initial_velocity * np.sin(angle_rad) * t - 0.5 * g * t**2
    return x, y, z

def plotly_plot_trajectory(x, y, z, fig=None):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines'))
    fig.update_layout(scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z'),
                    #title='Projectile Trajectory'
                    )
    LIM = 0.2
    fig.update_layout(
        scene = dict(
            xaxis = dict(nticks=4, range=[-LIM,LIM],),
            yaxis = dict(nticks=4, range=[-LIM,LIM],),
            zaxis = dict(nticks=4, range=[-0, LIM/2],
            ),),
        #width=700,
        #margin=dict(r=20, l=10, b=10, t=10)
        )
    return fig

def main():
    st.title("Projectile Motion Simulator")
    # Select between one single shot or several random shots
    options = ["Single Shot", "Random Shots"]
    c1, c2 = st.columns([1,2])
    sel_choice = c1.radio("Select Mode", options)
    fig = go.Figure()
    if sel_choice == "Single Shot":
        c21, c22 = c2.columns(2)
        initial_velocity = c21.slider("Initial Velocity (m/s)", min_value=0.9, max_value=1.1, value=1.0, step=0.01)
        angle = c22.slider("Launch Angle (degrees)", min_value=0, max_value=90, value=45, step=1)
        x, y, z = compute_trajectory(initial_velocity, angle)
        fig = plotly_plot_trajectory(x, y, z)
    else:
        N = 10
        spacial_angle = np.linspace(0, 360*(N-1)/N, N)
        initial_velocity = [1 for i in range(N)] #np.random.randint(0, 90, N)
        angle = np.random.randint(0, 90, N)
        fig = go.Figure()
        for i in range(N):
            x, y, z = compute_trajectory(initial_velocity[i], angle[i], spacial_angle[i])
            plotly_plot_trajectory(x, y, z, fig=fig)
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()