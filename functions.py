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

def defineColunaEGaveta(n):
    
    col = n[0:2]
    gav = n[2]

    return " COLUNA {} GAVETA 0{}".format(col, gav)

def transformaLocal(df, coluna):
    
    df[coluna] = df[coluna].map(lambda x: "RUA " + defineRua(str(x)[0]) + defineColunaEGaveta(str(x)[1:4]))

def coletaParaVA(df):
    df.insert(1, "Local Coletado", ['' for i in range(0, len(df.index))], allow_duplicates = True)
    
    df["Local Coletado"] = df["Peças Coletadas"].map(lambda x: int(str(x)[-6:]))
    transformaLocal(df, "Local Coletado")
    df["Peças Coletadas"] = df["Peças Coletadas"].map(lambda x: int(str(x)[:-6]))

    return df

def dataFrameToExcel_PcLD(df, endereco):
    
    condition = ((df["Local Coletado"].notna()) & (df["Local VA"].notna())) & (df["Local Coletado"] != df["Local VA"])
    
    filename = "Peças com Local Diferente.xlsx"
    
    df[condition].to_excel((endereco + filename), index=False)
    
def dataFrameToExcel_PSnS(df, endereco):
    
    filename = "Peças Somente no Sistema.xlsx"
    
    df[df["Local Coletado"].isna()][["Peça", "Local VA"]].to_excel((endereco + filename), index=False)
    
def dataFrameToExcel_PSnC(df, endereco):
    
    filename = "Peças Somente na Coleta.xlsx"
    
    df[df["Local VA"].isna()][["Peça", "Local Coletado"]].to_excel((endereco + filename), index=False)
    

def dataFrameToExcel(df, endereço):
    dataFrameToExcel_PcLD(df, endereço)
    dataFrameToExcel_PSnS(df, endereço)
    dataFrameToExcel_PSnC(df, endereço)