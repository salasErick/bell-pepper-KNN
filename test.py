import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, fftshift
from scipy.ndimage import sobel
import imageio.v2 as imageio
import os
import csv

# Function to compute and return FFT spectrum
def compute_fft_spectrum(image_path):
    # Load the image
    Bichoo_RGB = imageio.imread(image_path)
    M, N, _ = Bichoo_RGB.shape
    
    # Extract RGB channels and convert to double
    R_i = Bichoo_RGB[:, :, 0].astype(np.float64)
    G_j = Bichoo_RGB[:, :, 1].astype(np.float64)
    B_k = Bichoo_RGB[:, :, 2].astype(np.float64)
    
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
    
    return pQFT

# Function to compute statistics
def compute_statistics(spectrum):
    max_val = np.max(spectrum)
    min_val = np.min(spectrum)
    std_val = np.std(spectrum)
    return max_val, min_val, std_val

# Function to extract label from file name
def extract_label_from_filename(filename):
    if 'healthy' in filename:
        return 'healthy'
    elif 'overripe' in filename:
        return 'overripe'
    elif 'rotten' in filename:
        return 'rotten'
    else:
        return 'unknown'

# Process multiple images
image_folder = 'images/BellPepper_resized'
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg')]

statistics_list = []
labels = []

for image_file in image_files:
    spectrum = compute_fft_spectrum(image_file)
    stats = compute_statistics(spectrum)
    statistics_list.append(stats)
    label = extract_label_from_filename(os.path.basename(image_file))
    labels.append(label)

# Save statistics to a single CSV
output_file = 'output/spectrum_statistics.csv'
os.makedirs('output', exist_ok=True)

with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Image Index', 'Max Value', 'Min Value', 'Standard Deviation', 'Label'])
    for idx, (stats, label) in enumerate(zip(statistics_list, labels), start=1):
        max_val, min_val, std_val = stats
        csvwriter.writerow([idx, max_val, min_val, std_val, label])

print('Exportación de estadísticas a un único archivo CSV completada.')
