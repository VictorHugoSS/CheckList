import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist com Scanner", layout="centered")
st.title("📋 Checklist com Scanner")

# Campo onde o código escaneado será exibido
codigo = st.text_input("Número do Ticket", key="ticket")

# Ativador do scanner
abrir = st.checkbox("📷 Ativar câmera")

# Scanner via html5-qrcode (fora do iframe + câmera traseira)
if abrir:
    components.html(
        """
        <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
        <div id="reader" style="width: 100%; max-width: 400px;"></div>
        <script>
            const scanner = new Html5Qrcode("reader");
            scanner.start(
                { facingMode: { exact: "environment" } }, // traseira
                { fps: 10, qrbox: 250 },
                (decodedText, decodedResult) => {
                    const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
                    if (input) {
                        input.value = decodedText;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    scanner.stop().then(() => {
                        document.getElementById("reader").innerHTML = "✔️ Código escaneado!";
                    });
                },
                (error) => { /* ignora erros */ }
            ).catch((err) => {
                console.error("Erro ao acessar câmera:", err);
                document.getElementById("reader").innerHTML = "🚫 Falha ao acessar a câmera.";
            });
        </script>
        """,
        height=420
    )

# Formulário do checklist
colaborador = st.text_input("Colaborador")
data = st.date_input("Data", value=date.today())

st.subheader("Itens de Verificação")
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
