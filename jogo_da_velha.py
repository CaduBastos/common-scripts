
#--------------------------------------------------------------------------------------------------------------------------  
def show_tab(matriz):
    
    print(" -------")
    for j in range(3):
        print("| " + matriz[0][j] + " " + matriz[1][j] + " " + matriz[2][j] + " |") 
    print(" -------")

#--------------------------------------------------------------------------------------------------------------------------  
def read_line():

    line = 5
    while line < 1 or line > 2:
        line = int(input()) - 1
        if(line >= 0 and line <= 2):
            return line
        else:
            print("Número da linha inválido! Tente novamente.")
            print("Digite o número da linha: ")
        
#--------------------------------------------------------------------------------------------------------------------------  
def read_col():

    col = 5
    while col < 1 or col > 2:
        col = int(input()) - 1
        if(col >= 0 and col <= 2):
            return col
        else:
            print("Número da coluna inválido! Tente novamente.")
            print("Digite o número da coluna: ")

#--------------------------------------------------------------------------------------------------------------------------    
def valid_play(tab, line, col, player):

    if(tab[col][line] == " "):
        tab[col][line] = player
        return 1
    else:
        print("Jogada invalida! posicao do tabuleiro ja ocupada! Jogue novamente.")
        return 0
    
#--------------------------------------------------------------------------------------------------------------------------   
def valid_win(tab):

    #horizontais
    if((tab[0][0] == 'X' and tab[1][0] == 'X' and tab[2][0] == 'X') or (tab[0][0] == 'O' and tab[1][0] == 'O' and tab[2][0] == 'O')):
        return 1
    elif((tab[0][1] == 'X' and tab[1][1] == 'X' and tab[2][1] == 'X') or (tab[0][1] == 'O' and tab[1][1] == 'O' and tab[2][1] == 'O')):
        return 1
    elif((tab[0][2] == 'X' and tab[1][2] == 'X' and tab[2][2] == 'X') or (tab[0][2] == 'O' and tab[1][2] == 'O' and tab[2][2] == 'O')):
        return 1
    
    #verticais
    elif((tab[0][0] == 'X' and tab[0][1] == 'X' and tab[0][2] == 'X') or (tab[0][0] == 'O' and tab[0][1] == 'O' and tab[0][2] == 'O')):
        return 1
    elif((tab[1][0] == 'X' and tab[1][1] == 'X' and tab[1][2] == 'X') or (tab[1][0] == 'O' and tab[1][1] == 'O' and tab[1][2] == 'O')):
        return 1
    elif((tab[2][0] == 'X' and tab[2][1] == 'X' and tab[2][2] == 'X') or (tab[2][0] == 'O' and tab[2][1] == 'O' and tab[2][2] == 'O')):
        return 1

    #diagonais
    elif((tab[0][0] == 'X' and tab[1][1] == 'X' and tab[2][2] == 'X') or (tab[0][0] == 'O' and tab[1][1] == 'O' and tab[2][2] == 'O')):
        return 1
    elif((tab[0][2] == 'X' and tab[1][1] == 'X' and tab[2][0] == 'X') or (tab[0][2] == 'O' and tab[1][1] == 'O' and tab[2][0] == 'O')):
        return 1
    
    #empate
    elif((tab[0][0] != " " and tab[0][1] != " " and tab[0][2] != " " and
          tab[1][0] != " " and tab[1][1] != " " and tab[1][2] != " " and
          tab[2][0] != " " and tab[2][1] != " " and tab[2][2] != " ")):
        return 2
    else: 
        return 0

#--------------------------------------------------------------------------------------------------------------------------   

ctrl = 'r'

while(ctrl != 'n'):

    tab = [[" ", " ", " "],
           [" ", " ", " "],
           [" ", " ", " "]]
    
    print("Bem vindo ao jogo da velha!")
    print("Para jogar cada jogador deve inserir o numero da linha e coluna da posição a qual se deseja jogar.")
    
    while(ctrl == 'r'):


        play_status = 0
        while play_status == 0:
            show_tab(tab)
            print("Vez do jogador X: ")
            print("Digite o numero da linha: ")
            line = read_line()
            print("Digite o numero da coluna: ")
            col = read_col()
            play_status = valid_play(tab, line, col, "X")

        if(valid_win(tab) == 1):
            print("O Jogador X venceu!")
            show_tab(tab)
            break
        elif(valid_win(tab) == 2):
            print("O jogo terminou em empate!")
            show_tab(tab)
            break

        play_status = 0
        while play_status == 0:
            show_tab(tab)
            print("Vez do jogador O: ")
            print("Digite o numero da linha: ")
            line = read_line()
            print("Digite o numero da coluna: ")
            col = read_col()
            play_status = valid_play(tab, line, col, "O")

        if(valid_win(tab) == 1):
            print("O Jogador O venceu!")
            show_tab(tab)
            break
        elif(valid_win(tab) == 2):
            print("O jogo terminou em empate!")
            show_tab(tab)
            break

    while(ctrl == "null" or ctrl == 'r'):

        ctrl = input("Deseja jogar novamente (s - Sim, n - Nao)? ")
        if(ctrl != 's' and ctrl != 'n'):
            print("Caractere invalido, digite 's' ou 'n'!")
            ctrl = "null"
        elif(ctrl == 's'):
            ctrl = 'r'
            break
        else:
            break

    
    

















