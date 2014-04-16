#Kairavi Chahal
#kchahal@andrew.cmu.edu

import random
from Tkinter import *

def drawScore():
	score = canvas.data.score
	margin = canvas.data.margin
	cx = canvas.data.canvasWidth/2
	canvas.create_text(cx, margin/2, text="Score: %d" % (score))

def rowIsFull(row):
	emptyColor = canvas.data.emptyColor
	for col in xrange(len(row)):
		if (row > 0):
			if (row[col] == emptyColor):
				return False
	return True

def removeFullRows():
	score = canvas.data.score
	board = canvas.data.board
	emptyColor = canvas.data.emptyColor
	newRow = len(board)-1
	fullRows = 0
	for oldRow in xrange(len(board)-1, -1, -1):
		if (rowIsFull(board[oldRow]) == False):
			for col in xrange(len(board[0])):
				board[newRow][col] = board[oldRow][col]
			newRow -= 1
		elif (rowIsFull(board[oldRow]) == True):
			fullRows += 1
	for row in xrange(fullRows):
		for col in xrange(len(board[0])):
			board[row][col] = emptyColor
	score += (fullRows**2)
	canvas.data.score = score
	canvas.data.board = board
	redrawAll()
	

def placeFallingPiece():
	fallingPiece = canvas.data.fallingPiece
	board = canvas.data.board
	fallingPieceRow = canvas.data.fallingPieceRow
	fallingPieceCol = canvas.data.fallingPieceCol
	fallingPieceColor = canvas.data.fallingPieceColor
	for row in xrange(len(fallingPiece)):
		for col in xrange(len(fallingPiece[0])):
			if (fallingPiece[row][col]):
				board[row+fallingPieceRow][col+fallingPieceCol] = fallingPieceColor
	removeFullRows()

def timerFired():
	ignoreThisTimerEvent = canvas.data.ignoreNextTimerEvent
	canvas.data.ignoreNextTimerEvent = False
	if ((canvas.data.isGameOver == False) and (ignoreThisTimerEvent == False)):
		if (moveFallingPiece(canvas, 1, 0) == False):
			placeFallingPiece()
			redrawAll()
			newFallingPiece()
			if (fallingPieceIsLegal() == False):
				canvas.data.isGameOver = True
				cx = canvas.data.canvasWidth/2
				cy = canvas.data.canvasHeight/2
				canvas.create_text(cx, cy, text="Game over!", font=("Helvetica", 32, "bold"), fill="white")
				canvas.create_text(cx, cy+canvas.data.cellSize, text="Press 'r' to restart.", fill="white")
		elif (canvas.data.pause == True):
			ignoreThisTimerEvent = True
	if (ignoreThisTimerEvent == False):
		delay = 500
		canvas.after(delay, timerFired)
	else:
		delay = cancel
		canvas.after(delay, timerFired)

def fallingPieceCenter(piece):
	row = canvas.data.fallingPieceRow + (len(piece)/2)
	col = canvas.data.fallingPieceCol + (len(piece[0])/2)
	return (row, col)

def rotateFallingPiece(fallingPiece):
	oldRows = len(fallingPiece)
	oldCols = len(fallingPiece[0])
	(oldCenterRow, oldCenterCol) = fallingPieceCenter(fallingPiece)
	rRows = oldCols
	rCols = oldRows
	rPiece = []
	for row in xrange(rRows):
		rPiece += [[False]*rCols]
	for row in xrange(rRows):
		for col in xrange(rCols):
			rPiece[rRows-1-row][col] = fallingPiece[col][row]
	(newCenterRow, newCenterCol) = fallingPieceCenter(rPiece)
	canvas.data.fallingPiece = rPiece
	if (fallingPieceIsLegal() == False):
		canvas.data.fallingPiece = fallingPiece
	redrawAll()
	drawFallingPiece()

def fallingPieceIsLegal():
	rows = canvas.data.rows
	cols = canvas.data.cols
	board = canvas.data.board
	fallingPiece = canvas.data.fallingPiece
	fallingPieceRow = canvas.data.fallingPieceRow
	fallingPieceCol = canvas.data.fallingPieceCol
	fallingPieceColor = canvas.data.fallingPieceColor
	emptyColor = canvas.data.emptyColor
	for row in xrange(len(fallingPiece)):
		for col in xrange(len(fallingPiece[row])):
			if (fallingPiece[row][col] == True):
				if (fallingPieceRow+len(fallingPiece)-1 > rows-1) or (fallingPieceCol < 0) or (fallingPieceCol+len(fallingPiece[row])-1 > cols-1) or (board[row+fallingPieceRow][col+fallingPieceCol] != emptyColor):
					return False
	return True

def moveFallingPiece(canvas, drow, dcol):
	canvas.data.fallingPieceRow += drow
	canvas.data.fallingPieceCol += dcol
	moveOccured = True
	if (fallingPieceIsLegal() == False):
		canvas.data.fallingPieceRow = canvas.data.fallingPieceRow - drow
		canvas.data.fallingPieceCol = canvas.data.fallingPieceCol - dcol
		moveOccured = False
	redrawAll()
	drawFallingPiece()
	return moveOccured

