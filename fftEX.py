from scipy.fft import fft, fftfreq, fftshift
import numpy as np

# Number of sample points
N = 400
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.exp(50.0 * 1.j * 2.0*np.pi*x) + 0.5*np.exp(-80.0 * 1.j * 2.0*np.pi*x)

yf = fftshift(fft(y))
xf = fftshift(fftfreq(N, T))

import matplotlib.pyplot as plt
plt.plot(xf, 1.0/N * np.abs(yf))
plt.grid()
plt.show()
