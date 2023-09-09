import random
import math
from prettytable import PrettyTable
from reportlab.lib import colors
from reportlab.lib import pagesizes
from reportlab.lib.pagesizes import portrait, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class WordFindPuzzleGenerator:
    def __init__(self, rows, cols, current_word_list, current_font_size, current_title_size, debug):
        self.rows = rows
        self.cols = cols
        self.debug = debug

        # initialize lists
        self.placed_words = []
        self.placement_info = []
        self.remaining_words = current_word_list.copy()
        self.words_not_placed = []

        # Initializes the empty grid
        self.grid = [['' for _ in range(cols)] for _ in range(rows)]

        # Defin the table cell size
        self.cell_width = 20
        self.cell_height = 20

        # initialize font size variables
        self.font_size = -1
        self.title_font_size = -1

    # function to set font size
    def set_font_size(self, font_size, title_size):
        print("Entering set_font_size method")
        print(f'Font Size: {self.font_size}')
        print(f'Title Font Size: {self.title_font_size}')
        
        sizes = {
            'XS': 10,
            'S': 12,
            'M': 16,
            'L': 20,
            'XL': 24,
            'XXL': 28
        }
        if font_size in sizes:
            self.font_size = sizes[font_size]
        else:
            self.font_size = sizes['L'] # Default to 'L' if the size is not recognized

        title_sizes = {
            'XS': 'S',
            'S': 'M',
            'M': 'L',
            'L': 'XL',
            'XL': 'XXL'
        }
        if title_size in title_sizes:
            self.title_font_size = sizes[title_sizes[title_size]]
        else:
            self.title_font_size = sizes[title_sizes['L']] # Default to 'M' for title size

        # debug info: Print font sizes
        if self.debug:
            print(f'Font Size: {self.font_size}')
            print(f'Title Font Size: {self.title_font_size}')

    # function: fill grid with empty strings
    def fill_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = ''

    # function: replace empty strings with random letters
    def fill_grid_random(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == '':
                    self.grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # function: validate grid is able to accomodate all words
    def grid_all_word_validation(self):
        total_word_length = sum(len(word) for word in self.remaining_words)
        if total_word_length > self.rows * self.cols:
            raise ValueError("Error: Grid size is too small to accommodate all words.")

    # function: validate if word can be placed
    def can_place_word(self, word, row, col, direction):
        if direction == "horizontal":
            return self._can_place_horizontal(word, row, col)
        elif direction == "horizontal_backward":
            return self._can_place_horizontal_backward(word, row, col)
        elif direction == "vertical":
            return self._can_place_vertical(word, row, col)
        elif direction == "vertical_upward":
            return self._can_place_vertical_upward(word, row, col)
        elif direction == "diagonal_tl_br":
            return self._can_place_diagonal_tl_br(word, row, col)
        elif direction == "diagonal_tr_bl":
            return self._can_place_diagonal_tr_bl(word, row, col)
        elif direction == "diagonal_bl_tr":
            return self._can_place_diagonal_bl_tr(word, row, col)
        elif direction == "diagonal_br_tl":
            return self._can_place_diagonal_br_tl(word, row, col)
        else:
                raise ValueError("Invalid direction")

    # can_place_word helper function: to validate horizontal word placement
    def _can_place_horizontal(self, word, row, col):
        max_col = self.cols - len(word)
        return col + len(word) <= self.cols and all(self.grid[row][col + i] == '' or self.grid[row][col + i] == word[i] for i in range(len(word)))

    # can_place_word helper function: to validate horizontal_backward word placement
    def _can_place_horizontal_backward(self, word, row, col):
        max_col = self.cols - len(word)
        return col >= len(word) - 1 and all(self.grid[row][col - i] == '' or self.grid[row][col - i] == word[i] for i in range(len(word)))

    # can_place_word helper function: to validate vertical word placement
    def _can_place_vertical(self, word, row, col):
        max_row = self.rows - len(word)
        return row + len(word) <= self.rows and all(self.grid[row + i][col] == '' or self.grid[row + i][col] == word[i] for i in range(len(word)))

    # can_place_word helper function: to validate vertical upward word placement
    def _can_place_vertical_upward(self, word, row, col):
        max_row = self.rows - len(word)
        return row >= len(word) - 1 and all(self.grid[row - i][col] == '' or self.grid[row - i][col] == word[i] for i in range(len(word)))

    # can_place_word helper function: to validate diagonal TL -> BR word placement
    def _can_place_diagonal_tl_br(self, word, row, col):
        return (
            row + len(word) <= self.rows and col + len(word) <= self.cols and
            all(self.grid[row + i][col + i] == '' or self.grid[row + i][col + i] == word[i] for i in range(len(word)))
            )

    # can_place_word helper function: to validate diagonal TR -> BL word placement
    def _can_place_diagonal_tr_bl(self, word, row, col):
        return (
            row + len(word) <= self.rows and col >= len(word) - 1 and
            all(self.grid[row + i][col - i] == '' or self.grid[row + i][col - i] == word[i] for i in range(len(word)))
        )

    # can_place_word helper function: to validate diagonal BL -> TR word placement
    def _can_place_diagonal_bl_tr(self, word, row, col):
        return (
            row >= len(word) - 1 and col + len(word) <= self.cols and
            all(self.grid[row - i][col + i] == '' or self.grid[row - i][col + i] == word[i] for i in range(len(word)))
        )

    # can_place_word helper function: to validate diagonal BR -> TL word placement
    def _can_place_diagonal_br_tl(self, word, row, col):
        return (
            row >= len(word) - 1 and col >= len(word) - 1 and
            all(self.grid[row - i][col - i] == '' or self.grid[row - i][col - i] == word[i] for i in range(len(word)))
        )

    # fuction: place word in grid
    def place_word(self, word, row, col, direction):
        # initializing 
        start_row = 0
        start_col = 0
        end_row = 0 
        end_col = 0
        word_length = len(word)

        word = word.upper()  # convert word to upper case
        if direction == "horizontal":
            for i in range(len(word)):
                self.grid[row][col + i] = word[i]
            start_row, start_col = row, col
            end_row, end_col = row, col + word_length - 1
        elif direction == "horizontal_backward":
            for i in range(len(word)):
                self.grid[row][col - i] = word[i]
            start_row, start_col = row, col - word_length + 1
            end_row, end_col = row, col
        elif direction == "vertical":
            for i in range(len(word)):
                self.grid[row + i][col] = word[i]
                start_row, start_col = row, col
                end_row, end_col = row + word_length - 1, col
        elif direction == "vertical_upward":
            for i in range(len(word)):
                self.grid[row - i][col] = word[i]
                start_row, start_col = row, col
                end_row, end_col = row - word_length + 1, col
        elif direction.startswith("diagonal"):
            if direction == "diagonal_tl_br":
                for i in range(len(word)):
                    self.grid[row + i][col + i] = word[i]
                    start_row, start_col = row, col
                    end_row = row + word_length - 1
                    end_col = col + word_length - 1
            elif direction == "diagonal_tr_bl":
                for i in range(len(word)):
                    self.grid[row + i][col - i] = word[i]
                    start_row, start_col = row, col
                    end_row = row + word_length - 1
                    end_col = col - word_length + 1
            elif direction == "diagonal_bl_tr":
                for i in range(len(word)):
                    self.grid[row - i][col + i] = word[i]
                    start_row, start_col = row, col
                    end_row = row - word_length + 1
                    end_col = col + word_length - 1
            elif direction == "diagonal_br_tl":
                for i in range(len(word)):
                    self.grid[row - i][col - i] = word[i]
                    start_row, start_col = row, col
                    end_row = row - word_length + 1
                    end_col = col - word_length + 1

        # Print word with placement info for debugging
        if self.debug:  # Check if debugging is enabled
            human_start_row = start_row + 1
            human_start_col = start_col +1
            human_end_row = end_row + 1
            human_end_col = end_col + 1
            print(f"Placed word '{word}' starts at ({human_start_row}, {human_start_col}) and ends at ({human_end_row}, {human_end_col}) for direction '{direction}'")

        self.placement_info.append((word, start_row, start_col, end_row, end_col, direction))

    # function: Generate all possible positions for a word in a specific direction
    def possible_positions(self, word, direction):
        positions = []
        for row in range(self.rows):  
            for col in range(self.cols):  
                if self.can_place_word(word, row, col, direction):  
                    positions.append((row, col))
        
        # Print possible psoitions for debugging
        if self.debug:  # Check if debugging is enabled
            print(f'word to be plced: {word}')
            print(f'Generated Possible Positions')
            print(f'{positions}')

        return positions

    # function: Backtracing algorithm for proper word placement
        # Shuffling the directions and positions for equal distribution of words
    def backtracing_word_placement(self, word_index, words_not_placed, remaining_words):
        if word_index == len(remaining_words):
            return True

        # remove spaces from word while seting the word
        original_word = self.remaining_words[word_index]
        word = self.remaining_words[word_index].replace(" ", "")

        # Skip blank words
        if not word.strip():
            self.remaining_words.remove(word)
            return self.backtracing_word_placement(word_index, words_not_placed, remaining_words)

        directions = [
            "horizontal", "horizontal_backward",
            "vertical", "vertical_upward",
            "diagonal_tl_br", "diagonal_tr_bl", "diagonal_bl_tr", "diagonal_br_tl"
        ]
        random.shuffle(directions) # shuffle directions

        word_placed = False

        for direction in directions:
            positions = self.possible_positions(word, direction)
            random.shuffle(positions) # shuffle positions

            for row, col in positions:
                if self.can_place_word(word, row, col, direction):
                    self.place_word(word,row,col, direction)
                    self.placed_words.append(word)
                    self.remaining_words.remove(original_word)

                if self.backtracing_word_placement(word_index + 1, words_not_placed, remaining_words):
                    return True

                self.clear_cells(row, col, direction, len(word))
                self.placed_words.pop()
                self.remaining_words.append(word)

        if not word_placed:
            self.words_not_placed.append(word)

        return False

    # function: Remove words by clearing cells if not properly placed
    def clear_cells(self, row, col, direction, word_length):
        if direction == "horizontal":
            for i in range(word_length):
                self.grid[row][col + i] = ''
        elif direction == "horizontal_backward":
            for i in range(word_length):
                self.grid[row][col - i] = ''
        elif direction == "vertical":
            for i in range(word_length):
                self.grid[row + i][col] = ''
        elif direction == "vertical_upward":
            for i in range(word_length):
                self.grid[row - i][col] = ''
        elif direction == "diagonal_tl_br":
            for i in range(word_length):
                self.grid[row + i][col + i] = ''
        elif direction == "diagonal_tr_bl":
            for i in range(word_length):
                self.grid[row + i][col - i] = ''
        elif direction == "diagonal_bl_tr":
            for i in range(word_length):
                self.grid[row - i][col + i] = ''
        elif direction == "diagonal_br_tl":
            for i in range(word_length):
                self.grid[row - i][col - i] = ''

    # function: generate word find puzzle
    def generate_puzzle(self, current_word_list):

        # fill the grid with empty strings
        self.fill_grid()

        # place the words in the empty grid using backtracing
        self.backtracing_word_placement(0, self.words_not_placed, self.remaining_words)

        # fill the grid with random letters
        self.fill_grid_random()

        # Print grid for debuging [if enabled]
        if self.debug:
            for row in self.grid:
                print(' '.join(row))

            if self.placed_words:
                print(f"Words placed successfully ({len(self.placed_words)} words):", ", ".join(self.placed_words))
            if self.words_not_placed:
                print("Words not placed:", ", ".join(self.words_not_placed))

    # function: generate readable table from the grid using PrettyTable
    def generate_pretty_table(self):
        table = PrettyTable(border=False, header=False, align="c", valign="b", padding_width=1)

        # add columns to thble [must equal the number of columns in the grid]
        for _ in range(
            self.cols):
            table.add_column("", [""] * self.rows)

        # Populate the table with the letters from the grid
        for i in range(self.cols):
            for j in range(self.cols):
                table._rows[i][j] = self.grid[i][j]

        # Debug info: Print Table, and row/column counts
        if self.debug:
            # terminal output
            print("Generated PrettyTable:")
            print(table)
            print(f"Number of columns: {table.field_names}")
            print(f"Number of rows: {len(table._rows)}")

            # text document output
            with open("/Users/HA/Desktop/word_find_puzzle.txt", "w") as file:
                file.write(str(table))
                file.write("\n")  # Add this line to write a newline character
                file.write(f"Number of columns: {table.field_names}\n")  # Add this line to write a newline character
                file.write(f"Number of rows: {len(table._rows)}\n")  # Add this line to write a newline character

        return table

    # function: generate pdf for puzzle
    def generate_pdf(self, title, word_list, pdf_path, c):
        
        ### START Page Setup ###

        # set the font
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        font = "DejaVuSans"

        # set the margins (1 inch = 72 points)
        top_margin = 72
        bottom_margin = 72
        left_margin = 72
        right_margin = 72

        # calculate the effective page size with margins
        pagesize_with_margines = (
            pagesizes.letter[0] - left_margin - right_margin,
            pagesizes.letter[1] - top_margin - bottom_margin
        )
        # debug info: Print font sizes
        if self.debug:
            print(f'Effective page width: {pagesize_with_margines[0]}')
            print(f'Effective page height: {pagesize_with_margines[1]}')

        ### END Page Setup ###

        ### START Title Processing ###

        # Set title font size

        c.setFont(font, self.title_font_size)

        # debug info: Print font sizes
        if self.debug:
            print(f'Font Size: {self.font_size}')
            print(f'Title Font Size: {self.title_font_size}')

        # Remove the quote marks (") from the title
        title = title.replace('"', '')

        if self.debug:
            print(f'Title: {title}')

        # calculate the title width
        title_width = c.stringWidth(title, font, self.title_font_size)

        # debug info: Print the title width
        if self.debug:
            print(f"Title width: {title_width}")

        # Calculate the x coordinate for centering the title
        title_x = (letter[0] - title_width) / 2

        # debug info: Print the title x-coordinate
        if self.debug:
            print(f"Title x-cordinate: {title_x}")

        # Set title y coordinate
        title_y = 750

        # debug info: Print the title y-coordinate
        if self.debug:
            print(f"Title y-cordinate: {title_y}")

        # Draw the centered title on the page
        c.drawString(title_x, title_y, title)  # Adjust the y-coordinate (750) as needed

        ### END Title Processing ###

        ### START Grid Processing ###

        # set grid/word list font size
        c.setFont(font, self.font_size)

        # Calculate the grid width and height
        grid_width = self.cols * self.cell_width
        grid_height = self.rows * self.cell_height

        # debug info: Print the grid width & height
        if self.debug:
            print(f"Grid Width: {grid_width}")
            print(f"Grid Height: {grid_height}")

        # calculate the offsets for centering the grid
        horizontal_offset = (pagesize_with_margines[0] - grid_width) / 2
        vertical_offset = (pagesize_with_margines[1] - grid_height) / 2 # + 0 Adjust the value as needed to offset the Y-coordinate

        # debug info: Print the horizontal & vertical offset
        if self.debug:
            print(f"horizontal Offset: {horizontal_offset}")
            print(f"Vertical Offset: {vertical_offset}")

        # calculate the starting coordinates for the grid
        grid_x = left_margin + horizontal_offset
        grid_y = title_y - top_margin * 2 - vertical_offset - self.title_font_size 
        # old: grid_y = bottom_margin + vertical_offset

        # debug info: Print the starting coordinates
        if self.debug:
            print(f"Grid starting X: {grid_x}")
            print(f"Grid starting y: {grid_y}")

        # Darw the centered grid
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell_value in enumerate(row):

                # calculate the center of the cell
                cell_center_x = grid_x + col_idx * self.cell_width + self.cell_width / 2
                cell_center_y = grid_y + (self.rows - row_idx - 1) * self.cell_height + self.cell_height / 2

                x = cell_center_x - c.stringWidth(cell_value, font, self.font_size) / 2
                y = cell_center_y - self.font_size / 2
                c.drawString(x, y, cell_value)

        # debug info: draw parameters
        if self.debug:
            print(f'Cell center x-coordinate: {cell_center_x}')
            print(f'Cell center y-coordinate: {cell_center_y}')
            print(f'Grid x-coordinate: {x}')
            print(f'Grid y-coordinate: {y}')

        # Set border perameters
        c.setStrokeColorRGB(0, 0, 0) # adjust for color
        c.setLineWidth(2) # adjust for thingness

        # calculate the starting coordinates for the boarder
        border_x = grid_x - self.cell_width / 1.75
        border_y = grid_y - self.cell_height / 1.75

        # debug info: border start coordinates
        if self.debug:
            print(f'Border starting x-coordinate: {border_x}')
            print(f'Border starting y-coordinate: {border_y}')

        # Draw a boarder around the grid
        c.rect(border_x, border_y, grid_width + self.cell_width, grid_height + self.cell_height, stroke = 1, fill = 0)

        ### END  Grid Processing ###

        ### START Word List Processing ###

        # Remove blank words from the word list
        word_list = [word for word in word_list if word.strip()]
        
        # Add check box to start of word
        word_list = [f"\u2610 {word}" for word in word_list]

        # calculate the number of colomns
        min_words_per_column = 5
        total_words = len(word_list)

        # debug info: Print the count of words
        if self.debug:
            print(f'Total words: {total_words}')

        # calculate the number of columns with a minimum of 2 columns
        max_columns = 4
        num_columns = min(max_columns, (total_words + min_words_per_column - 1) // min_words_per_column)
        # ols max(2, total_words // min_words_per_column)

        # debug info: Print the number of columns
        if self.debug:
            print(f'Number of Columns: {num_columns}')

        # calculate the number of words per column
        words_per_column = (len(word_list) + num_columns - 1) // num_columns

        # debug info: Print the number of words per column
        if self.debug:
            print(f'Words per column: {words_per_column}')

        # calculate the maximum words column_width
        max_word_width = max(c.stringWidth(word, font, self.font_size) for word in word_list)

        # debug info: Print the max word width
        if self.debug:
            print(f'Max word width: {max_word_width}')

        # calculate the column spacing
        column_spacing = (((pagesize_with_margines[0] - (max_word_width * num_columns)) / num_columns - 1)) + 18

        # debug info: Print the column width
        if self.debug:
            print(f'Column column_spacing: {column_spacing}')

        # calculate the width of each solumn
        column_width = max_word_width + column_spacing

        # debug info: Print the column width
        if self.debug:
            print(f'Column Width: {column_width}')

        # Create PrettyTable for word list
        word_list_table = PrettyTable(border = False, header = False, align = "l", valign = "c")

        # add columns to word_list_table
        for _ in range(num_columns):
            word_list_table.add_column("", [""] * words_per_column)

        # populate the tabel with words from the word list
        word_list.sort()
        for i in range(words_per_column):
            for j in range(num_columns):
                word_index = j * words_per_column + i
                if word_index < len(word_list):
                    word_list_table._rows[i][j] = word_list[word_index]

        # Debug info: Print Word List Table, and row/column counts
        if self.debug:
            # terminal output
            print("Generated Word List Table:")
            print(word_list_table)
            print(f"Number of columns: {word_list_table.field_names}")
            print(f"Number of rows: {len(word_list_table._rows)}")

        # calculate the x-coordinate for starting the word list
        word_list_x = left_margin + horizontal_offset / 2

        # debug info: Print the x coordinate of the word list
        if self.debug:
            print(f'Word list x-coordinate: {word_list_x}')

        # calculate the y-coordinate for starting the word list
        word_list_y = grid_y - vertical_offset + bottom_margin * 1.75

        # debug info: Print the y coordinate of the word list
        if self.debug:
            print(f'Word list y-coordinate: {word_list_y}')
        
        # Draw the word list table by Looping through the rows and columns of the word list table
        for row_idx, row in enumerate(word_list_table._rows):
            for col_idx, cell_value in enumerate(row):

                # calculate the x coordiante for the cell
                column_x = word_list_x + (col_idx * column_width) - (self.cell_width / 1.75)

                # calculate the y coordinate for the cell
                column_y = word_list_y - row_idx * (self.font_size + self.font_size)

                # draw the cell text
                c.drawString(column_x, column_y, cell_value)

                if self.debug:
                    print(f'Column X coordinate: {column_x}')
                    print(f'Column Y coordinate: {column_y}')

        ### END Word List Processing

    def generate_solution_pdf(self, title, solution_pdf_path, solution_canvas, second_grid):
        
         ### START Page Setup ###

        # set the font
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        font = "DejaVuSans"

        # set the margins (1 inch = 72 points)
        top_margin = 72
        bottom_margin = 72
        left_margin = 72
        right_margin = 72

        # calculate the effective page size with margins
        pagesize_with_margines = (
            pagesizes.letter[0] - left_margin - right_margin,
            pagesizes.letter[1] - top_margin - bottom_margin
        )
        # debug info: Print font sizes
        if self.debug:
            print(f'Effective page width: {pagesize_with_margines[0]}')
            print(f'Effective page height: {pagesize_with_margines[1]}')

        ### END Page Setup ###

        ### START handling the Grid and title ###

        # debug info: Print font sizes
        if self.debug:
            print(f'Font Size: {self.font_size}')
            print(f'Title Font Size: {self.title_font_size}')

        # Remove the quote marks (") from the title
        title = title.replace('"', '')

        if self.debug:
            print(f'Title: {title}')

        # calculate the title width
        title_width = solution_canvas.stringWidth(title, font, self.title_font_size)

        # debug info: Print the title width
        if self.debug:
            print(f"Title width: {title_width}")

        
        # Calculate the grid width and height
        grid_width = self.cols * self.cell_width
        grid_height = self.rows * self.cell_height

        # debug info: Print the grid width & height
        if self.debug:
            print(f"Grid Width: {grid_width}")
            print(f"Grid Height: {grid_height}")

        # calculate the offsets for centering the grid
        horizontal_offset = (pagesize_with_margines[0] - grid_width) / 2
        vertical_offset = (pagesize_with_margines[1] - grid_height) / 2 

        # debug info: Print the horizontal & vertical offset
        if self.debug:
            print(f"horizontal Offset: {horizontal_offset}")
            print(f"Vertical Offset: {vertical_offset}")

        # calculate the starting coordinates for the grid
        grid_x = left_margin + horizontal_offset
        if not second_grid:
            grid_y = letter[1] - top_margin * 2 - vertical_offset - (self.title_font_size * 2)
        else:
            grid_y = (letter[1]/2) - top_margin * 1.75 - vertical_offset - (self.title_font_size * 2)
        # old: grid_y = bottom_margin + vertical_offset

        # debug info: Print the starting coordinates
        if self.debug:
            print(f"Grid starting X: {grid_x}")
            print(f"Grid starting y: {grid_y}")

         # Calculate the x coordinate for centering the title
        title_x = (letter[0] - title_width) / 2

        # debug info: Print the title x-coordinate
        if self.debug:
            print(f"Title x-cordinate: {title_x}")

        # Set title y coordinate
        if not second_grid:
            title_y = letter[1] - (0.5 * top_margin) - (self.title_font_size /2)
        else:
            title_y = (letter[1]/2) - (0.25 * top_margin) - (self.title_font_size /2)


        # debug info: Print the title y-coordinate
        if self.debug:
            print(f"Title y-cordinate: {title_y}")

        # draw encapsulation lines and half-circles
        self.draw_encapsulation(solution_canvas, grid_x, grid_y)

        # Darw the title and centered grid

        solution_canvas.setFont(font, self.title_font_size)
        solution_canvas.drawString(title_x, title_y, title)  # Adjust the y-coordinate (750) as needed

        for row_idx, row in enumerate(self.grid):
            for col_idx, cell_value in enumerate(row):

                # calculate the center of the cell
                cell_center_x = grid_x + col_idx * self.cell_width + self.cell_width / 2
                cell_center_y = grid_y + (self.rows - row_idx - 1) * self.cell_height + self.cell_height / 2


                x = cell_center_x - solution_canvas.stringWidth(cell_value, font, self.font_size) / 2
                y = cell_center_y - self.font_size / 2

                solution_canvas.setFont(font, self.font_size)
                solution_canvas.drawString(x, y, cell_value)

        # debug info: draw parameters
        if self.debug:
            print(f'Cell center x-coordinate: {cell_center_x}')
            print(f'Cell center y-coordinate: {cell_center_y}')
            print(f'Grid x-coordinate: {x}')
            print(f'Grid y-coordinate: {y}')

        # draw encapsulation lines and half-circles
        #self.draw_encapsulation(solution_canvas, grid_x, grid_y)

        # Set border perameters
        solution_canvas.setStrokeColorRGB(0, 0, 0) # adjust for color
        solution_canvas.setLineWidth(2) # adjust for thingness

        # calculate the starting coordinates for the boarder
        border_x = grid_x - self.cell_width / 1.75
        border_y = grid_y - self.cell_height / 1.75

        # debug info: border start coordinates
        if self.debug:
            print(f'Border starting x-coordinate: {border_x}')
            print(f'Border starting y-coordinate: {border_y}')

        # Draw a boarder around the grid
        solution_canvas.rect(border_x, border_y, grid_width + self.cell_width, grid_height + self.cell_height, stroke = 1, fill = 0)

        ### END START handling the Grid and title ###

    # method to circle the answers int he solution grid
    def draw_encapsulation(self, solution_canvas, grid_x, grid_y):
        # set encapsulation parameters
        '''encapsulation_color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
        solution_canvas.setStrokeColorRGB(*encapsulation_color, alpha=1)
        solution_canvas.setFillColorRGB(*encapsulation_color, alpha=1)
        solution_canvas.setLineWidth(2)
        '''
        half_circle_radius = min(self.cell_width, self.cell_height) / 2.5
        rotate_angle = 0
        origin_x = 0
        origin_y = 0

         # calculate offsets for centering
        vert_offset = self.cell_height / 6
        hor_offset = self.cell_width / 6

        for word, start_row, start_col, end_row, end_col, direction in self.placement_info:
            # set encapsulation parameters
            encapsulation_color = (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
            solution_canvas.setStrokeColorRGB(*encapsulation_color, alpha=1)
            solution_canvas.setFillColorRGB(*encapsulation_color, alpha=1)
            solution_canvas.setLineWidth(2)

            # Setting the base coordinates
            start_x = grid_x + self.cell_width * start_col + self.cell_width / 2
            start_y = grid_y + self.cell_height * (self.rows - start_row - 1) + self.cell_height / 2
            end_x = grid_x + self.cell_width * end_col + self.cell_width / 2
            end_y = grid_y + self.cell_height * (self.rows - end_row - 1) + self.cell_height / 2

            if direction in ["horizontal", "horizontal_backward"]:
                # adjust start coordinates as needed
                if direction == "horizontal_backward":
                    start_x, end_x = end_x, start_x
                    start_y, end_y = end_y, start_y

                # draw half-circles at the ends
                solution_canvas.circle(start_x, start_y - (vert_offset / 1.75), half_circle_radius, fill=1)
                solution_canvas.circle(end_x, start_y - (vert_offset / 1.75), half_circle_radius, fill=1)

                # draw rectangles to fill in the space
                rect_width =  (end_x - start_x)
                rect_height = half_circle_radius * 2 # (vert_offset * 2) - (vert_offset / 1.75)
                rect_x = start_x #- half_circle_radius # / 2.5
                rect_y = end_y - (vert_offset * 3)

                solution_canvas.rect(rect_x, rect_y, rect_width, rect_height, fill=1)
                
            elif direction in ["vertical", "vertical_upward"]:
                # adjust start coordinates as needed
                if direction == "vertical_upward":
                    start_y, end_y = end_y, start_y

                # Draw half-circles at the ends
                solution_canvas.circle(start_x, start_y - (vert_offset /2), half_circle_radius, fill=1)
                solution_canvas.circle(start_x, end_y - (vert_offset /2), half_circle_radius, fill=1)

                # Draw rectangles to fill in the space
                rect_width = half_circle_radius * 2
                rect_height = abs(end_y - start_y)
                rect_x = start_x - (hor_offset * 2.45)
                rect_y = min(start_y, end_y) - (vert_offset)

                solution_canvas.rect(rect_x, rect_y, rect_width, rect_height, fill=1)

            elif direction.startswith("diagonal"):
                # adjust start coordinates as needed
                # draw half-circles at the ends
                solution_canvas.circle(start_x, start_y - (vert_offset / 1.5), half_circle_radius, fill=1)
                solution_canvas.circle(end_x, end_y - (vert_offset / 1.5), half_circle_radius, fill=1)

                # Calculate the center point between start and end coordinates
                center_x = (start_x + end_x) / 2
                center_y = (start_y + end_y) / 2

                # Save current Canvas state to restore after rotate
                solution_canvas.saveState()

                # Translate to the center point for rotation
                solution_canvas.translate(center_x, center_y)

                if direction == "diagonal_tl_br":

                    # Calculate the angle of the diagonal line
                    angle_rad = math.atan2(end_y - start_y, end_x - start_x)
                    angle_deg = math.degrees(angle_rad)

                    # Rotate the canvas
                    solution_canvas.rotate(angle_deg)

                elif direction == "diagonal_tr_bl":
                    # Calculate the angle of the diagonal line (adjust as needed)
                    angle_rad = math.atan2(end_y - start_y, start_x - end_x)
                    angle_deg = math.degrees(angle_rad)

                    # Rotate the canvas
                    solution_canvas.rotate(-angle_deg)

                elif direction == "diagonal_bl_tr":
                    # Calculate the angle of the diagonal line (adjust as needed)
                    angle_rad = math.atan2(start_y - end_y, end_x - start_x)
                    angle_deg = math.degrees(angle_rad)

                    # Rotate the canvas
                    solution_canvas.rotate(-angle_deg)

                elif direction == "diagonal_br_tl":
                    # Calculate the angle of the diagonal line (adjust as needed)
                    angle_rad = math.atan2(start_y - end_y, start_x - end_x)
                    angle_deg = math.degrees(angle_rad)

                    # Rotate the canvas
                    solution_canvas.rotate(angle_deg)

                # Draw elements at the rotated angle (e.g., a rectangle)
                rect_width = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
                rect_height = half_circle_radius * 2
                solution_canvas.rect(-rect_width / 2, -(rect_height / 2) - 1.5, rect_width, rect_height, fill=1)

                if self.debug:
                    print(f'Coordinates: {start_x}, {start_y}')
                    print(f'Rotated: {center_x}, {center_y}')

                # Reset the transformation
                solution_canvas.restoreState()

        # reset colors
        solution_canvas.setStrokeColorRGB(0, 0, 0)  
        solution_canvas.setFillColorRGB(0, 0, 0)  

def main():
    debug_enabled = True # set to True for debug functions to execute
    
    # default values
    default_rows = 15
    default_cols = 25
    default_font_size = 'M'
    default_title_size = 'L'
    pdf_path = "/Users/HA/Desktop/Word Search/word_search_puzzles.pdf"
    solution_pdf_path = "/Users/HA/Desktop/Word Search/word_search_solution.pdf"

    pagesize = letter

    generator = None

    # with open("input.txt", "r") as input_file:
    with open("/Users/HA/Desktop/Word Search/Animal Kingdom.txt", "r") as input_file:
        lines = input_file.readlines()

    # initialize things
    current_title = None
    current_word_list = []
    current_word_list_started = False
    placement_info_list = []
    current_rows = default_rows
    current_cols = default_cols
    current_font_size = default_font_size
    current_title_size = default_title_size
    c = canvas.Canvas(pdf_path, pagesize)
    solution_canvas = canvas.Canvas(solution_pdf_path, pagesize)

    grid_counter = 0  # Counter for tracking grids added on the current page
    second_grid = False

    for line in lines:
        line = line.strip()

        if line.startswith("Rows:"):
            current_rows = int(line.replace("Rows:", "").strip())
        elif line.startswith("Cols:"):
            current_cols = int(line.replace("Cols:", "").strip())
        elif line.startswith("Font Size:"):
            current_font_size = line.replace("Font Size:", "").strip()
        elif line.startswith("Title:"):
            if current_title and current_word_list:
                generator = WordFindPuzzleGenerator(current_rows, current_cols, current_word_list, current_font_size, current_title_size, debug=debug_enabled)
                generator.set_font_size(current_font_size, current_title_size)
                generator.grid_all_word_validation()
                generator.generate_puzzle(current_word_list)

                # store the placement infor for each word
                # used to properly encapsulate the data in the solution grid
                for word, start_row, start_col, end_row, end_col, direction in generator.placement_info:
                        placement_info_list.append((word, start_row, start_col, end_row, end_col, direction))

                generator.generate_pdf(current_title, current_word_list, pdf_path, c)

                grid_counter += 1

                generator.generate_solution_pdf(current_title, solution_pdf_path, solution_canvas, second_grid)
                second_grid = True

                if grid_counter == 2:
                    generator.generate_solution_pdf(current_title, solution_pdf_path, solution_canvas, second_grid)
                    solution_canvas.showPage()
                    grid_counter = 0 # resets counter for next solution page
                    second_grid = False

                c.showPage() # save the current page and start a new one
            current_title = line.replace("Title:", "").strip()
            current_word_list = []
        elif line == "Word List:":
            current_word_list_started = True
        elif current_word_list_started:
            current_word_list.append(line)

    # Process the last puzzle
    if generator and current_title and current_word_list:
        generator = WordFindPuzzleGenerator(current_rows, current_cols, current_word_list, current_font_size, current_title_size, debug=debug_enabled)
        generator.set_font_size(current_font_size, current_title_size)
        generator.grid_all_word_validation()
        generator.generate_puzzle(current_word_list)
         # store the placement infor for each word
        # used to properly encapsulate the data in the solution grid
        for word, start_row, start_col, end_row, end_col, direction in generator.placement_info:
                placement_info_list.append((word, start_row, start_col, end_row, end_col, direction))
        generator.generate_pdf(current_title, current_word_list, pdf_path, c)
        generator.generate_solution_pdf(current_title, solution_pdf_path, solution_canvas, second_grid)
        c.showPage() # save the current page and start a new one
        solution_canvas.showPage()

    # Save the final pdf
    c.save()
    solution_canvas.save()

if __name__ == "__main__":
    main()