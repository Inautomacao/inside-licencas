import streamlit as st
import requests
import uuid
import os

# Configurações do Supabase
URL_SUPABASE = "https://tlvftsotimyzcufyqixn.supabase.co/rest/v1"
CHAVE_SUPABASE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsdmZ0c290aW15emN1ZnlxaXhuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MDM3MjAyNiwiZXhwIjoyMTA1OTQ4MDI2fQ.6g_GK338hpKaOOp--31cMdRKO4TG74MP3T2qilZcQ7Q"

HEADERS = {
    "apikey": CHAVE_SUPABASE,
    "Authorization": f"Bearer {CHAVE_SUPABASE}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

SENHA_EXCLUSAO = "78592121"

# Configuração da Página
st.set_page_config(page_title="INSIDE AUTOMAÇÃO - Gestão de Licenças", layout="wide", page_icon="🛡️")

# Estilização CSS Personalizada (Tema Escuro + Laranja Inside + Tabela Limpa)
st.markdown("""
<style>
    /* Estilo Geral */
    .stApp {
        background-color: #121214;
        color: #E1E1E6;
    }
    
    /* Tabelas e Caixas */
    .card-licenca {
        background-color: #202024;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 6px solid #00B37E;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
    }
    
    .card-licenca.bloqueado {
        border-left: 6px solid #F75A68;
        background-color: #291E21;
    }

    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
        background-color: #FF8C00;
        color: #FFFFFF;
        border: none;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #E07B00;
        color: #FFFFFF;
    }
    
    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #202024;
        border-radius: 6px 6px 0px 0px;
        padding: 10px 20px;
        color: #A8A8B3;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF8C00 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# Exibição do Logo e Título
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=220)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=220)
    else:
        st.markdown("<h2 style='color: #FF8C00;'>INSIDE</h2>", unsafe_allow_html=True)

with col_titulo:
    st.markdown("<h1 style='color: #FFFFFF; margin-top: 10px;'>Painel de Controlo de Licenças</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #A8A8B3;'>INSIDE AUTOMAÇÃO - Boas ideias para ajudar em seus negócios</p>", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2 = st.tabs(["📋 Licenças Cadastradas", "➕ Cadastrar Nova Licença"])

# ABA 2: CADASTRO DE NOVA LICENÇA
with tab2:
    st.subheader("Nova Licença")
    with st.form("nova_licenca", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome_fantasia = col1.text_input("Nome Fantasia *")
        nome_empresarial = col2.text_input("Nome Empresarial")
        cnpj = col1.text_input("CNPJ")
        endereco = col2.text_input("Endereço")
        cidade = col1.text_input("Cidade")
        estado = col2.text_input("Estado")
        
        col_r, col_o = st.columns(2)
        xd_rest = col_r.number_input("Postos XDRest", min_value=0, value=1)
        xd_orders = col_o.number_input("Postos XDOrders", min_value=0, value=0)
        
        token_gerado = str(uuid.uuid4()).split('-')[0].upper()
        st.info(f"🔑 **Token de Vínculo que será gerado:** `{token_gerado}`")
        
        submit = st.form_submit_button(" Emitir e Guardar Licença")
        
        if submit:
            if not nome_fantasia:
                st.error("O campo Nome Fantasia é obrigatório!")
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
                    st.success(f"Licença criada com sucesso para **{nome_fantasia}**! Token: `{token_gerado}`")
                    st.rerun()
                else:
                    st.error(f"Erro ao guardar licença: {res.text}")

# ABA 1: GERENCIAMENTO DE LICENÇAS (VISUAL EM TABELA / CARDS)
with tab1:
    res = requests.get(f"{URL_SUPABASE}/licencas?select=*&order=nome_fantasia.asc", headers=HEADERS)
    
    if res.status_code == 200:
        licencas = res.json()
        if licencas:
            # Filtro de busca rápido
            busca = st.text_input("🔍 Procurar por Cliente, CNPJ ou Token:", "")
            
            # Cabeçalho da Tabela
            col_t1, col_t2, col_t3, col_t4, col_t5, col_t6 = st.columns([2, 1.5, 1.5, 1, 1, 1])
            col_t1.markdown("**Cliente / Razão Social**")
            col_t2.markdown("**Token / CNPJ**")
            col_t3.markdown("**Módulos Liberados**")
            col_t4.markdown("**Status**")
            col_t5.markdown("**Ação Bloqueio**")
            col_t6.markdown("**Excluir Licença**")
            st.markdown("<hr style='margin: 5px 0px 15px 0px; border-color: #323238;'>", unsafe_allow_html=True)

            # Inicializa a chave de confirmação de exclusão na sessão
            if "confirmar_exclusao" not in st.session_state:
                st.session_state["confirmar_exclusao"] = None

            for lic in licencas:
                lic_id = lic.get('id')
                # Aplica o filtro de pesquisa
                if busca.lower() not in lic.get('nome_fantasia', '').lower() and \
                   busca.lower() not in lic.get('cnpj', '').lower() and \
                   busca.lower() not in lic.get('token_vinculo', '').lower():
                    continue

                is_bloqueado = lic.get('bloqueado', False)
                
                # Linha estilo Tabela Interativa
                with st.container():
                    c1, c2, c3, c4, c5, c6 = st.columns([2, 1.5, 1.5, 1, 1, 1])
                    
                    c1.markdown(f"**{lic.get('nome_fantasia')}**<br><small style='color: #8D8D99;'>{lic.get('nome_empresarial', '-')}</small>", unsafe_allow_html=True)
                    c2.markdown(f"`{lic.get('token_vinculo')}`<br><small style='color: #8D8D99;'>CNPJ: {lic.get('cnpj', '-')}</small>", unsafe_allow_html=True)
                    c3.markdown(f"XDRest: **{lic.get('xd_rest_postos')}** | XDOrders: **{lic.get('xd_orders_postos')}**")
                    
                    if is_bloqueado:
                        c4.markdown("<span style='color: #F75A68; font-weight: bold;'>🔴 BLOQUEADO</span>", unsafe_allow_html=True)
                        btn_label = "🔓 LIBERAR"
                    else:
                        c4.markdown("<span style='color: #00B37E; font-weight: bold;'>🟢 ATIVO</span>", unsafe_allow_html=True)
                        btn_label = "🔒 BLOQUEAR"
                        
                    # Botão de Alternar Bloqueio
                    if c5.button(btn_label, key=f"btn_bloqueio_{lic_id}"):
                        novo_status = not is_bloqueado
                        url_up = f"{URL_SUPABASE}/licencas?id=eq.{lic_id}"
                        res_up = requests.patch(url_up, json={"bloqueado": novo_status}, headers=HEADERS)
                        if res_up.status_code in [200, 204]:
                            st.rerun()
                        else:
                            st.error(f"Erro ao alterar status: {res_up.text}")
                    
                    # Botão de Solicitar Exclusão
                    if c6.button("🗑️ EXCLUIR", key=f"btn_exc_{lic_id}"):
                        st.session_state["confirmar_exclusao"] = lic_id
                        st.rerun()

                    # Caixa de Confirmação com Senha para Exclusão
                    if st.session_state.get("confirmar_exclusao") == lic_id:
                        with st.form(key=f"form_excluir_{lic_id}"):
                            st.warning(f"⚠️ Tem certeza que deseja excluir a licença do cliente **{lic.get('nome_fantasia')}**?")
                            pwd_input = st.text_input("Digite a senha de administrador para confirmar:", type="password")
                            
                            col_f1, col_f2 = st.columns(2)
                            btn_confirma = col_f1.form_submit_button("Confirmar Exclusão")
                            btn_cancela = col_f2.form_submit_button("Cancelar")
                            
                            if btn_confirma:
                                if pwd_input == SENHA_EXCLUSAO:
                                    url_del = f"{URL_SUPABASE}/licencas?id=eq.{lic_id}"
                                    res_del = requests.delete(url_del, headers=HEADERS)
                                    if res_del.status_code in [200, 204]:
                                        st.session_state["confirmar_exclusao"] = None
                                        st.success("Licença excluída com sucesso!")
                                        st.rerun()
                                    else:
                                        st.error(f"Erro ao excluir: {res_del.text}")
                                else:
                                    st.error("Senha incorreta! A exclusão foi cancelada.")
                            
                            if btn_cancela:
                                st.session_state["confirmar_exclusao"] = None
                                st.rerun()

                    st.markdown("<hr style='margin: 8px 0px; border-color: #29292E;'>", unsafe_allow_html=True)
        else:
            st.info("Nenhuma licença cadastrada no sistema.")
    else:
        st.error(f"Erro ao ligar ao banco de dados: {res.text}")
