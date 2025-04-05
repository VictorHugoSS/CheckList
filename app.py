import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist QR/Barra", layout="centered")

st.markdown("## 🧾 Checklist com Leitor Integrado")

# Criar um espaço no Streamlit para exibir o valor escaneado
if "codigo_lido" not in st.session_state:
    st.session_state["codigo_lido"] = ""

# Campo customizado com botão de scanner e ícone personalizado
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

                    // Enviar valor para Streamlit
                    const streamlitEvent = new CustomEvent("streamlit:setComponentValue", {{
                        detail: {{ value: decodedText }},
                        bubbles: true
                    }});
                    window.parent.document.dispatchEvent(streamlitEvent);

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
    height=530
)

# Captura do código escaneado (sem campo duplicado!)
codigo = st.experimental_get_query_params().get("ticket", [""])[0]

# Alternativa: mostrar o valor diretamente
if "value" in st.session_state:
    st.session_state["codigo_lido"] = st.session_state["value"]

if st.session_state["codigo_lido"]:
    st.success(f"Código escaneado: {st.session_state['codigo_lido']}")

# Agora os campos normais do checklist
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
        "ticket": st.session_state["codigo_lido"],
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
