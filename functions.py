import os
import glob
import pandas as pd
import numpy as np

## Função responsável por formatar o filtro para o formato do CSV do Virtual Age

def formataFiltros(filtro):
    
    return "RUA " + filtro[1] + " COLUNA " + filtro[4:6] + " GAVETA " + filtro[8:]
    
## Define o escopo real demarcado pelos filtros e faz a separação dos dados em 2 grupos: dentro e fora do escopo do filtro

def defineRangeLocal(df, inicio, fim):
    
    inicio_formatado = formataFiltros(inicio)
    fim_formatado = formataFiltros(fim)
    
    dfFiltrado = df[df["Local VA"] >= inicio_formatado]
    dfFiltrado = dfFiltrado[dfFiltrado["Local VA"] <= fim_formatado]
    
    dfForaDoFiltro1 = df[df["Local VA"] < inicio_formatado]
    dfForaDoFiltro2 = df[df["Local VA"] > fim_formatado]
    
    dfForaDoFiltro = pd.concat([dfForaDoFiltro1, dfForaDoFiltro2], ignore_index=True)
    
    return dfFiltrado, dfForaDoFiltro

## Função que checa se ambos os arquivos de entrada estão na pasta correta, ou se não estão duplicados

def checaArquivos():
    
    checaArquivoTXT = len(glob.glob(os.path.join(os.path.abspath('./input'), "*.txt")))
    checaArquivoCSV = len(glob.glob(os.path.join(os.path.abspath('./input'), "*.CSV")))
    
    if(checaArquivoTXT == 0 and checaArquivoCSV == 0):
        return False, "Em falta de ambos os arquivos na pasta 'input'!!", 'red'
    elif(checaArquivoTXT == 0 and checaArquivoCSV == 1):
        return False, "Em falta do arquivo de coleta na pasta 'input'!!", 'red'
    elif(checaArquivoTXT == 1 and checaArquivoCSV == 0):
        return False, "Em falta do arquivo do Virtual Age na pasta 'input'!!", 'red'
    elif(checaArquivoTXT == 2 or checaArquivoCSV == 2):
        return False, "Existem arquivos além dos esperados na pasta 'input'!!", 'red'
    else:
        return True, "Arquivos corretos!!", 'green'

## Função responsável por dividir os dados do primeiro comparativo nas 3 categorias de peça 
##   ( Peças com Local Diferente | Peças não Encontradas no Inventário | Peças não Encontradas no Sistema)

def divideClasses(df):
    
    condition = ((df["Local Coletado"].notna()) & (df["Local VA"].notna())) & (df["Local Coletado"] != df["Local VA"])
    PcLD = df[condition].reset_index(drop=True)
    
    PnEnI = df[df["Local Coletado"].isna()].reset_index(drop=True)
    PnEnS = df[df["Local VA"].isna()].reset_index(drop=True)
    
    return PcLD, PnEnI, PnEnS

## Função responsável por reorganizar os dados após o segundo comparativo, nas 3 categorias de peça 
##   ( Peças com Local Diferente | Peças não Encontradas no Inventário | Peças não Encontradas no Sistema)

def reorganizacaoDeClasses(PcLD, PnEnS, dfCompair2):
    
    comparacaoForaDoEscopo = dfCompair2['Peça'].to_list()
    
    PnEnS = PnEnS.drop(PnEnS[PnEnS['Peça'].astype('int64').isin(comparacaoForaDoEscopo)].index.to_list())
    PcLD = pd.concat([PcLD, dfCompair2], ignore_index=True)
    
    return PcLD, PnEnS

## Função responsável por comparar os dados entre Virtual Age e coleta dentro do escopo do filtro

def comparaNoEscopoDoFiltro(df1, df2):
    
    df1 = df1.rename(columns = {"Peças VA" : "Peça"})
    df2 = df2.rename(columns = {"Peças Coletadas" : "Peça"})

    dfMergeColeta = df2.merge(df1, how = "left", on = "Peça")
    dfMergeVA = df1.merge(df2, how = "left", on = "Peça")

    mergeAll = pd.concat([dfMergeVA, dfMergeColeta], ignore_index=True)
    mergeAll = mergeAll.astype({'Peça': 'string'})
    
    return mergeAll

## Função responsável por comparar os dados entre Virtual Age e coleta fora do escopo do filtro