def keyPressed(event):
	canvas = event.widget.canvas
	if (event.char == "q"):
		canvas.data.isGameOver = True
		cx = canvas.data.canvasWidth/2
		cy = canvas.data.canvasHeight/2
		canvas.create_text(cx, cy, text="Game over!", font=("Helvetica", 32, "bold"), fill="white")
		canvas.create_text(cx, cy+canvas.data.cellSize, text="Press 'r' to restart.", fill="white")
	elif (event.char == "r"):
		init()
	if (canvas.data.isGameOver == False):
		if (event.keysym == "Left"):
			moveFallingPiece(canvas, 0, -1)
		elif (event.keysym == "Right"):
			moveFallingPiece(canvas, 0, 1)
		elif (event.keysym == "Down"):
			moveFallingPiece(canvas, 1, 0)
		elif (event.keysym == "Up"):
			rotateFallingPiece(canvas.data.fallingPiece)
		elif (event.char == "p"):
			if (canvas.data.pause == True):
				canvas.data.pause = False
			else:
				canvas.data.pause = True

def drawFallingPiece():
	fallingPiece = canvas.data.fallingPiece
	fallingPieceRow = canvas.data.fallingPieceRow
	fallingPieceCol = canvas.data.fallingPieceCol
	fallingPieceColor = canvas.data.fallingPieceColor
	for row in xrange(len(fallingPiece)):
		for col in xrange(len(fallingPiece[0])):
			if (fallingPiece[row][col]):
				drawCell(fallingPiece, row+fallingPieceRow, col+fallingPieceCol, fallingPieceColor)

def newFallingPiece():
	tetrisPieces = canvas.data.tetrisPieces
	tetrisPieceColors = 	canvas.data.tetrisPieceColors
	index = random.randint(0, 6)
	fallingPiece = tetrisPieces[index]
	fallingPieceColor = tetrisPieceColors[index]
	canvas.data.fallingPiece = fallingPiece
	canvas.data.fallingPieceColor = fallingPieceColor
	cols = canvas.data.cols
	fallingPieceRows = len(fallingPiece)
	fallingPieceCols = len(fallingPiece[0])
	fallingPieceRow = 0
	fallingPieceCol = (cols/2) - (fallingPieceCols/2)
	canvas.data.fallingPieceRow = fallingPieceRow
	canvas.data.fallingPieceCol = fallingPieceCol
	canvas.data.fallingPieceRows = fallingPieceRows
	canvas.data.fallingPieceCols = fallingPieceCols
	if (fallingPieceIsLegal() == True):
		drawFallingPiece()

def createFallingPieces():
	iPiece = [[True, True, True, True]]
	jPiece = [[True, False, False], [True, True, True]]
	lPiece = [[False, False, True], [True, True, True]]
	oPiece = [[True, True], [True, True]]
	sPiece = [[False, True, True], [True, True, False]]
	tPiece = [[False, True, False], [True, True, True]]
	zPiece = [[True, True, False], [False, True, True]]
	tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
	tetrisPieceColors = [ "#F17000", "#FA1E1E", "#4BD838", "#5519BF", "#F1FA1E", "#3087FF", "#0F1DD7" ]
	canvas.data.tetrisPieces = tetrisPieces
	canvas.data.tetrisPieceColors = tetrisPieceColors

def drawCell(board, row, col, color):
	margin = canvas.data.margin
	cellSize = canvas.data.cellSize
	left = margin + col * cellSize
	right = left + cellSize
	top = margin + row * cellSize
	bottom = top + cellSize
	canvas.create_rectangle(left, top, right, bottom, fill="black")
	canvas.create_rectangle(left+1, top+1, right-1, bottom-1, fill=color)

def drawBoard():
	board = canvas.data.board
	rows = canvas.data.rows
	cols = canvas.data.cols
	for row in xrange(rows):
		for col in xrange(cols):
			drawCell(board, row, col, board[row][col])

def drawGame():
	canvasWidth = canvas.data.canvasWidth
	canvasHeight = canvas.data.canvasHeight
	canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="white")
	drawBoard()

def redrawAll():
	canvas.delete(ALL)
	drawGame()
	drawScore()

def init():
	pause = False
	score = 0
	rows = canvas.data.rows
	cols = canvas.data.cols
	board = []
	for row in xrange(rows):
		board += [["gray"]*cols]
	canvas.data.board = board
	canvas.data.emptyColor = "gray"
	canvas.data.isGameOver = False
	canvas.data.ignoreNextTimerEvent = False
	canvas.data.score = score
	canvas.data.pause = False
	createFallingPieces()
	redrawAll()
	newFallingPiece()

def run(rows, cols):
	global canvas
	root = Tk()
	root.title("TETRIS")
	margin = 30
	cellSize = 20
	canvasWidth = (cols*cellSize) + (2*margin)
	canvasHeight = (rows*cellSize) + (2*margin)
	canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
	canvas.pack()
	root.resizable(width=0, height=0)
	root.canvas = canvas.canvas = canvas
	class Struct(): pass
	canvas.data = Struct()
	canvas.data.margin = margin
	canvas.data.cellSize = cellSize
	canvas.data.canvasWidth = canvasWidth
	canvas.data.canvasHeight = canvasHeight
	canvas.data.rows = rows
	canvas.data.cols = cols
	init()
	root.bind("<Key>", keyPressed)
	timerFired()
	root.mainloop()

run(15, 10)

#hard drop
#pause
#splash screen
#levels
#piece preview
#high score
