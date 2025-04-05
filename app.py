import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist QR/Barra", layout="centered")

st.title("📋 Checklist com Scanner de Código")

# Campo real do ticket
codigo = st.text_input("Número do Ticket", key="ticket")

# Ativa o scanner
if st.button("📷 Escanear código"):
    components.html(
        """
        <script src="https://unpkg.com/html5-qrcode"></script>
        <div id="reader" style="width: 100%; max-width: 400px;"></div>

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
                (error) => {{ /* Ignora erros */ }}
            ).catch(err => {
                console.error("Erro ao acessar a câmera:", err);
                document.getElementById("reader").innerHTML = "🚫 Erro ao abrir câmera.";
            });
        </script>
        """,
        height=450
    )

# Formulário
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
