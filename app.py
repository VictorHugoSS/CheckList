import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
from datetime import date

# Detector usando OpenCV (QR code)
class QRCodeScanner(VideoTransformerBase):
    def __init__(self):
        self.result = ""
        self.detector = cv2.QRCodeDetector()

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        data, bbox, _ = self.detector.detectAndDecode(img)
        if bbox is not None and data:
            self.result = data
            for i in range(len(bbox)):
                pt1 = tuple(bbox[i][0])
                pt2 = tuple(bbox[(i+1) % len(bbox)][0])
                cv2.line(img, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (0, 255, 0), 2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return img

st.title("Checklist com Leitor de QR Code")

st.markdown("### 📷 Escaneie o QR Code com a câmera")

ctx = webrtc_streamer(key="qrscanner", video_transformer_factory=QRCodeScanner)

qr_code = ""
if ctx.video_transformer:
    qr_code = ctx.video_transformer.result

codigo = st.text_input("Número do Ticket (preenchido automaticamente)", value=qr_code)
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
