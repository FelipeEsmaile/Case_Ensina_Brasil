import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap
 
# Configuração inicial da página
st.set_page_config(
    page_title="Painel RH",
    page_icon="Projeto_RH/imagem_rh.png",
    layout="wide"
    )

# Função para carregar os dados (com cache para o painel não ficar lento ao filtrar)
@st.cache_data
def carregar_dados():
    # Carregando a nova base genérica para o portfólio
    return pd.read_csv('Tratamento_dados/Base_Dashboard.csv')

df = carregar_dados()

# ==================================================================================================================================================================================================================
#                      B A R R A    L A T E R A L    -    F I L T R O S
# ==================================================================================================================================================================================================================

# Isso é um pixel transparente gerado em código (nunca vai dar erro de carregamento)
img_transparente = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

# Configura a logo
st.logo(
    image=img_transparente, 
    icon_image="Projeto_RH/imagem_rh.png"
)

with st.sidebar:
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
        st.image("Projeto_RH/imagem_rh.png", width=300)
    st.markdown("---")

st.sidebar.title(":material/filter_list: Filtros")

# --- Filtros Primários (Sempre Visíveis) ---
st.sidebar.subheader("Filtros Principais")

# Filtro de Ano (Com opção 'Todos' para visão geral)
lista_anos = ["Todos"] + df['Ano'].unique().tolist()
ano_selecionado = st.sidebar.selectbox("Selecione o Ano:", options=lista_anos)

# Filtro de Filial
lista_filiais = df['Filial'].unique().tolist()
filiais_selecionadas = st.sidebar.multiselect(
    "Selecione a Filial:", 
    options=lista_filiais, 
    default=lista_filiais
)

# --- Filtros Secundários (Ocultos no Expander) ---
with st.sidebar.expander("Filtros de Diversidade e Formação"):

    # Extrai as categorias únicas da base
    lista_racas = df['Raça'].unique().tolist()
    lista_generos = df['Gênero'].unique().tolist()
    lista_graus = df['Grau Acadêmico'].unique().tolist()

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

# Aplica o filtro de Ano (somente se o usuário não escolheu "Todos")
if ano_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Ano'] == ano_selecionado]

# Trava de segurança: só filtra se todos os componentes tiverem pelo menos uma opção selecionada
if not filiais_selecionadas or not generos_selecionados or not racas_selecionadas or not graus_selecionados:
    df_filtrado = df_filtrado.iloc[0:0] # Esvazia a base por segurança
    st.warning("⚠️ Selecione pelo menos uma opção em todos os filtros para visualizar os dados.")
else:
    # Aplica os filtros de Múltipla Escolha com segurança
    df_filtrado = df_filtrado[
        (df_filtrado['Filial'].isin(filiais_selecionadas)) &
        (df_filtrado['Gênero'].isin(generos_selecionados)) &
        (df_filtrado['Raça'].isin(racas_selecionadas)) &
        (df_filtrado['Grau Acadêmico'].isin(graus_selecionados))
    ]

# ========================================================================================================================================================================
#                                              T E L A      P R I N C I P A L
# ========================================================================================================================================================================

# ========================================      C   A   R   D  S     ===============================================================================

# Código em CSS para reproduzir os cards com borda lateral, texto centralizado e bordas arredondadas
st.markdown("""
    <style>
    /* 1. Formata a caixa do Card (Fundo branco e borda grossa na esquerda) */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border-left: 7px solid #1c3a6b !important; 
        border-top: none !important;
        border-right: 100px !important;
        border-bottom: none !important;
        border-radius: 10px !important; 
        padding: 10px !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05); /* Leve sombra para destacar do fundo */
    }

    /* 2. Centraliza o Título e muda a cor */
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
        color: #0067AC !important; /* Cor Institucional Atualizada */
        font-weight: bold !important;
        margin: 0% !important;
        font-size: 14px !important; /* Tamanho da letra do título */
    }

    /* Alvo direto apenas no ícone do Google */
    [data-testid="stMetricLabel"] p span {
        font-size: 20px !important; 
        margin-right: 8px !important; /* Dá um espaço entre o ícone e a primeira letra */
    }

    /* 3. Centraliza o Valor e aplica a cor institucional */
    [data-testid="stMetricValue"] > div {
        width: 100%;
        display: flex;
        justify-content: center;
        color: #0067AC !important; /* Cor Institucional Atualizada */
    }
    </style>
    """, unsafe_allow_html=True)

