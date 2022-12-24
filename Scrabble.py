# Gavin Lusby 11/5/2020
# Scrabble Game

import random
import string
from tkinter import *
from tkinter import ttk

import Scoring


class CreateSquareInfo:  # Allows to call specific info about each tile

    def __init__(self, counter, row, column):
        self.item = Frame(game_frame, width=60, height=60, relief=RIDGE, borderwidth=6,
                          bg="#c7c2a5")  # Allows the frame itself to be called with .item
        self.number = counter  # Allows serial number to be called with .number
        self.row = row
        self.column = column
        self.button = Button(self.item,
                             command=lambda: placeTile(selected_letter, selected_slot, self.number, self.item,
                                                       current_player))

        self.image = self.button.cget("image")
        self.command = self.button.cget("command")
        self.state = self.button.cget("state")

        self.letter = None
        self.score = 0
        if self.number in TW_LIST:
            self.modifier = "tw"
        elif self.number in DW_LIST:
            self.modifier = "dw"
        elif self.number in TL_LIST:
            self.modifier = "tl"
        elif self.number in DL_LIST:
            self.modifier = "dl"
        else:
            self.modifier = "None"


class CreateSlotInfo:

    def __init__(self, letter, number):
        self.item = Frame(height=120, width=120, bg="#cae2ed", borderwidth=0)
        self.letter = letter
        self.number = number
        self.button = Button(self.item, command=lambda: selectLetter(self),
                             image=TileImage["medium"][self.letter], borderwidth=2, relief=FLAT, bg="#adc2cb")


class CacheSquareInfo:  # Allows to cache each specific Tile and its properties

    def __init__(self, item, number, row, column, button, letter, score, image, command, state, modifier):
        self.item = item
        self.number = number
        self.row = row
        self.column = column
        self.button = button
        self.letter = letter
        self.score = score
        self.modifier = modifier
        self.image = self.button.cget("image")
        self.command = self.button.cget("command")
        self.state = self.button.cget("state")


root = Tk()
from ImageSetup import *  # Must be imported AFTER creating root object because the images are tkinter objects

# -------------------------------------------
# ----------------WINDOW SETUP---------------
# -------------------------------------------

root.geometry("1728x972+96+20")
root.title("Scrabble by Gavin Lusby")
root.configure(bg="#cae2ed")
root.resizable(False, False)
root.iconbitmap("icon.ico")

# -------------------------------------------
# --------------VARIABLE SETUP---------------
# -------------------------------------------

# A lot of these variables might be redefined later but they don't get created at the beginning of the code it causes some issues(NO AUTOFILL!!!!!!!!!! D: ):   )


# Lists for which tiles have Modifiers
TW_LIST = [1, 8, 15, 106, 120, 211, 218, 225]
DW_LIST = [17, 29, 33, 43, 49, 57, 65, 71, 113, 155, 161, 169, 177, 183, 193, 197, 209]
TL_LIST = [21, 25, 77, 81, 85, 89, 137, 141, 145, 149, 201, 205]
DL_LIST = [4, 12, 37, 39, 46, 53, 60, 93, 97, 99, 103, 109, 117, 123, 127, 129, 133, 166, 173, 180, 187, 189, 214, 222]
RULES_FILE = open("rules.txt", "r")

# available_tile_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q"]

available_tile_list = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e",
                        "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h",
                        "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", "l", "m", "m", "n",
                        "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r",
                        "r", "r", "r", "r", "s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u",
                        "v", "v", "w", "w", "x", "y", "y", "z", "blank", "blank"]

# Creating the 7 letter slot values
slot_list = [0, 0, 0, 0, 0, 0, 0]

# Initial Positioning Method, becomes useless in a couple of lines
scrabble_positions = {"row1": {}, "row2": {}, "row3": {}, "row4": {}, "row5": {},
                      "row6": {}, "row7": {}, "row8": {}, "row9": {}, "row10": {},
                      "row11": {}, "row12": {}, "row13": {}, "row14": {}, "row15": {}, }
board_spaces_by_serial = []
board_spaces_by_row_column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
board_spaces_by_column_row = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

selected_letter = ""
selected_slot = ""
players = 2
tiles_by_player = [[], [], [], []]
letters_this_turn = 0
current_player = 1
letters_this_game = 0
turns_this_game = 0
player_letter_cache = []
board_cache = []
swap_list = []
board_words = []
old_words = []
new_words = []
invalid_words_this_turn = []
tiles_used_this_turn = []
swaps_this_turn = 0
scores = [0, 0, 0, 0]
score_this_turn = 0
tiles_on_board = 0
end_game_collapse = False

# -------------------------------------------
# ---------------TKINTER SETUP---------------
# -------------------------------------------

# Buttons use lambda sometimes because without a lambda, tkinter will raise an error due to function definition after use

# Frame for Gameboard to go in
game_frame = Frame(bg="#FFFFFF", width=900, height=900)

# ---------------- MAIN TITLE SCREEN ----------------

game_title = Label(text="Scrabble", font=("", 90), bg="#cae2ed")
game_title.place(x=864, y=200, anchor=CENTER)

two_player_button = Button(text="2 Person Play", bg="#089f1d", activebackground="#089f1d", borderwidth=12,
                           height=2,
                           width=12, font=("", 40), command=lambda: startGame(2))
two_player_button.place(x=414, y=400, anchor=CENTER)
three_player_button = Button(text="3 Person Play", bg="#089f1d", activebackground="#089f1d", borderwidth=12,
                             height=2,
                             width=12, font=("", 40), command=lambda: startGame(3))
three_player_button.place(x=864, y=400, anchor=CENTER)
four_player_button = Button(text="4 Person Play", bg="#089f1d", activebackground="#089f1d", borderwidth=12,
                            height=2,
                            width=12, font=("", 40), command=lambda: startGame(4))
four_player_button.place(x=1314, y=400, anchor=CENTER)

random_tile = Label(image=TileImage["large"][random.choice(string.ascii_lowercase)], borderwidth=0)
random_tile.place(x=864, y=733, anchor=CENTER)

