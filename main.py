import numpy as np
from scipy.fft import fft2, fftshift
import imageio.v2 as imageio
import os
import pandas as pd

directory = 'images/BellPepper'
temp = [f for f in os.listdir(directory) if f.endswith('.jpg')]

directory = 'images/BellPepper/'

file_paths = list(map(lambda x: directory + x, temp))
# print(file_paths)

# Function to compute and plot FFT spectrum
def compute_combined_fft(image_path):
    Bichoo_RGB = imageio.imread(image_path)
    M, N, _ = Bichoo_RGB.shape
    
    R_i = Bichoo_RGB[:, :, 0].astype(np.float64)
    G_j = Bichoo_RGB[:, :, 1].astype(np.float64)
    B_k = Bichoo_RGB[:, :, 2].astype(np.float64)
    
    haproof = fft2(R_i)
    z = 1j
    hctemp = B_k * z
    hdtemp = G_j
    sumgb = hdtemp + hctemp

    hbproof = fft2(sumgb)
    hbtemp = hbproof * z

    QFT = haproof + hbtemp
    cQFT = fftshift(QFT)
    pQFT = np.abs(cQFT)
    
    # Flatten the spectrum into a feature vector
    feature_vector = np.log(1 + pQFT).flatten()
    
    return feature_vector

# Generate a list of dummy labels, same length as file_paths
limited_filepaths = file_paths[:10]
labels = ['Ripe']
# Compute feature vectors
features = [compute_combined_fft(img_path) for img_path in limited_filepaths]

# Create a DataFrame to store features and labels
df = pd.DataFrame(features)
df['label'] = labels

# Save the DataFrame to a CSV file
df.to_csv('fft_features.csv', index=False)

print("Feature vectors saved to fft_features.csv")
