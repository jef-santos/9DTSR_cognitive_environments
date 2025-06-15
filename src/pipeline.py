import boto3
import re
import io
from PIL import Image
import unicodedata

# Clientes AWS
textract = boto3.client('textract') 
rekognition = boto3.client('rekognition') 

# Funções para extração de dados de CNH e comprovantes
def extrair_dados_cnh(caminho_imagem_cnh):
    with open(caminho_imagem_cnh, "rb") as image_file:
        imagem_cnh_bytes = image_file.read()

    imagem_pil = Image.open(io.BytesIO(imagem_cnh_bytes))

    # OCR com Textract
    resposta = textract.detect_document_text(Document={'Bytes': imagem_cnh_bytes})
    texto_total_cnh = " ".join([
        item['Text'] for item in resposta['Blocks'] if item['BlockType'] == 'LINE'
    ])

    # Regex mais robusto para CPF
    cpf_match = re.search(r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}", texto_total_cnh)
    
    # Nome: assume "NOME" vem antes e "DOC" pode estar ausente
    nome_match = re.search(r'NOME[\s:]*([A-ZÀ-Ú\s]{3,})DOC', texto_total_cnh)
    
    cpf_cnh = cpf_match.group() if cpf_match else "Não encontrado"
    nome_cnh = nome_match.group(1).strip() if nome_match else "Não encontrado"

    return nome_cnh, cpf_cnh

def extrair_face_cnh(caminho_imagem_cnh):
    with open(caminho_imagem_cnh, "rb") as image_file:
        imagem_cnh_bytes = image_file.read()

    imagem_pil = Image.open(io.BytesIO(imagem_cnh_bytes))

    # Detectar face
    resposta_faces = rekognition.detect_faces(
        Image={'Bytes': imagem_cnh_bytes},
        Attributes=['DEFAULT']
    )

    if not resposta_faces['FaceDetails']:
        return None

    bounding_box = resposta_faces['FaceDetails'][0]['BoundingBox']
    img_width, img_height = imagem_pil.size

    left = int(bounding_box['Left'] * img_width)
    top = int(bounding_box['Top'] * img_height)
    width = int(bounding_box['Width'] * img_width)
    height = int(bounding_box['Height'] * img_height)

    face_crop = imagem_pil.crop((left, top, left + width, top + height)).convert("RGB")
    return face_crop

def extrair_dados_comprovantes(caminho_imagem_comp):
    with open(caminho_imagem_comp, "rb") as image_file:
        imagem_comprovante_bytes = image_file.read()

    imagem_pil = Image.open(io.BytesIO(imagem_comprovante_bytes))

    resposta = textract.detect_document_text(Document={'Bytes': imagem_comprovante_bytes})
    texto = " ".join([
        item['Text'] for item in resposta['Blocks'] if item['BlockType'] == 'LINE'
    ])

    cpf_match = re.search(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', texto)
    nome_match = re.search(r'^(.+?)\s+Código Vencimento', texto, flags=re.DOTALL | re.IGNORECASE)

    cpf_comprovante = cpf_match.group(0) if cpf_match else None
    nome_comprovante = nome_match.group(1).strip().split('\n')[-1] if nome_match else None

    return nome_comprovante, cpf_comprovante

def normalizar_nome(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('utf-8')
    nome = nome.upper().strip()
    nome = re.sub(r'\s+', ' ', nome)
    nome = re.sub(r'[\u200b\r\n]+', '', nome)
    return nome.upper()

def validador(caminho_imagem_cnh, caminho_imagem_comp, caminho_selfie):
    #Extrair dados da CNH e comprovantes
    nome_cnh, cpf_cnh = extrair_dados_cnh(caminho_imagem_cnh)
    nome_comp, cpf_comp = extrair_dados_comprovantes(caminho_imagem_comp)
    #Extrair face da CNH
    face_cnh = extrair_face_cnh(caminho_imagem_cnh)
    if face_cnh is None:
        raise ValueError("Nenhuma face detectada na CNH.")
    # Extrair selfie
    with open(caminho_selfie, "rb") as image_file:
        selfie_bytes = image_file.read()
    try:
        face_selfie = Image.open(io.BytesIO(selfie_bytes))
    except Exception as e:
        raise ValueError("Erro ao abrir a selfie: ", str(e))


    # Converter imagens para bytes
    buffer_cnh = io.BytesIO()
    face_cnh.save(buffer_cnh, format="PNG")
    face_cnh_bytes = buffer_cnh.getvalue()

    buffer_selfie = io.BytesIO()
    face_selfie.convert("RGB").save(buffer_selfie, format="PNG")
    face_selfie_bytes = buffer_selfie.getvalue()

    # Normalizar nomes e verifica se os nomes e CPFs coincidem
    nome_cnh_normalizado = normalizar_nome(nome_cnh)
    nome_comp_normalizado = normalizar_nome(nome_comp)
    nomes_iguais = nome_cnh_normalizado == nome_comp_normalizado
    cpfs_iguais = cpf_cnh == cpf_comp

    # Verificar se faces são iguais
    resposta_comparacao = rekognition.compare_faces(
        SourceImage={'Bytes': face_cnh_bytes},
        TargetImage={'Bytes': face_selfie_bytes},
        SimilarityThreshold=80 
    )
    face_iguais = False
    for face_match in resposta_comparacao['FaceMatches']:
        similaridade = face_match['Similarity']
        if similaridade >= 90:
            face_iguais = True
            break


    return {
        "nome_cnh": nome_cnh_normalizado,
        "cpf_cnh": cpf_cnh,
        "nome_comprovante": nome_comp_normalizado,
        "cpf_comprovante": cpf_comp,
        "nomes_iguais": nomes_iguais,
        "cpfs_iguais": cpfs_iguais,
        "face_iguais": face_iguais
    }

