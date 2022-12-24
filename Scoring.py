from Wordlist import *
import string

board_words = []
old_words = []
count = 0
turn = 0
LETTER_SCORES = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3,
                 "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4,
                 "z": 10, "blank": 0}


class CreateWord:
    def __init__(self, current_word, current_score, length, word_modifiers, turn, first_tile, last_tile, direction):
        global count
        self.word = current_word
        self.pre_score = current_score
        self.length = length
        self.modifier = word_modifiers
        self.direction = direction
        self.count = count
        self.modified_score = self.pre_score * self.modifier
        self.turn_created = turn
        self.first_tile = first_tile
        self.last_tile = last_tile

        # This if could look a lot less complicated but I only want the program to check the word up against a list of words its own length
        if self.length == 2:
            if self.word in word_ml_2:
                validity = True
            else:
                validity = False
        elif self.length == 3:
            if self.word in word_ml_3:
                validity = True
            else:
                validity = False
        elif self.length == 4:
            if self.word in word_ml_4:
                validity = True
            else:
                validity = False
        elif self.length == 5:
            if self.word in word_ml_5:
                validity = True
            else:
                validity = False
        elif self.length == 6:
            if self.word in word_ml_6:
                validity = True
            else:
                validity = False
        elif self.length == 7:
            if self.word in word_ml_7:
                validity = True
            else:
                validity = False
        elif self.length == 8:
            if self.word in word_ml_8:
                validity = True
            else:
                validity = False
        else:
            validity = False
        self.valid = validity  # For some reason I couldnt use self.valid inside the double if's
        count += 1


def checkWords(board_spaces_by_row_column, board_spaces_by_column_row, board_words):
    global turn
    global current_score
    global word_modifiers
    old_words = tuple(board_words)

    current_word = ""
    current_score = 0
    word_modifiers = 1
    first_tile = None


    # -------------------------------------------
    # -----------HORIZONTAL WORD CHECK-----------
    # -------------------------------------------
    for row_item in board_spaces_by_row_column:
        for tile_item in row_item:
            if tile_item.letter != None and tile_item.column != 15:
                if current_word == "":
                    first_tile = tile_item
                current_word += tile_item.letter

                # I FIXED THE WIERD BUG AROUND HERE BTW, IT HAD TO DO WITH WHEN THE GAME RESTARTS YOUR TURN
                # IT CACHES EVERY TILE, BUT TO DO THAT IT HAS TO PASS THROUGH ALL ITS ATTRIBUTES, AND IT PASSED
                # THROUGH TILE_ITEM.LETTER INSTEAD OF TILE_ITEM.SCORE, BUT I DIDNT NOTICE CAUSE IT WAS JUST A BIG LIST
                # OF ARGUMENTS AND DIDNT REALIZE THAT IT HAD TILE_ITEM.LETTER TWICE IN A ROW

                doWithTileModifiers(tile_item)

            else:
                # Adds current letter to word if there is one and its in the last row
                if tile_item.column == 15 and tile_item.letter != None:
                    current_word += tile_item.letter
                    doWithTileModifiers(tile_item)

                if len(current_word) > 1:

                    # Makes last tile the current tile if the word ends at end of row/column,
                    # otherwise it is the tile before it since if it doesnt end at end of row/column
                    # then the game only checks for ends of word if it runs into a blank
                    if tile_item.column == 15:
                        last_tile = tile_item
                    else:
                        last_tile = board_spaces_by_row_column[tile_item.row - 1][tile_item.column - 2]
                    word_already_exists = False
                    for word_item in board_words:
                        # If word already exists(same word starting and ending in same place, to allow for multiple words in different places) set value to true
                        if word_item.word == current_word and word_item.first_tile == first_tile and word_item.last_tile == last_tile:
                            word_already_exists = True

                    if word_already_exists == False:
                        print(current_word)
                        board_words.append(
                            CreateWord(current_word, current_score, len(current_word), word_modifiers, turn, first_tile,
                                       last_tile, "horizontal"))
                # Reset Word info at end of word
                current_word = ""
                current_score = 0
                word_modifiers = 1
                first_tile = None
                last_tile = None

        # Reset Word info at end of column(so words cant carry to the next one)
        current_word = ""
        current_score = 0
        word_modifiers = 1
        first_tile = None

    # -------------------------------------------
    # ------------VERTICAL WORD CHECK------------
    # -------------------------------------------
    for column_item in board_spaces_by_column_row:
        for tile_item in column_item:
            if tile_item.letter != None and tile_item.row != 15:
                if current_word == "":
                    first_tile = tile_item
                current_word += tile_item.letter

                doWithTileModifiers(tile_item)

            else:
                # Adds current letter to word if there is one and its in the last row
                if tile_item.row == 15 and tile_item.letter != None:
                    current_word += tile_item.letter
                    doWithTileModifiers(tile_item)
                if len(current_word) > 1:

                    # Makes last tile the current tile if the word ends at end of row/column,
                    # otherwise it is the tile before it since if it doesnt end at end of row/column
                    # then the game only checks for ends of word if it runs into a blank
                    if tile_item.row == 15:
                        last_tile = tile_item
                    else:
                        last_tile = board_spaces_by_column_row[tile_item.column - 1][tile_item.row - 2]
                    word_already_exists = False # (False unless turned true)

                    # Checks if word already exists
                    for word_item in board_words:
                        # If word already exists(same word starting and ending in same place, to allow for multiple words in different places) set value to true
                        if word_item.word == current_word and word_item.first_tile == first_tile and word_item.last_tile == last_tile:
                            word_already_exists = True
                    # If word does not exist, add it to the word list, otherwise, don't
                    if word_already_exists == False:
                        board_words.append(
                            CreateWord(current_word, current_score, len(current_word), word_modifiers, turn, first_tile,
                                       last_tile, "vertical"))
                # Reset Word info at end of word
                current_word = ""
                current_score = 0
                word_modifiers = 1
                first_tile = None
                last_tile = None

        # Reset Word info at end of column(so words cant carry to the next one)
        current_word = ""
        current_score = 0
        word_modifiers = 1
        first_tile = None
        last_tile = None

    turn += 1
    return (board_words)

def doWithTileModifiers(tile_item):
    global word_modifiers
    global current_score

    if tile_item.modifier == "None":
        current_score += tile_item.score
    elif tile_item.modifier == "dl":
        print
        current_score += 2 * tile_item.score
    elif tile_item.modifier == "tl":
        current_score += 3 * tile_item.score
    elif tile_item.modifier == "dw":
        current_score += tile_item.score
        word_modifiers = word_modifiers * 2
    elif tile_item.modifier == "tw":
        current_score += tile_item.score
        word_modifiers = word_modifiers * 3
