import requests
from PIL import Image
import os 

class funcs:
    def __init__(self) -> None:
        self.input_path = os.path.join(
            "input_image_path" 
        )
        self.output_path = os.path.join(
            "output_image_path"  # Diretório de saída
        )
    def download_images(self, urls):
        save_directory = "input_image_path"

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
        
        self.get_icon_img(input_image_path=self.input_path, output_path=self.output_path)

    def get_icon_img(self, input_image_path, output_path):
        # Verifica se o diretório de entrada existe
        if not os.path.isdir(input_image_path):
            print(f"O diretório de entrada {input_image_path} não existe.")
            return

        # Cria o diretório de saída, se não existir
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
            print(f"O diretório de saída {output_path} foi criado.")

        # Itera sobre os arquivos no diretório de entrada
        for filename in os.listdir(input_image_path):
            if filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")
            ):
                try:
                    # Caminho completo para o arquivo de entrada
                    full_image_path = os.path.join(input_image_path, filename)

                    input_image = Image.open(full_image_path).convert("RGBA")

                    output_image_resized = input_image.resize((250, 250), Image.LANCZOS)

                    # Cria uma nova imagem com fundo branco
                    output_image_with_background = Image.new(
                        "RGBA", (250, 250), (255, 255, 255, 255)
                    )

                    output_image_with_background.paste(
                        output_image_resized, (0, 0), output_image_resized
                    )

                    # Converte para RGB antes de salvar
                    output_image_with_background = output_image_with_background.convert(
                        "RGB"
                    )
                    output_file_path = os.path.join(
                        output_path, f"{filename.rsplit('.', 1)[0]}.png"
                    )

                    # Salva a imagem redimensionada com fundo branco como PNG
                    output_image_with_background.save(output_file_path, format="PNG")
                    print(f"Imagem salva em: {output_file_path}")
                except Exception as e:
                    print(f"Erro ao processar a imagem {filename}: {e}")
