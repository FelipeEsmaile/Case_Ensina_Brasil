
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap
 
# 1. Configuração inicial da página
st.set_page_config(page_title="PAINEIS", layout="wide")

# Função para carregar os dados (com cache para o painel não ficar lento ao filtrar)
@st.cache_data
def carregar_dados():
    return pd.read_csv('Tratamento_dados/Base_Dashboard.csv')

df = carregar_dados()

# ==================================================================================================================================================================================================================
#                      B A R R A    L A T E R A L    -    F I L T R O S
# ==================================================================================================================================================================================================================

# Isso é um pixel transparente gerado em código (nunca vai dar erro de carregamento)
img_transparente = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

# 1. Configura a logo
st.logo(
    image=img_transparente, 
    icon_image="Case_Ensina_Brasil/ensina-bra.png"
)

with st.sidebar:
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
        st.image("Case_Ensina_Brasil/ensina-bra.png", width=300)
    st.markdown("---")

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



# ========================================      C   A   R   D  S     ===============================================================================


# Código em CSS para reproduzir os cards com borda lateral verde, texto centralizado e bordas arredondadas
st.markdown("""
    <style>
    /* 1. Formata a caixa do Card (Fundo branco e borda grossa na esquerda) */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border-left: 7px solid #1c3a6b !important; /* MUDAR A COR */
        border-top: none !important;
        border-right: 100px !important;
        border-bottom: none !important;
        border-radius: 10px !important; 
        padding: 0px !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05); /* Leve sombra para destacar do fundo */
    }

    /* 2. Centraliza o Título, muda a cor e AUMENTA O ÍCONE */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] > div {
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    [data-testid="stMetricLabel"] p {
        display: flex !important;
        align-items: center !important; /* Garante que o ícone e o texto fiquem na mesma linha */
        justify-content: center !important;
        color: #0067AC !important; /*MUDAR A COR */
        font-weight: bold !important;
        margin: 0% !important;
        font-size: 14px !important; /* Tamanho da letra do título */
    }

    /* Alvo direto apenas no ícone do Google */
    [data-testid="stMetricLabel"] p span {
        font-size: 20px !important; /* <-- AUMENTE OU DIMINUA O ÍCONE AQUI */
        margin-right: 8px !important; /* Dá um espaço entre o ícone e a primeira letra */
    }

    /* 3. Centraliza o Valor e muda a cor para verde */
    [data-testid="stMetricValue"] > div {
        width: 100%;
        display: flex;
        justify-content: center;
        color: #0067AC !important; /*MUDAR A COR */
    }
    </style>
    """, unsafe_allow_html=True)

# Verifica se a base não está vazia após os filtros para não gerar erro de cálculo
if len(df_filtrado) > 0:
    
    # 1. Preparação das listas de colunas
    competencias = [
        "Adaptação e Inovação", 
        "Capacidade de Execução", 
        "Colaboração e Parceria", 
        "Comunicação Empática", 
        "Desenvolvimento Contínuo", 
        "Visão Estratégica"
    ]
    
    colunas_auto = [f"{comp}_Auto" for comp in competencias]
    colunas_terc = [f"{comp}_Terc" for comp in competencias]

    # 2. Cálculos dos KPIs Básicos
    qtd_profissionais = len(df_filtrado)
    media_global_auto = df_filtrado[colunas_auto].mean().mean()
    media_global_terc = df_filtrado[colunas_terc].mean().mean()
    
    # 3. Cálculos de Forças e Oportunidades
    medias_por_competencia = {}
    for comp in competencias:
        # Calcula a média combinada (Auto + Terc) para cada competência
        media_comp = (df_filtrado[f"{comp}_Auto"].mean() + df_filtrado[f"{comp}_Terc"].mean()) / 2
        medias_por_competencia[comp] = media_comp
    
    # Identifica o nome da competência com maior e menor nota
    destaque = max(medias_por_competencia, key=medias_por_competencia.get)
    oportunidade = min(medias_por_competencia, key=medias_por_competencia.get)
    
    nota_destaque = medias_por_competencia[destaque]
    nota_oportunidade = medias_por_competencia[oportunidade]

    # Colunas
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(label="Profissionais Analisados", value=qtd_profissionais)
        
    with col2:
        # :.2f formata o número para ter apenas 2 casas decimais
        st.metric(
            label="Autoavaliação Pontuação Média", 
            value=f"{media_global_auto:.2f}"
            )
        
    with col3:
        # O parâmetro 'delta' cria aquela setinha verde/vermelha mostrando a variação
        st.metric(
            label="Avaliação por Terceiros Pontuação Média", 
            value=f"{media_global_terc:.2f}"
        )
        
    with col4:
        st.metric(label=f"🌟 Destaque: {destaque}", value=f"{nota_destaque:.2f}")
        
    with col5:
        st.metric(label=f"🎯 Foco: {oportunidade}", value=f"{nota_oportunidade:.2f}")

