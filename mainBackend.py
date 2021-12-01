import os
import glob
import pandas as pd

from functions import *

def mainBackend(localIni, localFin):

    ## Checa a quantidade de arquivos .CSV e .txt que existem na pasta 'input'

    status, message, color = checaArquivos()

    ## Se houver problemas com os arquivos, o programa retorna à janela principal imediatamente

    if(not status):
        return message, color
    
    ## Lê e formata dados provenientes da coleta

    dfColeta = pd.read_csv(glob.glob(os.path.join(os.path.abspath('./input'), "*.txt"))[0], delimiter = ' ').rename(columns = {'Peças': 'Peças Coletadas'})

    dfColeta = dfColeta[dfColeta["Peças Coletadas"].astype('string').str.len() == 16]   # Lê somentes códigos com tamanho 16 
    dfColeta = dfColeta[dfColeta["Peças Coletadas"].astype('string').str.isnumeric()]   # Lê somentes códigos que são totalmente numéricos 
                                                                                        #   (retira bipagem de 0200 (remontes e trocas de 
                                                                                        #   qualidade), que saem com caracteres e/ou símbolos)

    ## Lê e formata dados provenientes do Virtual Age

    dfVA = pd.read_csv(glob.glob(os.path.join(os.path.abspath('./input'), "*.CSV"))[0], delimiter = ';', usecols = ["Codigo 1000", "Local"]).rename(columns = {'Codigo 1000' : 'Peças VA', 'Local' : 'Local VA'}).fillna(0)[["Peças VA", "Local VA"]]
    dfVA = dfVA.astype({'Peças VA' : 'int64'}) 

    dfVA = dfVA[~dfVA['Peças VA'].astype("string").str.startswith("2000")]      # Lê somentes códigos com início diferente de 0200 
                                                                                #   (remontes e trocas de qualidade) 

    ## Faz a leitura dos filtros e separa o DataFrame do Virtual Age entre dados dentro e fora do escopo do filtro 
    ##   (dfVAPrimario e dfVASecundario, respectivamente)

    dfVAPrimario, dfVASecundario = defineRangeLocal(dfVA, "RA C01 G01", "RA C01 G02")

    ## Transforma os dados da coleta para o mesmo formato do Virtual Age

    dfColeta = coletaParaVA(dfColeta)

    ## Faz a comparação entre os dados do Virtual Age dentro do escopo e as peças coletadas

    dfCompair1 = comparaNoEscopoDoFiltro(dfVAPrimario, dfColeta)

    ## Separa os dados dados entre as 3 categorias de peças 
    ##   ( Peças com Local Diferente | Peças não Encontradas no Inventário | Peças não Encontradas no Sistema)

    PcLD, PnEnI, PnEnS = divideClasses(dfCompair1)

    ## Faz a comparação das peças que não foram encontradas no Virtual Age dentro daquele escopo com o restante das peças de outros locais

    dfCompair2 = comparaForaDoEscopoDoFiltro(dfVASecundario, PnEnS)

    ## Reorganiza os dados dados entre as 3 categorias de peças 
    ##   ( Peças com Local Diferente | Peças não Encontradas no Inventário | Peças não Encontradas no Sistema)

    PcLD, PnEnS = reorganizacaoDeClasses(PcLD, PnEnS, dfCompair2)

    ## Exporta as 3 categorias de peças ( Peças com Local Diferente | Peças não Encontradas no Inventário | Peças não Encontradas no Sistema) 
    ##   para 3 planilhas Excel diferentes

    dataFrameToExcel(PcLD, PnEnI, PnEnS, "./output/")

    ## Retorna a mensagem a ser computada no terminal juntamente com sua cor de exibição

    return "Resultados computados na pasta 'Saída(s)'\n", 'green'