import tkinter as tk

global currPlayer
currPlayer = 2 #white starts

global player1Score, player2Score
player1Score, player2Score = 0, 0

class Tile():
    def __init__(self, color, board, x, y):
        self.board = board
        self._color = color #previous color
        self.color = color
        self.x = x
        self.y = y
        
        self.label = tk.Label(self.board.root, width=50, height=50)
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
            numFlipped = self.board.check()
            if numFlipped:
                self.board.removePossibles()
                self.update()
                global currPlayer, player1Score, player2Score
                if self.conv(currPlayer) == 2:
                    player2Score += numFlipped
                else:
                    player1Score += numFlipped
                print("Player 1: {}\nPlayer 2: {}".format(player1Score, player2Score))
                self.board.updateScore()
                currPlayer += 1
                self.board.cpu.play()
            else:
                self._reset()

    def conv(self, num):
        if num == 0:
            return 0
        if num % 2 == 1:
            return 2
        return 1

class PossibleSpot():
    def __init__(self, board, x, y, num):
        self.board = board
        self.root = board.root
        self.label = tk.Label(self.root)
        self.label["bg"] = '#D8D8D8'
        image = tk.PhotoImage(file='resources/possible.gif')
        self.label['image'] = image
        self.label.img = image
        self.label.place_configure(x=x, y=y)
        self.x = x
        self.y = y
        self.num = num

        self.label.bind("<1>", self._onclick)
        
    def _onclick(self, *event):
        #To make sure that clicking a possible
        #Counts as clicking a tile
        self.board.tiles[self.num]._onclick()
        
