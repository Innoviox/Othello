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
        self.label.bind("<1>", self._onclick)
                                     
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
        self.label.update()
        
    def _onclick(self, *event):
        self.flip()
        self.update()
class Board():
    def __init__(self):
        self.root = tk.Tk()
        self.tiles = []

        for x in range(0, 480, 60):
            for y in range(0, 480, 60):
                self.tiles.append(Tile(1, self, x, y))
if __name__ == "__main__":
    board = Board()
    
