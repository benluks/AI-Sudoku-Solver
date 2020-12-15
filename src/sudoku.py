"""
sudoku.py
~~~~~~~~~

The following is an algorithm that solves simple sudokus.

"""

import numpy as np

class Sudoku:
	def __init__(self, puzzle):
        # return given row as list
		self.puzzle = puzzle
	
		self.possibilities = {}
		self.rows = range(len(self.puzzle))
		self.columns = range(len(self.puzzle[0]))
		self.changeInThisIteration = False


	def _row(self, rowNumber):
	    return self.puzzle[rowNumber]

	def _column(self, columnNumber):
	    # return given column as list
	    return[row[columnNumber] for row in self.puzzle]


	def _solveCell(self, rowNumber, columnNumber, answer):
	    self.puzzle[rowNumber][columnNumber] = answer


	def _flattenList(self, listOfLists):
	    # turn list of lists into list
	    flat_list = []
	    for lst in listOfLists:
	        for member in lst:
	            flat_list.append(member)
	    
	    return flat_list


	def _gridFromCoords(self, rowNumber, columnNumber):
	    """
	    Get grid from coordinates
	    """
	    
	    # use math floor to determine which set of 
	    # rows or coumns to use
	    startRow = (rowNumber // 3) * 3
	    startColumn = (columnNumber // 3) * 3
	    
	    rows = self.puzzle[startRow : (startRow + 3)]
	    grid = [row[startColumn : (startColumn + 3)] for row in rows]
	    
	    return self._flattenList(grid)






	def _gatherUnavailableDigitsFromCoord(self, rowNumber, columnNumber):
	    """
	    given a coordinate, gather list of all digits that share a row, 
	    column, or grid with this coordinate
	    """   
	    
	    # gather digits from row, column and grid
	    rowColGridRough = [self._row(rowNumber), self._column(columnNumber), 
	                        self._gridFromCoords(rowNumber, columnNumber)]
	    # flatten list
	    rowColGrid = self._flattenList(rowColGridRough)
	    return list(set(rowColGrid))

	def _gatherPossibleSolutions(self, rowNumber, columnNumber):
	    """
	    Make list of possible solutions for a coordinate
	    """
	    allPossibleDigits = range(1, 10)
	    
	    unavailableDigits = self._gatherUnavailableDigitsFromCoord(rowNumber, columnNumber)
	    availableDigits = [digit for digit in allPossibleDigits 
	                        if (digit != 0 and digit not in unavailableDigits)]

	    return availableDigits

	def _logPossibleSolutionsforCoord(self, rowNumber, columnNumber):
	    """
	    Add key/value pair for coordinate and its possible
	    solutions in 'possibilities' dictionary
	    """
	    self.possibilities[(rowNumber, columnNumber)] = self._gatherPossibleSolutions(rowNumber, columnNumber)


	def _logAllPossibleSolutions(self):
	    """
	    Go through puzzle, find each 0, and log possible solutions
	    in 'possibilities' dictionary
	    """
	    for row in self.rows:
	        for column in self.columns:
	            # iterate through rows and columns,
	            # find 0s
	            if self.puzzle[row][column] == 0:  
	                # log possible solutions to 'possibilities'
	                self._logPossibleSolutionsforCoord(row, column)
	           
	               


	def _computeCoordsFromGridIndex(self, gridIndex):
	    """
	    Given grid index, compute list of coordinates
	    which belong to said grid
	    """
	    #compute starting row and column for given grid
	    startRow = (gridIndex // 3) * 3
	    startColumn = (gridIndex % 3) * 3
	    
	    #list of row and column coordinates
	    rows = range(startRow, startRow + 3)
	    columns = range(startColumn, startColumn + 3)

	    
	    coordsInGrid = []

	    #populate list with coordinates
	    for row in rows:
	        for column in columns:
	            coordsInGrid.append((row, column))

	    return coordsInGrid

	def _possibilitiesGivenGrid(self, gridIndex):
	    """
	    Filter 'possibilities' down to coordinates within given grid
	    """
	    gridPossibilities = {}

	    for coord in self._computeCoordsFromGridIndex(gridIndex):
	        if coord in self.possibilities.keys():
	            gridPossibilities[coord] = self.possibilities[coord]

	    return gridPossibilities



	"""
	If the grid possibilities dictionary shows a digit 
	which is only available to one coordinate, then fill in that 
	coordinate with that possibility
	"""

	def _findSingles(self, gridIndex):
	    """
	    find any digit such that it is only available to one 
	    coordinate in its grid
	    """
	    # take grid dictionary, isolate values, and flatten
	    possibilitiesValues = self._possibilitiesGivenGrid(gridIndex).values()
	    flatListOfPossibilities = self._flattenList(possibilitiesValues)

	    singles = [digit for digit in flatListOfPossibilities 
	                if flatListOfPossibilities.count(digit) == 1]
	    if singles:
	    	self.changeInThisIteration = True

	    
	    return singles

	def _getCoordinatesFromSingles(self, gridIndex):
	    """
	    Get singles from grid and pair them with the coordinates 
	    to which they correspond
	    """

	    coordsAndSingles = {}

	    reference = self._possibilitiesGivenGrid(gridIndex)

	    for single in self._findSingles(gridIndex):
	        for coord in reference:
	            if single in reference[coord]:
	                coordsAndSingles[coord] = single

	    return coordsAndSingles

	def _fillInSinglesFromGrid(self, gridIndex):
	    """
	    Overwrite puzzle, solving singles
	    """
	    coords = self._getCoordinatesFromSingles(gridIndex)

	    for coord in coords:
	        rowNumber = coord[0]
	        columnNumber = coord[1]

	        answer = coords[coord]
	        
	        self._solveCell(rowNumber, columnNumber, answer)

	    

	def fillInSingles(self):
	    """
	    Fill in all singles in entire puzzle
	    """

	    #make sure 'possibilities' is filled out
	    self._logAllPossibleSolutions()

	    for grid in range(0, 9):
	        self._fillInSinglesFromGrid(grid)
	    
	    # clear possibilities for next round
	    self.possibilities.clear()

	def solve(self):
		"""
		Fill in all singles, then see if any changes are available, and if so, go again.
		Repeat until there are no changes to offer (ie. no more singles). Some lines are
		commented out. If you uncomment them, each solving iteration will be printed in your
		terminal, along with its iteration number. By no means necessary, but interesting.
		"""

		# iteration = 0
		isTheSame = False

		while not isTheSame:
	       
			# iteration += 1

			# print('Round {}: \n'.format(iteration))
			# for line in range(0, 9):
			# 	print (self.puzzle[line])
			# print('\n')

			
			self.fillInSingles()

			if not self.changeInThisIteration:
				isTheSame = True
			else:
				self.changeInThisIteration = False

		return self.puzzle