def comparaForaDoEscopoDoFiltro(df1, df2):
    
    df1 = df1.rename(columns = {"Peças VA" : "Peça"})
    df2 = df2[["Peça", "Local Coletado"]].astype({'Peça' : 'int64'})
        
    dfMergeColeta = df2.merge(df1, how = "left", on = "Peça")

    mergeAll = dfMergeColeta[["Peça", "Local VA", "Local Coletado"]]
    
    return mergeAll

## Função aninhada dentro de outra função ('transformaLocal')
## responsável por definir a rua de acordo com o código recebido

def defineRua(string):
    
    if string == '1':
        return 'A'
    elif string == '2':
        return 'B'
    elif string == '3':
        return 'C'
    elif string == '4':
        return 'D'
    elif string == '5':
        return 'E'
    elif string == '6':
        return 'F'
    elif string == '7':
        return 'G'
    elif string == '8':
        return 'H'
    elif string == '9':
        return 'I'
    else:
        return "ERRO"

## Função aninhada dentro de outra função ('transformaLocal')
## Responsável por definir a coluna e a gaveta de acordo com os códigos recebidos

def defineColunaEGaveta(n):
    
    col = n[0:2]
    gav = n[2]

    return " COLUNA {} GAVETA 0{}".format(col, gav)

## Função que engloba as 2 funções anteriores ('defineRua' e 'defineColunaEGaveta')
## Função também aninhada dentro de outra função ('coletaParaVA')
## Responsável por identificar e decodificar para o formato padrão do Virtual Age os dados de local

def transformaLocal(df, coluna):
    
    df[coluna] = df[coluna].map(lambda x: "RUA " + defineRua(str(x)[0]) + defineColunaEGaveta(str(x)[1:4]))

## Função que engloba a função anterior ('transformaLocal')
## Divide o dado recebido da coleta entre código da peça (código 1000) e local

def coletaParaVA(df):
    df.insert(1, "Local Coletado", ['' for i in range(0, len(df.index))], allow_duplicates = True)
    
    df["Local Coletado"] = df["Peças Coletadas"].map(lambda x: int(str(x)[-6:]))
    transformaLocal(df, "Local Coletado")
    df["Peças Coletadas"] = df["Peças Coletadas"].map(lambda x: int(str(x)[:-6]))

    return df

## Função aninhada dentro de outra função ('dataFrameToExcel')
## Responsável por transformar os dados de 'Peças com Local Diferente' (PcLD) em arquivo Excel

def dataFrameToExcel_PcLD(df, endereco):
    
    filename = "Peças com Local Diferente.xlsx"
    
    df.to_excel((endereco + filename), index=False)
    
## Função aninhada dentro de outra função ('dataFrameToExcel')
## Responsável por transformar os dados de 'Peças não Encontradas no Inventário' (PnEnI) em arquivo Excel

def dataFrameToExcel_PnEnI(df, endereco):
    
    filename = "Peças não Encontradas no Inventário.xlsx"
    
    df[["Peça", "Local VA"]].to_excel((endereco + filename), index=False)

## Função aninhada dentro de outra função ('dataFrameToExcel')
## Responsável por transformar os dados de 'Peças não Encontradas no Sistema' (PnEnS) em arquivo Excel

def dataFrameToExcel_PnEnS(df, endereco):
    
    filename = "Peças não Encontradas no Sistema.xlsx"
    
    df[["Peça", "Local Coletado"]].to_excel((endereco + filename), index=False)

## Função que engloba as 3 funções anteriores ('dataFrameToExcel_PcLD', 'dataFrameToExcel_PnEnI' e 'dataFrameToExcel_PnEnS')
## Função que faz a mudança dos formatos das colunas dos DataFrames (para serem melhor visualizados em Excel) e 
##   transforma as 3 categorias de peças ( Peças com Local Diferente | Peças não Encontradas no Inventário | Peças não Encontradas no Sistema)
##   em diferentes arquivos Excel

def dataFrameToExcel(PcLD, PnEnI, PnEnS, endereço):
    
    PcLD = PcLD.astype({"Peça" : 'string'})
    PnEnI = PnEnI.astype({"Peça" : 'string'})
    PnEnS = PnEnS.astype({"Peça" : 'string'})
    
    dataFrameToExcel_PcLD(PcLD, endereço)
    dataFrameToExcel_PnEnI(PnEnI, endereço)
    dataFrameToExcel_PnEnS(PnEnS, endereço)