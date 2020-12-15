"""
sudoku_loader.py
~~~~~~~~~~~~~~~~

This is the file that processes the sudokus scraped from the web.
It uses the sudoku.py module to solve the sudokus, and stores the unsolved 
and solved sudokus in the ``training_data`` file. ``training_data``
is one tuple, with two elements. The first is an array with as many items as
there are sudokus in ```data.json```. Each item is itself a 2D array, containing 
a matrix representation of a sudoku. The second element in the ```training_data```
tuple is an array of equal length, containing the solved sudokus, the indices of 
which corresponding to their respective unsolved counterparts in the first tuple item.

"""
### Libraries
## my libraries
from sudoku import Sudoku

## standard libraries
import json
import copy

# third party libraries
import numpy as np

def load_data():
    """
    Open and return data from ```data.json``` file.
    """
    with open('../sudokuscraper/data.json', 'r') as f:
        data=f.read()

    training_examples = json.loads(data)
    return training_examples




def create_data_tuples():
    """
    This function takes the loaded data, solves the puzzles,
    and creates a tuple with the unsolved-- and solved sudokus
    as described above.
    """
    
    sudokus = [sudoku['puzzle'] for sudoku in load_data()]

    solved_sudokus = []
    for old_sudoku in sudokus:
        sudoku = copy.deepcopy(old_sudoku)
        sud = Sudoku(sudoku)
        solved_sud = sud.solve()
        solved_sudokus.append(solved_sud)

    return (sudokus, solved_sudokus)

def write_data_to_file():
    """
    This stores the data tuple from the above function 
    in a file, to have at our disposal for use in the
    neural network.
    """
    with open("sudoku_loader", "w") as f:
        f.write(str(create_data_tuples()))

def vectorize_data():
    """
    For our purposes, it may be useful to have the data
    represented as an n*1 dimensional vector. This function
    converts the tuple from ```create_data_tuple()``` into that 
    """

    data_tuples = create_data_tuples()
    
    unsolved_vectors, solved_vectors = reshape_sudokus(data_tuples[0]), reshape_sudokus(data_tuples[1])

    return (unsolved_vectors, solved_vectors)

def reshape_sudokus(sudokus):
    return [np.reshape(sudoku, (81, 1)) for sudoku in sudokus]
