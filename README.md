# Inventário de Peças - Paraguaçu Têxtil LTDA (PTL)

Implementação de um software que faça a comparação das peças de tecido entre o sistema ERP e a coleta feita localmente.

<br/>

## Formato de arquivo da coleta

  

Formato: ***.txt***

Número de Linhas: **Variável**

Número de Colunas: **1**

Nome da(s) coluna(s): **Peças Coletadas**

<br/>
A coluna "Peças" já engloba o código da peça e o local da peça no mesmo dado. Exemplo:  


<br/>

**Dado colhido:** 1000918544101101

<br/>
<img src="https://latex.codecogs.com/png.image?\dpi{150}&space;\bg_white&space;\begin{array}{r|r}\underbrace{\begin{array}{rrrrrrrrrr}&space;1&space;&&space;0&space;&&space;0&space;&&space;0&space;&&space;9&space;&&space;1&space;&&space;8&space;&&space;5&space;&&space;4&space;&&space;4&space;\end{array}}_{\text{Codigo&space;1000}}&space;&&space;\underbrace{\begin{array}{rrrr}&space;\overbrace{\begin{array}{r}1\end{array}}^{\text{Rua}}&space;&&space;\overbrace{\begin{array}{rr}&space;0&space;&&space;1&space;\end{array}}^{\text{Coluna}}&space;&&space;\overbrace{\begin{array}{r}1\end{array}}^{\text{Gaveta}}&space;&&space;\overbrace{\begin{array}{rr}&space;0&space;&&space;1&space;\end{array}}^{\text{Sequencia&space;de&space;bipagem}}&space;\end{array}}_{\text{Local}}\end{array}" title="\bg_white \begin{array}{r|r}\underbrace{\begin{array}{rrrrrrrrrr} 1 & 0 & 0 & 0 & 9 & 1 & 8 & 5 & 4 & 4 \end{array}}_{\text{Codigo 1000}} & \underbrace{\begin{array}{rrrr} \overbrace{\begin{array}{r}1\end{array}}^{\text{Rua}} & \overbrace{\begin{array}{rr} 0 & 1 \end{array}}^{\text{Coluna}} & \overbrace{\begin{array}{r}1\end{array}}^{\text{Gaveta}} & \overbrace{\begin{array}{rr} 0 & 1 \end{array}}^{\text{Sequencia de bipagem}} \end{array}}_{\text{Local}}\end{array}" />

<br/>

## Formato de arquivo do Virtual Age

  
Formato: ***.CSV***

Número de Linhas: **Variável**

Número de Colunas: **4**

Nome da(s) coluna(s): **Local | Codigo 1000 | Artigo | Metragem**

<br/>
Apenas as colunas "Local" e "Codigo 1000" são utilizadas do arquivo, respectivamente renomeadas como "Peças VA" e "Local VA". Exemplo:
<br/><br/><br/>

| Local | Codigo 1000 | Artigo | Metragem |
|-------|-------------|--------|----------|
| RUA A COLUNA 02 GAVETA 03 | 1000989323 | 28 01 1111 |  96,84 |
| RUA D COLUNA 18 GAVETA 03 | 1000972073 | 28 03 4511 | 138,43 |

<img src="https://latex.codecogs.com/png.image?\dpi{150}&space;\bg_white&space;\Rightarrow&space;" title="\bg_white \Rightarrow " />
