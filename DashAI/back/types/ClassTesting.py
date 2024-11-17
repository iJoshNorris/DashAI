# from dataclasses import dataclass
# import numpy as np
# from io import BytesIO
# from PIL import Image as PILImage
# from pathlib import Path

# from datasets.features.image import Image, list_image_compression_formats, objects_to_list_of_image_dicts


# sample_image_path = "DashAI/back/types/shaq.jpg"

# image_feature = Image(mode="RGB", decode=True)

# # 1. **list_image_compression_formats()** - Obtener formatos de compresión de imagen disponibles
# formats = list_image_compression_formats()
# print("Formatos de compresión de imagen disponibles:", formats)

# # 2. **encode_example()** - Codificar imagen en diferentes formatos
# # Ejemplo de codificación desde una ruta de archivo
# encoded_from_path = image_feature.encode_example(sample_image_path)
# print("Codificación desde ruta de archivo:", encoded_from_path)

# # Ejemplo de codificación desde bytes
# with open(sample_image_path, "rb") as f:
#     bytes_data = f.read()
# encoded_from_bytes = image_feature.encode_example(bytes_data)
# print("Codificación desde bytes:", encoded_from_bytes)

# # Ejemplo de codificación desde un array de NumPy
# array_data = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)  # Imagen aleatoria
# encoded_from_array = image_feature.encode_example(array_data)
# print("Codificación desde array de NumPy:", encoded_from_array)

# # Ejemplo de codificación desde una imagen PIL
# image_pil = PILImage.open(sample_image_path)
# encoded_from_pil = image_feature.encode_example(image_pil)
# print("Codificación desde imagen PIL:", encoded_from_pil)

# # 3. **decode_example()** - Decodificar una imagen desde diferentes formatos
# # Decodificar imagen desde ruta
# decoded_image_from_path = image_feature.decode_example(encoded_from_path)
# decoded_image_from_path.show()  # Esto debería abrir la imagen

# # Decodificar imagen desde bytes
# decoded_image_from_bytes = image_feature.decode_example(encoded_from_bytes)
# decoded_image_from_bytes.show()

# # Decodificar imagen desde un array de NumPy (necesita pasar primero por encode_example para tener el formato correcto)
# decoded_image_from_array = image_feature.decode_example(encoded_from_array)
# decoded_image_from_array.show()

# # 4. **flatten()** - Obtener la estructura de almacenamiento
# flattened_feature = image_feature.flatten()
# print("Estructura de almacenamiento al aplanar:", flattened_feature)

# # 5. **cast_storage()** - Convertir diferentes tipos de datos en el tipo de almacenamiento de Arrow
# import pyarrow as pa

# # Crear arrays de ejemplo en pyarrow y hacer el casting
# storage_path_array = pa.array([sample_image_path], type=pa.string())
# casted_storage_from_path = image_feature.cast_storage(storage_path_array)
# print("Cast de almacenamiento desde ruta:", casted_storage_from_path)

# storage_bytes_array = pa.array([bytes_data], type=pa.binary())
# casted_storage_from_bytes = image_feature.cast_storage(storage_bytes_array)
# print("Cast de almacenamiento desde bytes:", casted_storage_from_bytes)

# # Convertir un array NumPy a una lista y hacer el cast
# numpy_storage_list = pa.array([array_data.tolist()], type=pa.list_(pa.int32()))
# casted_storage_from_list = image_feature.cast_storage(numpy_storage_list)
# print("Cast de almacenamiento desde array NumPy:", casted_storage_from_list)

# # 6. **objects_to_list_of_image_dicts()** - Convertir una lista de objetos de imágenes a diccionarios de imagen
# image_paths = [sample_image_path, sample_image_path]
# image_ndarrays = [array_data, array_data]
# image_bytes = [bytes_data, bytes_data]

# # Convertir lista de paths de imágenes
# encoded_images_from_paths = objects_to_list_of_image_dicts(image_paths)
# print("Lista de diccionarios desde paths de imágenes:", encoded_images_from_paths)

# # Convertir lista de arrays de NumPy
# encoded_images_from_arrays = objects_to_list_of_image_dicts(image_ndarrays)
# print("Lista de diccionarios desde arrays de NumPy:", encoded_images_from_arrays)

# # Convertir lista de bytes
# encoded_images_from_bytes = objects_to_list_of_image_dicts(image_bytes)
# print("Lista de diccionarios desde bytes de imágenes:", encoded_images_from_bytes)

