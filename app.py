import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist com Leitor de QR/Barra", layout="centered")

st.title("📋 Checklist com Leitor de QR Code / Código de Barras")

st.markdown("### 📸 Leitor integrado (use a câmera do celular)")

# Componente HTML/JS que escaneia QR Code e Códigos de Barras
components.html(
    """
    <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
    <div id="reader" style="width:100%; max-width:400px"></div>
    <input type="text" id="barcode-result" hidden>

    <script>
        function docReady(fn) {
            if (document.readyState === "complete" || document.readyState === "interactive") {
                setTimeout(fn, 1);
            } else {
                document.addEventListener("DOMContentLoaded", fn);
            }
        }

        docReady(function () {
            const resultBox = document.getElementById("barcode-result");

            const scanner = new Html5QrcodeScanner("reader", {
                fps: 10,
                qrbox: 250,
                rememberLastUsedCamera: true,
                supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA]
            });

            scanner.render((decodedText, decodedResult) => {
                resultBox.value = decodedText;
                const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInput"]');
                if (streamlitInput) {
                    streamlitInput.value = decodedText;
                    streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
            });
        });
    </script>
    """,
    height=450,
)

# Campo preenchido automaticamente após leitura
codigo = st.text_input("Número do Ticket (preenchido automaticamente)")
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
