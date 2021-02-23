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
    with open('../sudokuscraper/sudokuscraper/scrapes.json', 'r') as f:
        data=f.read()

    training_examples = json.loads(data)
    return training_examples




def create_data_tuples():
    """
    This function takes the loaded data, solves the puzzles,
    and creates a tuple with the unsolved-- and solved sudokus
    as described above.
    """
    
    sudokus = np.array([sudoku['puzzle'] for sudoku in load_data()])
    solved_sudokus  = copy.deepcopy(sudokus)
    
    solved = [Sudoku(sudoku) for sudoku in solved_sudokus]
    solved = np.array([sudoku.solve() for sudoku in solved])
    
    return(sudokus, solved_sudokus)



def flatten_sudokus(sudokus):
    """
    Input is a list of training examples and output
    is the same list flattened to 2 dimensions: (m, 81)
    """
    return sudokus.reshape(-1, 81)

def write_data_to_file():
    """
    This stores the data tuple from the above function 
    in a file, to have at our disposal for use in the
    neural network.
    """
    sudokus, solved_sudokus = create_data_tuples()
    X = flatten_sudokus(sudokus)
    Y = flatten_sudokus(solved_sudokus)

    np.savetxt('./inputs.csv', X, delimiter=',')
    np.savetxt('./outputs.csv', Y, delimiter=',')




if __name__ == '__main__':
    write_data_to_file()