class Board():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("%dx%d%+d%+d" % (480, 580, 0, 0))
        self.root.config(bg="lightblue")

        self.tiles = []

        for x in range(0, 480, 60):
            for y in range(0, 480, 60):
                self.tiles.append(Tile(0, self, x, y))
                
        #Middle tiles are set up.
        for (index, value) in enumerate([28, 37, 29, 36]):
            self.tiles[value-1].color = index//2+1
            self.tiles[value-1].update()

        self.scoreLabel = tk.Label(self.root, text="White: 0\nBlack: 0", width=10)
        self.scoreLabel.place_configure(y=480)
        self.updateScore()

        self.cpu = CPU(self)

        self.addPossibles()
        
    def updateScore(self):
        colors = self.getColors()
 #       text = "White: {}\nBlack: {}".format(player1Score, player2Score)
        text = "White Tiles: {}\nBlack Tiles: {}".format(colors.count(2), colors.count(1))
        self.scoreLabel.config(text=text)
        self.scoreLabel['text'] = text
        self.scoreLabel.update()
        
    def getColors(self):
        return [self.conv(tile.color) for tile in self.tiles]


    def __diagonals(self, l):
        rs = l
        d = []
        for i in range(len(rs)):
            d.append([])
            q=i
            for r in rs:
                try:
                    d[i].append(r[q])
                except IndexError:
                    break
                q += 1
        return d
    def _diagonals(self, l):
        #l = self.columns(l)
        d = [[v[d-i] for i,v in enumerate(l) if d-i>=0] for d in range(len(l[0]))]
        d.extend([[v[d-len(l[0])+i+1] for i,v in enumerate(l) if d-len(l[0])+i+1>=0] for d in range(len(l[0]))])
        return d
    def diagonals(self, l):
            diagonals = []
            l = self.columns(l)
            for i in range( len(l[0])+len(l) - 1):
                    diagonal = []
                    for _l in l:
                            if len(_l)>i and i>=0:
                                    diagonal.append(_l[i])
                            i-=1
                    diagonals.append(diagonal)
            diagonals.extend(self._diagonals(l)) #first workaround
            diagonals.extend(self.__diagonals(l)) #second workaround
            #print('\n'.join(str(i) for i in sorted(diagonals)))
            return diagonals
    def columns(self, l):
        return [i for i in zip(*[l[i::8] for i in range(8)])]

    def rows(self, l):
        l = self.columns(l)
        return [[s[i] for s in l] for i in range(len(l))]
    
    def inRow(self, newIndex, oldIndex, add):
        if not self.onBoard(newIndex):
            return False

        if add in [-1, 1]:
            cols = self.columns(range(64))
            for col in cols:
                if oldIndex in col:
                    if newIndex not in col:
                        return False

        elif add in [-8, 8]:
            rows = self.rows(range(64))
            for row in rows:
                if oldIndex in row:
                    if newIndex not in row:
                        return False
        else:
            diags = self.diagonals(range(64))
            for diag in diags:
                if oldIndex in diag and newIndex in diag:
                    return True
            return False
        return True

        
    def onBoard(self, newIndex):
        if newIndex < 0:
            return False
        if newIndex >= len(self.tiles):
            return False
        return True
    
    def flipRow(self, indexPlayed, colorPlayed, add, flip=True, override = False):
        numFlipped = 0
        flippedTiles = []
        newIndex = indexPlayed + add
        
        while self.inRow(newIndex, indexPlayed, add) and \
              self.conv(self.tiles[newIndex].color) not in [0, self.conv(colorPlayed)]:
            if flip or override:
                flippedTile = self.tiles[newIndex]
                flippedTile._set(colorPlayed)
                flippedTiles.append(flippedTile)
            else:
                flippedTiles.append(newIndex)
            newIndex += add

        if self.onBoard(newIndex) and \
           self.conv(self.tiles[newIndex].color) == self.conv(colorPlayed):

            for tile in flippedTiles:
                numFlipped += 1
                if flip or override:
                    tile.update()
        else:
            if flip or override:
                for tile in flippedTiles:
                    tile._reset()
        if not flip:
            return numFlipped#, flippedTiles
        return numFlipped
    
    def check(self, tilePlayed=None, override=False, colorOverride=1):
        if tilePlayed is None:
            tilePlayed = [tile for tile in self.tiles if tile._color != tile.color][0] #Gets tile where previous color is different from current color                                                                                          #Filter is useless because only looking for one value
            colorPlayed = tilePlayed.color
            indexPlayed = self.tiles.index(tilePlayed)
            flip = True
        else:
            indexPlayed = tilePlayed
            colorPlayed = colorOverride
            flip = False
            
        numFlipped = sum(self.flipRow(indexPlayed, colorPlayed, add, flip, override) for add in [-9, -8, -7, -1, 1, 7, 8, 9])

        if numFlipped > 0:
            return numFlipped
        return False

    def conv(self, num):
        if num == 0:
            return 0
        if num % 2 == 1:
            return 2
        return 1

    def addPossibles(self):
        self.removePossibles()
        self.possibles = []
        for i in range(64):
            if self.tiles[i].color == 0 and self.check(tilePlayed=i, colorOverride=2):
                self.possibles.append(PossibleSpot(self, (i//8)*60+10, (i%8)*60+10, i))
                    
    def removePossibles(self):
        try:
            for possible in self.possibles:
                possible.label.destroy()
        except AttributeError: pass
        
class CPU():
    def __init__(self, board):
        self.board = board
        self.color = 1

    def play(self):
        self.board.removePossibles()
        allPlays = {}
        for i in range(64):
            if self.board.tiles[i].color == 0:
                allPlays[i] = self.board.check(tilePlayed=i)

        plays = {}
        for (i, v) in allPlays.items():
            if v != False:
                plays[i] = v

        try:
            bestspot = [i for i in plays.keys() if plays[i] == max(plays.values())][0]
        except IndexError: pass
            #print("Game over!")
            #colors = self.board.getColors()
            #print(colors.count(1), colors.count(2))
            #raise SystemExit
        numFlipped = self.board.check(bestspot, override=True) #override overriden functionality :)
        t = self.board.tiles[bestspot] #check doesn't flip tile that was clicked
        t.color = 1
        t.update()
        print(bestspot)
        global currPlayer, player1Score, player2Score
        if self.board.conv(currPlayer) == 2:
            player2Score += numFlipped
        else:
            player1Score += numFlipped
        print("Player 1: {}\nPlayer 2: {}".format(player1Score, player2Score))
        colors = self.board.getColors()
        print("White Tiles: {}\nBlack Tiles: {}".format(colors.count(2), colors.count(1)))
        currPlayer += 1

        self.board.addPossibles()

            
        
        
if __name__ == "__main__":
    board = Board()
    
