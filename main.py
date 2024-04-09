import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass, field
from numba import jit


@dataclass
class Parameters:
    """
    A dataclass to store parameters for the wave function.

    Attributes:
        a_1 (float): The amplitude of the first sine wave.
        a_2 (float): The amplitude of the second sine wave.
        t (np.ndarray): An array of time values.
        w_1 (float): The frequency of the first sine wave.
        w_2 (float): The frequency of the second sine wave.
        g_1 (float): The phase of the first sine wave.
        g_2 (float): The phase of the second sine wave.

    Methods:
        to_tuple(): Returns a tuple of all attributes.
    """

    a_1: float = -0.41
    a_2: float = -0.3
    t: np.ndarray = field(default_factory=lambda: np.linspace(-1, 1, 100))
    w_1: float = 1
    w_2: float = 2
    g_1: float = 1
    g_2: float = 9.92

    def to_tuple(self):
        """
        Returns a tuple of all attributes.

        Returns:
            tuple: The tuple containing the parameters.
        """
        return (
            self.a_1,
            self.a_2,
            self.t,
            self.w_1,
            self.w_2,
            self.g_1,
            self.g_2,
        )


@jit(nopython=True)
def wave(x: np.ndarray, t: np.ndarray, params: tuple) -> np.ndarray:
    """
    The wave function is a function of x and t, which are the spatial and temporal coordinates.
    It returns an array of values for each point in space at a given time.
    """
    a_1, a_2, _, w_1, w_2, g_1, g_2 = params
    return a_1 * np.sin(x * w_1 + t * g_1) + a_2 * np.sin(x * w_2 + t * g_2)


# Initialize figure and axes
fig, ax = plt.subplots()

# Create x-coordinates
x = np.linspace(-10, 10, 1000)

# Initialize lines to be updated
(line1,) = ax.plot(x, wave(x, 0, Parameters().to_tuple()))


def update(t):
    """
    The update function is called by the FuncAnimation object.
    It takes a single argument, t, which is the current time in seconds.
    The update function must return an iterable of artists that have changed.
    In this case we are only updating one artist (line), so we return it as a tuple with one element.
    """
    line1.set_ydata(wave(x, t, Parameters().to_tuple()))
    return (line1,)


# Create animation
ani = animation.FuncAnimation(
    fig, update, frames=np.linspace(0, 2 * np.pi, 100), interval=100
)

# Add grid
ax.grid(True)
ax.minorticks_on()
ax.grid(which="major", linestyle=":", linewidth="0.5", color="black")

# Set axis limits
ax.set_xlim([-10, 10])
ax.set_ylim([-6.78, 6.78])

# Set axis ticks
ax.set_xticks(np.arange(-10, 11, 1))
ax.set_yticks(np.arange(-6.78, 6.78, 0.5))

plt.show()
