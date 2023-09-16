'''
Used to build the dictionaries in dicts.py
'''
wins = {} # Maps win pattern with filled square
coord_win = {} # Matches coordinate with winning pattern


for column in range(7):
    for row in range(6):
        ls = []
        # Horizontal
        if -1 < column < 4:
            ls.append(f"H{row}_0")
        if 0 < column < 5:
            ls.append(f"H{row}_1")
        if 1 < column < 6:
            ls.append(f"H{row}_2")
        if 2 < column < 7:
            ls.append(f"H{row}_3")
        # Vertical
        if -1 < row < 4:
            ls.append(f"V0_{column}")
        if -2 < row < 5:
            ls.append(f"V1_{column}")
        if -3 < row < 6:
            ls.append(f"V2_{column}")
        coord_win[(row, column)] = ls

# Vertical win patterns
for column in range(7):
    for row in range(3):
        wins[f"V{row}_{column}"] = 0
# Horizontal win patterns
for row in range(6):
    for column in range(4):
        wins[f"H{row}_{column}"] = 0
# Diagonal up and down win patterns
for row in range(3):
    for column in range(4):
        wins[f"DU{row}_{column}"] = 0
        wins[f"DD{row}_{column}"] = 0
        for i in range(4):
            coord_win[(row + i, column + i)].append(f"DU{row}_{column}")
            coord_win[(row+i), column + 3-i].append(f"DD{row}_{column}")
        