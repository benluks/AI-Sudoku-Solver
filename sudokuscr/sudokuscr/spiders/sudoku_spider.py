"""
sudoku_spider.py
~~~~~~~~~~~~~~~~

Scrapes the site for sudokus, and stores them in an array 
in a JSON file called ```data.json```. To run this, cd 
into the ``sudokuscraper`` directory and run:
'scrapy crawl sudoku -o data.json' ('sudoku' being the name given to 
the spider in the class declaration).
"""

### Libraries
## Third-party libraries
import scrapy
import numpy as np


class SudokuSpider(scrapy.Spider):
    name = "sudoku"

    ### change accordingly depending on
    # desired sample size.
    num_of_data = 100

    start_urls = [
        f'http://nine.websudoku.com/?level=1&set_id={i}' for i in range(num_of_data)
    ]

    def __init__(self):
        self.puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], 
                       ]

    def parse(self, response):
        cells = response.xpath('//input')
        for cell_number in range(81):
            row = int(cell_number / 9)
            column = int(cell_number % 9)
            value = cells[cell_number].xpath('@value').get()
            if value is None:
                self.puzzle[row][column] = 0
            else:
                self.puzzle[row][column] = int(value)
            
        yield {'puzzle': self.puzzle}