# Quit Button
quit_button = Button(text="Quit", bg="#da6363", activebackground="#da6363", borderwidth=12,
                     height=2,
                     width=12, font=("", 30), command=quit)
quit_button.place(x=1394, y=800)

# Rules Button
rules_button = Button(text="Rules", bg="#9e931d", activebackground="#9e931d", borderwidth=12,
                      height=2,
                      width=12, font=("", 30), command=lambda: showRules())
rules_button.place(x=28, y=800)

# ---------------- MAIN INGAME SCREEN ----------------

# Indication for Selected Letter
selected_label = Label(text="Selected Letter: ", bg="#cae2ed", font=("", 20))

# Button to End Turn

end_turn_button = Button(text="End Turn", bg="#a2a2a2", activebackground="#a2a2a2", borderwidth=12, height=2, width=16,
                         font=("", 16), command=lambda: endTurn(), state=DISABLED)

# Restart Turn Button
restart_turn_button = Button(text="Restart Turn", bg="#a2a2a2", activebackground="#a2a2a2", borderwidth=12, height=2,
                             width=16, font=("", 16), command=lambda: restartTurn(), state=DISABLED)

# Swap Letter Button
swap_letter_button = Button(text="Swap Selected Tile", bg="#089f1d", activebackground="#089f1d", borderwidth=12,
                            height=2,
                            width=16, font=("", 16), command=lambda: swapLetter())

# Player Indicator Label
which_player_label = Label(text="Player 1", bg="#cae2ed", font=("", 40))

# Player's points indicators
player_points_label = Label(text="Points", bg="#cae2ed", font=("", 28))

player_one_points_label = Label(bg="#cae2ed", font=("", 28))
player_two_points_label = Label(bg="#cae2ed", font=("", 28))
player_three_points_label = Label(bg="#cae2ed", font=("", 28))
player_four_points_label = Label(bg="#cae2ed", font=("", 28))

# Player's points indicators
tiles_left_label = Label(bg="#cae2ed", font=("", 36))

# ---------------- PROMPT SCREEN ----------------

# Creates background blocker for prompt
bg_block = Frame(width=1728, height=972, bg="#cae2ed")

# Creates Prompt Frame
prompt_frame = Frame(height=600, width=600, borderwidth=20, relief=RIDGE, bg="#a2b5be")

# Creates Prompt Text Words
prompt_text = Label(prompt_frame, bg="#a2b5be", wraplength=400, font=("", 20))

# Creates Prompt Entrybox

prompt_entry = Entry(prompt_frame, width=20, font=("", 20), justify=CENTER)

# Creates Prompt Submit Button
prompt_submit_blank = Button(prompt_frame, text="Submit", bg="#99acb4", activebackground="#99acb4",
                             command=lambda: submitBlank(), height=2,
                             width=16, font=("", 16), borderwidth=12)
error_label = Label(fg="#7f0000", font=("", 16), bg="#a2b5be")

# Enter Blank Letter Entrybox
entry_blank = Entry(prompt_frame)

# Restart from invalid word prompt button
prompt_restart = Button(prompt_frame, text="Restart Turn", bg='#9f5e02', activebackground="#9f5e02", borderwidth=12,
                        height=2,
                        width=16, font=("", 16), command=lambda: invalidRestart())
# Listbox for invalid words
prompt_listbox = Listbox(prompt_frame, font=("", 20), justify=CENTER,state=DISABLED)

# ---------------- SWITCH SCREEN ----------------

# Last player's points indication
last_player_points = Label(bg="#cae2ed", font=("", 28))

# Show this if the last player got +50 for using all tiles
got_fifty_points_label = Label(bg="#cae2ed", font=("", 20))

# Continue to next turn button
next_turn_button = Button(text="Continue", bg="#0e1598", activebackground="#0e1598", borderwidth=12,
                          height=2,
                          width=16, font=("", 30), command=lambda: nextTurn())

# ---------------- POST GAME SCREEN ----------------

# Explains the technicality if two players tie
technicality_label = Label(bg="#cae2ed", font=("", 20), wraplength=400, fg="#f0ab60")

# Back to menu button
menu_button = Button(text="Return to Menu", bg="#0e1598", activebackground="#0e1598", borderwidth=12,
                     height=2,
                     width=16, font=("", 30), command=lambda: returnToMenu("game"))

# ---------------- RULES SCREEN ----------------

rules_scroll_frame = Frame(width=30, height=900)

rules_scroller = Scrollbar(rules_scroll_frame, width=30)

rules_text = Text(width=80, height=28, yscrollcommand=rules_scroller.set, wrap=CHAR, font=("", 20))
rules_text.insert(END, RULES_FILE.read())
rules_text.configure(state=DISABLED)

rules_scroller.config(command=rules_text.yview)


# -------------------------------------------
# -------------GAME BOARD SETUP--------------
# -------------------------------------------


# -------------------------------------------
# ----------------FUNCTIONS------------------
# -------------------------------------------

def checkForDuplicates(dupe_list):
    counter = 0
    inner_counter = 0
    dupes = []
    for list_item in dupe_list:
        for other_item in dupe_list:
            if counter == inner_counter:
                inner_counter += 1
                continue
            else:
                if list_item == other_item:
                    dupes.append(list_item)
            inner_counter += 1

        counter += 1

        inner_counter = 0
    return dupes


def updatePlayerPointDisplay():
    if players > 1:
        player_one_points_label.place(x=40, y=248)
        player_two_points_label.place(x=40, y=296)
    if players > 2:
        player_three_points_label.place(x=40, y=344)
    if players > 3:
        player_four_points_label.place(x=40, y=392)

    player_one_string = f"Player 1: {scores[0]}"
    player_two_string = f"Player 2: {scores[1]}"
    player_three_string = f"Player 3: {scores[2]}"
    player_four_string = f"Player 4: {scores[3]}"

    list_of_strings = [0, 0, 0, 0]

    if game_over == True:
        for counter in range(4):
            if scores[counter] > pre_removal_scores[counter]:
                list_of_strings[
                    counter] = f"Player {counter + 1}: {pre_removal_scores[counter]} + {benefactor_points_received} = {scores[counter]}"
            elif scores[counter] < pre_removal_scores[counter]:
                list_of_strings[
                    counter] = f"Player {counter + 1}: {pre_removal_scores[counter]} - {remove_score[counter]} = {scores[counter]}"
            counter += 1
            if counter >= players:
                break
        player_one_string = list_of_strings[0]
        player_two_string = list_of_strings[1]
        player_three_string = list_of_strings[2]
        player_four_string = list_of_strings[3]

    player_one_points_label.configure(text=player_one_string)
    player_two_points_label.configure(text=player_two_string)
    player_three_points_label.configure(text=player_three_string)
    player_four_points_label.configure(text=player_four_string)

    player_points_label.place(x=40, y=200)


