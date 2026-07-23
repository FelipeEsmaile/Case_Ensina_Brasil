''' AQUI É O QUE SERÁ USADO PARA GERAR O DASHBOARD '''

import streamlit as st
import pandas as pd

# 1. Configuração inicial da página
st.set_page_config(page_title="Dashboard", layout="wide")

# Função para carregar os dados (com cache para o painel não ficar lento ao filtrar)
@st.cache_data
def carregar_dados():
    return pd.read_csv('Tratamento_dados/Base_Dashboard.csv')

df = carregar_dados()

# ==================================================================================================================================================================================================================
#                      B A R R A    L A T E R A L    -    F I L T R O S
# ==================================================================================================================================================================================================================
st.sidebar.title("Filtros do Painel")

# --- Filtros Primários (Sempre Visíveis) ---
st.sidebar.subheader("Filtros Principais")

# Filtro de Ano (Com opção 'Todas' para visão geral)
lista_turmas = ["Todas"] + df['Turma_Ensina'].unique().tolist()
turma_selecionada = st.sidebar.selectbox("Selecione a Turma (Ano):", options=lista_turmas)

# Filtro de Polo
lista_polos = df['Polo_Ensina'].unique().tolist()
polos_selecionados = st.sidebar.multiselect(
    "Selecione o Polo:", 
    options=lista_polos, 
    default=lista_polos
)

# --- Filtros Secundários (Ocultos no Expander) ---
with st.sidebar.expander("Filtros de Diversidade e Formação"):

    # Extrai as categorias únicas da base
    lista_racas = df['Raça_Ensina'].unique().tolist()
    lista_generos = df['Gênero_Ensina'].unique().tolist()
    lista_graus = df['Grau Acadêmico_Ensina'].unique().tolist()

    # Cria as pílulas interativas para Grau Acadêmico
    graus_selecionados = st.pills(
        "Selecione o Grau Acadêmico:",
        options=lista_graus,
        selection_mode="multi", 
        default=lista_graus     
    )
    
    # Cria as pílulas interativas para Raça
    racas_selecionadas = st.pills(
        "Selecione a Raça/Cor:",
        options=lista_racas,
        selection_mode="multi", 
        default=lista_racas     
    )

    # Cria as pílulas interativas para Gênero
    generos_selecionados = st.pills(
        "Selecione o Gênero:",
        options=lista_generos,
        selection_mode="multi", 
        default=lista_generos     
    )


# MOTOR DE FILTRAGEM (PANDAS)
# Fatiando a base original conforme as seleções do usuário
df_filtrado = df.copy()

# Aplica o filtro de Ano (somente se o usuário não escolheu "Todas")
if turma_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Turma_Ensina'] == turma_selecionada]

# Trava de segurança: só filtra se todos os componentes tiverem pelo menos uma opção selecionada
if not polos_selecionados or not generos_selecionados or not racas_selecionadas or not graus_selecionados:
    df_filtrado = df_filtrado.iloc[0:0] # Esvazia a base por segurança
    st.warning("⚠️ Selecione pelo menos uma opção em todos os filtros para visualizar os dados.")
else:
    # Aplica os filtros de Múltipla Escolha com segurança
    df_filtrado = df_filtrado[
        (df_filtrado['Polo_Ensina'].isin(polos_selecionados)) &
        (df_filtrado['Gênero_Ensina'].isin(generos_selecionados)) &
        (df_filtrado['Raça_Ensina'].isin(racas_selecionadas)) &
        (df_filtrado['Grau Acadêmico_Ensina'].isin(graus_selecionados))
    ]

# ========================================================================================================================================================================
#                                              T E L A      P R I N C I P A L
# ========================================================================================================================================================================
st.title("Panorama de Avaliações")

# Validador rápido para testar se os botões estão funcionando
st.markdown(f"**Analisando dados de {len(df_filtrado)} profissionais.**")

# Mostra uma prévia da tabela atualizada para você conferir na construção
st.dataframe(df_filtrado.head())