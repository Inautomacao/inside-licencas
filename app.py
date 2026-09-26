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
    background-attachment: fixed;
""" if fundo_b64 else "background-color: #0E0F12;"

# Aplicação de Estilos CSS
st.markdown(f"""
<style>
    .stApp {{ {bg_css} }}

    .logo-header {{ display: flex; justify-content: center; width: 100%; margin: 15px 0 10px 0; }}
    
    /* RESTAURANDO O QUADRO BRANCO SÓLIDO */
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div {{
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 30px !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.6) !important;
        margin-bottom: 30px !important;
    }}

    /* FORÇAR FONTE PRETA NO QUADRO BRANCO */
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div *, 
    .stMarkdown p, .stMarkdown span, .stMarkdown strong, label, p, span, h1, h2, h3, h4, h5, h6 {{
        color: #000000 !important;
    }}

    .inner-title {{
        font-size: 30px !important; font-weight: 800 !important; color: #000000 !important;
        border-bottom: 2px solid #DEE2E6; padding-bottom: 10px; margin-bottom: 15px;
    }}

    /* Inputs e Caixas de Texto */
    div[data-baseweb="input"] > div, input, select {{
        background-color: #F1F3F5 !important; color: #000000 !important;
        border: 1px solid #CED4DA !important; border-radius: 6px !important; font-weight: 600 !important;
    }}

    /* === EFEITO HOVER NAS LINHAS DA TABELA === */
    div[data-testid="stVerticalBlock"]:has(> div.element-container span.row-hook) {{
        padding: 5px 10px;
        border-radius: 12px;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }}
    div[data-testid="stVerticalBlock"]:has(> div.element-container span.row-hook):hover {{
        background-color: #F8F9FA !important;
        transform: scale(1.02);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
        border: 1px solid #DEE2E6;
        z-index: 10;
    }}

    /* === BOTÕES DO FORMULÁRIO (Buscar e Salvar) === */
    div.element-container:has(.btn-buscar) + div button {{
        background-color: #FFC107 !important; border: 2px solid #28A745 !important; 
        color: #000000 !important; font-weight: bold !important; border-radius: 6px !important;
    }}
    div.element-container:has(.btn-salvar) + div button {{
        background-color: #FFFFFF !important; border: 2px solid #28A745 !important; 
        color: #000000 !important; font-weight: bold !important; border-radius: 6px !important;
    }}

    /* === BOTÕES DA TABELA === */
    /* Coluna 6: Bloquear/Liberar */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6) div.stButton > button {{
        background-color: #1A1D20 !important; border: 2px solid #000000 !important; border-radius: 6px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6) div.stButton > button p {{
        color: #FFFFFF !important; font-weight: 800 !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(6) div.stButton > button:hover {{
        background-color: #FF8C00 !important; border-color: #FF8C00 !important;
    }}
    
    /* Coluna 7 -> Sub 1: Info (i) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(1) div.stButton > button {{
        background-color: #0D6EFD !important; border: none !important; border-radius: 6px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(1) div.stButton > button p {{
        color: #FFFFFF !important; font-weight: 900 !important; font-size: 16px !important;
    }}
    
    /* Coluna 7 -> Sub 2: Editar (✏️) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(2) div.stButton > button {{
        background-color: #FFC107 !important; border: none !important; border-radius: 6px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(2) div.stButton > button p {{
        color: #000000 !important; font-weight: 900 !important; font-size: 16px !important;
    }}

    /* Coluna 7 -> Sub 3: Excluir (X) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(3) div.stButton > button {{
        background-color: #DC3545 !important; border: none !important; border-radius: 6px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(7) div[data-testid="column"]:nth-child(3) div.stButton > button p {{
        color: #FFFFFF !important; font-weight: 900 !important; font-size: 16px !important;
    }}

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {{ border-bottom: 2px solid #DEE2E6; }}
    .stTabs [data-baseweb="tab"] {{ background-color: #E9ECEF !important; border-radius: 6px 6px 0 0 !important; }}
    .stTabs [aria-selected="true"] {{ background-color: #FF8C00 !important; }}
    .stTabs [aria-selected="true"] p {{ color: #FFFFFF !important; }}
</style>
""", unsafe_allow_html=True)

# Logo Centralizada
st.markdown('<div class="logo-header">', unsafe_allow_html=True)
col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
with col_l2:
    if os.path.exists("logo.jpg"): st.image("logo.jpg", use_container_width=True)
    elif os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    else: st.markdown("<h1 style='text-align: center; color: #FF8C00;'>INSIDE AUTOMAÇÃO</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Injeção da marcação para o quadro branco
st.markdown('<div class="box-branco"></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="inner-title">Licenças</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Licenças Cadastradas", "+ Cadastrar Nova Licença"])

    # ABA 2: CADASTRO DE NOVA LICENÇA
    with tab2:
        st.markdown("### Nova Licença de Sistema")
        if "cnpj_dados" not in st.session_state: st.session_state["cnpj_dados"] = {}

        col_cnpj1, col_cnpj2 = st.columns([3, 1])
        input_cnpj_busca = col_cnpj1.text_input("CNPJ para busca automática:", placeholder="Digite o CNPJ...", key="busca_cnpj")
        
        st.markdown('<span class="btn-buscar"></span>', unsafe_allow_html=True)
        if col_cnpj2.button("Buscar CNPJ", use_container_width=True):
            cnpj_limpo = re.sub(r'\D', '', input_cnpj_busca)
            if len(cnpj_limpo) == 14:
                with st.spinner("Buscando..."):
                    try:
                        res_cnpj = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=10)
                        if res_cnpj.status_code == 200:
                            data = res_cnpj.json()
                            end_c = f"{data.get('logradouro', '')}, {data.get('numero', '')}".strip(", ")
                            st.session_state["cnpj_dados"] = {
                                "cnpj": input_cnpj_busca,
                                "fantasia": data.get("nome_fantasia") or data.get("razao_social"),
                                "razao": data.get("razao_social"),
                                "endereco": end_c, "bairro": data.get("bairro", ""),
                                "complemento": data.get("complemento", ""),
                                "cidade": data.get("municipio"), "estado": data.get("uf")
                            }
                            st.success("Dados encontrados!")
                    except: st.error("Erro na busca do CNPJ.")
            else: st.warning("Digite 14 números válidos.")

        st.markdown("---")
        d_cnpj = st.session_state["cnpj_dados"]
        
        # CAMPOS FORA DO st.form PARA ATUALIZAR O PREÇO EM TEMPO REAL
        st.markdown("#### Identificação do Cliente")
        nome_fantasia = st.text_input("Nome Fantasia *", value=d_cnpj.get("fantasia", ""), key="cad_nf")
        col_id1, col_id2 = st.columns(2)
        nome_empresarial = col_id1.text_input("Razão Social", value=d_cnpj.get("razao", ""), key="cad_rz")
        cnpj = col_id2.text_input("CNPJ", value=d_cnpj.get("cnpj", input_cnpj_busca), key="cad_cnpj")
        
        st.markdown("#### Endereço")
        endereco = st.text_input("Logradouro e Número", value=d_cnpj.get("endereco", ""), key="cad_end")
        col_end1, col_end2, col_end3, col_end4 = st.columns(4)
        bairro = col_end1.text_input("Bairro", value=d_cnpj.get("bairro", ""), key="cad_br")
        complemento = col_end2.text_input("Complemento", value=d_cnpj.get("complemento", ""), key="cad_comp")
        cidade = col_end3.text_input("Cidade", value=d_cnpj.get("cidade", ""), key="cad_cid")
        estado = col_end4.text_input("Estado (UF)", value=d_cnpj.get("estado", ""), key="cad_est")
        
        st.markdown("#### Configuração e Valores")
        col_s1, col_s2 = st.columns(2)
        tipo_sistema = col_s1.selectbox("Tipo de Sistema *", ["XDRest", "XDCoffee", "XDDisco"], key="cad_sis")
        num_lic_input = col_s2.text_input("Nº Licença (Ex: 100355) *", key="cad_num")
        
        col_r, col_o, col_ot = st.columns([1, 1, 1.5])
        xd_rest = col_r.number_input("Postos XDRest", min_value=0, value=1, key="cad_rest")
        xd_orders = col_o.number_input("Qtd. XDOrders", min_value=0, value=0, key="cad_ord")
        tipo_xdorders = col_ot.selectbox("Tipo XDOrders", ["Comum (R$ 8/cada)", "Esfiharia (R$ 6/cada)"], key="cad_tipo_ord")
        
        # CÁLCULO DINÂMICO EM TEMPO REAL
        preco_unit = 6 if "Esfiharia" in tipo_xdorders else 8
        total_calc = xd_orders * preco_unit
        st.info(f"💰 **Valor Total que compõe a Licença (XDOrders): R$ {total_calc},00**")
        
        token_gerado = str(uuid.uuid4()).split('-')[0].upper()
        st.markdown(f"**Token de Vínculo:** `{token_gerado}`")
        
        st.markdown('<span class="btn-salvar"></span>', unsafe_allow_html=True)
        if st.button("Emitir e Salvar Licença", use_container_width=True):
            if not nome_fantasia or not num_lic_input: st.error("Nome Fantasia e Nº Licença são obrigatórios!")
            else:
                num_formatado = re.sub(r'\D', '', num_lic_input).zfill(6)
                end_completo = f"{endereco} - {bairro}".strip(" - ") + (f" ({complemento})" if complemento else "")
                dados = {
                    "token_vinculo": token_gerado, "numero_licenca": f"XDBR.{num_formatado}",
                    "tipo_sistema": tipo_sistema, "nome_fantasia": nome_fantasia,
                    "nome_empresarial": nome_empresarial, "cnpj": cnpj, "estado": estado,
                    "cidade": cidade, "endereco": end_completo, "xd_rest_postos": int(xd_rest),
                    "xd_orders_postos": int(xd_orders), "tipo_xdorders": "Esfiharia" if "Esfiharia" in tipo_xdorders else "Comum",
                    "bloqueado": False
                }
                res = requests.post(f"{URL_SUPABASE}/licencas", json=dados, headers=HEADERS)
                if res.status_code in [200, 201]:
                    st.session_state["cnpj_dados"] = {}
                    st.success("Licença salva com sucesso!")
                    st.rerun()

    # ABA 1: GERENCIAMENTO
    with tab1:
        res = requests.get(f"{URL_SUPABASE}/licencas?select=*&order=nome_fantasia.asc", headers=HEADERS)
        if res.status_code == 200:
            licencas = res.json()
            if licencas:
                busca = st.text_input("Procurar Cliente, CNPJ, Token ou Licença:", placeholder="Digite para pesquisar...")
                
                col_t1, col_t2, col_t3, col_t4, col_t5, col_t6, col_t7 = st.columns([1.2, 2.2, 1.8, 1.3, 1.1, 1.3, 1.5])
                col_t1.markdown("**Nº Licença**")
                col_t2.markdown("**Cliente / Razão**")
                col_t3.markdown("**CNPJ / Token**") 
                col_t4.markdown("**Sistema**")
                col_t5.markdown("**Status**")
                col_t6.markdown("**Ação**")
                col_t7.markdown("**Opções**")
                st.markdown("<hr style='margin: 5px 0px; border-color: #DEE2E6;'>", unsafe_allow_html=True)

                for lic in licencas:
                    lic_id = lic.get('id')
                    num_lic = lic.get('numero_licenca', 'XDBR.------')
                    if num_lic == 'None': num_lic = "XDBR.------"
                    
                    if busca.lower() not in str(lic).lower(): continue

                    is_bloqueado = lic.get('bloqueado', False)
                    
                    with st.container():
                        st.markdown('<span class="row-hook"></span>', unsafe_allow_html=True)
                        c1, c2, c3, c4, c5, c6, c7 = st.columns([1.2, 2.2, 1.8, 1.3, 1.1, 1.3, 1.5])
                        
                        c1.markdown(f"<strong style='color: #D97706;'>{num_lic}</strong>", unsafe_allow_html=True)
                        c2.markdown(f"**{lic.get('nome_fantasia')}**<br><small style='color: #495057;'>{lic.get('nome_empresarial', '-')}</small>", unsafe_allow_html=True)
                        
                        # CNPJ EM CIMA (Preto), TOKEN EMBAIXO (Apagadinho)
                        c3.markdown(f"<strong style='color: #000000;'>CNPJ: {lic.get('cnpj', '-')}</strong><br><small style='color: #ADB5BD; font-family: monospace;'>Token: {lic.get('token_vinculo')}</small>", unsafe_allow_html=True)
                        
                        c4.markdown(f"**{lic.get('tipo_sistema', 'XDRest')}**<br><small style='color: #495057;'>Rest: {lic.get('xd_rest_postos')} | Ord: {lic.get('xd_orders_postos')}</small>", unsafe_allow_html=True)
                        
                        # STATUS CORES FORTES E PURAS
                        if is_bloqueado:
                            c5.markdown('<div style="background-color: #FF0000; color: #FFFFFF; font-weight: 900; padding: 6px 10px; border-radius: 20px; font-size: 11px; text-align: center;">BLOQUEADO</div>', unsafe_allow_html=True)
                        else:
                            c5.markdown('<div style="background-color: #00C851; color: #FFFFFF; font-weight: 900; padding: 6px 10px; border-radius: 20px; font-size: 11px; text-align: center;">ATIVO</div>', unsafe_allow_html=True)
                            
                        if c6.button("LIBERAR" if is_bloqueado else "BLOQUEAR", key=f"btn_bloqueio_{lic_id}"):
                            requests.patch(f"{URL_SUPABASE}/licencas?id=eq.{lic_id}", json={"bloqueado": not is_bloqueado}, headers=HEADERS)
                            st.rerun()
                        
                        col_i, col_e, col_d = c7.columns(3)
                        if col_i.button("i", key=f"btn_info_{lic_id}"):
                            st.session_state["acao_painel"] = ("info", lic_id)
                            st.rerun()
                        if col_e.button("✏️", key=f"btn_edit_{lic_id}"):
                            st.session_state["acao_painel"] = ("edit", lic_id)
                            st.rerun()
                        if col_d.button("X", key=f"btn_exc_{lic_id}"):
                            st.session_state["acao_painel"] = ("del", lic_id)
                            st.rerun()

                        acao = st.session_state.get("acao_painel", (None, None))
                        
                        # INFORMAÇÕES TOTALMENTE PRETAS
                        if acao == ("info", lic_id):
                            st.markdown(f"""
                            <div style="background-color: #F8F9FA; padding: 20px; border-radius: 8px; border: 1px solid #CED4DA; margin: 10px 0;">
                                <h4 style="color: #000000; margin-top: 0;">Informações de {lic.get('nome_fantasia')}</h4>
                                <ul style="color: #000000; line-height: 1.8; font-weight: 500;">
                                    <li><b>Nº Licença:</b> {num_lic}</li>
                                    <li><b>Sistema:</b> {lic.get('tipo_sistema', 'XDRest')}</li>
                                    <li><b>CNPJ:</b> {lic.get('cnpj', '-')}</li>
                                    <li><b>Endereço:</b> {lic.get('endereco', '-')}</li>
                                    <li><b>Postos:</b> XDRest ({lic.get('xd_rest_postos')}) | XDOrders ({lic.get('xd_orders_postos')})</li>
                                    <li><b>Tipo XDOrders:</b> {lic.get('tipo_xdorders', 'Comum')}</li>
                                    <li><b>Token do PC:</b> {lic.get('token_vinculo')}</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)

                        # EDIÇÃO
                        if acao == ("edit", lic_id):
                            with st.form(key=f"form_edit_{lic_id}"):
                                st.write(f"**Editando Licença:** {num_lic}")
                                e_nome = st.text_input("Nome Fantasia", value=lic.get('nome_fantasia'))
                                e_rest = st.number_input("XDRest", value=int(lic.get('xd_rest_postos', 1)))
                                e_ord = st.number_input("XDOrders", value=int(lic.get('xd_orders_postos', 0)))
                                
                                c_ok, c_cc = st.columns(2)
                                if c_ok.form_submit_button("💾 Salvar Alterações"):
                                    up_data = {"nome_fantasia": e_nome, "xd_rest_postos": e_rest, "xd_orders_postos": e_ord}
                                    requests.patch(f"{URL_SUPABASE}/licencas?id=eq.{lic_id}", json=up_data, headers=HEADERS)
                                    st.session_state["acao_painel"] = (None, None)
                                    st.rerun()
                                if c_cc.form_submit_button("Cancelar"):
                                    st.session_state["acao_painel"] = (None, None)
                                    st.rerun()

                        # EXCLUSÃO
                        if acao == ("del", lic_id):
                            with st.form(key=f"form_del_{lic_id}"):
                                st.warning(f"Excluir definitivamente a licença de {lic.get('nome_fantasia')}?")
                                pwd = st.text_input("Senha Admin:", type="password")
                                c_ok, c_cc = st.columns(2)
                                if c_ok.form_submit_button("Confirmar Exclusão"):
                                    if pwd == SENHA_EXCLUSAO:
                                        requests.delete(f"{URL_SUPABASE}/licencas?id=eq.{lic_id}", headers=HEADERS)
                                        st.session_state["acao_painel"] = (None, None)
                                        st.rerun()
                                    else: st.error("Senha Incorreta!")
                                if c_cc.form_submit_button("Cancelar"):
                                    st.session_state["acao_painel"] = (None, None)
                                    st.rerun()

                        st.markdown("<hr style='margin: 0; border-color: #E9ECEF;'>", unsafe_allow_html=True)
