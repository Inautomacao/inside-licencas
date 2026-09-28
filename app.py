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
                            
                            # INJEÇÃO DIRETA NA MEMÓRIA DOS CAMPOS
                            st.session_state["cad_nf"] = data.get("nome_fantasia") or data.get("razao_social", "")
                            st.session_state["cad_rz"] = data.get("razao_social", "")
                            st.session_state["cad_cnpj"] = input_cnpj_busca
                            st.session_state["cad_end"] = end_c
                            st.session_state["cad_br"] = data.get("bairro", "")
                            st.session_state["cad_comp"] = data.get("complemento", "")
                            st.session_state["cad_cid"] = data.get("municipio", "")
                            st.session_state["cad_est"] = data.get("uf", "")
                            
                            st.success("Dados encontrados e preenchidos!")
                        else:
                            st.error("CNPJ não encontrado.")
                    except: 
                        st.error("Erro na busca do CNPJ.")
            else: 
                st.warning("Digite 14 números válidos.")
