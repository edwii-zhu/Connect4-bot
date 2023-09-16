from copy import deepcopy as copy
from dicts import wins, coord_win

class board(object):
    def __init__(self, state = [[None for i in range(7)] for j in range(6)], past_board = None):
        self.player: int; self.adv: float;self.p_board: board #Defining the types of the board attributes
        self.state = state
        self.p_board = past_board
        self.player = 1
        self.wins = [None, wins(), wins()] # Index indicates the player it belongs to
        self.coord_win = coord_win()
        self.score = 0
        self.won = False
        
    def __repr__(self): # Representing the board as a string
        rep = ""
        for row in self.state:
            rep = rep + str(row) + "\n"
        return rep
    
    def __gt__(self, other):
        return True
    
    def check_player(self): #Determine who's turn it is to play and returns the player (1 or 2)
        if self.p_board == None or self.p_board.player == 2:
            player = 1
        else:
            player = 2
        self.player = player
    
    def check_possible_moves(self): # Returns a list of possible moves if there is any, otherwise, print the draw
        pml = [] # pvm stands for possible moves list
        for i in range(7):
            if self.state[0][i] == None:
                pml.append(i)
        if self.won is True:
            return []
        if pml != []:
            return pml
        else:
            print("It seems it is a draw")
            return []
    
    def check_win(self, coord):
        player = self.player 
        other = 1 if self.player == 2 else 2
        for w in self.coord_win[coord]:
            try:
                # Editing wins
                self.wins[player][w] += 1
                #Updating score
                self.score = self.score + 1 if player == 1 else self.score - 1
                # Detecting Win
                if self.wins[player][w] == 4:
                    self.score = 9999 if player == 1 else -9999
                    self.won = True
                    return True
            except KeyError:
                pass
            try:
                if self.player == 1:
                    self.score += self.wins[other].pop(w)
                else:
                    self.score -= self.wins[other].pop(w)
            except KeyError:
                pass
    
    def refresh(self, coord):
        self.check_win(coord)
        self.check_player()
    
    def move_b(self, column):
        current = copy(self)
        for row in range(6)[::-1]:
            if current.state[row][column] == None:
                current.state[row][column] = current.player
                current.p_board = self
                current.refresh((row, column))
                return current
            
class tree():
    def __init__(self, origin, bd, minmax):
        self.board: board
        self.minmax = minmax # True if max, False if min
        self.score = None
        self.score_board = None
        self.origin = origin
        self.board = bd
        self.children = []
    
    def add_children(self, child):
        self.children.append(child)
    
    def add_score(self, score, board, player):
        if self.score == None:
            self.score = score
            self.score_board = board
        elif player == 1:
            if self.minmax and self.score < score:
                self.score = score
                self.score_board = board
            elif (not self.minmax) and self.score > score:
                self.score = score
                self.score_board = board
        elif player == 2:
            if self.minmax and self.score > score:
                self.score = score
                self.score_board = board
            elif (not self.minmax) and self.score < score:
                self.score = score
                self.score_board = board
    
    def __repr__(self):
        st = f"{self.score}\n"
        return st
        
            
        
        
        
class game():
    def __init__(self): # Contains the current board in play
        self.board: board
        self.board = board()
        self.coord_win = coord_win()
        self.turn = 1
        
    def __repr__(self): # Returns the representation of the current board
        return self.board.__repr__()
    
    def move(self, column): # lets you make a move by inputting the column
        self.turn += 1
        current = copy(self.board)
        if column in current.check_possible_moves():
            for row in range(6)[::-1]:
                if current.state[row][column] == None:
                    current.state[row][column] = current.player
                    current.p_board = self.board
                    current.refresh((row, column))
                    self.board = current
                    break
        else:
            raise ValueError("This move cannot be done")

    def move_bot(self, DEPTH): #Minmax algorithm to determine best move
        # Edge Case
        edge_case_check = False
        # Creating tree
        current = copy(self.board)
        tr = tree(None, current, True)
        parent = tr
        ls = [tr]
        for i in range(1, DEPTH + 1):
            new_ls = []
            for bds in ls:
                bds: tree
                parent = bds
                if bds.board.won:
                    new_ls.append(bds)
                else:
                    for column in bds.board.check_possible_moves():
                        lost = False
                        turn2_ls = []
                        result = bds.board.move_b(column)
                        child = tree(parent, result, i%2 == 0)
                        if i == 1 and result.won:
                            self.board = result
                            return
                        if i != 2:
                            # Edge case
                            if edge_case_check is False:
                                if self.board.state[-1][3] == 1 and self.board.state[-1][4] == 1 and self.board.state[-1][2] == None and self.board.state[-1][5] == None:
                                    self.move(5)
                                    return
                                if self.board.state[-1][3] == 1 and self.board.state[-1][2] == 1 and self.board.state[-1][1] == None and self.board.state[-1][4] == None:
                                    self.move(1)
                                    return
                                edge_case_check = True
                            # --------------------------
                        # Stupid mistake preventer
                            new_ls.append(child)
                        else:
                            if result.won:
                                lost = True
                                break
                            else:
                                turn2_ls.append(child)
                    if not lost:
                        for ch in turn2_ls:
                            new_ls.append(ch)
                            # -----------------------------                    
            ls = new_ls
        # Searching through Tree:
        for child in ls:
            child.score = child.board.score
        if not ls:
            self.board = current.move_b(current.check_possible_moves()[0])
            return
        while ls[0].origin != None:
            new_ls = []
            for child in ls:
                new_ls.append(child.origin)
                if child.origin == None:
                    self.board = child.score_board
                    return
                child.origin.add_score(child.score, child.board, self.board.player)
            ls = new_ls
        # Updating game
        self.board = tr.score_board
        if self.board.won:
            print(f"Player {self.board.player} has won!")
            exit()


                