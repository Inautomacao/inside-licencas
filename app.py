import streamlit as st
import requests
import uuid

# Configurações do Supabase
URL_SUPABASE = "https://tlvftsotimyzcufyqixn.supabase.co/rest/v1"
CHAVE_SUPABASE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsdmZ0c290aW15emN1ZnlxaXhuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MDM3MjAyNiwiZXhwIjoyMTA1OTQ4MDI2fQ.6g_GK338hpKaOOp--31cMdRKO4TG74MP3T2qilZcQ7Q"

HEADERS = {
    "apikey": CHAVE_SUPABASE,
    "Authorization": f"Bearer {CHAVE_SUPABASE}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

st.set_page_config(page_title="INSIDE AUTOMAÇÃO - Licenças", layout="wide")
st.title("🛡️ Controle de Licenças - INSIDE AUTOMAÇÃO")

tab1, tab2 = st.tabs(["📋 Licenças Ativas", "➕ Nova Licença"])

with tab2:
    st.subheader("Cadastrar Nova Licença")
    with st.form("nova_licenca"):
        col1, col2 = st.columns(2)
        nome_fantasia = col1.text_input("Nome Fantasia")
        nome_empresarial = col2.text_input("Nome Empresarial")
        cnpj = col1.text_input("CNPJ")
        estado = col2.text_input("Estado")
        cidade = col1.text_input("Cidade")
        endereco = col2.text_input("Endereço")
        
        xd_rest = col1.number_input("Postos XDRest", min_value=0, value=1)
        xd_orders = col2.number_input("Postos XDOrders", min_value=0, value=0)
        
        token_gerado = str(uuid.uuid4()).split('-')[0].upper()
        
        submit = st.form_submit_button("Criar Licença")
        
        if submit:
            if not nome_fantasia:
                st.warning("Por favor, preencha pelo menos o Nome Fantasia.")
            else:
                dados = {
                    "token_vinculo": token_gerado,
                    "nome_fantasia": nome_fantasia,
                    "nome_empresarial": nome_empresarial,
                    "cnpj": cnpj,
                    "estado": estado,
                    "cidade": cidade,
                    "endereco": endereco,
                    "xd_rest_postos": int(xd_rest),
                    "xd_orders_postos": int(xd_orders),
                    "bloqueado": False
                }
                res = requests.post(f"{URL_SUPABASE}/licencas", json=dados, headers=HEADERS)
                if res.status_code in [200, 201]:
                    st.success(f"Licença criada com sucesso! O Token do cliente é: {token_gerado}")
                    st.rerun()
                else:
                    st.error(f"Erro ao salvar licença: {res.text}")

with tab1:
    st.subheader("Gerenciar Clientes")
    res = requests.get(f"{URL_SUPABASE}/licencas?select=*", headers=HEADERS)
    
    if res.status_code == 200:
        licencas = res.json()
        if licencas:
            for licenca in licencas:
                with st.expander(f"{licenca.get('nome_fantasia')} - Token: {licenca.get('token_vinculo')}"):
                    st.write(f"**CNPJ:** {licenca.get('cnpj')} | **Cidade:** {licenca.get('cidade')}/{licenca.get('estado')}")
                    st.write(f"**XDRest:** {licenca.get('xd_rest_postos')} postos | **XDOrders:** {licenca.get('xd_orders_postos')} postos")
                    
                    status_atual = licenca.get('bloqueado', False)
                    cor_status = "🔴 BLOQUEADO" if status_atual else "🟢 ATIVO"
                    st.write(f"**Status Atual:** {cor_status}")
                    
                    if st.button("Alternar Bloqueio / Liberar", key=licenca.get('id')):
                        novo_status = not status_atual
                        url_update = f"{URL_SUPABASE}/licencas?id=eq.{licenca.get('id')}"
                        res_up = requests.patch(url_update, json={"bloqueado": novo_status}, headers=HEADERS)
                        if res_up.status_code in [200, 204]:
                            st.rerun()
                        else:
                            st.error(f"Erro ao atualizar status: {res_up.text}")
        else:
            st.info("Nenhuma licença cadastrada no momento.")
    else:
        st.error(f"Erro ao carregar licenças do banco: {res.text}")
