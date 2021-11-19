import pandas as pd
import numpy as np

from functions import *

def main():

    dfColeta = pd.read_csv('input/coleta.txt', delimiter = ' ').rename(columns = {'Peças': 'Peças Coletadas'})
    dfColeta = dfColeta[dfColeta["Peças Coletadas"].astype('string').str.len() == 16]

    dfVA = pd.read_csv('input/peçasDoSistema.CSV', delimiter = ';', usecols = ["Codigo 1000", "Local"], dtype = {"Codigo 1000": np.int64}).rename(columns = {'Codigo 1000' : 'Peças VA', 'Local' : 'Local VA'})[["Peças VA", "Local VA"]]

    dfColeta = coletaParaVA(dfColeta)

    dfVA = dfVA.rename(columns = {"Peças VA" : "Peça"})
    dfColeta = dfColeta.rename(columns = {"Peças Coletadas" : "Peça"})

    dfMergeVA = dfVA.merge(dfColeta, how = "left", on = "Peça")
    dfMergeColeta = dfColeta.merge(dfVA, how = "left", on = "Peça")

    mergeAll = pd.concat([dfMergeVA, dfMergeColeta], ignore_index=True)

    dataFrameToExcel(mergeAll, "output/")

if __name__ == "__main__":
    main()