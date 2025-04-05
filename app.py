import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist QR/Barra", layout="centered")

st.markdown("## 🧾 Checklist com Leitor Integrado")

# Inicializar a variável de sessão para o ticket
if "ticket" not in st.session_state:
    st.session_state.ticket = ""

# Exibir o campo com ícone e botão de scanner
components.html(
    f"""
    <style>
        .barcode-wrapper {{
            position: relative;
            width: 100%;
            max-width: 400px;
            margin-bottom: 10px;
        }}
        input.barcode-input {{
            width: 100%;
            padding: 0.6rem 2.5rem 0.6rem 0.8rem;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-sizing: border-box;
        }}
        .barcode-btn {{
            position: absolute;
            top: 50%;
            right: 10px;
            transform: translateY(-50%);
            background: none;
            border: none;
            padding: 0;
            cursor: pointer;
        }}
        .barcode-btn img {{
            width: 22px;
            height: 22px;
        }}
        #reader {{
            margin-top: 10px;
            max-width: 400px;
            width: 100%;
        }}
    </style>

    <div class="barcode-wrapper">
        <input class="barcode-input" id="barcodeInput" placeholder="Número do Ticket" />
        <button class="barcode-btn" onclick="startScanner()">
            <img src="https://i.imgur.com/oJHSmE3.png" alt="Scan">
        </button>
    </div>

    <div id="reader"></div>

    <script src="https://unpkg.com/html5-qrcode"></script>
    <script>
        let scannerStarted = false;
        let html5QrcodeScanner;

        function startScanner() {{
            if (scannerStarted) return;
            scannerStarted = true;

            html5QrcodeScanner = new Html5Qrcode("reader");

            html5QrcodeScanner.start(
                {{ facingMode: {{ exact: "environment" }} }},
                {{ fps: 10, qrbox: 250 }},
                (decodedText) => {{
                    document.getElementById("barcodeInput").value = decodedText;

                    // Escreve em um campo hidden usado para recuperar no Streamlit
                    const hiddenInput = window.parent.document.querySelector('input[data-testid="stTextInput"][aria-label="Número do Ticket"]');
                    if (hiddenInput) {{
                        hiddenInput.value = decodedText;
                        hiddenInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}

                    html5QrcodeScanner.stop().then(() => {{
                        document.getElementById("reader").innerHTML = "";
                        scannerStarted = false;
                    }});
                }},
                (errorMessage) => {{}}
            ).catch(err => {{
                console.error(err);
                scannerStarted = false;
            }});
        }}
    </script>
    """,
    height=540
)

# Exibir o campo real (oculto para o usuário, mas sincronizado)
codigo = st.text_input("Número do Ticket", value=st.session_state.ticket, key="ticket")

# Campos do checklist
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
        "ticket": st.session_state.ticket,
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
