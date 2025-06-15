# Validação de Identidade - Projeto Final | Cognitive Environments (FIAP - MBA 9DTSR)

Este repositório contém o projeto final da disciplina **Cognitive Environments**, do MBA em Data Science & Artificial Intelligence da FIAP (turma 9DTSR).

---

## 🎯 Objetivo

Desenvolver uma aplicação de validação de identidade utilizando **serviços em nuvem**, que permita validar o "self" do usuário com base em documentos e imagens, com foco em:

1. Extração de **Nome**, **CPF** e **Face** da Carteira Nacional de Habilitação (CNH);
2. Comparação da face da CNH com uma **selfie**;
3. Extração de **Nome** e **CPF** de um **comprovante de residência** e verificação com os dados da CNH.

> A solução visa atender uma demanda do setor de fraudes, que identificou inconsistências em processos de contratação de crédito pessoal com base em indicadores de vivacidade.

---

## 📦 Estrutura do Repositório
```
9DTSR_cognitive_environments/
│
├── data
│ └── raw
│ └── processed
│
├── notebook
│ ├── notebook.ipynb
│ └── validacao.ipynb
│
├── src
│ ├── pipeline.py
│
├── requirements.txt
├── README.md 
```

## ☁️ Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** para a interface interativa
- **AWS Textract** para OCR (leitura de texto de imagens)
- **AWS Rekognition** para detecção e comparação de rostos
- **Pillow**, **boto3**, **unicodedata**, entre outras


## 🚀 Executando o Projeto

### 1. Clone o repositório
```
git clone https://github.com/jef-santos/9DTSR_cognitive_environments.git
cd 9DTSR_cognitive_environments
```

### 2. Crie um ambiente virtual e instale as dependências
```
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### 3. Configure suas credenciais AWS
Certifique-se de configurar suas credenciais no ambiente local, via aws configure ou variáveis de ambiente.

### 4. Rode o aplicativo Streamlit
```
streamlit run app/app.py
```

## ☁️ Tecnologias Utilizadas
- **Python 3.10+**
- **Streamlit** para a interface interativa
- **AWS Textract** para OCR (leitura de texto de imagens)
- **AWS Rekognition** para detecção e comparação de rostos
- **Pillow**, **boto3**, **unicodedata**, entre outras

