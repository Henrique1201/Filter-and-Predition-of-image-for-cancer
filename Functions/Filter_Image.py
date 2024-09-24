import numpy as np
from PIL import Image

def apply_mean_filter(image, filter_size):
    if image is None:
        raise ValueError("A imagem não pode ser None")

    image_array = np.array(image, dtype=np.float32)  # Usar float para evitar overflow
    filtered_image = np.zeros_like(image_array)
    r = filter_size // 2

    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            sum_val = 0
            count = 0
            
            for k in range(-r, r + 1):
                for l in range(-r, r + 1):
                    if 0 <= i + k < image_array.shape[0] and 0 <= j + l < image_array.shape[1]:
                        sum_val += image_array[i + k, j + l]
                        count += 1
            
            filtered_image[i, j] = sum_val / count  # Usar média como float

    return filtered_image.astype(np.uint8)  # Converter de volta para uint8

def quantize_image(image, num_levels):
    if image is None:
        raise ValueError("A imagem não pode ser None")

    image_array = np.array(image, dtype=np.float32)  # Usar float para evitar overflow
    height, width = image_array.shape
    max_val = 255
    quantized_image = np.zeros_like(image_array)
    intervalo = (max_val + 1) // num_levels

    for i in range(height):
        for j in range(width):
            valor = image_array[i, j]
            nivel = valor // intervalo
            quantized_image[i, j] = min(nivel * intervalo + intervalo // 2, max_val)  # Garantir que não ultrapasse max_val

    return quantized_image.astype(np.uint8)

def create_scm(img, qtzd, N):
    if img.shape != qtzd.shape:
        raise ValueError("As imagens devem ter o mesmo tamanho")

    scm = np.zeros((N, N), dtype=np.uint32)  # Usar uint32 para evitar overflow

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # Converter img e qtzd para float antes da multiplicação
            x = float(img[i, j]) * (N - 1) / 255
            y = float(qtzd[i, j]) * (N - 1) / 255
            x = int(x)  # Garantir que x seja um inteiro
            y = int(y)  # Garantir que y seja um inteiro
            
            if 0 <= x < N and 0 <= y < N:  # Garantir que x e y estejam dentro dos limites
                scm[x, y] += 1

    return scm

def imprimir_scm(arquivo, scm, N, final):
    for i in range(N):
        for j in range(N):
            arquivo.write(f"{scm[i, j]}, ")
    arquivo.write(f"{final}\n")

# Exemplo de uso
TAM_SCM = 8
TAM_MEAN = 3
file_path = 'images/0_10300_Colon TMA.pgm'  # Caminho da imagem
image = Image.open(file_path).convert('L')  # Converter para escala de cinza

# Aplicar o filtro de média
image_mean_filter = apply_mean_filter(image, TAM_MEAN)

# Quantizar a imagem
image_quantized = quantize_image(image_mean_filter, TAM_SCM)

# Criar a matriz SCM
scm_image = create_scm(np.array(image_mean_filter), np.array(image_quantized), TAM_SCM)

# Salvar a matriz SCM em um arquivo
with open('scm_output.csv', 'w') as file:
    imprimir_scm(file, scm_image, 8, "fim")

print("Processamento concluído. SCM salva em 'scm_output.csv'.")
