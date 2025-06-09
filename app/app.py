import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import tempfile
from src.pipeline import validador

st.title("Validação de Identidade")

st.write("Envie os arquivos necessários para validar a identidade:")

# Upload dos arquivos
cnh_file = st.file_uploader("Upload da CNH (frente)", type=["png", "jpg", "jpeg"])
comprovante_file = st.file_uploader("Upload do Comprovante de Endereço", type=["png", "jpg", "jpeg"])
selfie_file = st.file_uploader("Upload da Selfie", type=["png", "jpg", "jpeg"])

if st.button("Validar Identidade"):
    if cnh_file and comprovante_file and selfie_file:
        # Salvar os arquivos temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_cnh, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_comp, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_selfie:
            
            tmp_cnh.write(cnh_file.read())
            tmp_comp.write(comprovante_file.read())
            tmp_selfie.write(selfie_file.read())

            resultado = validador(
                caminho_imagem_cnh=tmp_cnh.name,
                caminho_imagem_comp=tmp_comp.name,
                caminho_selfie=tmp_selfie.name
            )

        st.subheader("Resultado da Validação:")
        if resultado:
            st.json(resultado)
        else:
            st.warning("Nenhum resultado retornado.")
    else:
        st.warning("Por favor, envie todos os arquivos.")
