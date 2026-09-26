import streamlit as st
import requests
import uuid
import os
import re
import base64

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
st.set_page_config(page_title="INSIDE AUTOMAÇÃO - Licenças", layout="wide", page_icon="🛡️")

# Converter imagem local para base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

fundo_b64 = get_base64_image("fundo.png") or get_base64_image("fundo.jpg") or get_base64_image("FUNDO ESCURO.png")

bg_css = f"""
    background-image: url("data:image/png;base64,{fundo_b64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
""" if fundo_b64 else "background-color: #0E0F12;"

# Aplicação de Estilos CSS com Força Máxima (Preto nos Textos e Botões Fortes)
st.markdown(f"""
<style>
    /* Fundo Geral da Página */
    .stApp {{
        {bg_css}
    }}

    /* Centralização da Logo */
    .logo-header {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 15px;
        margin-bottom: 10px;
    }}

    /* QUADRO BRANCO SÓLIDO */
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div,
    .main-white-card {{
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 30px !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.6) !important;
        margin-bottom: 30px !important;
    }}

    /* FORÇAR FONTE PRETA EM TODOS OS TEXTOS DO QUADRO */
    .main-white-card *, 
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown strong,
    label, p, span, h1, h2, h3, h4, h5, h6, caption {{
        color: #000000 !important;
    }}

    /* Título Licenças DENTRO do Quadro Branco */
    .inner-title {{
        font-size: 30px !important;
        font-weight: 900 !important;
        color: #000000 !important;
        margin-bottom: 15px;
        border-bottom: 2px solid #DEE2E6;
        padding-bottom: 10px;
    }}

    /* CAIXA DE PESQUISA E INPUTS - NÍTIDOS E CLAROS */
    div[data-baseweb="input"] > div, 
    input[type="text"], input, select {{
        background-color: #F1F3F5 !important;
        color: #000000 !important;
        border: 1px solid #CED4DA !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }}
    
    input::placeholder {{
        color: #6C757D !important;
    }}

    /* ESTILO DAS ABAS */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 5px;
        border-bottom: 2px solid #DEE2E6;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #E9ECEF !important;
        border-radius: 6px 6px 0px 0px !important;
        padding: 10px 20px !important;
    }}
    .stTabs [data-baseweb="tab"] *, 
    .stTabs [data-baseweb="tab"] p, 
    .stTabs [data-baseweb="tab"] span {{
        color: #212529 !important;
        font-weight: 800 !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #FF8C00 !important;
    }}
    .stTabs [aria-selected="true"] *, 
    .stTabs [aria-selected="true"] p, 
    .stTabs [aria-selected="true"] span {{
        color: #FFFFFF !important;
    }}

    /* === CORES FORTES E NÍTIDAS PARA OS BOTÕES DA TABELA === */
    
    /* 1. Botão Bloquear / Liberar (Coluna 6) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6) div.stButton > button {{
        background-color: #1A1D20 !important;
        border: 2px solid #000000 !important;
        border-radius: 6px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6) div.stButton > button p {{
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 14px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6) div.stButton > button:hover {{
        background-color: #FF8C00 !important;
    }}

    /* 2. Botão Informação "i" (Coluna 7 -> Subcoluna 1) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(1) div.stButton > button {{
        background-color: #0D6EFD !important;
        border: 2px solid #0A58CA !important;
        border-radius: 6px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(1) div.stButton > button p {{
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 16px !important;
    }}

    /* 3. Botão Excluir "X" (Coluna 7 -> Subcoluna 2) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(2) div.stButton > button {{
        background-color: #DC3545 !important;
        border: 2px solid #B02A37 !important;
        border-radius: 6px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(2) div.stButton > button p {{
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 16px !important;
    }}
</style>
""", unsafe_allow_html=True)

# Logo Centralizada
st.markdown('<div class="logo-header">', unsafe_allow_html=True)
col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
with col_l2:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)
    elif os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #FF8C00;'>INSIDE AUTOMAÇÃO</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Marcador para envolver o container em fundo branco