# Used for unbinding buttons so they have no functionality but aren't in the "disabled"(greyed out) state
def unbind():
    return


def gameboardSetup():
    global scrabble_positions
    global board_spaces_by_serial
    global board_spaces_by_row_column
    global board_spaces_by_column_row
    counter = 0

    # Allows each tile to be referenced by serial number
    for row in range(1, 16):
        for column in range(1, 16):
            counter += 1
            scrabble_positions["row" + str(row)]["col" + str(column)] = CreateSquareInfo(counter, row, column)
            board_spaces_by_serial.append(scrabble_positions["row" + str(row)]["col" + str(column)])

    counter = 0
    # Allows each tile to be referenced by row and then column
    for i in board_spaces_by_row_column:

        counter += 1
        for tile_item in board_spaces_by_serial:
            if tile_item.row == counter:
                i.append(tile_item)

    counter = 0
    # Allows each tile to be referenced by column and then row
    for i in board_spaces_by_column_row:
        counter += 1
        for tile_item in board_spaces_by_serial:

            if tile_item.column == counter:
                i.append(tile_item)
    # Dictionary used to make 225 instances of scrabble tiles while being able to use loops

    counter = 0  # Resets Loop Counter
    for tile_item in board_spaces_by_serial:

        tile_item.item.grid(row=counter // 15,
                            column=counter % 15)  # Grid place each square
        # tile_item.button.pack()
        counter += 1

        # Create TW,DW,TL,DL Tiles
        if counter in TW_LIST:
            tile_item.button.configure(image=ModifierImage["tw"],
                                       borderwidth=0,
                                       state=DISABLED)
            tile_item.button.pack()
            tile_item.item.configure(bg="#970000")

        elif counter in DW_LIST:
            tile_item.button.configure(image=ModifierImage["dw"],
                                       borderwidth=0,
                                       state=DISABLED)
            tile_item.button.pack()
            tile_item.item.configure(bg="#fb6b4d")
        elif counter in TL_LIST:
            tile_item.button.configure(image=ModifierImage["tl"],
                                       borderwidth=0,
                                       state=DISABLED)
            tile_item.button.pack()
            tile_item.item.configure(bg="#003c97")
        elif counter in DL_LIST:
            tile_item.button.configure(image=ModifierImage["dl"],
                                       borderwidth=0,
                                       state=DISABLED)
            tile_item.button.pack()
            tile_item.item.configure(bg="#459ebc")
        else:
            tile_item.button.configure(
                image=ModifierImage["default"],
                borderwidth=0, state=DISABLED)
            tile_item.button.pack()
            tile_item.item.configure(bg="#c7c2a5")
        if counter == 113:
            tile_item.button.configure(
                image=ModifierImage["center"],
                borderwidth=0, state=DISABLED)
            tile_item.button.pack()
            tile_item.item.configure(bg="#fcb5a8")


def deselect():
    global selected_letter
    global selected_slot
    selected_label.configure(text="Selected Letter: ")
    selected_letter = ""
    selected_slot = ""


def randomDraw(player):
    try:
        this_tile = random.choice(available_tile_list)
        available_tile_list.remove(this_tile)
        tiles_by_player[player - 1].append(this_tile)
        return this_tile
    except IndexError:
        print("All out")
        return None


def givePlayersSevenLetters():  # Gives all players seven letters for start of game
    for i in range(7):
        for player in range(1, players + 1):
            randomDraw(player)


def refillLetters(player):
    n_of_refills = 7 - len(tiles_by_player[player - 1])
    for i in range(n_of_refills):
        (randomDraw(player))


def updateLetterSlots(player):
    counter = 0
    # AttributeError will be raised when this runs the first time when slot_list = [0,0,0,0,0,0,0]
    try:
        for slot_item in slot_list:
            slot_item.button.pack_forget()
            slot_item.item.place_forget()
    except:
        AttributeError
    for letter in tiles_by_player[player - 1]:
        slot_list[counter] = CreateSlotInfo(letter, counter)
        slot_list[counter].item.place(x=636, y=19 + (counter) * 135)
        slot_list[counter].button.pack()
        counter += 1


def selectLetter(slot_object):
    global selected_letter
    global selected_slot
    for slot_item in slot_list:
        slot_item.button.configure(bg="#adc2cb")
        if slot_item.button.cget("state") == "disabled":
            slot_item.button.configure(bg="#089f1d")
    slot_object.button.configure(bg="#000000")
    selected_letter = slot_object.letter
    selected_slot = slot_object.number
    selected_label.configure(text="Selected Letter: " + selected_letter.upper())


def swapLetter():
    global selected_letter
    global selected_slot
    global available_tile_list
    global swaps_this_turn
    global swap_list

    if selected_letter == "":
        return

    for slot_item in slot_list:
        if slot_item.number == selected_slot:
            swap_list.append(selected_letter)
            slot_item.button.configure(bg="#089f1d", state=DISABLED, image=SwapImage)

    for tile_item in board_spaces_by_serial:
        tile_item.button.configure(state=DISABLED)
    counter = 0
    for slot_item in slot_list:
        slot_item.number = counter
        counter += 1

    deselect()
    swaps_this_turn += 1
    if swaps_this_turn == 7:
        swap_letter_button.configure(bg="#a2a2a2", activebackground="#a2a2a2", state=DISABLED)
    restart_turn_button.configure(bg='#9f5e02', activebackground="#9f5e02", state=NORMAL)
    end_turn_button.configure(bg="#da6363", activebackground="#da6363", state=NORMAL, text="End Turn")


