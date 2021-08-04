from scipy.fft import fft, fftfreq, fftshift
import numpy as np

# Number of sample points
N = 400
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N, endpoint=False) #values 0 to 0.5, 400 pts
y = np.exp(50.0 * 1.j * 2.0*np.pi*x) + 0.5*np.exp(-80.0 * 1.j * 2.0*np.pi*x)
print(len(y))

yf = fftshift(fft(y))
print(len(yf))
xf = fftshift(fftfreq(N, T)) #len xf also 400


import matplotlib.pyplot as plt
plt.plot(xf, 1.0/N * np.abs(yf))
plt.grid()
plt.show()
