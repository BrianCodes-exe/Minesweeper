"""
Minesweeper -The Game-
Created with Python
Using Tkinter -A Python GUI Widget Library-

Creators/Contributors - Brian Kim
"""
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Creating a class for the game Minesweeper
class Minesweeper(Tk):

	# Constructor
	def __init__(self, *args, **kargs):
		Tk.__init__(self, *args, **kargs)
		
		# Creating reference to the given tk window
		container = Frame(self)

		# Initialize main window
		self.title('Minesweeper')
		self.resizable(False, False)
		self.iconbitmap(self, default='images\\flagged.ico')

		# Additional Window content display settings
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# Size of display for each difficulty
		self.size = {'beginner': '370x370', 
					 'intermediate': '660x660',
					 'hard': '1235x660',
					 'expert': '1235x825'}

		# Creating a menu bar
		menubar = Menu(self)
		self.config(menu=menubar)

		# The difficulty tab in the menubar
		difficulty = Menu(menubar, tearoff=0)
		menubar.add_cascade(label='Difficulty', menu=difficulty)
		difficulty.add_command(label='Beginner', command=lambda:self.start_game('beginner'))
		difficulty.add_command(label='Intermediate', command=lambda:self.start_game('intermediate'))
		difficulty.add_command(label='Hard', command=lambda:self.start_game('hard'))
		difficulty.add_command(label='Expert', command=lambda:self.start_game('expert'))
		
		# Set default game difficulty as beginner
		self.start_game('beginner')

	# Takes in the parameter difficulty and gets the game difficulty
	def start_game(self, difficulty):
		# Set the size of the window according to difficulty
		self.difficulty = difficulty
		self.set_window_size(difficulty)

		self.setup_game(difficulty)

	# Initialize/Set display size of the window
	def set_window_size(self, difficulty):
		self.geometry(self.size[difficulty])

	# Initialize variables and create the gameboard tiles
	def setup_game(self, difficulty):
		self.correct_flags = 0
		self.num_flags = 0
		self.num_clicks = 0
		self.tile_count = {'beginner': [9, 9, 10],
						   'intermediate': [16, 16, 40],
						   'hard': [16, 30, 99],
						   'expert': [20, 30, 145]}
		self.num_mines = self.tile_count[difficulty][2]

		# Initializa images for the tiles
		self.images = {
			'facingdown': ImageTk.PhotoImage(Image.open('images\\facingdown.png')),
			'flagged': ImageTk.PhotoImage(Image.open('images\\flagged.png')),
			'mine': ImageTk.PhotoImage(Image.open('images\\mine.png')),
		}
		for num in range(9):
			self.images[num] = ImageTk.PhotoImage(Image.open(f'images\\{num}.png'))
		
		# Create and initialize the tiles using a list of dictionaries data structure
		'''
			The tiles will be organized in a list
			Each tile will be a dictionary and consist of...
			
			1. The Button() attribute from tkinter library. Which
			will retrieve event from the user such as a left or
			right click, and will display the blank tile image at first
			but will change image upon the user clicking the button/tile

			2. The coordinates attribute of type dict. This dictionary will 
			consist of two values that will act as a unique primary key of the 
			location of the tile on the board

			3. The hasMine attribute of type boolean. This will
			indicate whether or not the current tile holds a mine

			4. The isFlagged attribute of type boolean. This will
			indicate whether or not the user has flagged this tile

			5. The mines_around attribute of type int. This will indicate
			the number of mines surrounding the current tile if the current
			tile is not a mine

			6. The checked attribute of type boolean. This will be used later
			on in the main algorithm when the program will check the tile and
			the tile around it. This attribute will act as an indicator of whether
			the specific tile has been already checked or not

			--Side note--
			The hasMine is set to a default value of False and the mines_around
			is set to a default value of -1. These attributes will be later on be
			updated accordingly. This is because the program will always ensure
			that the first tile that the user picks will never be a mine or a number
			tile.

		'''
		self.num_row = self.tile_count[difficulty][0]
		self.num_col = self.tile_count[difficulty][1]
		self.tiles = [[0] * self.num_col for _ in range(self.num_row)]
		for row in range(self.num_row):
			for col in range(self.num_col):
				tile = {
				'button': Button(self, image = self.images['facingdown']),
				'coordinates': {
					'row': row,
					'col': col
					},
				'hasMine': False,
				'isFlagged': False,
				'mines_around': -1,
				'checked': False
				}

				tile['button'].bind('<Button-1>', self.on_click_helper(row, col))
				tile['button'].bind('<Button-3>', self.on_flag_helper(row, col))
				tile['button'].grid(row = row+1, column = col)
				
				self.tiles[row][col] = tile
	
	# This function will generate and place the mines in random tiles.
	# It will also always ensure that first picked tile will never have
	# the mine.
	def initialize_mines(self, first_row, first_col):
		# Determine which tiles will contain mines
		self.tiles_with_mines = []
		i = self.num_mines

		while i > 0:
			row = random.randint(0, self.tile_count[self.difficulty][0]-1)
			col = random.randint(0, self.tile_count[self.difficulty][1]-1)

			# Making sure the first picked tile isn't a mine and to make sure mines aren't placed in the same tile multiple times
			if ((row, col) not in self.tiles_with_mines) and ((row,col) != (first_row, first_col)) and ((row,col) not in self.surrounding(first_row, first_col)):
				self.tiles_with_mines.append((row, col))
				i-=1
			else:
				continue

		# Update hasMine attribute accordingly
		for row in range(self.num_row):
			for col in range(self.num_col):
				if (row, col) in self.tiles_with_mines:
					self.tiles[row][col]['hasMine'] = True

		# Check for nearby mines for each tile. Update mine_around attribute
		for row in range(self.num_row):
			for col in range(self.num_col):
				count = 0
				if not self.tiles[row][col]['hasMine']:
					for coord in self.surrounding(row, col):
						if self.tiles[coord[0]][coord[1]]['hasMine']:
							count+=1
					self.tiles[row][col]['mines_around'] = count	

	# This function will create a list of tiles that are surrounding the given tile
	def surrounding(self, row, col):
		surroundings = [(row-1, col-1), (row-1, col), (row-1, col+1), 
					   (row, col-1), (row, col+1), 
					   (row+1, col-1), (row+1, col), (row+1, col+1)]
		
		# Check for out of bounds values
		out_of_bounds = []
		for coord in surroundings:
			if coord[0] < 0 or coord[1] < 0 or coord[0] > self.num_row-1 or coord[1] > self.num_col-1:
				out_of_bounds.append(coord)
		return list(set(surroundings) - set(out_of_bounds))	
	
	# This function contains the main algorithm
	'''
		This algorithm will take in a tile that the user has clicked. Knowing that the tile is not a mine
		the surrounding tiles will be checked. For each tile that is a 'blank' tile or a tile that has no
		mines around it, that tile will be passed into the function recursively to have its surrounding 
		checked. If the checked attribute is True, that tile has already been checked, so the program
		will automatically skip checking that tile again.
	'''
	def check_nearby(self, tile):
		tile['checked'] = True
		tile['button'].config(image = self.images[tile['mines_around']])
		for coord in self.surrounding(tile['coordinates']['row'], tile['coordinates']['col']):
			if self.tiles[coord[0]][coord[1]]['mines_around'] == 0 and not self.tiles[coord[0]][coord[1]]['checked']:
				self.check_nearby(self.tiles[coord[0]][coord[1]])
			else:
				self.tiles[coord[0]][coord[1]]['button'].config(image = self.images[self.tiles[coord[0]][coord[1]]['mines_around']])
				self.tiles[coord[0]][coord[1]]['button'].unbind('<Button-3>')

	# This function gets called when the user left clicks a tile.
	# This function is used as a helper function to pass the
	# clicked tile to the on_click function
	def on_click_helper(self, row, col):
		return lambda Button: self.on_click(self.tiles[row][col])

	# This function gets called when the user right clicks a tile.
	# This function is used as a helper function to pass the
	# clicked tile to the on_flag function
	def on_flag_helper(self, row, col):
		return lambda Button: self.on_flag(self.tiles[row][col])

	# This function plays along with the check_nearby function.
	'''
		This function will take the tile that has been left-clicked on.
		It will first check if it was the first clicked of the game.
			-If so, the function will call initialize_mines function
			to initialize all mines and make sure that the first clicked
			tile isn't a mine.
		Then it will check if the tile itself is a mine
			-If so, the tile will be flipped over, revealing that it is
			a mine. Then will finish the game by calling gameover function
		Then it will check for any blank tiles.
			-If so, the blank tile will be passed to the check_nearby function
			to check its surrounding.
		Then the last choice would be if the tile has at least one mine around it (non-blank)
			-If so, the tile will have the image updated to the correct number of mines
			surrounding that tile.
	'''
	def on_click(self, tile):
		if self.num_clicks == 0:
			self.num_clicks += 1 
			self.initialize_mines(tile['coordinates']['row'], tile['coordinates']['col'])
			self.check_nearby(tile)
		elif tile['hasMine']:
			tile['button'].config(image = self.images['mine'])
			self.gameover(False)
		elif tile['mines_around'] == 0:
			self.check_nearby(tile)
		else:
			tile['button'].config(image = self.images[tile['mines_around']])

	'''
		This is a simple function that takes in the tile that was right clicked.
		It simply checks to see if the user wants to flag the tile or not.
		However, if the user flags all the tiles with a mine, the gameover function
		will be called to congratulate the user.
	'''
	def on_flag(self, tile):

		# If tile is not already flagged
		if not tile['isFlagged']:

			# Change button image and unbind the left click key
			tile['button'].config(image = self.images['flagged'])
			tile['button'].unbind('<Button-1>')
			tile['isFlagged'] = True

			# Check if the tile has a mine and check if user found all mines
			if tile['hasMine'] == True:
				self.correct_flags+=1

				if self.correct_flags == self.num_mines:
					self.gameover(True)

		# If tile is already flagged
		elif tile['isFlagged']:
			tile['button'].config(image = self.images['facingdown'])
			tile['button'].bind('<Button-1>', self.on_click_helper(tile['coordinates']['row'], tile['coordinates']['col']))
			tile['isFlagged'] = False

			if tile['hasMine'] == True:
				self.correct_flags-=1

	def refresh_flag_label(self):
		self.flag_label.config(text = f'Flag: {self.num_flags}')

	'''
		This function will end the game and unbind all buttons. Depending on whether the user has
		won or not, the function will have a messagebox pop up to either congratulate the user
		for finding all the mines, or to notify that the user has clicked on a mine and then reveal
		all the locations of the mines on the board.
	'''
	def gameover(self, won):
		if won:
			messagebox.showinfo(title = 'GAMEOVER', message = 'Congratulations You Win! You have found all the mines!')
		elif not won:
			for row in range(self.num_row):
				for col in range(self.num_col):	
					self.tiles[row][col]['button'].unbind('<Button-1>')
					self.tiles[row][col]['button'].unbind('<Button-3>')		
					if (row, col) in self.tiles_with_mines:
						self.tiles[row][col]['button'].config(image = self.images['mine'])
			messagebox.showinfo(title = 'GAMEOVER', message = 'You Lose! You have clicked on the mine!')


# Instantiation of the Game Minesweeper
app = Minesweeper()

# Show the window through mainloop
app.mainloop()		