def updateAvailableTiles(mode):
    global letters_this_turn
    global firstrow
    global firstcolumn

    # Mode one: Center Square is unblocked

    # Trigger: Game Starts

    if mode == 1:
        for tile_item in board_spaces_by_serial:
            if tile_item.number == 113:
                tile_item.button.configure(state=NORMAL)
            else:
                tile_item.button.configure(state=DISABLED)


    # Mode two: four squares surrounding middle square are unblocked

    # Trigger: After first move of game

    elif mode == 2:
        for tile_item in board_spaces_by_serial:
            if tile_item.number in [98, 112, 113, 114, 128]:
                tile_item.button.configure(state=NORMAL)
            else:
                tile_item.button.configure(state=DISABLED)



    # Mode three: All tiles adjacent to letter tiles are unblocked

    # Trigger: Beggining of new turn

    elif mode == 3:
        for tile_item in board_spaces_by_serial:
            if tile_item.letter != None:
                if tile_item.row != 15:
                    board_spaces_by_row_column[tile_item.row][tile_item.column - 1].button.configure(state=NORMAL)
                if tile_item.row != 1:
                    board_spaces_by_row_column[tile_item.row - 2][tile_item.column - 1].button.configure(state=NORMAL)
                if tile_item.column != 15:
                    board_spaces_by_row_column[tile_item.row - 1][tile_item.column].button.configure(state=NORMAL)
                if tile_item.column != 1:
                    board_spaces_by_row_column[tile_item.row - 1][tile_item.column - 2].button.configure(state=NORMAL)


    # Mode four: Tiles surrounding the first tile placed in a turn(
    # excluding first move of game) get unblocked, and any empty tiles
    # where all the spaces in a straight line between the first tile, and that tile are letters get unblocked
    #
    # Trigger: After first move of turn(excluding first move of game)

    elif mode == 4:
        for tile_item in board_spaces_by_serial:
            if tile_item.letter == None:
                board_spaces_by_row_column[tile_item.row - 1][tile_item.column - 1].button.configure(state=DISABLED)
        if last_tile.row != 15:
            board_spaces_by_row_column[last_tile.row][last_tile.column - 1].button.configure(state=NORMAL)
        if last_tile.row != 1:
            board_spaces_by_row_column[last_tile.row - 2][last_tile.column - 1].button.configure(state=NORMAL)
        if last_tile.column != 15:
            board_spaces_by_row_column[last_tile.row - 1][last_tile.column].button.configure(state=NORMAL)
        if last_tile.column != 1:
            board_spaces_by_row_column[last_tile.row - 1][last_tile.column - 2].button.configure(state=NORMAL)
            # Unrestricts all letter tiles and one tile after in row going left-right starting from first_tile_of_turn
            for tile_item in board_spaces_by_row_column[first_tile_of_turn.row - 1]:
                if tile_item.number < first_tile_of_turn.number:
                    continue
                else:
                    if tile_item.letter != None:
                        tile_item.button.configure(state=NORMAL)
                        continue
                    tile_item.button.configure(state=NORMAL)
                    break
            # Unrestricts all letter tiles and one tile after in row going right-left starting from first_tile_of_turn
            for tile_item in reversed(board_spaces_by_row_column[first_tile_of_turn.row - 1]):
                if tile_item.number > first_tile_of_turn.number:
                    continue
                else:
                    if tile_item.letter != None:
                        tile_item.button.configure(state=NORMAL)
                        continue
                    tile_item.button.configure(state=NORMAL)
                    break
            for tile_item in board_spaces_by_column_row[first_tile_of_turn.column - 1]:
                if tile_item.number < first_tile_of_turn.number:
                    continue
                else:
                    if tile_item.letter != None:
                        tile_item.button.configure(state=NORMAL)
                        continue
                    tile_item.button.configure(state=NORMAL)
                    break
            # Unrestricts all letter tiles and one tile after in column going upwards starting from first_tile_of_turn
            for tile_item in reversed(board_spaces_by_column_row[first_tile_of_turn.column - 1]):
                if tile_item.number > first_tile_of_turn.number:
                    continue
                else:
                    if tile_item.letter != None:
                        tile_item.button.configure(state=NORMAL)
                        continue
                    tile_item.button.configure(state=NORMAL)
                    break


    # Mode five: All tiles in row or column chosen restricted by the placement of the first two tiles of the turn
    # are unblocked, assuming that there are letters to connect them the whole way

    # Trigger: After second move of any turn

    elif mode == 5:
        if first_tile_of_turn.row == second_tile_of_turn.row:  # If first two pieces are in same row
            turn_direction = "horizontal"
        if first_tile_of_turn.column == second_tile_of_turn.column:  # IF first two pieces are in same column
            turn_direction = "vertical"
        # Disables Tiles that aren't letters
        for tile_item in board_spaces_by_serial:
            if tile_item.letter == None:
                board_spaces_by_row_column[tile_item.row - 1][tile_item.column - 1].button.configure(state=DISABLED)
        # Enables valid tiles in row
        if turn_direction == "horizontal":
            # Unrestricts all letter tiles and one tile after in row going left-right starting from first_tile_of_turn
            for tile_item in board_spaces_by_row_column[first_tile_of_turn.row - 1]:
                if tile_item.number < first_tile_of_turn.number:
                    continue
                else:
                    if tile_item.letter != None:
                        tile_item.button.configure(state=NORMAL)
                        continue
                    tile_item.button.configure(state=NORMAL)
                    break
            # Unrestricts all letter tiles and one tile after in row going right-left starting from first_tile_of_turn
            for tile_item in reversed(board_spaces_by_row_column[first_tile_of_turn.row - 1]):
                if tile_item.number > first_tile_of_turn.number:
                    continue
                else:
                    if tile_item.letter != None:
                        tile_item.button.configure(state=NORMAL)
                        continue
                    tile_item.button.configure(state=NORMAL)
                    break
        elif turn_direction == "vertical":

            # Unrestricts all letter tiles and one tile after in column going downwards starting from first_tile_of_turn
            for tile_item in board_spaces_by_column_row[first_tile_of_turn.column - 1]:
                if tile_item.number < first_tile_of_turn.number:
                    continue
                else:
                    if tile_item.letter != None:
                        tile_item.button.configure(state=NORMAL)
                        continue
                    tile_item.button.configure(state=NORMAL)
                    break
            # Unrestricts all letter tiles and one tile after in column going upwards starting from first_tile_of_turn
            for tile_item in reversed(board_spaces_by_column_row[first_tile_of_turn.column - 1]):
                if tile_item.number > first_tile_of_turn.number:
                    continue
                else:
                    if tile_item.letter != None:
                        tile_item.button.configure(state=NORMAL)
                        continue
                    tile_item.button.configure(state=NORMAL)
                    break

                # This does the same thing, but it also enables some spots that shouldn't be
                # if tile_item.row != 15 and tile_item.letter != None:
                #     board_spaces_by_row_column[tile_item.row][tile_item.column-1].button.configure(state=NORMAL)
                # if tile_item.row != 1 and tile_item.letter != None:
                #     board_spaces_by_row_column[tile_item.row - 2][tile_item.column - 1].button.configure(state=NORMAL)


