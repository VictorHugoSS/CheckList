import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist QR/Barra", layout="centered")

st.markdown("## 🧾 Checklist com Scanner Integrado")

# Campo real que receberá o ticket
codigo = st.text_input("Número do Ticket", key="ticket")

# Campo visual com ícone e botão embutido
col1, col2 = st.columns([10, 1])
with col1:
    st.markdown('<input class="barcode-input" id="fakeInput" placeholder="Clique no botão para escanear" disabled>', unsafe_allow_html=True)
with col2:
    scan = st.button("📷")

# Renderiza scanner apenas se clicar no botão
if scan:
    components.html(
        """
        <style>
            .barcode-input {
                width: 100%;
                padding: 0.6rem 2.5rem 0.6rem 0.8rem;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 8px;
                margin-bottom: 1rem;
            }
            #reader {
                margin-top: 10px;
                max-width: 400px;
                width: 100%;
                margin-left: auto;
                margin-right: auto;
            }
        </style>

        <script src="https://unpkg.com/html5-qrcode"></script>
        <div id="reader"></div>

        <script>
            const scanner = new Html5Qrcode("reader");
            scanner.start(
                { facingMode: { exact: "environment" } },
                { fps: 10, qrbox: 250 },
                (decodedText, decodedResult) => {
                    const inputs = window.parent.document.querySelectorAll('input[aria-label="Número do Ticket"]');
                    if (inputs.length > 0) {
                        const input = inputs[0];
                        input.value = decodedText;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    scanner.stop().then(() => {
                        document.getElementById("reader").innerHTML = "<b>✅ Código escaneado!</b>";
                    });
                },
                (error) => { }
            ).catch(err => {
                console.error("Erro ao abrir câmera:", err);
                document.getElementById("reader").innerHTML = "🚫 Erro ao acessar a câmera.";
            });
        </script>
        """,
        height=450
    )

# Campos do checklist (visualmente alinhados)
colaborador = st.text_input("Colaborador")
data = st.date_input("Data", value=date.today())

st.markdown("### Itens de Verificação")
col_a, col_b = st.columns(2)
with col_a:
    check1 = st.checkbox("Equipamento limpo")
    check2 = st.checkbox("Sem vazamentos")
    check3 = st.checkbox("Sinalização adequada")
with col_b:
    check4 = st.checkbox("EPI utilizado corretamente")
    check5 = st.checkbox("Área isolada")

observacoes = st.text_area("Observações")

# Botão de salvar
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
