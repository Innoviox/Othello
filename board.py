import tkinter as tk

global currPlayer
currPlayer = 2 #white starts


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

    def _reset(self):
        self.color = self._color #reset; move was not legal
        
    def update(self):
        self._color = self.color #update previous color
        if self.color != 0:
            image = tk.PhotoImage(file="resources/tile{}.gif".format(self.color % 2))
        else:
            image = tk.PhotoImage(file="resources/empty.gif")
        self.label["image"] = image
        self.label.img = image
        self.label.update()
        
    def _onclick(self, *event):
        #self.flip()
        if self.color == 0: #Player can only flip empty tile
            self._set(currPlayer)
            if self.board.check():
                self.update()
                global currPlayer
                currPlayer += 1 
            else:
                self._reset()
            
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

    def inRow(self, newIndex, oldIndex, add):
        if newIndex < 0:
            return False
        if newIndex >= len(self.tiles):
            return False
        
        r = oldIndex-4*add, oldIndex+4*add
        if newIndex not in range(min(r), max(r)):
            return False
           
        return True

    def flipRow(self, indexPlayed, colorPlayed, add):
        numFlipped = 0
        flippedTiles = []
        newIndex = indexPlayed + add
        while self.inRow(newIndex, indexPlayed, add) and self.conv(self.tiles[newIndex].color) not in [0, self.conv(colorPlayed)]:
            flippedTile = self.tiles[newIndex]
            flippedTile._set(colorPlayed)
            flippedTiles.append(flippedTile)
            newIndex += add
            
        if self.inRow(newIndex, indexPlayed, add) and self.conv(self.tiles[newIndex].color) == self.conv(colorPlayed):
            for tile in flippedTiles:
                numFlipped += 1
                tile.update()
        else:
            for tile in flippedTiles:
                tile._reset()
        return numFlipped
    
    def check(self):
        tilePlayed = [tile for tile in self.tiles if tile._color != tile.color][0] #Gets tile where previous color is different from current color
                                                                                   #Filter is useless because only looking for one value
        colorPlayed = tilePlayed.color
        indexPlayed = self.tiles.index(tilePlayed)

        numFlipped = sum(self.flipRow(indexPlayed, colorPlayed, add) for add in [-9, -8, -7, -1, 1, 7, 8, 9])

        if numFlipped > 0:
            return True
        return False

    def conv(self, num):
        if num == 0:
            return 0
        if num % 2 == 1:
            return 2
        return 1
        
if __name__ == "__main__":
    board = Board()
    