st.markdown('<div class="box-branco"></div>', unsafe_allow_html=True)

# QUADRO BRANCO PRINCIPAL
with st.container():
    st.markdown('<div class="main-white-card">', unsafe_allow_html=True)
    
    # Título Licenças DENTRO do quadro branco
    st.markdown('<div class="inner-title">Licenças</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Licenças Cadastradas", "+ Cadastrar Nova Licença"])

    # ABA 2: CADASTRO DE NOVA LICENÇA
    with tab2:
        st.markdown("### Nova Licença de Sistema")
        
        if "cnpj_dados" not in st.session_state:
            st.session_state["cnpj_dados"] = {}

        col_cnpj1, col_cnpj2 = st.columns([3, 1])
        input_cnpj_busca = col_cnpj1.text_input("CNPJ para busca automática:", placeholder="Digite o CNPJ...")
        
        if col_cnpj2.button("Buscar CNPJ", use_container_width=True):
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
                            st.success("Empresa localizada com sucesso!")
                        else:
                            st.error("CNPJ não encontrado.")
                    except Exception as e:
                        st.error(f"Erro ao consultar CNPJ: {e}")
            else:
                st.warning("CNPJ inválido. Digite 14 números.")

        st.markdown("---")
        
        d_cnpj = st.session_state["cnpj_dados"]
        
        with st.form("form_nova_licenca", clear_on_submit=True):
            st.markdown("#### Identificação do Cliente")
            nome_fantasia = st.text_input("Nome Fantasia *", value=d_cnpj.get("fantasia", ""))
            nome_empresarial = st.text_input("Nome Empresarial / Razão Social", value=d_cnpj.get("razao", ""))
            cnpj = st.text_input("CNPJ", value=d_cnpj.get("cnpj", input_cnpj_busca))
            
            st.markdown("#### Endereço")
            endereco = st.text_input("Logradouro e Número", value=d_cnpj.get("endereco", ""))
            col_end1, col_end2 = st.columns(2)
            bairro = col_end1.text_input("Bairro", value=d_cnpj.get("bairro", ""))
            complemento = col_end2.text_input("Complemento", value=d_cnpj.get("complemento", ""))
            
            col_loc1, col_loc2 = st.columns(2)
            cidade = col_loc1.text_input("Cidade", value=d_cnpj.get("cidade", ""))
            estado = col_loc2.text_input("Estado (UF)", value=d_cnpj.get("estado", ""))
            
            st.markdown("#### Configuração da Licença")
            tipo_sistema = st.selectbox("Tipo de Sistema *", ["XDRest", "XDCoffee", "XDDisco"])
            
            col_lic_num, col_r, col_o = st.columns([2, 1, 1])
            num_lic_input = col_lic_num.text_input("Nº Licença (Digite até 6 números) *", placeholder="Ex: 100355")
            
            xd_rest = col_r.number_input("Postos XDRest", min_value=0, value=1)
            xd_orders = col_o.number_input("Postos XDOrders", min_value=0, value=0)
            
            token_gerado = str(uuid.uuid4()).split('-')[0].upper()
            st.info(f"Token de Vínculo do PC: `{token_gerado}`")
            
            submit = st.form_submit_button("Emitir e Salvar Licença", use_container_width=True)
            
            if submit:
                if not nome_fantasia or not num_lic_input:
                    st.error("Campos Nome Fantasia e Nº Licença são obrigatórios!")
                else:
                    num_formatado = re.sub(r'\D', '', num_lic_input).zfill(6)
                    num_licenca_final = f"XDBR.{num_formatado}"
                    
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
                        st.success(f"Licença {num_licenca_final} emitida com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao salvar: {res.text}")

    # ABA 1: GERENCIAMENTO DE LICENÇAS
    with tab1:
        res = requests.get(f"{URL_SUPABASE}/licencas?select=*&order=nome_fantasia.asc", headers=HEADERS)
        
        if res.status_code == 200:
            licencas = res.json()
            if licencas:
                busca = st.text_input("Procurar por Cliente, Razão Social, CNPJ, Token ou Nº da Licença:", placeholder="Digite para pesquisar...")
                
                # Cabeçalho da Tabela
                col_t1, col_t2, col_t3, col_t4, col_t5, col_t6, col_t7 = st.columns([1.5, 2.2, 1.8, 1.3, 1.1, 1.3, 1.2])
                col_t1.markdown("<strong style='color: #000000;'>Nº Licença</strong>", unsafe_allow_html=True)
                col_t2.markdown("<strong style='color: #000000;'>Cliente / Razão Social</strong>", unsafe_allow_html=True)
                col_t3.markdown("<strong style='color: #000000;'>Token / CNPJ</strong>", unsafe_allow_html=True)
                col_t4.markdown("<strong style='color: #000000;'>Sistema / Postos</strong>", unsafe_allow_html=True)
                col_t5.markdown("<strong style='color: #000000;'>Status</strong>", unsafe_allow_html=True)
                col_t6.markdown("<strong style='color: #000000;'>Ação Bloqueio</strong>", unsafe_allow_html=True)
                col_t7.markdown("<strong style='color: #000000;'>Opções</strong>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 5px 0px 15px 0px; border-color: #DEE2E6;'>", unsafe_allow_html=True)

                if "confirmar_exclusao" not in st.session_state:
                    st.session_state["confirmar_exclusao"] = None
                if "ver_info" not in st.session_state:
                    st.session_state["ver_info"] = None

                for lic in licencas:
                    lic_id = lic.get('id')
                    
                    num_lic_raw = lic.get('numero_licenca')
                    if not num_lic_raw or num_lic_raw == 'None':
                        num_lic = "XDBR.------"
                    else:
                        num_lic = str(num_lic_raw)

                    sys_tipo = lic.get('tipo_sistema')
                    if not sys_tipo or sys_tipo == 'None':
                        sys_tipo = "XDRest"

                    if busca.lower() not in lic.get('nome_fantasia', '').lower() and \
                       busca.lower() not in lic.get('nome_empresarial', '').lower() and \
                       busca.lower() not in lic.get('cnpj', '').lower() and \
                       busca.lower() not in lic.get('token_vinculo', '').lower() and \
                       busca.lower() not in num_lic.lower():
                        continue

                    is_bloqueado = lic.get('bloqueado', False)
                    
                    with st.container():
                        c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 2.2, 1.8, 1.3, 1.1, 1.3, 1.2])
                        
                        c1.markdown(f"<strong style='color: #D97706;'>{num_lic}</strong>", unsafe_allow_html=True)
                        c2.markdown(f"<strong style='color: #000000;'>{lic.get('nome_fantasia')}</strong><br><small style='color: #495057;'>{lic.get('nome_empresarial', '-')}</small>", unsafe_allow_html=True)
                        c3.markdown(f"<span style='color: #000000; font-weight: bold; font-family: monospace;'>{lic.get('token_vinculo')}</span><br><small style='color: #495057;'>CNPJ: {lic.get('cnpj', '-')}</small>", unsafe_allow_html=True)
                        c4.markdown(f"<strong style='color: #000000;'>{sys_tipo}</strong><br><small style='color: #495057;'>Rest: {lic.get('xd_rest_postos')} | Ord: {lic.get('xd_orders_postos')}</small>", unsafe_allow_html=True)
                        
                        # APLICAÇÃO DE CORES FORTES E PURAS NO STATUS (Ignorando qualquer bloqueio de tema)
                        if is_bloqueado:
                            c5.markdown('<div style="background-color: #FF0000; color: #FFFFFF; font-weight: 900; padding: 6px 14px; border-radius: 20px; font-size: 13px; text-align: center; box-shadow: 0px 4px 6px rgba(0,0,0,0.2);">BLOQUEADO</div>', unsafe_allow_html=True)
                            btn_label = "LIBERAR"
                        else:
                            c5.markdown('<div style="background-color: #00C851; color: #FFFFFF; font-weight: 900; padding: 6px 14px; border-radius: 20px; font-size: 13px; text-align: center; box-shadow: 0px 4px 6px rgba(0,0,0,0.2);">ATIVO</div>', unsafe_allow_html=True)
                            btn_label = "BLOQUEAR"
                            
                        if c6.button(btn_label, key=f"btn_bloqueio_{lic_id}"):
                            novo_status = not is_bloqueado
                            url_up = f"{URL_SUPABASE}/licencas?id=eq.{lic_id}"
                            res_up = requests.patch(url_up, json={"bloqueado": novo_status}, headers=HEADERS)
                            if res_up.status_code in [200, 204]:
                                st.rerun()
                            else:
                                st.error(f"Erro ao alterar status: {res_up.text}")
                        
                        col_i, col_d = c7.columns(2)
                        if col_i.button("i", key=f"btn_info_{lic_id}"):
                            st.session_state["ver_info"] = None if st.session_state["ver_info"] == lic_id else lic_id
                            st.rerun()
                            
                        if col_d.button("X", key=f"btn_exc_{lic_id}"):
                            st.session_state["confirmar_exclusao"] = lic_id
                            st.rerun()

                        # Painel de Informações Detalhadas (FUNDO CLARO COM LETRAS 100% PRETAS)
                        if st.session_state.get("ver_info") == lic_id:
                            st.markdown(f"""
                            <div style="background-color: #F8F9FA; padding: 20px; border-radius: 8px; border: 1px solid #CED4DA; margin-top: 10px;">
                                <h4 style="color: #000000; margin-top: 0;">Informações Detalhadas do Cliente</h4>
                                <ul style="color: #000000; font-size: 15px; font-weight: 500; line-height: 1.8;">
                                    <li><strong style="color: #000000;">Nº da Licença:</strong> {num_lic}</li>
                                    <li><strong style="color: #000000;">Tipo de Sistema:</strong> {sys_tipo}</li>
                                    <li><strong style="color: #000000;">Nome Fantasia:</strong> {lic.get('nome_fantasia')}</li>
                                    <li><strong style="color: #000000;">Razão Social:</strong> {lic.get('nome_empresarial', '-')}</li>
                                    <li><strong style="color: #000000;">CNPJ:</strong> {lic.get('cnpj', '-')}</li>
                                    <li><strong style="color: #000000;">Endereço Completo:</strong> {lic.get('endereco', '-')}</li>
                                    <li><strong style="color: #000000;">Cidade / UF:</strong> {lic.get('cidade', '-')}/{lic.get('estado', '-')}</li>
                                    <li><strong style="color: #000000;">Postos Liberados:</strong> XDRest: {lic.get('xd_rest_postos')} | XDOrders: {lic.get('xd_orders_postos')}</li>
                                    <li><strong style="color: #000000;">Token de Vínculo:</strong> <code>{lic.get('token_vinculo')}</code></li>
                                    <li><strong style="color: #000000;">Status do Sistema:</strong> {"BLOQUEADO" if is_bloqueado else "ATIVO"}</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)

                        # Modal de Exclusão (FUNDO CLARO COM LETRAS PRETAS)
                        if st.session_state.get("confirmar_exclusao") == lic_id:
                            with st.form(key=f"form_excluir_{lic_id}"):
                                st.markdown(f"<h4 style='color: #000000;'>Confirma a exclusão da licença {num_lic} de {lic.get('nome_fantasia')}?</h4>", unsafe_allow_html=True)
                                pwd_input = st.text_input("Senha de Administrador:", type="password")
                                
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
                                        st.error("Senha incorreta!")
                                
                                if btn_cancela:
                                    st.session_state["confirmar_exclusao"] = None
                                    st.rerun()

                        st.markdown("<hr style='margin: 8px 0px; border-color: #E9ECEF;'>", unsafe_allow_html=True)
            else:
                st.info("Nenhuma licença cadastrada.")
        else:
            st.error(f"Erro ao ligar ao banco de dados: {res.text}")
            
    st.markdown('</div>', unsafe_allow_html=True)
