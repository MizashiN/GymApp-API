import requests
from PIL import Image
import os
from SQLiteOperations import Operations


class funcs:
    def __init__(self) -> None:
        self.input_path = os.path.join("input_image_path")
        self.output_path = os.path.join("output_image_path")  # Diretório de saída
        self.operation = Operations()

    def download_image(self, image_src_url):
        save_directory = "input_image_path"
        
        file_name = os.path.basename(image_src_url) + ".png"
        file_name = file_name.replace("?", "").replace("&", "")
        save_path = os.path.join(save_directory, file_name)

        try:
            response = requests.get(image_src_url)
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print(f"Imagem baixada com sucesso em: {save_path}")
            else:
                print(
                    f"Falha ao fazer o download da imagem {image_src_url}. Código de status: {response.status_code}"
                )
        except Exception as e:
            print(f"Ocorreu um erro ao baixar a imagem {image_src_url}: {e}")

        self.get_icon_img(
            input_image_path=self.input_path, output_path=self.output_path
        )
        self.blob = self.GetBlobImg(path=self.output_path, filename=file_name)
        self.DeleteFiles(input_path=self.input_path, output_path=self.output_path)
        
        return self.blob

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

    def GetBlobImg(self, path, filename):

        full_image_path = os.path.join(path, filename)
        with open(full_image_path, "rb") as file:
            blob_data = file.read()

        return blob_data

    def DeleteFiles(self, input_path, output_path):
        # Lista todos os arquivos na pasta e os remove
        for arquivo in os.listdir(input_path):
            full_path = os.path.join(input_path, arquivo)

            # Verifica se é um arquivo (ignora diretórios)
            if os.path.isfile(full_path):
                os.remove(full_path)  # Remove o arquivo
                print(f"Arquivo '{arquivo}' removido em {input_path}.")
            else:
                print(f"'{arquivo}' não é um arquivo, ignorado.")

        for arquivo in os.listdir(output_path):
            full_path = os.path.join(output_path, arquivo)

            # Verifica se é um arquivo (ignora diretórios)
            if os.path.isfile(full_path):
                os.remove(full_path)  # Remove o arquivo
                print(f"Arquivo '{arquivo}' removido em {output_path}.")
            else:
                print(f"'{arquivo}' não é um arquivo, ignorado.")