def playBlank():
    bg_block.place(x=0, y=0)
    prompt_frame.place(x=864, y=486, anchor=CENTER)
    for slot_item in slot_list:
        slot_item.item.place(relx=1, rely=0)
    prompt_text.configure(text="What letter is the blank?")
    prompt_text.place(x=280, y=120, anchor=CENTER)
    prompt_entry.place(x=280, y=280, anchor=CENTER)
    prompt_submit_blank.place(x=280, y=360, anchor=CENTER)
    root.bind("<Return>", lambda e: submitBlank())
    prompt_entry.focus()


def submitBlank():
    entry_text = prompt_entry.get().strip().lower()
    if entry_text not in string.ascii_lowercase or entry_text == "":
        error_label.configure(text="Please enter a valid letter in the alphabet.")
        error_label.place(x=864, y=700, anchor=CENTER)
        prompt_entry.delete(0, END)
    else:
        prompt_entry.delete(0, END)
        for tile_item in board_spaces_by_serial:
            if tile_item.letter == "blank":
                tile_item.letter = entry_text
                tile_item.image = TileImage["small"][tile_item.letter]
                tile_item.button.configure(image=tile_item.image)
                #tile_item.score = Scoring.LETTER_SCORES[tile_item.letter] # Having this line would make blanks count
                root.bind("<Return>", unbind())
                error_label.place_forget()
                prompt_entry.place_forget()
                prompt_submit_blank.place_forget()
                prompt_text.place_forget()
                prompt_frame.place_forget()
                bg_block.place_forget()
                for slot_item in slot_list:
                    slot_item.item.place(relx=0, rely=0)


def invalidPrompt():
    bg_block.place(x=0, y=0)
    prompt_frame.place(x=864, y=486, anchor=CENTER)
    for slot_item in slot_list:
        slot_item.item.place(relx=1, rely=0)
    prompt_text.configure(text="The following words are invalid:")
    prompt_text.place(x=280, y=80, anchor=CENTER)
    prompt_listbox.configure(state=NORMAL)
    prompt_listbox.delete(0, END)
    for word_item in invalid_words_this_turn:
        prompt_listbox.insert(END, word_item.word)
    prompt_listbox.configure(state=DISABLED)
    prompt_listbox.place(x=280, y=280, anchor=CENTER)
    prompt_restart.place(x=280, y=500, anchor=CENTER)
    root.bind("<Return>", lambda e: invalidRestart())


def invalidRestart():
    root.bind("<Return>", unbind())
    prompt_restart.place_forget()
    prompt_listbox.place_forget()
    prompt_text.place_forget()
    prompt_frame.place_forget()
    bg_block.place_forget()
    for slot_item in slot_list:
        slot_item.item.place(relx=0, rely=0)
    restartTurn()


def placeTile(placing_letter, slot_number, number, frame, player):
    global letters_this_turn
    global letters_this_game
    global last_tile
    global first_tile_of_turn
    global second_tile_of_turn
    global tiles_used_this_turn
    global scores
    global score_this_turn
    global tiles_on_board
    global end_game_collapse
    if (placing_letter.lower() in string.ascii_lowercase) or (placing_letter.lower() == "blank"):
        for tile_item in board_spaces_by_serial:

            if tile_item.number == number:

                if placing_letter == "":
                    return
                tile_item.image = TileImage["small"][placing_letter]
                tile_item.button.configure(image=tile_item.image)

                tile_item.letter = placing_letter
                tile_item.score = Scoring.LETTER_SCORES[placing_letter]
                last_tile = tile_item
                if tile_item.letter == "blank":
                    playBlank()
                for slot in slot_list:
                    if slot.number == slot_number:
                        slot.item.winfo_children()[0].pack_forget()

                tiles_used_this_turn.append(selected_letter)
                # Reset Selection Info
                deselect()
                # Unbind this tile
                frame.winfo_children()[0].configure(command=unbind)
                letters_this_turn += 1
                letters_this_game += 1
                if letters_this_turn == 1:
                    first_tile_of_turn = last_tile

                elif letters_this_turn == 2:
                    second_tile_of_turn = last_tile

                if letters_this_game == 1:
                    updateAvailableTiles(2)
                elif turns_this_game > 0 and letters_this_turn == 1:
                    updateAvailableTiles(4)
                elif letters_this_turn > 1:
                    updateAvailableTiles(5)

                swap_letter_button.configure(bg='#a2a2a2', activebackground="#a2a2a2", state=DISABLED)
                restart_turn_button.configure(bg="#c09511", activebackground="#c09511", state=NORMAL)
                if letters_this_game > 1:
                    end_turn_button.configure(bg="#da6363", activebackground="#da6363", state=NORMAL, text="End Turn")
                break


