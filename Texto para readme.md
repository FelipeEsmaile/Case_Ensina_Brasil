Dashboard de People Analytics



Painel em Python (Streamlit) que calcula a diferença entre a autoavaliação de um funcionário e as notas dadas pelos seus pares.



**O Problema:**

Identificar em números se os funcionários subestimam o próprio trabalho (excesso de autocrítica) ou se avaliam o próprio desempenho acima da nota dada pela equipe.



**Como foi construído:**

O código resolve o problema em três etapas diretas:



\- Pandas: Limpa a base, calcula as médias de cada competência e extrai a diferença exata entre as notas.



\- Plotly e Matplotlib: Gera gráficos em formato tornado para mostrar desvios (positivos ou negativos) e mapas de calor para comparar o desempenho por filial.



\- Streamlit: Roda o front-end, aplica filtros interativos e hospeda a aplicação na nuvem.



**Funcionalidades:**



Destaque automático para a competência com a maior e a menor nota na base filtrada.



Filtros de gênero, raça e grau acadêmico que recalculam os gráficos em tempo real.



Tabela de dados formatada para leitura rápida e exportação.

