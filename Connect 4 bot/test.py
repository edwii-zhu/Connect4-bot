from classes import game
from frontend import connect4


a = game()
for i in range(100):
    a.move(int(input("Move? "))-1)
    a.move_bot(3)
    print(a)