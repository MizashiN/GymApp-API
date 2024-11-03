import os
import requests

# Lista de URLs das imagens a serem baixadas
urls = [
    "https://darkness.vtexassets.com/assets/vtex.file-manager-graphql/images/f78f7bcd-9759-4c24-a9c1-adee7265cb97___275ed5786356729bb4cc4a565df9c232.webp",
    "https://example.com/image1.jpg",
    "https://example.com/image2.png",
    # Adicione mais URLs conforme necessário
]

save_directory = "input_image_path"

os.makedirs(save_directory, exist_ok=True)


# Função para baixar as imagens
def download_images(urls):
    for url in urls:
        file_name = os.path.basename(url)
        save_path = os.path.join(save_directory, file_name)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print(f"Imagem baixada com sucesso em: {save_path}")
            else:
                print(
                    f"Falha ao fazer o download da imagem {url}. Código de status: {response.status_code}"
                )
        except Exception as e:
            print(f"Ocorreu um erro ao baixar a imagem {url}: {e}")


# Chama a função para baixar as imagens
download_images(urls)