# Verifica se a base não está vazia após os filtros para não gerar erro de cálculo
if len(df_filtrado) > 0:
    
    # Preparação das listas de colunas
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

    # Cálculos dos KPIs Básicos
    qtd_profissionais = len(df_filtrado)
    media_global_auto = df_filtrado[colunas_auto].mean().mean()
    media_global_terc = df_filtrado[colunas_terc].mean().mean()
    
    # Cálculos de Destaque e Oportunidades
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
        st.metric(label=":material/Pin: Colaboradores Analisados", value=qtd_profissionais)
        
    with col2:
        st.metric(label=":material/Show_Chart: Autoavaliação Média", value=f"{media_global_auto:.2f}")
        
    with col3:
        st.metric(label=":material/Show_Chart: Avaliação Terceiros Média", value=f"{media_global_terc:.2f}")
        
    with col4:
        st.metric(label=f":material/star:Destaque: {destaque}", value=f"{nota_destaque:.2f}")
        
    with col5:
        st.metric(label=f":material/target:Foco: {oportunidade}", value=f"{nota_oportunidade:.2f}")

else:
    # Mensagem de segurança caso os filtros deixem a base vazia
    st.warning("⚠️ Não há dados para exibir. Ajuste os filtros na barra lateral.")

# ========================================      G   R   Á   F   I   C   O   S     ===============================================================================

# --------------------------------------- Gráfico de Barras  ---------------------------------------
    
# Título utilizando markdown para centralizar
st.markdown(
    "<h3 style='text-align: center;'>Comparação das Competências: Autoavaliação X Avaliação por Terceiros</h3>", 
    unsafe_allow_html=True
)

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
    marker_color='#1C3A6B', # Cor Primária
    text=[f"{val:.2f}" for val in medias_auto], 
    textposition='auto' 
))
    
# Adiciona as colunas de Avaliação de Terceiros
fig_barras.add_trace(go.Bar(
    x=competencias,
    y=medias_terc,
    name='Avaliação Terceiros',
    marker_color='#8DB4E2', # Cor Secundária
    text=[f"{val:.2f}" for val in medias_terc],
    textposition='auto',
))

fig_barras.update_traces(
    hovertemplate="<b>Tipo:</b> %{data.name}<br>" +
                  "<b>Competência:</b> %{x}<br>" +
                  "<b>Pontuação Média:</b> %{y:.2f}<extra></extra>",
    
    hoverlabel=dict(
        bgcolor="#FAFAFA",      # Fundo off-white
        bordercolor="#1C3A6B",  # Borda Azul-marinho
        font=dict(                
            size=13,
            color="#3A3A3A"     # Texto Cinza-chumbo
        )
    )
)

fig_barras.update_layout(
    barmode='group', 
    barcornerradius=10, 
    xaxis_title="Competências",
    yaxis_title="Pontuação Média",
    xaxis= dict(showgrid=False,   
                showline=False,   
                zeroline=False),  
    yaxis= dict(showgrid=False,   
                showline=False,   
                zeroline=False, range=[0, 1]), # NOTA MÁXIMA (Se for outra, ajuste aqui)
    margin=dict(t=40, b=40, l=40, r=40),
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

col1, col2 = st.columns(2)

# --------------------------------------- Gráfico de Rank das Competências  ---------------------------------------

with col1:

    # Título utilizando markdown para centralizar
    st.markdown(
    "<h3 style='text-align: center;'>Gap de Percepção</h3>", 
    unsafe_allow_html=True
    )   
    
    # Calcula a diferença: Terceiros - Auto
    gaps = [t - a for t, a in zip(medias_terc, medias_auto)]
        
    # Cores personalizadas do portfólio
    cores_gap = ['#1C3A6B' if val >= 0 else '#E07A5F' for val in gaps]
        
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
    hovertemplate="%{y} <br>" +
                  "<b>Gap: %{x:.2f}</b><extra></extra>",
    
    hoverlabel=dict(
        bgcolor="#FAFAFA",      
        bordercolor="#1C3A6B",  
        font=dict(                
            size=13,
            color="#3A3A3A"     
            )
        )
    )
        
    fig_tornado.update_layout(
        barcornerradius=10, 
        xaxis_title="Gap (Terceiros - Auto)",
        xaxis=dict(showgrid=False, 
                   showline=False,   
                   zeroline=True, 
                   zerolinewidth=2, 
                   zerolinecolor='black'
                   ),
        yaxis=dict(showgrid=False,  
                   showline=False,  
                   zeroline=False   
                   ),           
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig_tornado, use_container_width=True)
    st.caption("IMPORTANTE: Gap = Avaliação de Terceiros - Autoavaliação")
  
