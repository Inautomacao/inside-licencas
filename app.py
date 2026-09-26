import streamlit as st
import requests
import uuid
import os
import re

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

# Configuração Inicial da Página
st.set_page_config(page_title="INSIDE AUTOMAÇÃO - Gestão de Licenças", layout="wide", page_icon="🛡️")

# Estado de Tema (Escuro / Claro)
if "tema" not in st.session_state:
    st.session_state["tema"] = "escuro"

def alternar_tema():
    st.session_state["tema"] = "claro" if st.session_state["tema"] == "escuro" else "escuro"

is_escuro = st.session_state["tema"] == "escuro"

# Definição de Cores Dinâmicas conforme o Tema
bg_color = "#121214" if is_escuro else "#F5F5F7"
text_color = "#E1E1E6" if is_escuro else "#1C1C1E"
card_bg = "#202024" if is_escuro else "#FFFFFF"
card_border = "#323238" if is_escuro else "#E5E5EA"
subtext_color = "#8D8D99" if is_escuro else "#6E6E73"

st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Logo Centralizado */
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0px 15px 0px;
    }}
    
    /* Badges de Status */
    .badge-status {{
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
        text-align: center;
    }}
    .status-ativo {{
        background-color: rgba(0, 179, 126, 0.2);
        color: #00B37E;
        border: 1px solid #00B37E;
    }}
    .status-bloqueado {{
        background-color: rgba(247, 90, 104, 0.2);
        color: #F75A68;
        border: 1px solid #F75A68;
    }}

    /* Botão de Excluir Personalizado (Vermelho com Letra Branca) */
    div.stButton > button[key*="btn_exc_"] {{
        background-color: #D32F2F !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: bold !important;
    }}
    div.stButton > button[key*="btn_exc_"]:hover {{
        background-color: #9A0007 !important;
        color: #FFFFFF !important;
    }}

    /* Estilização das Abas */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {card_bg};
        border-radius: 6px 6px 0px 0px;
        padding: 10px 20px;
        color: {subtext_color};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #FF8C00 !important;
        color: #FFFFFF !important;
    }}
