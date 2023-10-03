import cv2
import os
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import random
import shutil
from datetime import datetime

class DatasetMaker:
    @staticmethod
    def extrair_frames_de_video_opemcv(video_path, pasta_saida):
        # Abra o vídeo
        cap = cv2.VideoCapture(video_path)
        
        # Verifique se o vídeo foi aberto com sucesso
        if not cap.isOpened():
            print("Erro ao abrir o vídeo.")
            return
        
        # Certifique-se de que a pasta de saída exista
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)
        
        # Loop para extrair e salvar cada quadro do vídeo
        frame_count = 0
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Salve o quadro como uma imagem
            frame_filename = os.path.join(pasta_saida, f"frame_{frame_count:04d}.png")
            cv2.imwrite(frame_filename, frame)
            
            frame_count += 1
        
        # Feche o vídeo
        cap.release()
        
        print(f"{frame_count} quadros extraídos e salvos em {pasta_saida}")

    @staticmethod
    def extrair_frames_de_video_moviepy(video_path, pasta_saida):
        # Certifique-se de que a pasta de saída exista
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)

        # Abra o vídeo usando o MoviePy
        video = VideoFileClip(video_path)
        
        # Percorra os quadros e salve-os como imagens
        for i, frame in enumerate(video.iter_frames(fps=30)):  # fps é a taxa de quadros por segundo
            frame_filename = os.path.join(pasta_saida, f"frame_{i:04d}.png")
            frame.save_frame(frame_filename)
        
        print(f"{i + 1} quadros extraídos e salvos em {pasta_saida}")

    @staticmethod    
    def extrair_frames_de_video_com_intervalo(video_path, pasta_saida, intervalo=1):
       # Certifique-se de que a pasta de saída exista
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)

        # Abra o vídeo usando o MoviePy
        video = VideoFileClip(video_path)
        
        # Percorra os quadros e salve-os como imagens com o intervalo especificado
        frame_count = 0
        saved_frame_count = 0
        for frame in video.iter_frames(fps=video.fps):
            if frame_count % intervalo == 0:
                frame_filename = os.path.join(pasta_saida, f"frame_{saved_frame_count:04d}.png")
                Image.fromarray(frame).save(frame_filename)
                saved_frame_count += 1
            
            frame_count += 1

    @staticmethod
    def contar_arquivos_em_pasta(video_path):
        if not os.path.exists(pasta):
            return 0

        arquivos = [arquivo for arquivo in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, arquivo))]
        return len(arquivos)

    @staticmethod
    def separar_dados_train_test_pasta(source_dir, treinamento_dir, teste_dir, validacao_dir, ratio=(0.2, 0.2, 0.6), seed=42):
        # Define a semente para garantir reproducibilidade
        random.seed(seed)

        # Lista todos os arquivos no diretório de origem
        image_files = [file for file in os.listdir(source_dir)]

        # Embaralha a lista de arquivos
        random.shuffle(image_files)

        # Calcula o número de imagens para treinamento, validação e teste
        num_images = len(image_files)
        num_train = int(num_images * ratio[0])
        num_val = int(num_images * ratio[1])
        num_test = num_images - num_train - num_val

        # Divide a lista de imagens em conjuntos de treinamento, validação e teste
        train_images = image_files[:num_train]
        val_images = image_files[num_train:num_train + num_val]
        test_images = image_files[num_train + num_val:]

        # Cria os diretórios de treinamento, validação e teste, se não existirem
        for directory in [treinamento_dir, validacao_dir, teste_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Copia as imagens para os diretórios correspondentes
        for image in train_images:
            shutil.copy(os.path.join(source_dir, image), os.path.join(treinamento_dir, image))

        for image in val_images:
            shutil.copy(os.path.join(source_dir, image), os.path.join(validacao_dir, image))

        for image in test_images:
            shutil.copy(os.path.join(source_dir, image), os.path.join(teste_dir, image))

        # Exibe as informações sobre a quantidade de dados
        print("Diretorio: ", source_dir)
        print("Quantidade total de dados: ", num_images)
        print("Quantidade de dados de treinamento: ", len(train_images))
        print("Quantidade de dados de validacao: ", len(val_images))
        print("Quantidade de dados de teste: ", len(test_images))

    @staticmethod
    def processar_videos_em_pasta( pasta_de_videos, pasta_de_imagens, intervalo_de_quadros=30):
        """
        Processa os vídeos na pasta de vídeos e extrai quadros em intervalos especificados,
        salvando-os como imagens na pasta de imagens.

        Parâmetros:
        - pasta_de_videos (str): O caminho para a pasta contendo os arquivos de vídeo a serem processados.
        - pasta_de_imagens (str): O caminho para a pasta onde as imagens processadas serão salvas.
        - intervalo_de_quadros (int): O intervalo entre os quadros a serem extraídos (padrão é 30).

        Notas:
        - A função processará todos os arquivos .mp4 na pasta de vídeos.
        - Cada vídeo será convertido em uma série de imagens em intervalos especificados.
        - As imagens resultantes terão nomes baseados no timestamp.
        - Será criada uma pasta separada para cada vídeo na pasta de imagens.

        Exemplo de uso:
        processar_videos_em_pasta('/caminho/para/videos', '/caminho/para/imagens', intervalo_de_quadros=15)
        """
        video_files = [f for f in os.listdir(pasta_de_videos) if f.endswith('.mp4')]

        for video_file in video_files:
            video_path = os.path.join(pasta_de_videos, video_file)
            
            # Chama a função para converter o vídeo em imagens com timestamp
            # Abre o vídeo para leitura
            cap = cv2.VideoCapture(video_path)
            
            # Verifica se o vídeo foi aberto corretamente
            if not cap.isOpened():
                print("Erro ao abrir o vídeo.")
                return
            
            # Obtém o nome do vídeo sem a extensão
            video_name = os.path.splitext(os.path.basename(video_path))[0]

            # Cria uma pasta para o vídeo dentro da pasta de saída
            video_output_folder = os.path.join(pasta_de_imagens, video_name)
            os.makedirs(video_output_folder, exist_ok=True)
            
            # Inicializa o contador de quadros
            frame_number = 0
            cont = 0
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Salva o quadro como imagem em intervalos especificados
                if frame_number % intervalo_de_quadros == 0:
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
                    image_name = f"{timestamp}_{cont}.jpg"
                    image_path = os.path.join(video_output_folder, image_name)
                    cv2.imwrite(image_path, frame)
                    cont += 1
                
                frame_number += 1
            
            # Libera o objeto de captura e fecha o vídeo
            cap.release()
            cv2.destroyAllWindows()

    @staticmethod
    def separar_dados_train_test_pasta_anotacao(source_dir, treinamento_dir, teste_dir, validacao_dir, annotation_dir, ratio=(0.2, 0.2, 0.6), seed=42, image_extension='.bmp', annotation_extension='.txt'):
        # Define a semente para garantir a reproducibilidade
        random.seed(seed)

        # Lista todos os arquivos de imagem no diretório de origem com a extensão especificada
        image_files = [file for file in os.listdir(source_dir) if file.endswith(image_extension)]

        # Embaralha a lista de arquivos
        random.shuffle(image_files)

        # Calcula o número de imagens para treinamento, validação e teste
        num_images = len(image_files)
        num_train = int(num_images * ratio[0])
        num_val = int(num_images * ratio[1])
        num_test = num_images - num_train - num_val

        # Divide a lista de imagens em conjuntos de treinamento, validação e teste
        train_images = image_files[:num_train]
        val_images = image_files[num_train:num_train + num_val]
        test_images = image_files[num_train + num_val:]

        # Cria os diretórios de treinamento, validação e teste, se não existirem
        for directory in [treinamento_dir, validacao_dir, teste_dir, annotation_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Copia as imagens
        for image in train_images:
            shutil.copy(os.path.join(source_dir, image), os.path.join(treinamento_dir, image))

        for image in val_images:
            shutil.copy(os.path.join(source_dir, image), os.path.join(validacao_dir, image))

        for image in test_images:
            shutil.copy(os.path.join(source_dir, image), os.path.join(teste_dir, image))

        # Move os arquivos de anotação para a pasta de anotações
        for image in image_files:
            annotation_file = os.path.splitext(image)[0] + annotation_extension
            if os.path.exists(os.path.join(source_dir, annotation_file)):
                shutil.move(os.path.join(source_dir, annotation_file), os.path.join(annotation_dir, annotation_file))

        # Exibe as informações sobre a quantidade de dados
        print("Diretorio: ", source_dir)
        print("Quantidade total de dados: ", num_images)
        print("Quantidade de dados de treinamento: ", len(train_images))
        print("Quantidade de dados de validacao: ", len(val_images))
        print("Quantidade de dados de teste: ", len(test_images))        