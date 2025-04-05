import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist com Leitor QR/Barra", layout="centered")

st.title("📋 Checklist com Leitor de QR Code / Código de Barras")

# Estado para armazenar resultado do scanner
if "ticket_lido" not in st.session_state:
    st.session_state.ticket_lido = ""

# Botão para abrir o leitor
if st.button("📷 Escanear código"):
    components.html(
        """
        <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
        <div id="reader" style="width:100%; max-width:400px; margin:auto;"></div>
        <script>
            const streamlitInput = window.parent.document.querySelector('input[aria-label="Número do Ticket"]');

            function onScanSuccess(decodedText, decodedResult) {
                const streamlitInput = window.parent.document.querySelector('input[aria-label="Número do Ticket"]');
                if (streamlitInput) {
                    streamlitInput.value = decodedText;
                    streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                html5QrcodeScanner.clear();
            }

            let html5QrcodeScanner = new Html5QrcodeScanner("reader", {
                fps: 10,
                qrbox: 250,
                rememberLastUsedCamera: true,
                supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA]
            }, false);

            html5QrcodeScanner.render(onScanSuccess);
        </script>
        """,
        height=500
    )

# Campo que será preenchido automaticamente
codigo = st.text_input("Número do Ticket", value=st.session_state.ticket_lido, key="ticket")

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
