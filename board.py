import tkinter as tk

currPlayer = 0

class Tile():
    def __init__(self, color, board, x, y):
        self.board = board
        self._color = color #previous color
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

    def _set(self, color):
        self.color = color

    def reset(self):
        self.color = self._color #reset; move was not legal
        
    def update(self):
        self._color = color #update previous color
        if self.color != 0:
            image = tk.PhotoImage(file="resources/tile{}.gif".format(self.color % 2))
        else:
            image = tk.PhotoImage(file="resources/empty.gif")
        self.label["image"] = image
        self.label.img = image
        self.label.update()
        
    def _onclick(self, *event):
        #self.flip()
        self._set(currPlayer)
        if self.board.check():
            self.update()
            
class Board():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("%dx%d%+d%+d" % (480, 480, 0, 0))
        self.root.config(bg="lightblue")
        self.tiles = []

        for x in range(0, 480, 60):
            for y in range(0, 480, 60):
                self.tiles.append(Tile(0, self, x, y))
                
        #Middle tiles are set up.
        for (index, value) in enumerate([28, 37, 29, 36]):
            self.tiles[value-1].color = index//2+1
            self.tiles[value-1].update()

    def getColors(self):
        return [tile.color for tile in self.tiles]

    def check(self):
        tilePlayed = filter(lambda tile: tile._color != tile.color, self.tiles)[0] #Gets tile where previous color is different from current color
        
        

        
if __name__ == "__main__":
    board = Board()
    