else:
    # Mensagem de segurança caso os filtros deixem a base vazia
    st.warning("⚠️ Não há dados para exibir. Ajuste os filtros na barra lateral.")


# ========================================      G   R   Á   F   I   C   O   S     ===============================================================================

# --------------------------------------- Gráfico de Barras  ---------------------------------------
    
# 1. Gráfico de Barras Agrupadas: Comparativo Auto vs Terceiros
st.subheader("Análise de Competências: Autoavaliação vs. Terceiros")
    
# Calculando as médias usando as listas que já criamos nos Cards
medias_auto = [df_filtrado[col].mean() for col in colunas_auto]
medias_terc = [df_filtrado[col].mean() for col in colunas_terc]
    
# Montando a figura com Plotly
fig_barras = go.Figure()
    
# Adiciona as colunas da Autoavaliação
fig_barras.add_trace(go.Bar(
    x=competencias,
    y=medias_auto,
    name='Autoavaliação',
    marker_color='#F5C518', # Amerelo
    text=[f"{val:.2f}" for val in medias_auto], # Formata a nota com 2 casas decimais
    textposition='auto' # Coloca o número automaticamente dentro ou fora da barra
))
    
# Adiciona as colunas de Terceiros
fig_barras.add_trace(go.Bar(
    x=competencias,
    y=medias_terc,
    name='Avaliação Terceiros',
    marker_color='#3CAA4E', # Verde '#3CAA4E'
    text=[f"{val:.2f}" for val in medias_terc],
    textposition='auto',
))

fig_barras.update_traces(
    # Mantemos o nosso truque do <extra></extra> e a formatação com %{x} e %{y}
    hovertemplate="<b>Tipo:</b> %{data.name}<br>" +
                  "<b>Competência:</b> %{x}<br>" +
                  "<b>Pontuação Média:</b> %{y:.2f}<extra></extra>",
    
    # Sintaxe rigorosa do Plotly para a caixa
    hoverlabel=dict(
        bgcolor="#FAFAFA",      # Fundo off-white
        bordercolor="#1C3A6B",  # Borda Azul-marinho
        font=dict(              # A fonte OBRIGATORIAMENTE precisa ser um sub-dicionário
            size=13,
            color="#0067AC"     # Texto Cinza-chumbo
        )
    )
)

# Ajustes de layout para agrupar as barras e formatar o eixo
fig_barras.update_layout(
    barmode='group', # Garante que as colunas fiquem lado a lado (e não empilhadas)
    barcornerradius=10, # <--- Curvatura do gráfico
    xaxis_title="Competências",
    yaxis_title="Pontuação Média",
    xaxis= dict(showgrid=False,   # Remove a grade do fundo
                showline=False,   # Remove a linha principal do eixo X
                zeroline=False), # Remove a linhas que cortando o gráfico
    yaxis= dict(showgrid=False,   # Remove a grade do fundo
                showline=False,   # Remove a linha principal do eixo Y
                zeroline=False, range=[0, 1]), # <-- NOTA MÁXIMA 
    margin=dict(t=40, b=40, l=40, r=40),
    # Move a legenda para o topo para economizar espaço
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5
    )
)
    
# Exibe o gráfico no Streamlit
st.plotly_chart(fig_barras, use_container_width=True)






# ====================================================================================
    #           2. PADRÕES POR GRUPOS (MAPA DE CALOR) --
    # ====================================================================================

st.subheader("Padrões de Desempenho por Grupo")
    
    # IMPORTANTE: Aqui estamos usando 'Polo_Ensina', mas você pode criar um 
    # selectbox no Streamlit para o usuário escolher entre Polo, Raça ou Grau.
coluna_agrupamento = 'Polo_Ensina' 
    
# Calcula a média por grupo na visão de Terceiros
df_heatmap = df_filtrado.groupby(coluna_agrupamento)[colunas_terc].mean().round(3)
df_heatmap.columns = competencias # Limpa os nomes das colunas
    
fig_heat = go.Figure(data=go.Heatmap(
    z=df_heatmap.values,
    x=df_heatmap.columns,
    y=df_heatmap.index,
    colorscale=[[0.0, '#FFFFFF'], [0.5, '#F5C518'], [1.0, '#3CAA4E']],
    text=df_heatmap.values,
    texttemplate="%{text:.2f}",
    showscale=True
))

fig_heat.update_traces(
    # Mantemos o nosso truque do <extra></extra> e a formatação com %{x} e %{y}
    hovertemplate="<b>Competência:</b> %{x}<br>" +
                  "<b>Polo:</b> %{y}<br>" +
                  "<b>Pontuação Média:</b> %{z:.2f}<extra></extra>",
    
    # Sintaxe rigorosa do Plotly para a caixa
    hoverlabel=dict(
        bgcolor="#FAFAFA",      # Fundo off-white
        bordercolor="#1C3A6B",  # Borda Azul-marinho
        font=dict(              # A fonte OBRIGATORIAMENTE precisa ser um sub-dicionário
            size=13,
            color="#0067AC"     # Texto Cinza-chumbo
        )
    )
)
    