</style>
""", unsafe_allow_html=True)

# Barra Superior com Alternador de Tema e Logo Central
col_top1, col_top2, col_top3 = st.columns([1, 3, 1])

with col_top2:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=380)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=380)
    else:
        st.markdown("<h1 style='text-align: center; color: #FF8C00;'>INSIDE AUTOMAÇÃO</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_top3:
    st.button("☀️ Modo Claro" if is_escuro else "🌙 Modo Escuro", on_click=alternar_tema)

st.markdown(f"<h3 style='text-align: center; color: {subtext_color}; margin-bottom: 25px;'>Painel de Controle e Emissão de Licenças</h3>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📋 Licenças Cadastradas", "➕ Cadastrar Nova Licença"])

# ABA 2: CADASTRO DE NOVA LICENÇA
with tab2:
    st.subheader("Nova Licença de Sistema")
    
    # Estados para armazenar dados da busca do CNPJ
    if "cnpj_dados" not in st.session_state:
        st.session_state["cnpj_dados"] = {}

    col_cnpj1, col_cnpj2 = st.columns([3, 1])
    input_cnpj_busca = col_cnpj1.text_input("Digite o CNPJ para buscar dados automaticamente:", placeholder="00.000.000/0000-00 ou 00000000000000")
    
    if col_cnpj2.button("🔍 BUSCAR CNPJ", use_container_width=True):
        cnpj_limpo = re.sub(r'\D', '', input_cnpj_busca)
        if len(cnpj_limpo) == 14:
            with st.spinner("Buscando dados da empresa..."):
                try:
                    res_cnpj = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=10)
                    if res_cnpj.status_code == 200:
                        data = res_cnpj.json()
                        logradouro = data.get("logradouro", "")
                        numero = data.get("numero", "")
                        bairro = data.get("bairro", "")
                        complemento = data.get("complemento", "")
                        
                        endereco_comp = f"{logradouro}, {numero}".strip(", ")
                        
                        st.session_state["cnpj_dados"] = {
                            "cnpj": input_cnpj_busca,
                            "fantasia": data.get("nome_fantasia") or data.get("razao_social"),
                            "razao": data.get("razao_social"),
                            "endereco": endereco_comp,
                            "bairro": bairro,
                            "complemento": complemento,
                            "cidade": data.get("municipio"),
                            "estado": data.get("uf")
                        }
                        st.success("Dados encontrados com sucesso!")
                    else:
                        st.error("CNPJ não encontrado ou indisponível na consulta automática.")
                except Exception as e:
                    st.error(f"Erro ao consultar serviço de CNPJ: {e}")
        else:
            st.warning("Por favor, digite um CNPJ válido com 14 dígitos.")

    st.markdown("---")
    
    # Formulário em estrutura vertical/limpa
    d_cnpj = st.session_state["cnpj_dados"]
    
    with st.form("form_nova_licenca", clear_on_submit=True):
        st.markdown("#### 1. Identificação do Cliente e Empresa")
        nome_fantasia = st.text_input("Nome Fantasia *", value=d_cnpj.get("fantasia", ""))
        nome_empresarial = st.text_input("Nome Empresarial / Razão Social", value=d_cnpj.get("razao", ""))
        cnpj = st.text_input("CNPJ", value=d_cnpj.get("cnpj", input_cnpj_busca))
        
        st.markdown("#### 2. Endereço Completo")
        endereco = st.text_input("Logradouro e Número", value=d_cnpj.get("endereco", ""))
        col_end1, col_end2 = st.columns(2)
        bairro = col_end1.text_input("Bairro", value=d_cnpj.get("bairro", ""))
        complemento = col_end2.text_input("Complemento", value=d_cnpj.get("complemento", ""))
        
        col_loc1, col_loc2 = st.columns(2)
        cidade = col_loc1.text_input("Cidade", value=d_cnpj.get("cidade", ""))
        estado = col_loc2.text_input("Estado (UF)", value=d_cnpj.get("estado", ""))
        
        st.markdown("#### 3. Dados do Sistema e Licença")
        
        tipo_sistema = st.selectbox("Tipo de Sistema *", ["XDRest", "XDCoffee", "XDDisco"])
        
        col_lic_num, col_r, col_o = st.columns([2, 1, 1])
        num_lic_input = col_lic_num.text_input("Nº Licença (Digite apenas os números até 6 dígitos) *", placeholder="Ex: 100355")
        
        xd_rest = col_r.number_input("Postos XDRest", min_value=0, value=1)
        xd_orders = col_o.number_input("Postos XDOrders", min_value=0, value=0)
        
        token_gerado = str(uuid.uuid4()).split('-')[0].upper()
        st.info(f"🔑 **Token de Vínculo que será gerado automaticamente:** `{token_gerado}`")
        
        submit = st.form_submit_button(" Emitir e Guardar Licença", use_container_width=True)
        
        if submit:
            if not nome_fantasia or not num_lic_input:
                st.error("Os campos Nome Fantasia e Nº Licença são obrigatórios!")
            else:
                num_formatado = re.sub(r'\D', '', num_lic_input).zfill(6)
                num_licenca_final = f"XDBR.{num_formatado}"
                
                # Monta endereço completo consolidado
                end_completo = f"{endereco} - {bairro}".strip(" - ")
                if complemento:
                    end_completo += f" ({complemento})"

                dados = {
                    "token_vinculo": token_gerado,
                    "numero_licenca": num_licenca_final,
                    "tipo_sistema": tipo_sistema,
                    "nome_fantasia": nome_fantasia,
                    "nome_empresarial": nome_empresarial,
                    "cnpj": cnpj,
                    "estado": estado,
                    "cidade": cidade,
                    "endereco": end_completo,
                    "xd_rest_postos": int(xd_rest),
                    "xd_orders_postos": int(xd_orders),
                    "bloqueado": False
                }
                res = requests.post(f"{URL_SUPABASE}/licencas", json=dados, headers=HEADERS)
                if res.status_code in [200, 201]:
                    st.session_state["cnpj_dados"] = {}
                    st.success(f"Licença **{num_licenca_final}** emitida com sucesso para **{nome_fantasia}**!")
                    st.rerun()
                else:
                    st.error(f"Erro ao guardar licença: {res.text}")

# ABA 1: GERENCIAMENTO DE LICENÇAS
with tab1:
    res = requests.get(f"{URL_SUPABASE}/licencas?select=*&order=nome_fantasia.asc", headers=HEADERS)
    
    if res.status_code == 200:
        licencas = res.json()
        if licencas:
            busca = st.text_input("🔍 Procurar por Cliente, Razão Social, CNPJ, Token ou Nº da Licença (ex: XDBR.100355):", "")
            
            # Cabeçalho da Tabela
            col_t1, col_t2, col_t3, col_t4, col_t5, col_t6, col_t7 = st.columns([1.2, 2, 1.5, 1.2, 1, 1.2, 1])
            col_t1.markdown("**Nº Licença**")
            col_t2.markdown("**Cliente / Razão Social**")
            col_t3.markdown("**Token / CNPJ**")
            col_t4.markdown("**Sistema / Postos**")
            col_t5.markdown("**Status**")
            col_t6.markdown("**Ação Bloqueio**")
            col_t7.markdown("**Opções**")
            st.markdown(f"<hr style='margin: 5px 0px 15px 0px; border-color: {card_border};'>", unsafe_allow_html=True)

            if "confirmar_exclusao" not in st.session_state:
                st.session_state["confirmar_exclusao"] = None
            if "ver_info" not in st.session_state:
                st.session_state["ver_info"] = None

            for lic in licencas:
                lic_id = lic.get('id')
                num_lic = lic.get('numero_licenca', 'N/A')
                sys_tipo = lic.get('tipo_sistema', 'XDRest')
                
                # Filtro de pesquisa amplo
                if busca.lower() not in lic.get('nome_fantasia', '').lower() and \
                   busca.lower() not in lic.get('nome_empresarial', '').lower() and \
                   busca.lower() not in lic.get('cnpj', '').lower() and \
                   busca.lower() not in lic.get('token_vinculo', '').lower() and \
                   busca.lower() not in str(num_lic).lower():
                    continue

                is_bloqueado = lic.get('bloqueado', False)
                
                with st.container():
                    c1, c2, c3, c4, c5, c6, c7 = st.columns([1.2, 2, 1.5, 1.2, 1, 1.2, 1])
                    
                    c1.markdown(f"<strong style='color: #FF8C00;'>{num_lic}</strong>", unsafe_allow_html=True)
                    c2.markdown(f"**{lic.get('nome_fantasia')}**<br><small style='color: {subtext_color};'>{lic.get('nome_empresarial', '-')}</small>", unsafe_allow_html=True)
                    c3.markdown(f"`{lic.get('token_vinculo')}`<br><small style='color: {subtext_color};'>CNPJ: {lic.get('cnpj', '-')}</small>", unsafe_allow_html=True)
                    c4.markdown(f"**{sys_tipo}**<br><small style='color: {subtext_color};'>Rest: {lic.get('xd_rest_postos')} | Ord: {lic.get('xd_orders_postos')}</small>", unsafe_allow_html=True)
                    
                    if is_bloqueado:
                        c5.markdown('<span class="badge-status status-bloqueado">BLOQUEADO</span>', unsafe_allow_html=True)
                        btn_label = "🔓 LIBERAR"
                    else:
                        c5.markdown('<span class="badge-status status-ativo">ATIVO</span>', unsafe_allow_html=True)
                        btn_label = "🔒 BLOQUEAR"
                        
                    # Botão Bloqueio/Liberar Interativo
                    if c6.button(btn_label, key=f"btn_bloqueio_{lic_id}"):
                        novo_status = not is_bloqueado
                        url_up = f"{URL_SUPABASE}/licencas?id=eq.{lic_id}"
                        res_up = requests.patch(url_up, json={"bloqueado": novo_status}, headers=HEADERS)
                        if res_up.status_code in [200, 204]:
                            st.rerun()
                        else:
                            st.error(f"Erro ao alterar status: {res_up.text}")
                    
                    col_info, col_del = c7.columns(2)
                    if col_info.button("ℹ️", key=f"btn_info_{lic_id}"):
                        st.session_state["ver_info"] = None if st.session_state["ver_info"] == lic_id else lic_id
                        st.rerun()
                        
                    if col_del.button("🗑️", key=f"btn_exc_{lic_id}"):
                        st.session_state["confirmar_exclusao"] = lic_id
                        st.rerun()

                    # Painel de Informações Detalhadas (Aparece ao clicar no ℹ️)
                    if st.session_state.get("ver_info") == lic_id:
                        st.info(f"""
                        📌 **DETALHES DA LICENÇA - INSIDE AUTOMAÇÃO**
                        
                        * **Nº da Licença:** `{num_lic}`
                        * **Tipo de Sistema:** {sys_tipo}
                        * **Nome Fantasia:** {lic.get('nome_fantasia')}
                        * **Razão Social:** {lic.get('nome_empresarial', '-')}
                        * **CNPJ:** {lic.get('cnpj', '-')}
                        * **Endereço Completo:** {lic.get('endereco', '-')}
                        * **Cidade / UF:** {lic.get('cidade', '-')}/{lic.get('estado', '-')}
                        * **Postos Liberados:** XDRest: {lic.get('xd_rest_postos')} | XDOrders: {lic.get('xd_orders_postos')}
                        * **Token de Vínculo do PC:** `{lic.get('token_vinculo')}`
                        * **Status Atual:** {"🔴 BLOQUEADO" if is_bloqueado else "🟢 ATIVO"}
                        """)

                    # Caixa de Confirmação para Exclusão
                    if st.session_state.get("confirmar_exclusao") == lic_id:
                        with st.form(key=f"form_excluir_{lic_id}"):
                            st.warning(f"⚠️ Confirma a exclusão definitiva da licença **{num_lic}** do cliente **{lic.get('nome_fantasia')}**?")
                            pwd_input = st.text_input("Digite a senha de administrador:", type="password")
                            
                            col_f1, col_f2 = st.columns(2)
                            btn_confirma = col_f1.form_submit_button(" Confirmar Exclusão")
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
                                    st.error("Senha incorreta!")
                            
                            if btn_cancela:
                                st.session_state["confirmar_exclusao"] = None
                                st.rerun()

                    st.markdown(f"<hr style='margin: 8px 0px; border-color: {card_border};'>", unsafe_allow_html=True)
        else:
            st.info("Nenhuma licença cadastrada no sistema.")
    else:
        st.error(f"Erro ao ligar ao banco de dados: {res.text}")