def endTurn():
    # Some of these globals might be useless as this is split off from endTurn and i dont have time to remove redundancies
    global current_player
    global letters_this_turn
    global turns_this_game
    global first_tile_of_turn
    global second_tile_of_turn
    global player_letter_cache
    global board_cache
    global swaps_this_turn
    global swap_list
    global board_words
    global old_words
    global new_words
    global invalid_words_this_turn
    global tiles_used_this_turn
    global score_this_turn
    global subsequent_skips
    global fifty_points_bool

    # --------------DONT PUT ANYTHING ELSE IN HERE--------------

    board_words = Scoring.checkWords(board_spaces_by_row_column, board_spaces_by_column_row, board_words)

    new_words = []

    for word_item in board_words:
        if word_item not in old_words:
            new_words.append(word_item)

    invalid_words_this_turn = []
    for word_item in new_words:
        if word_item.valid == False:
            invalid_words_this_turn.append(word_item)



    # --------------OKAY YOU CAN PUT THINGS NOW--------------

    #if 0 == 0:
    if len(invalid_words_this_turn) < 1:

        old_words = tuple(board_words)

        for word_item in new_words:
            scores[current_player - 1] += word_item.modified_score

        tiles_on_board = 0
        for tile_item in board_spaces_by_serial:
            if tile_item.letter != None:
                tiles_on_board += 1
                tile_item.item.configure(bg="#c7c2a5")
                tile_item.modifier = "None"
                if tile_item.score == 0:
                    tile_item.item.configure(bg="#70207f")

        for swap_char in swap_list:
            tiles_by_player[current_player - 1].remove(swap_char)
            refillLetters(current_player)
            available_tile_list.append(
                swap_char)  # Refilling them after the turn is over prevents the amount of tiles from
            # being shown as too high. If this is done outside this loop(but still in this func), it will show the
            # subsequent players that there are less tiles than there actually are available for draw. The number of
            # tiles the player sees as "remaining" should not be how many tiles it will be next time they have to draw,
            # but rather the current amount of tiles, so if players after them have to refill at the beginning of turn,
            # this number might become 0

        for char in tiles_used_this_turn:
            tiles_by_player[current_player - 1].remove(char)
        if letters_this_turn == 7:
            scores[current_player - 1] += 50
            fifty_points_bool = True
        else:
            fifty_points_bool = False

        if end_turn_button.cget("text") == "Skip Turn":
            subsequent_skips += 1
        elif end_turn_button.cget("text") == "End Turn":
            subsequent_skips = 0

        if end_game_collapse == True and len(tiles_by_player[current_player - 1]) == 0:
            endGame(1)

        elif subsequent_skips == players:
            endGame(2)
        else:
            screenBetweenTurns()

    else:
        invalidPrompt()


def screenBetweenTurns():
    for slot_item in slot_list:
        slot_item.item.place(relx=1, rely=0)
    next_turn_button.place(x=389, y=650, anchor=CENTER)

    if current_player == players:
        which_player_label.configure(text="Player 1 is up next!")
    else:
        which_player_label.configure(text="Player " + str(current_player + 1) + " is up next!")
    which_player_label.place(x=389)

    if fifty_points_bool == True:
        got_fifty_points_label.configure(
            text="Player " + str(current_player) + " got 50 extra points for using all their tiles!")
        got_fifty_points_label.place(x=389, y=500, anchor=CENTER)
    selected_label.place_forget()
    end_turn_button.place_forget()
    restart_turn_button.place_forget()
    swap_letter_button.place_forget()
    tiles_left_label.place_forget()
    tiles_left_label.place_forget()
    updatePlayerPointDisplay()


def nextTurn():
    # Some of these globals might be useless as this is split off from endTurn and i dont have time to remove redundancies
    global current_player
    global letters_this_turn
    global turns_this_game
    global first_tile_of_turn
    global second_tile_of_turn
    global player_letter_cache
    global board_cache
    global swaps_this_turn
    global swap_list
    global board_words
    global old_words
    global new_words
    global invalid_words_this_turn
    global tiles_used_this_turn
    global score_this_turn
    global tiles_on_board
    global end_game_collapse

    selected_label.place(x=300, y=900)
    end_turn_button.place(x=36, y=850)
    restart_turn_button.place(x=36, y=750)
    swap_letter_button.place(x=36, y=650)
    next_turn_button.place_forget()
    got_fifty_points_label.place_forget()

    if current_player == players:
        current_player = 1
    else:
        current_player += 1

    refillLetters(current_player)

    which_player_label.configure(text="Player " + str(current_player))
    which_player_label.place(x=318)
    updateLetterSlots(current_player)
    deselect()

    # This must be a tuple, otherwise tiles_by_player[player - 1].remove(selected_letter) applies to this variable for some dumb reason
    player_letter_cache = tuple(tiles_by_player[current_player - 1])
    board_cache = []
    for tile_item in board_spaces_by_serial:
        board_cache.append(
            CacheSquareInfo(tile_item.item, tile_item.number, tile_item.row, tile_item.column, tile_item.button,
                            tile_item.letter, tile_item.score, tile_item.image, tile_item.command, tile_item.state,
                            tile_item.modifier))
    letters_this_turn = 0
    first_tile_of_turn = None
    second_tile_of_turn = None
    turns_this_game += 1
    swaps_this_turn = 0
    swap_list = []
    tiles_used_this_turn = []

    score_this_turn = 0
    updatePlayerPointDisplay()

    if letters_this_game == 0:
        updateAvailableTiles(1)
    else:
        updateAvailableTiles(3)

    tiles_on_board = 0
    for tile_item in board_spaces_by_serial:
        if tile_item.letter != None:
            tiles_on_board += 1
    if (tiles_on_board + len(tiles_by_player[0]) + len(tiles_by_player[1]) + len(tiles_by_player[2]) + len(
            tiles_by_player[3]) - len(tiles_used_this_turn)) >= 100:
        end_game_collapse = True
        tiles_left_label.configure(text="No more tiles in bag!", bg="#cae2ed", font=("", 36), fg="#7f0000")
    else:
        tiles_left_label.configure(text="Tiles left:" + str(len(available_tile_list)))

    tiles_left_label.place(x=318, y=500, anchor=CENTER)

    if end_game_collapse == True:
        tiles_left_label.place(x=318, y=500, anchor=CENTER)
        swap_letter_button.configure(bg="#a2a2a2", activebackground="#a2a2a2", state=DISABLED)
    else:
        swap_letter_button.configure(bg="#089f1d", activebackground="#089f1d", state=NORMAL)
    restart_turn_button.configure(bg='#a2a2a2', activebackground="#a2a2a2", state=DISABLED)
    if end_game_collapse == False:
        end_turn_button.configure(bg="#a2a2a2", activebackground="#a2a2a2", state=DISABLED, text="End Turn")
    else:
        end_turn_button.configure(bg="#da6363", activebackground="#da6363", state=NORMAL, text="Skip Turn")


