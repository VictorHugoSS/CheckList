import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist Scanner", layout="centered")

st.title("📋 Checklist com Leitor")

ticket = st.text_input("Número do Ticket", key="ticket")

# Local onde o scanner será exibido temporariamente
scanner_placeholder = st.empty()

if st.button("📷 Escanear Código"):
    with scanner_placeholder:
        components.html(
            """
            <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
            <div id="reader" style="width: 100%; max-width: 400px;"></div>
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
                    document.getElementById("reader").innerHTML = "🚫 Erro ao abrir câmera.";
                });
            </script>
            """,
            height=440
        )

# Checklist
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
        "ticket": ticket,
        "colaborador": colaborador,
        "data": data.isoformat(),
        "equipamento_limpo": check1,
        "sem_vazamentos": check2,
        "sinalizacao": check3,
        "uso_epi": check4,
        "area_isolada": check5,
        "observacoes": observacoes
    }
    scanner_placeholder.empty()  # remove o scanner do layout
    st.success("Checklist salvo com sucesso!")
    st.write(dados)