# --------------------------------------- Gráfico de Gap de Percepção  ---------------------------------------

with col2:

    # Título utilizando markdown para centralizar
    st.markdown(
    "<h3 style='text-align: center;'>Rank das Competências</h3>", 
    unsafe_allow_html=True
    ) 

    df_forcas = pd.DataFrame({
        'Competência': competencias,
        'Nota Média': medias_terc
    }).sort_values(by='Nota Média', ascending=False).reset_index(drop=True)

    df_forcas.index = df_forcas.index + 1

    # Cria um degradê personalizado usando as cores Azul Marinho -> Azul Aço
    meu_degrade = LinearSegmentedColormap.from_list('CoresInstitucionais', ['#8DB4E2', '#1C3A6B'])

    # Exibe a tabela aplicando o seu degradê
    st.dataframe(
        df_forcas.style.background_gradient(cmap=meu_degrade, subset=['Nota Média'])
                    .format({'Nota Média': '{:.2f}'}),
        use_container_width=True
    )

    st.caption("IMPORTANTE: Com base na média das notas da Avaliação por Terceiros.")

# --------------------------------------- Gráfico de Desempenho por Filial  ---------------------------------------

# Título utilizando markdown para centralizar
st.markdown(
    "<h3 style='text-align: center;'>Desempenho por Filial</h3>", 
    unsafe_allow_html=True
)  
    
coluna_agrupamento = 'Filial' 
    
# Calcula a média por grupo na visão de Terceiros
df_heatmap = df_filtrado.groupby(coluna_agrupamento)[colunas_terc].mean().round(3)
df_heatmap.columns = competencias # Limpa os nomes das colunas
    
fig_heat = go.Figure(data=go.Heatmap(
    z=df_heatmap.values,
    x=df_heatmap.columns,
    y=df_heatmap.index,
    colorscale=[[0.0, '#FFFFFF'], [0.5, '#8DB4E2'], [1.0, '#1C3A6B']],
    text=df_heatmap.values,
    texttemplate="%{text:.2f}",
    showscale=True
))

fig_heat.update_traces(
    hovertemplate="<b>Competência:</b> %{x}<br>" +
                  "<b>Filial:</b> %{y}<br>" +
                  "<b>Pontuação Média:</b> %{z:.2f}<extra></extra>",
    
    hoverlabel=dict(
        bgcolor="#FAFAFA",      
        bordercolor="#1C3A6B",  
        font=dict(                
            size=13,
            color="#3A3A3A"     
        )
    )
)
    
fig_heat.update_layout(
    yaxis_title="Filial",
    xaxis_title="Competências",
    margin=dict(t=20, b=20, l=20, r=20)
)
st.plotly_chart(fig_heat, use_container_width=True)

# ----------------------------------------------- Tabela -----------------------------------------------

with st.expander(":material/Bar_Chart: Base de Dados"):

    # Filtramos apenas as colunas que importam para o gestor ler
    colunas_numericas = colunas_auto + colunas_terc
    colunas_para_exibir = ['ID_Colaborador', 'Ano', 'Filial', 'Grau Acadêmico'] + colunas_numericas
        
    # Fazemos uma cópia para não alterar a base original
    df_tabela = df_filtrado[colunas_para_exibir].copy()
       
    # Aplicar a máscara de 2 casas decimais direto no Styler
    df_estilizado = (
        df_tabela.style
        .format(formatter="{:.0f}", subset=['ID_Colaborador']) # Tratando o ID como número inteiro (sem decimais)
        .format(formatter="{:.2f}", subset=colunas_numericas) 
        .set_properties(**{
            'background-color': '#FFFFFF', 
            'color': "#000000",            
            'border-color': '#FFFFFF'      
        })
    )
            
    # Mostramos a tabela no Streamlit
    st.dataframe(
        df_estilizado, 
        use_container_width=True,
        hide_index=True 
    )