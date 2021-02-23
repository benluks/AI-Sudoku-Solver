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
    num_of_data = 10

    start_urls = [
        f'http://grid.websudoku.com/?level=1&set_id={i}' for i in range(num_of_data)
    ]

    def __init__(self):
        self.puzzle = [0]*81

    def parse(self, response):
        cells = response.xpath('//input')
        values = [cells[cn].xpath('@value').get() for cn in range(81)]
        for i in range(len(values)):
            if values[i] is None:
                values[i] = 0
            else:
                values[i] = int(values[i])

        yield {'puzzle': values}