# Very similar to endTurn but it was too buggy and finicky when I tried to have this function use parts of endTurn so
# that's why they're seperate functions
def restartTurn():
    global first_tile_of_turn
    global second_tile_of_turn
    global letters_this_turn
    global letters_this_game
    global tiles_by_player
    global board_spaces_by_serial
    global swaps_this_turn
    global swap_list
    global board_words
    global invalid_words_this_turn
    global tiles_used_this_turn
    global score_this_turn
    global tiles_on_board

    board_words = list(old_words)
    invalid_words_this_turn = []

    first_tile_of_turn = None
    second_tile_of_turn = None
    letters_this_game -= letters_this_turn
    letters_this_turn = 0
    swaps_this_turn = 0
    swap_list = []
    tiles_used_this_turn = []

    scores[current_player - 1] -= score_this_turn
    score_this_turn = 0
    updatePlayerPointDisplay()

    tiles_by_player[current_player - 1] = list(player_letter_cache)
    updateLetterSlots(current_player)
    deselect()

    counter = 0
    for tile_item in board_spaces_by_serial:
        tile_item.button.pack_forget()
        tile_item.tile_item = board_cache[counter].item
        tile_item.number = board_cache[counter].number
        tile_item.row = board_cache[counter].row
        tile_item.column = board_cache[counter].column
        tile_item.button = board_cache[counter].button
        tile_item.letter = board_cache[counter].letter
        tile_item.score = board_cache[counter].score
        tile_item.image = board_cache[counter].image
        tile_item.command = board_cache[counter].command
        tile_item.state = board_cache[counter].state
        tile_item.modifier = board_cache[counter].modifier
        tile_item.button.configure(image=board_cache[counter].image, command=board_cache[counter].command,
                                   state=board_cache[counter].state)
        tile_item.button.pack()
        counter += 1

    if letters_this_game == 0:
        updateAvailableTiles(1)
    else:
        updateAvailableTiles(3)

    tiles_on_board = 0
    for tile_item in board_spaces_by_serial:
        if tile_item.letter != None:
            tiles_on_board += 1

    if end_game_collapse == True:
        swap_letter_button.configure(bg="#a2a2a2", activebackground="#a2a2a2", state=DISABLED)
    else:
        swap_letter_button.configure(bg="#089f1d", activebackground="#089f1d", state=NORMAL)
    restart_turn_button.configure(bg='#a2a2a2', activebackground="#a2a2a2", state=DISABLED)

    if end_game_collapse == False:
        end_turn_button.configure(bg="#a2a2a2", activebackground="#a2a2a2", state=DISABLED, text="End Turn")
    else:
        end_turn_button.configure(bg="#da6363", activebackground="#da6363", state=NORMAL, text="Skip Turn")


# -------------------------------------------
# --------BEGGINING OF GAME FUNCTIONS--------
# -------------------------------------------
def startGame(players_arg):
    global available_tile_list
    global slot_list
    global scrabble_positions
    global board_spaces_by_serial
    global board_spaces_by_row_column
    global board_spaces_by_column_row
    global selected_letter
    global selected_slot
    global players
    global tiles_by_player
    global letters_this_turn
    global current_player
    global letters_this_game
    global turns_this_game
    global player_letter_cache
    global board_cache
    global swap_list
    global board_words
    global old_words
    global new_words
    global invalid_words_this_turn
    global tiles_used_this_turn
    global swaps_this_turn
    global scores
    global score_this_turn
    global tiles_on_board
    global end_game_collapse
    global subsequent_skips
    global game_over
    global pre_removal_scores
    global remove_score
    global benefactor_points_received

    # available_tile_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
    #                        "s", "t", "u", "v", "w", "x"]

    # A-9, B-2, C-2, D-4, E-12, F-2, G-3, H-2, I-9, J-1, K-1, L-4, M-2, N-6, O-8, P-2, Q-1, R-6, S-4, T-6, U-4, V-2, W-2, X-1, Y-2, Z-1 and Blanks-2.
    available_tile_list = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e",
                           "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h",
                           "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", "l", "m", "m", "n",
                           "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r",
                           "r", "r", "r", "r", "s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u",
                           "v", "v", "w", "w", "x", "y", "y", "z", "blank", "blank"]
    print(len(available_tile_list))

    # Creating the 7 letter slot values
    slot_list = [0, 0, 0, 0, 0, 0, 0]

    # Initial Positioning Method, becomes useless in a couple of lines
    scrabble_positions = {"row1": {}, "row2": {}, "row3": {}, "row4": {}, "row5": {},
                          "row6": {}, "row7": {}, "row8": {}, "row9": {}, "row10": {},
                          "row11": {}, "row12": {}, "row13": {}, "row14": {}, "row15": {}, }
    board_spaces_by_serial = []
    board_spaces_by_row_column = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    board_spaces_by_column_row = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    selected_letter = ""
    selected_slot = ""
    tiles_by_player = [[], [], [], []]
    letters_this_turn = 0
    current_player = 1
    letters_this_game = 0
    turns_this_game = 0
    player_letter_cache = []
    board_cache = []
    swap_list = []
    board_words = []
    old_words = []
    new_words = []
    invalid_words_this_turn = []
    tiles_used_this_turn = []
    swaps_this_turn = 0
    scores = [0, 0, 0, 0]
    score_this_turn = 0
    tiles_on_board = 0
    end_game_collapse = False
    subsequent_skips = 0
    game_over = False
    pre_removal_scores = scores
    remove_scores = scores
    benefactor_points_received = 0

    players = players_arg

    game_title.place_forget()
    two_player_button.place_forget()
    three_player_button.place_forget()
    four_player_button.place_forget()
    quit_button.place_forget()
    rules_button.place_forget()
    random_tile.place_forget()

    game_frame.place(x=777, y=21)
    selected_label.place(x=300, y=900)
    end_turn_button.place(x=36, y=850)
    restart_turn_button.place(x=36, y=750)
    swap_letter_button.place(x=36, y=650)
    which_player_label.place(x=318, y=100, anchor=CENTER)
    tiles_left_label.configure(fg="#000000")

    # First time setup stuff
    gameboardSetup()
    givePlayersSevenLetters()

    tiles_left_label.configure(text="Tiles left:" + str(len(available_tile_list)))
    tiles_left_label.place(x=318, y=500, anchor=CENTER)

    # New turn stuff
    for tile_item in board_spaces_by_serial:
        board_cache.append(
            CacheSquareInfo(tile_item.item, tile_item.number, tile_item.row, tile_item.column, tile_item.button,
                            tile_item.letter, tile_item.score, tile_item.image, tile_item.command, tile_item.state,
                            tile_item.modifier))
    player_letter_cache = tuple(tiles_by_player[0])

    updatePlayerPointDisplay()

    updateLetterSlots(1)
    updateAvailableTiles(1)


