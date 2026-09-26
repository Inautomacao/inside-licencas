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

# Função para converter imagem local para base64 e usar no CSS do fundo
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

# Aplicação de Estilos CSS Personalizados
st.markdown(f"""
<style>
    /* Aplicação do Fundo Customizado na Página */
    .stApp {{
        {bg_css}
        color: #FFFFFF;
    }}
    
    /* Centralização do Logo */
    .logo-header {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 10px;
    }}
    
    /* Título Licenças */
    .main-title {{
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 10px;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
        text-shadow: 0px 2px 10px rgba(0, 0, 0, 0.8);
    }}
    
    /* Container Principal Branco/Claro Isolado para a Tabela e Abas */
    .main-container-box {{
        background-color: #FFFFFF;
        color: #1A1D20;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.5);
        margin-top: 10px;
    }}

    /* Estilo das Abas no Container Branco */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #E2E8F0;
        border-radius: 6px 6px 0px 0px;
        padding: 10px 22px;
        color: #475569;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #FF8C00 !important;
        color: #FFFFFF !important;
    }}

    /* Badges de Status Modernos */
    .badge-status {{
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
        text-align: center;
    }}
    .status-ativo {{
        background-color: #E6F4EA;
        color: #137333;
        border: 1px solid #CEEAD6;
    }}
    .status-bloqueado {{
        background-color: #FCE8E6;
        color: #C5221F;
        border: 1px solid #FAD2CF;
    }}

    /* Botão de Excluir estilizado com 'X' em Vermelho */
    div.stButton > button[key*="btn_exc_"] {{
        background-color: #FCE8E6 !important;
        color: #D32F2F !important;
        border: 1px solid #F5C6CB !important;
        font-weight: 800 !important;
        font-size: 14px !important;
        border-radius: 6px !important;
        padding: 2px 10px !important;
    }}
    div.stButton > button[key*="btn_exc_"]:hover {{
        background-color: #D32F2F !important;
        color: #FFFFFF !important;
    }}

    div.stButton > button[key*="btn_info_"] {{
        background-color: #E8F0FE !important;
        color: #1A73E8 !important;
        border: 1px solid #AECBFA !important;
        font-weight: bold !important;
        font-size: 13px !important;
        border-radius: 6px !important;
    }}
    div.stButton > button[key*="btn_info_"]:hover {{
        background-color: #1A73E8 !important;
        color: #FFFFFF !important;
    }}
</style>
""", unsafe_allow_html=True)

# Logo Perfeitamente Centralizada
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

# Título Licenças
st.markdown('<div class="main-title">Licenças</div>', unsafe_allow_html=True)

