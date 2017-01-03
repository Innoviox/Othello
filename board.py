import tkinter as tk

class Tile():
    def __init__(self, color, board, x, y):
        self.board = board
        self.color = color
        self.x = x
        self.y = y
        
        self.label = tk.Label(board.root, width=50, height=50)
        self.label.place_configure(x=x, y=y)
        self.update()
                              
    def flip(self):
        #0 is empty
        #Odds are black
        #Evens are white
        if self.color != 0:
            self.color += 1 #switches even/odd

    def update(self):
        if self.color != 0:
            image = tk.PhotoImage(file="resources/tile{}.gif".format(self.color % 2))
        else:
            image = tk.PhotoImage(file="resources/empty.gif")
        self.label["image"] = image
        self.label.img = image

class Board():
    def __init__(self):
        self.root = tk.Tk()
        self.tiles = []

        for x in range(0, 400, 50):
            for y in range(0, 400, 50):
                self.tiles.append(Tile(0, self, x, y))
if __name__ == "__main__":
    board = Board()
    
