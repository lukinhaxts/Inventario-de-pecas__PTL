## Importa a biblioteca Tkinter

from os import truncate
from tkinter import *
from tkinter import font
from tkinter import messagebox
import re

## Importa o programa 'main.py'

from mainBackend import *

## Cria a classe da janela principal (inicial) do app

class mainWindow:

    def __init__(self, toplevel):
        
        ## Cria o atributo toplevel do Frame

        self.toplevel = toplevel

        ## Cria o Frame principal do Toplevel

        self.frameTitle = Frame(toplevel, background = "#abd9f4")
        self.frameTitle.pack(expand = True, fill = "both") 

        ## Cria a Label do título do app 

        self.labelTitle = Label(self.frameTitle, text="Inventário de Peças", font = ('Arial Black', '20', 'bold'), pady = 20, padx = 100, foreground = "#f51f1f", background = "#abd9f4")
        self.labelTitle.pack()

        ## Cria a Label central, onde se posicionarão inicialmente o filtro, e em seguida os textos informativos

        self.middleLabel = Label(self.frameTitle, background = "#abd9f4")
        self.middleLabel.pack(pady = 10)

        ## Cria o título do filtro de Local

        self.inputTitle = Label(self.middleLabel, text="Local ( inicial / final ) :", font = ('Arial Black', '12', 'bold'), foreground="black", background = "#abd9f4")
        self.inputTitle.pack(side='left')

        ## Cria o campo de texto 'inicial' do filtro de local

        self.inputTextIni = Entry(self.middleLabel, width = 10, font = ('Arial Black', '12', 'bold'))
        self.inputTextIni.configure(validate = 'key', validatecommand = (self.inputTextIni.register(self.limitaEntrada), '%d', '%P'))
        self.inputTextIni.pack(side='left', padx = 5)

        ## Cria o campo de texto 'final' do filtro de local

        self.inputTextFin = Entry(self.middleLabel, width = 10, font = ('Arial Black', '12', 'bold'))
        self.inputTextFin.configure(validate = 'key', validatecommand = (self.inputTextFin.register(self.limitaEntrada), '%d', '%P'))
        self.inputTextFin.pack(side='left', padx = 5)

        ## Cria o botão de "Iniciar Processo"

        self.startButton = Button(self.frameTitle, text="Iniciar Inventário", width = 30, height = 3, background = '#f51f1f', command = self.iniciaMain)
        self.startButton.pack(padx = 15, pady = 15)
    
    ## Função que limita o tamanho da entrada nos filtros 

    def limitaEntrada(self, action, text):

        if(action == '1'):
            if(len(text) > 10):
                return False
            else:
                return True
        else:
            return True

    ## Função que valida o pattern do filtro

    def validaPattern(self):

        patternA = "[R][A-H]\s[C](0[1-9]|1[0-9]|2[0-9]|3[0-6])\s[G][0][1-8]"                ## 36 colunas - 8 gavetas
        patternB = "[R][A-H]\s[C](0[1-9]|1[0-9]|2[0-9]|3[0-6])\s[G][0][1-8]"                ## 36 colunas - 8 gavetas
        patternC = "[R][A-H]\s[C](0[1-9]|1[0-9]|2[0-9]|3[0-6])\s[G][0][1-8]"                ## 36 colunas - 8 gavetas
        patternD = "[R][A-H]\s[C](0[1-9]|1[0-9]|2[0-9]|3[0-6])\s[G][0][1-8]"                ## 36 colunas - 8 gavetas
        patternE = "[R][A-H]\s[C](0[1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-3])\s[G][0][1-8]"         ## 43 colunas - 8 gavetas
        patternF = "[R][A-H]\s[C](0[1-9]|1[0-2])\s[G][0][1-8]"                              ## 12 colunas - 8 gavetas
        patternG = "[R][A-H]\s[C](0[1-9]|1[0-2])\s[G][0][1-7]"                              ## 12 colunas - 7 gavetas
        patternH = "[R][A-H]\s[C](0[1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|50)\s[G][0][1-5]"      ## 50 colunas - 5 gavetas

        filter1 = self.inputTextIni.get()
        filter2 = self.inputTextFin.get()

        rua1 = filter1[1]
        rua2 = filter2[1]

        coluna1 = filter1[4:6]
        coluna2 = filter2[4:6]

        gaveta1 = filter1[8:]
        gaveta2 = filter2[8:]

        patternFiltro1 = eval("pattern" + rua1)
        patternFiltro2 = eval("pattern" + rua2)

        if((re.fullmatch(patternFiltro1, filter1) == None) or (re.fullmatch(patternFiltro2, filter2) == None)):
            messagebox.showerror(title = "Filtro Incorreto", message = "Formato Padrão de filtro: \n\n R[A-H] C[01-25] G[01-08] \n\n Exemplos: \n\n RA C13 G02 \n RD C05 G03")
            validaFiltros = 0
        elif((rua1 > rua2) or ((rua1 == rua2) and (coluna1 > coluna2)) or ((rua1 == rua2) and (coluna1 == coluna2) and (gaveta1 > gaveta2))):
            messagebox.showerror(title = "Filtro Incorreto", message = "O filtro de local de início deve ser menor que o filtro de local final")
            validaFiltros = 0
        else:
            validaFiltros = 1

        return validaFiltros, filter1, filter2

    ## Função chamada ao clicar no botão 'Tentar Novamente'

    def tentarNovamente(self):

        self.status.destroy()

        self.inputTitle.pack(side='left')
        self.inputTextIni.pack(side='left', padx = 5)
        self.inputTextFin.pack(side='left', padx = 5)

        self.startButton.configure(text="Iniciar Inventário", background = '#f51f1f', command = self.iniciaMain)

    ## Função chamada ao clicar no botão 'Sair'

    def fecharPrograma(self):
        self.toplevel.destroy()
    
    ## Função para exibir texto de aguardo enquanto executa o programa

    def aguardando(self):

        if self.startButton['text'] == "Iniciar Inventário":
            self.inputTitle.pack_forget()
            self.inputTextIni.pack_forget()
            self.inputTextFin.pack_forget()
        else:
            self.status.destroy()
        

        self.waiting = Label(self.middleLabel, text="Programa em Execução!!", font = ('Arial Black', '10', 'bold'), foreground="#f51f1f", background = "#abd9f4")
        self.waiting.pack()

    ## Função que insere o texto de feedback do programa na janela

    def insereTexto(self, textoResult, color):

        self.waiting.destroy()
        self.status = Label(self.middleLabel, text=textoResult, font = ('Arial Black', '10', 'bold'), foreground=color, background = "#abd9f4")
        self.status.pack()

        if color == "red":
            self.startButton.configure(text="Tentar Novamente", background = '#fff14a', command = self.tentarNovamente)
        elif color == "green":
            self.startButton.configure(text = "Sair", command = self.fecharPrograma)
        else:
            exit(1)

    ## Função que faz a chamada do programa mainBackend e exibe ao usuário o feedback do programa

    def iniciaMain(self):
        
        validaFiltros, localIni, localFin = self.validaPattern()

        if(validaFiltros == 1):
            self.aguardando()
            result, color = mainBackend(localIni, localFin)
            self.insereTexto(result, color)
        else:
            pass

## Função que centraliza a janela no monitor quando executado

def centerWindow(root):

    ## Mantém a tela root em constante atualização de tamanho

    root.update_idletasks()

    ## Captura a altura e largura do monitor

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    ## Captura a altura e largura do frame

    frameWidth = int(root.geometry().split('x')[0])
    frameHeight = int(root.geometry().split('x')[-1].split('+')[0])

    ## Calcula a posição (x,y) do frame centralizado 

    posX = (screenWidth / 2) - (frameWidth / 2)
    posY = (screenHeight / 2) - (frameHeight / 2)

    ## Aplica a posição (x,y) centralizada no frame

    root.geometry("%dx%d+%d+%d" %(frameWidth, frameHeight, posX, posY))

## Função principal que: cria, centraliza, e executa a janela do Tkinter

def main():

    ## Cria a instância de Tk (instância principal do Tkinter) e define seu título

    root = Tk()
    root.title("Inventário de Peças")

    ## Cria a tela principal (Toplevel) da GUI do app

    mainWindow(root)

    ## Centraliza a tela Toplevel

    centerWindow(root)

    ## Comando para manter rodando a GUI

    root.mainloop()

if __name__ == '__main__':
    main()