def endGame(condition):
    global pre_removal_scores
    global game_over
    global remove_score
    global scores
    global benefactor_points_received

    game_over = True

    tiles_left_label.place_forget()
    swap_letter_button.place_forget()
    restart_turn_button.place_forget()
    end_turn_button.place_forget()
    selected_label.place_forget()

    which_player_label.place(x=389, y=100, anchor=CENTER)
    menu_button.place(x=389, y=800, anchor=CENTER)

    for slot_item in slot_list:
        slot_item.item.place_forget()

    for tile_item in board_spaces_by_serial:
        tile_item.button.configure(command=unbind, state=NORMAL)
    pre_removal_scores = tuple(scores)
    remove_score = [0, 0, 0, 0]
    counter = 0

    if fifty_points_bool == True:
        got_fifty_points_label.configure(
            text="Player " + str(current_player) + " got 50 extra points for using all their tiles!")
        got_fifty_points_label.place(x=20, y=450)

    for player in tiles_by_player:
        for letter in player:
            remove_score[tiles_by_player.index(player)] += Scoring.LETTER_SCORES[letter]
        counter += 1

    if condition == 1:
        benefactor = current_player
        benefactor_points_received = 0
        for points_left in remove_score:
            benefactor_points_received += points_left

        scores[benefactor - 1] += benefactor_points_received

    counter = 0
    for score in scores:
        scores[counter] = score - remove_score[counter]
        counter += 1

    duplicateScores = checkForDuplicates(scores)

    # If all players have negative scores, then null players will win, so set their scores very negative so that if 0
    # is still higher than all ppls scores it doesnt matter
    if players < 4:
        scores[3] = -99999
    if players < 3:
        scores[2] = -99999

    if duplicateScores == [] or max(duplicateScores) < max(scores):
        which_player_label.configure(text=("Player", scores.index(max(scores)) + 1, "wins!"))
    elif max(duplicateScores) == max(scores):
        preDuplicateScores = checkForDuplicates(pre_removal_scores)

        if preDuplicateScores == [] or max(preDuplicateScores) < max(pre_removal_scores):
            which_player_label.configure(
                text=("Player", pre_removal_scores.index(max(pre_removal_scores)) + 1, "wins!"))
            technicality_label.configure(text="Two or more players tied, but since Player " + str(
                pre_removal_scores.index(
                    max(pre_removal_scores)) + 1) + " had more points pre-point addition/subtraction, they win.",
                                         justify=LEFT)

            technicality_label.place(x=20, y=498)
        else:
            which_player_label.configure(text=("Absolute Tie!"))
            technicality_label.configure(text="Two or more players tied and also had the same pre-point addition/subtraction \
             score, so it is an Absolute Tie", justify=LEFT)
            technicality_label.place(x=20, y=498)

    updatePlayerPointDisplay()


def returnToMenu(return_from):
    if return_from == "game":
        which_player_label.place_forget()
        player_points_label.place_forget()
        player_one_points_label.place_forget()
        player_two_points_label.place_forget()
        player_three_points_label.place_forget()
        player_four_points_label.place_forget()
        game_frame.place_forget()
        technicality_label.place_forget()
        got_fifty_points_label.place_forget()
        menu_button.place_forget()
    elif return_from == "rules":
        rules_text.place_forget()
        rules_scroll_frame.place_forget()
        rules_scroller.place_forget()

    game_title.place(x=864, y=200, anchor=CENTER)
    two_player_button.place(x=414, y=400, anchor=CENTER)
    three_player_button.place(x=864, y=400, anchor=CENTER)
    four_player_button.place(x=1314, y=400, anchor=CENTER)
    quit_button.place(x=1394, y=800)
    random_tile.configure(image=TileImage["large"][random.choice(string.ascii_lowercase)])
    random_tile.place(x=864, y=733, anchor=CENTER)
    rules_button.configure(command = lambda: showRules(),text="Rules")


def showRules():
    game_title.place_forget()
    two_player_button.place_forget()
    three_player_button.place_forget()
    four_player_button.place_forget()
    quit_button.place_forget()
    random_tile.place_forget()

    # rules_scroll_frame = Frame(width=30, height=900, bg="#FF0000")
    #
    # rules_scroller = Scrollbar(width=30)
    #
    # rules_text = Text(width=1200, height=900, yscrollcommand=rules_scroller.set)
    # for i in range(1000):
    #     rules_text.insert(END, "YO MAN ORDER ME A NUMBA " + str(i))
    #
    # rules_scroller.config(command=rules_text.yview))
    rules_text.place(x=398, y=21)
    rules_scroll_frame.place(x=1598, y=21)
    rules_scroller.place(x=0, y=0, height=900)
    rules_button.configure(command = lambda: returnToMenu("rules"),text="Menu")


root.mainloop()
