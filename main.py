import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, fftshift, ifft2
from scipy.ndimage import sobel
import imageio.v2 as imageio

# Load the image
image_path = 'images/BellPepper/3.jpg'
Bichoo_RGB = imageio.imread(image_path)
M, N, _ = Bichoo_RGB.shape

# Display the original image
plt.figure()
plt.imshow(Bichoo_RGB)
plt.title('Original Image')
plt.axis('off')

# Extract RGB channels and convert to double
R_i = Bichoo_RGB[:, :, 0].astype(np.float64)
G_j = Bichoo_RGB[:, :, 1].astype(np.float64)
B_k = Bichoo_RGB[:, :, 2].astype(np.float64)

# Function to compute and plot FFT spectrum
def plot_fft_spectrum(channel, title):
    FaFT = fft2(channel)
    cFaFT = fftshift(FaFT)
    pFaFT = np.abs(cFaFT)
    plt.figure()
    plt.imshow(np.log(1 + pFaFT), extent=(-M/2, M/2, -N/2, N/2), aspect='auto')
    plt.title(f'Espectro de potencia {title}')
    plt.xlabel('frecuencias horizontales')
    plt.ylabel('frecuencias verticales')
    plt.colorbar()
    plt.gca().set_aspect('auto')

# Plot FFT spectrum for R, G, B channels
plot_fft_spectrum(R_i, 'R')
plot_fft_spectrum(G_j, 'G')
plot_fft_spectrum(B_k, 'B')

# Compute FT(R*i)
haproof = fft2(R_i)
z = 1j  # imaginary unit
hctemp = B_k * z
hdtemp = G_j
sumgb = hdtemp + hctemp

# Compute FT(G + B*i)
hbproof = fft2(sumgb)
hbtemp = hbproof * z

# Combine FT results
QFT = haproof + hbtemp
cQFT = fftshift(QFT)
pQFT = np.abs(cQFT)
plt.figure()
plt.imshow(np.log(1 + pQFT), extent=(-M/2, M/2, -N/2, N/2), aspect='auto')
plt.title('Espectro de potencia RGB')
plt.xlabel('frecuencias horizontales')
plt.ylabel('frecuencias verticales')
plt.colorbar()
plt.gca().set_aspect('auto')

# Apply inverse FFT
IQFT = ifft2(QFT)
IQFTrp = np.abs(IQFT)

plt.figure()
plt.imshow(IQFTrp, cmap='gray')
plt.title('Inverse FFT Image')
plt.axis('off')

# Apply Sobel filters
H1 = sobel(IQFT, axis=0, mode='constant')
H2 = sobel(IQFT, axis=1, mode='constant')

plt.figure()
plt.imshow(np.abs(H1), cmap='gray')
plt.title('Sobel Filter H1')
plt.axis('off')

plt.figure()
plt.imshow(np.abs(H2), cmap='gray')
plt.title('Sobel Filter H2')
plt.axis('off')

plt.show()
