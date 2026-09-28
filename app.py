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

st.set_page_config(page_title="INSIDE AUTOMAÇÃO - Licenças", layout="wide")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

fundo_b64 = get_base64_image("fundo.png") or get_base64_image("fundo.jpg") or get_base64_image("FUNDO ESCURO.png")

bg_css = f"""
    background-image: url("data:image/png;base64,{fundo_b64}");
    background-size: cover; background-position: center; background-attachment: fixed;
""" if fundo_b64 else "background-color: #0E0F12;"

# ESTILOS CSS FORÇADOS E LIMPOS
st.markdown(f"""
<style>
    .stApp {{ {bg_css} }}
    .logo-header {{ display: flex; justify-content: center; width: 100%; margin: 15px 0 10px 0; }}
    
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div {{
        background-color: #FFFFFF !important; border-radius: 8px !important; padding: 30px !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.6) !important; margin-bottom: 30px !important;
    }}

    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div p:not(button p),
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div span:not(button span),
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div label,
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div h1,
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div h2,
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div h3,
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.box-branco) + div h4 {{
        color: #000000 !important;
    }}

    .inner-title {{ font-size: 30px !important; font-weight: 800 !important; border-bottom: 2px solid #DEE2E6; padding-bottom: 10px; margin-bottom: 15px; }}

    div[data-baseweb="input"] > div, input, select {{
        background-color: #F1F3F5 !important; color: #000000 !important;
        border: 1px solid #CED4DA !important; border-radius: 6px !important; font-weight: 600 !important;
    }}

    div[data-baseweb="select"] > div > div:nth-child(2),
    div[data-baseweb="base-input"] button {{
        background-color: #1A1D20 !important;
    }}
    div[data-baseweb="select"] svg,
    div[data-baseweb="base-input"] svg,
    button[aria-label="Step up"] svg,
    button[aria-label="Step down"] svg {{
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }}

    div[data-testid="stVerticalBlock"]:has(> div.element-container span.row-hook) {{
        padding: 5px 10px; border-radius: 12px; transition: all 0.3s ease; border: 1px solid transparent;
    }}
    div[data-testid="stVerticalBlock"]:has(> div.element-container span.row-hook):hover {{
        background-color: #F8F9FA !important; transform: scale(1.01); box-shadow: 0px 8px 20px rgba(0,0,0,0.15); border: 1px solid #DEE2E6; z-index: 10;
    }}

    div.stButton > button {{
        background-color: #1A1D20 !important; border: 1px solid #343A40 !important; border-radius: 6px !important; padding: 8px !important;
    }}
    div.stButton > button p, div.stButton > button span {{
        color: #FFFFFF !important; font-weight: 800 !important; font-size: 15px !important;
    }}
    div.stButton > button:hover {{
        background-color: #343A40 !important;
    }}
    
    div.element-container:has(.btn-ativo-hook) + div button {{ background-color: #00C851 !important; border-radius: 20px !important; border: none !important; width: 100% !important; padding: 6px 0 !important; }}
    div.element-container:has(.btn-ativo-hook) + div button p {{ color: #FFFFFF !important; font-weight: 900 !important; font-size: 13px !important; text-align: center !important; }}
    
    div.element-container:has(.btn-bloq-hook) + div button {{ background-color: #FF0000 !important; border-radius: 20px !important; border: none !important; width: 100% !important; padding: 6px 0 !important; }}
    div.element-container:has(.btn-bloq-hook) + div button p {{ color: #FFFFFF !important; font-weight: 900 !important; font-size: 13px !important; text-align: center !important; }}

    div.element-container:has(.btn-info-hook) + div button {{ background-color: #0D6EFD !important; border-radius: 6px !important; border: none !important; }}
    div.element-container:has(.btn-info-hook) + div button p {{ color: #FFFFFF !important; font-weight: 900 !important; font-size: 16px !important; }}
    
    div.element-container:has(.btn-edit-hook) + div button {{ background-color: #D97706 !important; border-radius: 6px !important; border: none !important; }}
    div.element-container:has(.btn-edit-hook) + div button p {{ color: #FFFFFF !important; font-weight: 900 !important; font-size: 16px !important; }}
    
    div.element-container:has(.btn-exc-hook) + div button {{ background-color: #DC3545 !important; border-radius: 6px !important; border: none !important; }}
    div.element-container:has(.btn-exc-hook) + div button p {{ color: #FFFFFF !important; font-weight: 900 !important; font-size: 16px !important; }}

    .stTabs [data-baseweb="tab-list"] {{ border-bottom: 2px solid #DEE2E6; }}
    .stTabs [data-baseweb="tab"] {{ background-color: #E9ECEF !important; border-radius: 6px 6px 0 0 !important; }}
    .stTabs [aria-selected="true"] {{ background-color: #FF8C00 !important; }}
    .stTabs [aria-selected="true"] p {{ color: #FFFFFF !important; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo-header">', unsafe_allow_html=True)
col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
with col_l2:
    if os.path.exists("logo.jpg"): st.image("logo.jpg", use_container_width=True)
    elif os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    else: st.markdown("<h1 style='text-align: center; color: #FF8C00;'>INSIDE AUTOMAÇÃO</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="box-branco"></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="inner-title">Licenças</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Licenças Cadastradas", "+ Cadastrar Nova Licença"])

    # === ABA DE CADASTRO ===
    with tab2:
        chaves_cadastro = ["cad_nf", "cad_rz", "cad_cnpj", "cad_end", "cad_br", "cad_comp", "cad_cid", "cad_est"]
        for chave in chaves_cadastro:
            if chave not in st.session_state:
                st.session_state[chave] = ""

        col_cnpj1, col_cnpj2 = st.columns([3, 1])
        input_cnpj_busca = col_cnpj1.text_input("CNPJ para busca automática:", placeholder="Digite o CNPJ...", key="busca_cnpj")
        
        if col_cnpj2.button("Buscar CNPJ", use_container_width=True):
            cnpj_limpo = re.sub(r'\D', '', input_cnpj_busca)
            if len(cnpj_limpo) == 14:
                with st.spinner("Buscando..."):
                    try:
                        res_cnpj = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=10)
                        if res_cnpj.status_code == 200:
                            data = res_cnpj.json()
                            end_c = f"{data.get('logradouro', '')}, {data.get('numero', '')}".strip(", ")
                            
                            st.session_state["cad_nf"] = data.get("nome_fantasia") or data.get("razao_social", "")
                            st.session_state["cad_rz"] = data.get("razao_social", "")
                            st.session_state["cad_cnpj"] = input_cnpj_busca
                            st.session_state["cad_end"] = end_c
                            st.session_state["cad_br"] = data.get("bairro", "")
                            st.session_state["cad_comp"] = data.get("complemento", "")
                            st.session_state["cad_cid"] = data.get("municipio", "")
                            st.session_state["cad_est"] = data.get("uf", "")
                            
                            st.success("Dados encontrados e preenchidos automaticamente!")
                        else:
                            st.error("CNPJ não encontrado.")
                    except: 
                        st.error("Erro na busca do CNPJ.")
            else: 
                st.warning("Digite 14 números válidos.")

        st.markdown("---")
        
        st.markdown("#### Identificação do Cliente")
        nome_fantasia = st.text_input("Nome Fantasia *", key="cad_nf")
        col_id1, col_id2 = st.columns(2)
        nome_empresarial = col_id1.text_input("Razão Social", key="cad_rz")
        cnpj = col_id2.text_input("CNPJ", key="cad_cnpj")
        
        st.markdown("#### Endereço")
        endereco = st.text_input("Logradouro e Número", key="cad_end")
        col_end1, col_end2, col_end3, col_end4 = st.columns(4)
        bairro = col_end1.text_input("Bairro", key="cad_br")
        complemento = col_end2.text_input("Complemento", key="cad_comp")
        cidade = col_end3.text_input("Cidade", key="cad_cid")
        estado = col_end4.text_input("Estado (UF)", key="cad_est")
        
        st.markdown("#### Configuração e Valores da Licença")
        col_s1, col_s2 = st.columns(2)
        tipo_sistema = col_s1.selectbox("Tipo de Sistema *", ["XDRest", "XDCoffee", "XDDisco"], key="cad_sis")
        num_lic_input = col_s2.text_input("Nº Licença (Até 6 números) *", placeholder="Ex: 100355", key="cad_num")
        
        col_r, col_o, col_ot = st.columns([1, 1, 1.5])
        xd_rest = col_r.number_input("Postos Extra", min_value=0, value=1, key="cad_rest")
        xd_orders = col_o.number_input("Qtd. XDOrders", min_value=0, value=0, key="cad_ord")
        tipo_xdorders = col_ot.selectbox("Tipo XDOrders", ["Comum (R$ 8/cada)", "Esfiharia (R$ 6/cada)"], key="cad_tipo_ord")

        st.markdown("#### Ajustes de Faturamento")
        col_desc, col_acres = st.columns(2)
        cad_desconto = col_desc.number_input("Desconto (R$)", min_value=0.0, value=0.0, format="%.2f", key="cad_desc")
        cad_acrescimo = col_acres.number_input("Acréscimo (R$)", min_value=0.0, value=0.0, format="%.2f", key="cad_acresc")
        
        # CÁLCULO DE VALORES
        v_postos = 280.0 + (max(0, int(xd_rest) - 1) * 60.0)
        v_orders = int(xd_orders) * (6.0 if "Esfiharia" in tipo_xdorders else 8.0)
        subtotal = v_postos + v_orders
        total_calc = subtotal + cad_acrescimo - cad_desconto
        
        html_cadastro = f"""<div style="background-color: #E9ECEF; color: #000000; padding: 15px; border-radius: 6px; border: 1px solid #CED4DA;">
<h5 style="margin-top: 0; color: #343A40;">Detalhamento da Licença</h5>
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span>Postos Extra ({int(xd_rest)}):</span> <span>R$ {f'{v_postos:.2f}'.replace('.', ',')}</span>
</div>
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span>XDOrders ({int(xd_orders)}):</span> <span>R$ {f'{v_orders:.2f}'.replace('.', ',')}</span>
</div>
<div style="display: flex; justify-content: space-between; margin-bottom: 4px; border-top: 1px solid #CED4DA; padding-top: 4px; font-weight: bold;">
<span>Subtotal:</span> <span>R$ {f'{subtotal:.2f}'.replace('.', ',')}</span>
</div>
<div style="display: flex; justify-content: space-between; margin-bottom: 4px; color: #DC3545;">
<span>Desconto:</span> <span>- R$ {f'{cad_desconto:.2f}'.replace('.', ',')}</span>
</div>
<div style="display: flex; justify-content: space-between; margin-bottom: 4px; color: #198754;">
<span>Acréscimo:</span> <span>+ R$ {f'{cad_acrescimo:.2f}'.replace('.', ',')}</span>
</div>
<div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: 900; margin-top: 10px; border-top: 2px solid #ADB5BD; padding-top: 8px;">
<span>TOTAL A FATURAR:</span> <span>R$ {f'{total_calc:.2f}'.replace('.', ',')}</span>
</div>
</div>
<br>"""
        st.markdown(html_cadastro, unsafe_allow_html=True)
        
        token_gerado = str(uuid.uuid4()).split('-')[0].upper()
        st.markdown(f"**Token de Vínculo:** `{token_gerado}`", unsafe_allow_html=True)
        
        if st.button("Emitir e Salvar Licença", use_container_width=True):
            if not nome_fantasia or not num_lic_input: 
                st.error("Nome Fantasia e Nº Licença são obrigatórios!")
            else:
                num_formatado = re.sub(r'\D', '', num_lic_input).zfill(6)
                end_completo = f"{endereco} - {bairro}".strip(" - ") + (f" ({complemento})" if complemento else "")
                dados = {
                    "token_vinculo": token_gerado, "numero_licenca": f"XDBR.{num_formatado}",
                    "tipo_sistema": tipo_sistema, "nome_fantasia": nome_fantasia, "nome_empresarial": nome_empresarial,
                    "cnpj": cnpj, "estado": estado, "cidade": cidade, "endereco": end_completo,
                    "xd_rest_postos": int(xd_rest), "xd_orders_postos": int(xd_orders),
                    "tipo_xdorders": "Esfiharia" if "Esfiharia" in tipo_xdorders else "Comum",
                    "desconto": float(cad_desconto), "acrescimo": float(cad_acrescimo),
                    "bloqueado": False
                }
                res = requests.post(f"{URL_SUPABASE}/licencas", json=dados, headers=HEADERS)
                if res.status_code in [200, 201]:
                    chaves_para_limpar = ["cad_nf", "cad_rz", "cad_cnpj", "cad_end", "cad_br", "cad_comp", "cad_cid", "cad_est", "cad_num", "busca_cnpj", "cad_desc", "cad_acresc"]
                    for chave in chaves_para_limpar:
                        if chave in st.session_state:
                            del st.session_state[chave]
                    
                    if "cad_rest" in st.session_state: del st.session_state["cad_rest"]
                    if "cad_ord" in st.session_state: del st.session_state["cad_ord"]
                    
                    st.success("Licença salva com sucesso!")
                    st.rerun()

    # === ABA DE GERENCIAMENTO ===
    with tab1:
        res = requests.get(f"{URL_SUPABASE}/licencas?select=*&order=nome_fantasia.asc", headers=HEADERS)
        if res.status_code == 200:
            licencas = res.json()
            if licencas:
                busca = st.text_input("Procurar Cliente, CNPJ, Token ou Licença:", placeholder="Digite para pesquisar...")
                
                col_t1, col_t2, col_t3, col_t4, col_t5, col_t6 = st.columns([1.5, 2.5, 2, 1.5, 1.5, 1.5])
                col_t1.markdown("**Nº Licença**")
                col_t2.markdown("**Cliente / Razão**")
                col_t3.markdown("**CNPJ / Token**") 
                col_t4.markdown("**Sistema**")
                col_t5.markdown("<div style='text-align: center;'>**Status**</div>", unsafe_allow_html=True)
                col_t6.markdown("<div style='text-align: center;'>**Opções**</div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 5px 0px; border-color: #DEE2E6;'>", unsafe_allow_html=True)

                if "acao_painel" not in st.session_state: st.session_state["acao_painel"] = {}

                for lic in licencas:
                    lic_id = lic.get('id')
                    num_lic_raw = lic.get('numero_licenca')
                    num_lic = str(num_lic_raw) if num_lic_raw and str(num_lic_raw) != "None" else "XDBR.------"
                    
                    if busca.lower() not in str(lic).lower(): continue

                    is_bloqueado = lic.get('bloqueado', False)
                    
                    with st.container():
                        st.markdown('<span class="row-hook"></span>', unsafe_allow_html=True)
                        c1, c2, c3, c4, c5, c6 = st.columns([1.5, 2.5, 2, 1.5, 1.5, 1.5])
                        
                        c1.markdown(f"<strong style='color: #D97706;'>{num_lic}</strong>", unsafe_allow_html=True)
                        c2.markdown(f"**{lic.get('nome_fantasia')}**<br><small style='color: #495057;'>{lic.get('nome_empresarial', '-')}</small>", unsafe_allow_html=True)
                        c3.markdown(f"<strong style='color: #000000;'>CNPJ: {lic.get('cnpj', '-')}</strong><br><small style='color: #868E96;'>Token: <code>{lic.get('token_vinculo')}</code></small>", unsafe_allow_html=True)
                        c4.markdown(f"**{lic.get('tipo_sistema', 'XDRest')}**<br><small style='color: #495057;'>Extra: {lic.get('xd_rest_postos')} | Ord: {lic.get('xd_orders_postos')}</small>", unsafe_allow_html=True)
                        
                        if is_bloqueado:
                            c5.markdown('<span class="btn-bloq-hook"></span>', unsafe_allow_html=True)
                            if c5.button("BLOQUEADO", key=f"btn_status_{lic_id}"):
                                requests.patch(f"{URL_SUPABASE}/licencas?id=eq.{lic_id}", json={"bloqueado": False}, headers=HEADERS)
                                st.rerun()
                        else:
                            c5.markdown('<span class="btn-ativo-hook"></span>', unsafe_allow_html=True)
                            if c5.button("ATIVO", key=f"btn_status_{lic_id}"):
                                requests.patch(f"{URL_SUPABASE}/licencas?id=eq.{lic_id}", json={"bloqueado": True}, headers=HEADERS)
                                st.rerun()
                        
                        col_i, col_e, col_d = c6.columns(3)
                        col_i.markdown('<span class="btn-info-hook"></span>', unsafe_allow_html=True)
                        if col_i.button("i", key=f"btn_info_{lic_id}"): 
                            st.session_state["acao_painel"][lic_id] = "info" if st.session_state["acao_painel"].get(lic_id) != "info" else None
                            st.rerun()
                            
                        col_e.markdown('<span class="btn-edit-hook"></span>', unsafe_allow_html=True)
                        if col_e.button("✎", key=f"btn_edit_{lic_id}"): 
                            st.session_state["acao_painel"][lic_id] = "edit" if st.session_state["acao_painel"].get(lic_id) != "edit" else None
                            st.rerun()
                            
                        col_d.markdown('<span class="btn-exc-hook"></span>', unsafe_allow_html=True)
                        if col_d.button("X", key=f"btn_exc_{lic_id}"): 
                            st.session_state["acao_painel"][lic_id] = "del" if st.session_state["acao_painel"].get(lic_id) != "del" else None
                            st.rerun()

                        acao = st.session_state["acao_painel"].get(lic_id)
                        
                        if acao == "info":
                            qtd_extra = int(lic.get('xd_rest_postos', 1))
                            qtd_ord = int(lic.get('xd_orders_postos', 0))
                            tipo_ord = lic.get('tipo_xdorders', 'Comum')
                            desc = float(lic.get('desconto') or 0.0)
                            acresc = float(lic.get('acrescimo') or 0.0)
                            
                            v_postos_info = 280.0 + (max(0, qtd_extra - 1) * 60.0)
                            v_orders_info = qtd_ord * (6.0 if "Esfiharia" in tipo_ord else 8.0)
                            subtotal_info = v_postos_info + v_orders_info
                            total_info = subtotal_info + acresc - desc

                            html_info = f"""<div style="background-color: #F8F9FA; padding: 20px; border-radius: 8px; border: 1px solid #CED4DA; margin: 10px 0;">
<h4 style="color: #000; margin-top: 0; margin-bottom: 15px;">Informações de {lic.get('nome_fantasia')}</h4>
<div style="display: flex; gap: 20px; flex-wrap: wrap;">
<div style="flex: 1; min-width: 300px;">
<ul style="color: #000; line-height: 1.8; font-weight: 500; list-style-type: none; padding-left: 0;">
<li><b>Nº Licença:</b> {num_lic}</li>
<li><b>Sistema:</b> {lic.get('tipo_sistema', 'XDRest')}</li>
<li><b>CNPJ:</b> {lic.get('cnpj', '-')}</li>
<li><b>Endereço:</b> {lic.get('endereco', '-')}</li>
<li><b>Cidade/UF:</b> {lic.get('cidade', '-')} - {lic.get('estado', '-')}</li>
<li><b>Postos:</b> Postos Extra ({qtd_extra}) | XDOrders ({qtd_ord})</li>
<li><b>Tipo XDOrders:</b> {tipo_ord}</li>
<li><b>Token do PC:</b> <code>{lic.get('token_vinculo')}</code></li>
</ul>
</div>
<div style="flex: 1; min-width: 280px; background-color: #E9ECEF; padding: 15px; border-radius: 6px; border: 1px solid #DEE2E6; color: #000;">
<h5 style="margin-top: 0; border-bottom: 1px solid #CED4DA; padding-bottom: 5px;">Detalhamento Financeiro</h5>
<div style="display: flex; justify-content: space-between;"><span>Postos Extra ({qtd_extra} un.):</span> <span>R$ {f'{v_postos_info:.2f}'.replace('.', ',')}</span></div>
<div style="display: flex; justify-content: space-between;"><span>XDOrders ({qtd_ord} un.):</span> <span>R$ {f'{v_orders_info:.2f}'.replace('.', ',')}</span></div>
<div style="display: flex; justify-content: space-between; font-weight: bold; margin-top: 5px;"><span>Subtotal:</span> <span>R$ {f'{subtotal_info:.2f}'.replace('.', ',')}</span></div>
<div style="display: flex; justify-content: space-between; color: #DC3545;"><span>Desconto:</span> <span>- R$ {f'{desc:.2f}'.replace('.', ',')}</span></div>
<div style="display: flex; justify-content: space-between; color: #198754;"><span>Acréscimo:</span> <span>+ R$ {f'{acresc:.2f}'.replace('.', ',')}</span></div>
<div style="display: flex; justify-content: space-between; font-size: 16px; font-weight: 900; margin-top: 10px; border-top: 2px solid #ADB5BD; padding-top: 5px;"><span>Total da Licença:</span> <span>R$ {f'{total_info:.2f}'.replace('.', ',')}</span></div>
</div>
</div>
</div>"""
                            st.markdown(html_info, unsafe_allow_html=True)

                        if acao == "edit":
                            with st.form(key=f"form_edit_{lic_id}"):
                                st.markdown("#### Editando Informações da Licença")
                                col_e1, col_e2 = st.columns(2)
                                e_nome = col_e1.text_input("Nome Fantasia", value=lic.get('nome_fantasia'))
                                e_razao = col_e2.text_input("Razão Social", value=lic.get('nome_empresarial', ''))
                                
                                col_e3, col_e4 = st.columns([1, 2])
                                e_cnpj = col_e3.text_input("CNPJ", value=lic.get('cnpj', ''))
                                e_end = col_e4.text_input("Endereço Completo", value=lic.get('endereco', ''))
                                
                                col_e5, col_e6 = st.columns(2)
                                e_cid = col_e5.text_input("Cidade", value=lic.get('cidade', ''))
                                e_est = col_e6.text_input("Estado (UF)", value=lic.get('estado', ''))

                                col_e7, col_e8, col_e9 = st.columns(3)
                                sys_opts = ["XDRest", "XDCoffee", "XDDisco"]
                                cur_sys = lic.get('tipo_sistema', 'XDRest')
                                e_sys = col_e7.selectbox("Sistema", sys_opts, index=sys_opts.index(cur_sys) if cur_sys in sys_opts else 0)
                                
                                ord_opts = ["Comum (R$ 8/cada)", "Esfiharia (R$ 6/cada)"]
                                cur_ord = "Esfiharia (R$ 6/cada)" if "Esfiharia" in lic.get('tipo_xdorders', '') else "Comum (R$ 8/cada)"
                                e_tord = col_e8.selectbox("Tipo XDOrders", ord_opts, index=ord_opts.index(cur_ord))
                                
                                num_only = num_lic.replace("XDBR.", "") if num_lic and "XDBR." in num_lic else ""
                                e_nlic = col_e9.text_input("Nº Licença", value=num_only)

                                col_r, col_o = st.columns(2)
                                e_rest = col_r.number_input("Postos Extra", value=int(lic.get('xd_rest_postos', 1)))
                                e_ord = col_o.number_input("Postos XDOrders", value=int(lic.get('xd_orders_postos', 0)))

                                st.markdown("#### Ajustes de Faturamento")
                                col_ed, col_ea = st.columns(2)
                                e_desc = col_ed.number_input("Desconto (R$)", value=float(lic.get('desconto') or 0.0), format="%.2f")
                                e_acresc = col_ea.number_input("Acréscimo (R$)", value=float(lic.get('acrescimo') or 0.0), format="%.2f")
                                
                                c_ok, c_cc = st.columns(2)
                                
                                if c_ok.form_submit_button("Salvar Modificações", use_container_width=True):
                                    num_formatado = re.sub(r'\D', '', e_nlic).zfill(6)
                                    up_data = {
                                        "nome_fantasia": e_nome, "nome_empresarial": e_razao, "cnpj": e_cnpj, "endereco": e_end,
                                        "cidade": e_cid, "estado": e_est, "tipo_sistema": e_sys, "numero_licenca": f"XDBR.{num_formatado}",
                                        "xd_rest_postos": e_rest, "xd_orders_postos": e_ord, "tipo_xdorders": "Esfiharia" if "Esfiharia" in e_tord else "Comum",
                                        "desconto": e_desc, "acrescimo": e_acresc
                                    }
                                    requests.patch(f"{URL_SUPABASE}/licencas?id=eq.{lic_id}", json=up_data, headers=HEADERS)
                                    st.session_state["acao_painel"][lic_id] = None
                                    st.rerun()
                                    
                                if c_cc.form_submit_button("Cancelar", use_container_width=True):
                                    st.session_state["acao_painel"][lic_id] = None
                                    st.rerun()

                        if acao == "del":
                            with st.form(key=f"form_del_{lic_id}"):
                                st.warning(f"Excluir definitivamente a licença de {lic.get('nome_fantasia')}?")
                                pwd = st.text_input("Senha Admin:", type="password")
                                c_ok, c_cc = st.columns(2)
                                
                                if c_ok.form_submit_button("Confirmar Exclusão", use_container_width=True):
                                    if pwd == SENHA_EXCLUSAO:
                                        requests.delete(f"{URL_SUPABASE}/licencas?id=eq.{lic_id}", headers=HEADERS)
                                        st.session_state["acao_painel"][lic_id] = None
                                        st.rerun()
                                    else: st.error("Senha Incorreta!")
                                        
                                if c_cc.form_submit_button("Cancelar", use_container_width=True):
                                    st.session_state["acao_painel"][lic_id] = None
                                    st.rerun()

                        st.markdown("<hr style='margin: 0; border-color: #E9ECEF;'>", unsafe_allow_html=True)
            else: st.info("Nenhuma licença cadastrada.")
        else: st.error(f"Erro ao ligar ao banco de dados: {res.text}")
            
    st.markdown('</div>', unsafe_allow_html=True)
