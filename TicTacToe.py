def display_board(board):
    print(board[7],'|',board[8],'|',board[9])
    print('--|---|--')
    print(board[4],'|',board[5],'|',board[6])
    print('--|---|--')
    print(board[1],'|',board[2],'|',board[3])

def win(board):
    if board[1] == board[5] and board[1] == board[9] and board[5] == board[9]:
        return True
    elif board[7] == board[3] and board[7] == board[5] and board[5] == board[3]:
        return True
    elif board[7] == board[8] and board[7] == board[9] and board[9] == board[8]:
        return True
    elif board[4] == board[5] and board[6] == board[5] and board[4] == board[6]: 
        return True
    elif board[1] == board[3] and board[2] == board[3] and board[1] == board[2]:
        return True    
    elif board[7] == board[4] and board[7] == board[1] and board[1] == board[4]:
        return True    
    elif board[5] == board[8] and board[8] == board[2] and board[5] == board[2]:
        return True   
    elif board[3] == board[6] and board[6] == board[9] and board[3] == board[9]:
        return True    
    else:
        return False
        
def player(taken_symbols):
    print('Game has 2 players!')
    while True:
        choice = input('Player 1 pick X or O\n')
        if choice not in ['X', 'O']:
            print('Please pick X or O!')    
        else:
            taken_symbols.remove(choice)
            break       
    return choice

def decision():
    loop = True
    while loop:
        board = [0,1,2,3,4,5,6,7,8,9]
        board2 = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        taken_symbols = ['X','O']
        choice1 = player(taken_symbols)
        print('Pick where to play')
        count = 0
        rng = [1,2,3,4,5,6,7,8,9]
        display_board(board)
        one = True
        two = True
        while two: 
            while(one):
                print('Your turn player 1')
                decision1 = int(input('Imagine as numpad and input corresponding number like shown above: '))
                if decision1 not in rng:
                    print("Out of range")
                    break
                else:    
                    rng.remove(decision1)
                    board[decision1] = choice1
                    board2[decision1] = choice1
                    display_board(board2)
                    count += 1 
                    if win(board):
                        two = False
                        break
                    elif count == 9:
                        two = False
                        break
                    one = False    
            while(not one):
                print('Your turn player 2')
                decision2 = int(input('Imagine as numpad and input corresponding number like shown above: '))
                if decision2 not in rng:
                    print("Out of range")
                    break
                else:    
                    rng.remove(decision2)
                    choice2 = taken_symbols[0]
                    board[decision2] = choice2
                    board2[decision2] = choice2
                    display_board(board2)
                    count += 1  
                    if win(board):
                        two = False
                        break
                    elif count == 9:
                        two = False
                        break
                    one = True    

        if win(board):
            if board.count(choice1) > board.count(choice2):
                print('Player 1 wins!')
            else:    
                print('Player 2 wins!')
        else:
            print('Draw')
            
        x = input('Would you like to restart or end the game?\n')
        if x == 'restart':
            continue
        elif x == 'end':
            loop = False
        else:
            'Please type restart or end'
                            

def main():
    print("Welcome to TicTacToe")
    decision()

main()            