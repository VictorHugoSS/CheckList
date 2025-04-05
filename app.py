import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist QR/Barra", layout="centered")

st.markdown("""
    <style>
    .barcode-wrapper {
        position: relative;
        width: 100%;
        max-width: 400px;
        margin-bottom: 1rem;
    }

    input#ticket_input {
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
        padding: 0;
        cursor: pointer;
    }

    .barcode-btn img {
        width: 24px;
        height: 24px;
    }

    #reader {
        margin-top: 10px;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🧾 Checklist com Scanner Integrado")

# Campo de input (real) com scanner embutido por HTML
codigo = st.text_input("Número do Ticket", key="ticket", label_visibility="collapsed", placeholder="Número do Ticket")

# Scanner aparece após clicar no botão
if st.button("📷 Abrir Scanner"):
    components.html(
        """
        <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
        <div id="reader"></div>
        <script>
            const scanner = new Html5Qrcode("reader");
            scanner.start(
                { facingMode: { exact: "environment" } },
                { fps: 10, qrbox: 250 },
                function(decodedText) {
                    const input = window.parent.document.querySelector('input[aria-label="Número do Ticket"]');
                    if (input) {
                        input.value = decodedText;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    scanner.stop().then(() => {
                        document.getElementById("reader").innerHTML = "✅ Código escaneado!";
                    });
                },
                function(error) {}
            ).catch(err => {
                document.getElementById("reader").innerHTML = "🚫 Erro ao acessar câmera.";
            });
        </script>
        """,
        height=460
    )

# Demais campos
colaborador = st.text_input("Colaborador")
data = st.date_input("Data", value=date.today())

st.markdown("### Itens de Verificação")
col1, col2 = st.columns(2)
with col1:
    check1 = st.checkbox("Equipamento limpo")
    check2 = st.checkbox("Sem vazamentos")
    check3 = st.checkbox("Sinalização adequada")
with col2:
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
