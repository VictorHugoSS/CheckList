import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist QR/Barra", layout="centered")
st.markdown(
    """
    <style>
    .barcode-wrapper {
        position: relative;
        width: 100%;
        max-width: 400px;
        margin-bottom: 10px;
    }

    input.barcode-input {
        width: 100%;
        padding: 0.6rem 2.5rem 0.6rem 0.8rem;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 8px;
        box-sizing: border-box;
    }

    .barcode-btn {
        position: absolute;
        top: 50%;
        right: 10px;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
    }

    .barcode-btn img {
        width: 22px;
        height: 22px;
    }

    #reader {
        margin-top: 10px;
        max-width: 400px;
        width: 100%;
    }

    section.main > div {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("## 🧾 Checklist com Leitor Integrado")

# Componente HTML do campo com botão e leitor
components.html(
    """
    <script src="https://unpkg.com/html5-qrcode"></script>

    <div class="barcode-wrapper">
        <input class="barcode-input" id="barcodeInput" placeholder="Número do Ticket" aria-label="Número do Ticket"/>
        <button class="barcode-btn" onclick="startScanner()">
            <img src="https://cdn-icons-png.flaticon.com/512/545/545705.png" alt="Scan">
        </button>
    </div>

    <div id="reader"></div>

    <script>
        let scannerStarted = false;
        let html5QrcodeScanner;

        function startScanner() {
            if (scannerStarted) return;
            scannerStarted = true;
            html5QrcodeScanner = new Html5Qrcode("reader");

            html5QrcodeScanner.start(
                { facingMode: { exact: "environment" } },
                {
                    fps: 10,
                    qrbox: 250
                },
                (decodedText) => {
                    const input = window.parent.document.querySelector('input[aria-label="Número do Ticket"]');
                    if (input) {
                        input.value = decodedText;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    html5QrcodeScanner.stop().then(() => {
                        document.getElementById("reader").innerHTML = "";
                        scannerStarted = false;
                    });
                },
                (errorMessage) => {}
            ).catch(err => {
                console.error(err);
                scannerStarted = false;
            });
        }
    </script>
    """,
    height=520
)

# Campo que será preenchido pelo scanner
# (O valor virá via JavaScript no input com mesmo label)
codigo = st.text_input("Número do Ticket", key="ticket")

# Campos normais do checklist
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
