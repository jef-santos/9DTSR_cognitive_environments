import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import tempfile
from src.pipeline import validador
from PIL import Image

st.title("Validação de Identidade")

st.write("Envie os arquivos necessários para validar a identidade:")

# Upload dos arquivos
cnh_file = st.file_uploader("Upload da CNH (frente)", type=["png", "jpg", "jpeg"])
comprovante_file = st.file_uploader("Upload do Comprovante de Endereço", type=["png", "jpg", "jpeg"])
selfie_file = st.file_uploader("Upload da Selfie", type=["png", "jpg", "jpeg"])

if st.button("Validar Identidade"):
    if cnh_file and comprovante_file and selfie_file:
        col1, col2, col3 = st.columns(3)
        # Exibe as imagens em cada coluna com largura controlada (ex: 150 pixels)
        with col1:
            st.image(Image.open(cnh_file), caption="CNH", width=150)
        with col2:
            st.image(Image.open(comprovante_file), caption="Comprovante", width=150)
        with col3:
            st.image(Image.open(selfie_file), caption="Selfie", width=150)

        # Salvar os arquivos temporariamente para passar para o validador
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_cnh, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_comp, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_selfie:
            
            tmp_cnh.write(cnh_file.getbuffer())
            tmp_comp.write(comprovante_file.getbuffer())
            tmp_selfie.write(selfie_file.getbuffer())

            resultado = validador(
                caminho_imagem_cnh=tmp_cnh.name,
                caminho_imagem_comp=tmp_comp.name,
                caminho_selfie=tmp_selfie.name
            )

        st.subheader("Resultado da Validação:")

        if resultado:
            # Supondo que resultado é um dicionário com as chaves abaixo
            nomes_iguais = resultado.get("nomes_iguais", False)
            cpfs_iguais = resultado.get("cpfs_iguais", False)
            face_iguais = resultado.get("face_iguais", False)

            if nomes_iguais and cpfs_iguais and face_iguais:
                st.success("Documentos validados!")
            else:
                st.error("Documentos com erros:")
                st.write(f" - Nomes iguais: {nomes_iguais}")
                st.write(f" - CPFs iguais: {cpfs_iguais}")
                st.write(f" - Faces iguais: {face_iguais}")
        else:
            st.warning("Nenhum resultado retornado.")
    else:
        st.warning("Por favor, envie todos os arquivos.")
