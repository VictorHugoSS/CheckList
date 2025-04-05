import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from datetime import date

# Transformador para leitura de QR/barcode
class BarcodeReader(VideoTransformerBase):
    def __init__(self):
        self.result = ""

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded_objs = decode(img)

        for obj in decoded_objs:
            self.result = obj.data.decode("utf-8")
            cv2.rectangle(img, (obj.rect.left, obj.rect.top),
                          (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height),
                          (0, 255, 0), 2)
            cv2.putText(img, self.result, (obj.rect.left, obj.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return img

st.title("Checklist com Leitor de Código de Barras")

st.markdown("### 📷 Leitor de QR Code / Código de Barras")

ctx = webrtc_streamer(key="barcode", video_transformer_factory=BarcodeReader)

barcode = ""
if ctx.video_transformer:
    barcode = ctx.video_transformer.result

# Formulário do checklist
codigo = st.text_input("Número do Ticket (preenchido pela câmera ou manual)", value=barcode)
colaborador = st.text_input("Colaborador")
data = st.date_input("Data", value=date.today())

st.markdown("### Itens de Verificação")
check1 = st.checkbox("Equipamento limpo")
check2 = st.checkbox("Sem vazamentos")
check3 = st.checkbox("Sinalização adequada")
check4 = st.checkbox("EPI utilizado corretamente")
check5 = st.checkbox("Área isolada")

observacoes = st.text_area("Observações")

if st.button("Salvar"):
    dados = {
        "ticket": codigo,
        "colaborador": colaborador,
        "data": data.isoformat(),
        "equipamento_limpo": check1,
        "sem_vazamentos": check2,
        "sinalizacao": check3,
        "uso_epi": check4,
        "area_isolada": check5,
        "observacoes": observacoes
    }
    st.success("Checklist salvo com sucesso!")
    st.write(dados)
