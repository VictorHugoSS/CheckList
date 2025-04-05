import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist QR/Barra", layout="centered")

st.title("📋 Checklist com Leitor Integrado")

# Campo estilizado com ícone e botão embutido
components.html(
    """
    <style>
        .barcode-wrapper {
            position: relative;
            width: 100%;
            max-width: 400px;
            margin-bottom: 1rem;
        }

        input.barcode-input {
            width: 100%;
            padding: 0.6rem 2.5rem 0.6rem 0.8rem;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 8px;
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
            width: 24px;
            height: 24px;
        }

        #reader {
            margin-top: 1rem;
        }
    </style>

    <div class="barcode-wrapper">
        <input class="barcode-input" id="barcodeInput" placeholder="Número do Ticket" aria-label="Número do Ticket"/>
        <button class="barcode-btn" onclick="startScanner()">
            <img src="https://cdn-icons-png.flaticon.com/512/565/565547.png" alt="Scan">
        </button>
    </div>

    <div id="reader" style="width: 100%; max-width: 400px;"></div>

    <script src="https://unpkg.com/html5-qrcode"></script>
    <script>
        let scannerStarted = false;
        let html5QrcodeScanner;

        function startScanner() {
            if (scannerStarted) return;

            scannerStarted = true;
            html5QrcodeScanner = new Html5Qrcode("reader");

            html5QrcodeScanner.start(
                { facingMode: { exact: "environment" } },  // força traseira
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
                (errorMessage) => {
                    // erros ignorados
                }
            ).catch(err => {
                console.error(err);
                scannerStarted = false;
            });
        }
    </script>
    """,
    height=550
)

# Agora o restante do formulário
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
        "ticket": st.session_state.get("Número do Ticket", ""),
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