# Bloco de Conteúdo Branco (Separado do Fundo.png)
with st.container():
    tab1, tab2 = st.tabs(["Licenças Cadastradas", "+ Cadastrar Nova Licença"])

    # ABA 2: CADASTRO DE NOVA LICENÇA
    with tab2:
        st.markdown("<h3 style='color: #1A1D20;'>Nova Licença de Sistema</h3>", unsafe_allow_html=True)
        
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
            st.markdown("<h4 style='color: #1A1D20;'>Identificação do Cliente</h4>", unsafe_allow_html=True)
            nome_fantasia = st.text_input("Nome Fantasia *", value=d_cnpj.get("fantasia", ""))
            nome_empresarial = st.text_input("Nome Empresarial / Razão Social", value=d_cnpj.get("razao", ""))
            cnpj = st.text_input("CNPJ", value=d_cnpj.get("cnpj", input_cnpj_busca))
            
            st.markdown("<h4 style='color: #1A1D20;'>Endereço</h4>", unsafe_allow_html=True)
            endereco = st.text_input("Logradouro e Número", value=d_cnpj.get("endereco", ""))
            col_end1, col_end2 = st.columns(2)
            bairro = col_end1.text_input("Bairro", value=d_cnpj.get("bairro", ""))
            complemento = col_end2.text_input("Complemento", value=d_cnpj.get("complemento", ""))
            
            col_loc1, col_loc2 = st.columns(2)
            cidade = col_loc1.text_input("Cidade", value=d_cnpj.get("cidade", ""))
            estado = col_loc2.text_input("Estado (UF)", value=d_cnpj.get("estado", ""))
            
            st.markdown("<h4 style='color: #1A1D20;'>Configuração da Licença</h4>", unsafe_allow_html=True)
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
                col_t1.markdown("<strong style='color: #1A1D20;'>Nº Licença</strong>", unsafe_allow_html=True)
                col_t2.markdown("<strong style='color: #1A1D20;'>Cliente / Razão Social</strong>", unsafe_allow_html=True)
                col_t3.markdown("<strong style='color: #1A1D20;'>Token / CNPJ</strong>", unsafe_allow_html=True)
                col_t4.markdown("<strong style='color: #1A1D20;'>Sistema / Postos</strong>", unsafe_allow_html=True)
                col_t5.markdown("<strong style='color: #1A1D20;'>Status</strong>", unsafe_allow_html=True)
                col_t6.markdown("<strong style='color: #1A1D20;'>Ação Bloqueio</strong>", unsafe_allow_html=True)
                col_t7.markdown("<strong style='color: #1A1D20;'>Opções</strong>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 5px 0px 15px 0px; border-color: #E2E8F0;'>", unsafe_allow_html=True)

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
                        c2.markdown(f"<strong style='color: #1A1D20;'>{lic.get('nome_fantasia')}</strong><br><small style='color: #64748B;'>{lic.get('nome_empresarial', '-')}</small>", unsafe_allow_html=True)
                        c3.markdown(f"<code style='color: #0F172A;'>{lic.get('token_vinculo')}</code><br><small style='color: #64748B;'>CNPJ: {lic.get('cnpj', '-')}</small>", unsafe_allow_html=True)
                        c4.markdown(f"<strong style='color: #1A1D20;'>{sys_tipo}</strong><br><small style='color: #64748B;'>Rest: {lic.get('xd_rest_postos')} | Ord: {lic.get('xd_orders_postos')}</small>", unsafe_allow_html=True)
                        
                        if is_bloqueado:
                            c5.markdown('<span class="badge-status status-bloqueado">BLOQUEADO</span>', unsafe_allow_html=True)
                            btn_label = "LIBERAR"
                        else:
                            c5.markdown('<span class="badge-status status-ativo">ATIVO</span>', unsafe_allow_html=True)
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

                        # Painel de Informações Detalhadas
                        if st.session_state.get("ver_info") == lic_id:
                            st.info(f"""
                            **Informações Detalhadas do Cliente**
                            
                            * **Nº da Licença:** `{num_lic}`
                            * **Tipo de Sistema:** {sys_tipo}
                            * **Nome Fantasia:** {lic.get('nome_fantasia')}
                            * **Razão Social:** {lic.get('nome_empresarial', '-')}
                            * **CNPJ:** {lic.get('cnpj', '-')}
                            * **Endereço Completo:** {lic.get('endereco', '-')}
                            * **Cidade / UF:** {lic.get('cidade', '-')}/{lic.get('estado', '-')}
                            * **Postos Liberados:** XDRest: {lic.get('xd_rest_postos')} | XDOrders: {lic.get('xd_orders_postos')}
                            * **Token de Vínculo:** `{lic.get('token_vinculo')}`
                            * **Status do Sistema:** {"BLOQUEADO" if is_bloqueado else "ATIVO"}
                            """)

                        # Modal de Exclusão
                        if st.session_state.get("confirmar_exclusao") == lic_id:
                            with st.form(key=f"form_excluir_{lic_id}"):
                                st.warning(f"Confirma a exclusão da licença {num_lic} de {lic.get('nome_fantasia')}?")
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

                        st.markdown("<hr style='margin: 8px 0px; border-color: #E2E8F0;'>", unsafe_allow_html=True)
            else:
                st.info("Nenhuma licença cadastrada.")
        else:
            st.error(f"Erro ao ligar ao banco de dados: {res.text}")
