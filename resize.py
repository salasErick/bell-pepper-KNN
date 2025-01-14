from PIL import Image
import os

# Directorio que contiene las imágenes
input_dir = 'images/BellPepper'
output_dir = 'images/BellPepper_resized'

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Función para redimensionar una imagen
def resize_image(image_path, output_path, scale_factor=0.1):
    with Image.open(image_path) as img:
        # Calcular las nuevas dimensiones
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        
        # Redimensionar la imagen
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Guardar la imagen redimensionada
        resized_img.save(output_path, 'JPEG')

# Contador de imágenes
image_counter = 1

# Recorrer todos los archivos en el directorio de entrada
for filename in os.listdir(input_dir):
    if filename.lower().endswith('.jpg'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f'healthy_{image_counter}.jpg')
        
        # Redimensionar y guardar la imagen
        resize_image(input_path, output_path)
        
        # Incrementar el contador de imágenes
        image_counter += 1

print(f"Redimensionamiento completado. {image_counter-1} imágenes procesadas.")
