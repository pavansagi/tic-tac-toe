import pygame       #this is where we play the game
import numpy        #for 2d array
import math         #for infinity
import random       #for random move
import time         #to wait for opponent after some time

pygame.init()

SIZE = WIDTH,HEIGHT = 470,470

def rect(screen, color, x, y, w, h, fill=0):
    pygame.draw.rect(screen, color, (x, y, w, h), fill)

def square(screen, color, x, y, s, fill=0):
    rect(screen, color, x, y, s, s, fill)

def check_win(board):
    n = len(board)
    first = board[0][0]
   
    diagonal = first != ""
    for i in range(n):
        if board[i][i] != first:
            diagonal = False
            break
    if diagonal:
        return first
    first = board[0][n-1]
    back_diag = first != ""
    for i in range(1, n+1):
        if board[i-1][n-i] != first:
            back_diag = False
            break
    if back_diag:
        return first

    for i in range(n):
        first = board[i][0]
        sideways = first != ""
        for j in range(n):
            if board[i][j] != first:
                sideways = False
        if sideways:
            return first

    for i in range(n):
        first = board[0][i]
        # print(first)
        sideways = first != ""
        for j in range(n):
            if board[j][i] != first:
                sideways = False
        if sideways:
            return first
    
    open_spots = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                open_spots += 1
    if open_spots == 0:
        return "tie"
    return None

scores = {
    "x" : 10,
    "o" : -10,
    "tie" : 0
}

def minmax(board,is_max,n,alpha,beta):
    winner = check_win(board)
    if winner:
        return scores[winner]
    if is_max:
        best_score = -math.inf
        flag = False
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    board[i][j] = "x"
                    score = minmax(board,False,n,alpha,beta)
                    board[i][j] = ""
                    best_score = max(best_score,score)
                    alpha = max(alpha,score)
                    if beta <= alpha:
                        flag = True
            if flag:
                break
        return best_score
    else:
        best_score = math.inf
        flag = False
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    board[i][j] = "o"
                    score = minmax(board,True,n,alpha,beta)
                    board[i][j] = ""
                    best_score = min(best_score,score)
                    beta = min(beta,score)
                    if beta <= alpha:
                        flag = True
            if flag:
                break
        return best_score

def best_move(board):
    n = len(board)
    best_score = -math.inf
    move = (0,0)
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                board[i][j] = "x"
                score = minmax(board,False,n,-math.inf,math.inf)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i,j)
    board[move[0]][move[1]] = "x"
    return board

def reset(n):
    board = [["" for i in range(n)]for j in range(n)]
    loop = True
    return board,loop,None,True

    
def main():
    n = 3
    board = [["" for i in range(n)] for j in range(n)]
    padding = 10
    s = (WIDTH - padding*2)//n

    x_image = pygame.image.load(r"ex.png")
    x_image = pygame.transform.scale(x_image , (s,s));
    o_image = pygame.image.load(r"o.png")
    o_image = pygame.transform.scale(o_image , (s,s));


    loop = True
    gameover = False
    human_played = False
    winner = False
    restarted = False
    running = True
    turn = "o"
    
    screen = pygame.display.set_mode(SIZE)

    while running:
        mouse_x , mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board,loop,winner,restarted = reset(n)
            if event.type == pygame.MOUSEBUTTONDOWN:
                i = int(mouse_y//s)
                j = int(mouse_x//s)

                if i<n and j<n:
                    if board[i][j]=="":
                        board[i][j] = turn
                        turn = "x" if turn=="o" else "o"
                        human_played = True
                    winner = check_win(board)

        if loop:
            rect(screen, (255, 255, 255), padding, padding, WIDTH-padding*2, HEIGHT-padding*2)
            
            # Logic goes here
            if not winner:
                winner = check_win(board)
            # print(winner)
            if winner:
                if winner == "tie":
                    print(winner.upper()+"!")
                else:
                    print(winner.upper(), "Wins!")
                print("Press 'r' to restart")
                loop = False

            for i in range(n):
                for j in range(n):
                    item = board[i][j]
                    if item == "x":
                        screen.blit(x_image, (j*s+padding, i*s+padding))
                    elif item == "o":
                        screen.blit(o_image, (j*s+padding, i*s+padding))
                    square(screen, (0,0, 0), j*s+padding, i*s+padding, s, 3)

            pygame.display.update()

            if restarted:
                turn = "o"
                restarted = False

            if human_played:
                time.sleep(.5)
                board = best_move(board)
                turn = "o"
                human_played = False
    pygame.quit()

if __name__ == '__main__':
    main()
