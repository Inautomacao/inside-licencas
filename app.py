import streamlit as st
from supabase import create_client, Client
import uuid

# Configurações do Supabase
URL_SUPABASE = "https://tlvftsotimyzcufyqixn.supabase.co"
# Usando a Secret Key para garantir acesso total de escrita/leitura no Painel
CHAVE_SUPABASE = "sb_secret_r-dQsIIou2_hJ71yFs-TVg_8KpgJuF-"

@st.cache_resource
def init_connection():
    return create_client(URL_SUPABASE, CHAVE_SUPABASE)

try:
    supabase: Client = init_connection()
except Exception as e:
    st.error(f"Erro ao conectar com o Supabase: {e}")
    st.stop()

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
                try:
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
                    supabase.table("licencas").insert(dados).execute()
                    st.success(f"Licença criada com sucesso! O Token do cliente é: {token_gerado}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar licença: {e}")

with tab1:
    st.subheader("Gerenciar Clientes")
    try:
        resposta = supabase.table("licencas").select("*").execute()
        licencas = resposta.data
        
        if licencas:
            for licenca in licencas:
                with st.expander(f"{licenca['nome_fantasia']} - Token: {licenca['token_vinculo']}"):
                    st.write(f"**CNPJ:** {licenca['cnpj']} | **Cidade:** {licenca['cidade']}/{licenca['estado']}")
                    st.write(f"**XDRest:** {licenca['xd_rest_postos']} postos | **XDOrders:** {licenca['xd_orders_postos']} postos")
                    
                    status_atual = licenca['bloqueado']
                    cor_status = "🔴 BLOQUEADO" if status_atual else "🟢 ATIVO"
                    st.write(f"**Status Atual:** {cor_status}")
                    
                    if st.button("Alternar Bloqueio / Liberar", key=licenca['id']):
                        novo_status = not status_atual
                        supabase.table("licencas").update({"bloqueado": novo_status}).eq("id", licenca['id']).execute()
                        st.rerun()
        else:
            st.info("Nenhuma licença cadastrada no momento.")
    except Exception as e:
        st.error(f"Erro ao carregar licenças do banco: {e}")
