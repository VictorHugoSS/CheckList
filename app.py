import streamlit as st
import streamlit.components.v1 as components
from datetime import date

st.set_page_config(page_title="Checklist QR/Barra", layout="centered")

st.markdown("## 🧾 Checklist com Leitor Integrado")

# Campo real onde será preenchido o valor do código escaneado
ticket = st.text_input("Número do Ticket", key="ticket")

# Botão que ativa o scanner
if st.button("📷 Escanear código"):
    components.html(
        """
        <script src="https://unpkg.com/html5-qrcode"></script>
        <div id="reader" style="width: 100%; max-width: 400px;"></div>
        <script>
            let scanner = new Html5Qrcode("reader");
            scanner.start(
                { facingMode: { exact: "environment" } },
                { fps: 10, qrbox: 250 },
                (decodedText, decodedResult) => {
                    const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
                    if (input) {
                        input.value = decodedText;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    scanner.stop();
                    document.getElementById("reader").innerHTML = "";
                },
                (error) => {}
            ).catch((err) => {
                console.error("Camera error:", err);
            });
        </script>
        """,
        height=400
    )

# Restante do formulário
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
    st.success("Checklist salvo com sucesso!")
    st.write(dados)