fig_heat.update_layout(
    yaxis_title="Grupos",
    margin=dict(t=20, b=20, l=20, r=20)
)
st.plotly_chart(fig_heat, use_container_width=True)




col_div, col_forcas = st.columns(2)

with col_div:
        # -------------------------------------------------------------------------
        # 3. DIVERGÊNCIAS (GRÁFICO DE GAP)
        # -------------------------------------------------------------------------
    st.subheader("Divergências de Perspectiva")
        
        # Calcula a diferença: Terceiros - Auto
    gaps = [t - a for t, a in zip(medias_terc, medias_auto)]
        
        # Cores: Verde se Terceiros > Auto, Vermelho se Terceiros < Auto
    cores_gap = ['#3CAA4E' if val >= 0 else '#F5C518' for val in gaps]
        
    fig_tornado = go.Figure()
    fig_tornado.add_trace(go.Bar(
        x=gaps, 
        y=competencias,
        orientation='h',
        marker_color=cores_gap,
        text=[f"{val:+.2f}" for val in gaps],
        textposition='auto'
    ))

    fig_tornado.update_traces(
    # Mantemos o nosso truque do <extra></extra> e a formatação com %{x} e %{y}
    hovertemplate="<b>%{y}</b> <br>" +
                  "<b>Gap:</b> %{x:.2f}<extra></extra>",
    
    # Sintaxe rigorosa do Plotly para a caixa
    hoverlabel=dict(
        bgcolor="#FAFAFA",      # Fundo off-white
        bordercolor="#1C3A6B",  # Borda Azul-marinho
        font=dict(              # A fonte OBRIGATORIAMENTE precisa ser um sub-dicionário
            size=13,
            color="#0067AC"     # Texto Cinza-chumbo
            )
        )
    )
        
    fig_tornado.update_layout(
        barcornerradius=10, # <--- Curvatura do gráfico
        xaxis_title="Gap (Terceiros - Auto)",
        xaxis=dict(showgrid=False, 
                   showline=False,   
                   zeroline=True, 
                   zerolinewidth=2, 
                   zerolinecolor='black'
                   ),
        yaxis=dict(showgrid=False,  # Remove a linha da moldura/borda externa do eixo
                   showline=False,  # Remove a grade do fundo
                   zeroline=False  # Remove a linha específica que marca o número zero (0).
                   ),           
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig_tornado, use_container_width=True)

# -------------------------------------------------------------------------
# PERGUNTA 4: Destaque principais forças e oportunidades
# -------------------------------------------------------------------------

with col_forcas:

    st.subheader("4. Forças e Oportunidades")
    st.caption("Classificação de competências (Visão Terceiros)")

    import pandas as pd
    df_forcas = pd.DataFrame({
        'Competência': competencias,
        'Nota Média': medias_terc
    }).sort_values(by='Nota Média', ascending=False).reset_index(drop=True)

    df_forcas.index = df_forcas.index + 1

    # 1. Cria um degradê personalizado usando AS SUAS cores exatas (Amarelo -> Verde)
    meu_degrade = LinearSegmentedColormap.from_list('CoresInstitucionais', ['#F5C518', '#3CAA4E'])

    # 2. Exibe a tabela aplicando o seu degradê
    st.dataframe(
        df_forcas.style.background_gradient(cmap=meu_degrade, subset=['Nota Média'])
                    .format({'Nota Média': '{:.2f}'}),
        use_container_width=True
    )

# ====================================================================================
    #                           V I S Ã O   D E   D A D O S
    # ====================================================================================
    
# st.expander cria uma barra clicável que expande e esconde o conteúdo
with st.expander("📊 Visualizar Base de Dados Detalhada"):

    # Filtramos apenas as colunas que importam para o gestor ler
    colunas_para_exibir = ['Turma_Ensina', 'Polo_Ensina', 'Grau Acadêmico_Ensina'] + colunas_auto + colunas_terc
        
    # Fazemos uma cópia para o Pandas não reclamar da formatação
    df_tabela = df_filtrado[colunas_para_exibir].copy()
        
    # Pintamos as colunas de dados com o seu Azul Marinho
    df_estilizado = df_tabela.style.set_properties(**{
        'background-color': '#FFFFFF', # Fundo branco
        'color': '#302f2f',            # Texto azul
        'border-color': '#FFFFFF'      # Linhas de grade brancas
    })
            
    # Mostramos a tabela no Streamlit
    st.dataframe(
        df_estilizado, 
        use_container_width=True,
        hide_index=True # Esconde aquela coluna de números 0, 1, 2, 3 do Pandas
    )