import pygame  # import pygame module
import questions_lists

pygame.init()  # initialize pygame module

WIDTH = 1000  # set screen to fixed 1000 pixels width
HEIGHT = 800  # set screen to fixed 800 pixels height
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # define screen dimensions
pygame.display.set_caption('Trivia Game!')  # caption at top of window
timer = pygame.time.Clock()  # define clock for pygame game loop running at fixed speed
font = pygame.font.Font('freesansbold.ttf', 32)  # import generic font file in 'regular' size
big_font = pygame.font.Font('freesansbold.ttf', 48)  # import generic font file in 'large' size
fps = 60  # define gameplay frame rate
mode = 0  # mode to track whether we are in single jeopardy, double jeopardy or final jeopardy
w = WIDTH / 5  # individual square width based on overall screen size for squares drawn during gameplay
h = HEIGHT / 6  # see above note but for height
text_id = 4549
answered_count = 0  # track how many questions have been answered
answered = [[False for _ in range(5)] for _ in range(5)]  # list to track which questions have been answered
# get list of questions from text files scraped from jeopardy website
questions_list = questions_lists.get_list(text_id)
# print(questions_list)
players = [{'name': 'CME 1', 'score': 0},
           {'name': 'CME 2', 'score': 0},
           {'name': 'CME 3', 'score': 0}]  # initial names of players and initial scores at zero
active_question = False  # bit to track whether or not there's an active question
who_went = [False, False, False]  # list to track which players have answered the active question
player_active = 0  # integer tpo track which player is answering
active_size = [w, h]  # size of the box as a question is growing to fill the window
countdown_sp = 300  # time (5 seconds @ 60 fps) that a question stays on screen for
countdown_tmr = 300  # time countdown after a player starts answering to complete their answer
menu_active = True  # is the menu screen currently up
reset_menu = False  # is the reset menu currently up
rules_menu = False  # is the rules menu currently up
info_menu = False  # is the info menu currently up
build_menu = False  # is the 'build a level' menu currently up
load_menu = False  # is the 'load a saved level' menu currently up?
popup = False  # tracker if we are in any popup menu or not
reset_popup = False  # close out of the popup windows
add_it = False  # bit for appending characters in the adjust scores and player info screen
remove_it = False  # bit for removing characters in the adjust scores and player info screen
reveal_final = False  # when final jeopardy is active, bit to control whether or not to reveal the answer
mode = 0  # 0 single jeopardy, 1 double jeopardy, 2 final jeopardy
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']
characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
              '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ', '!',
              '@', '#', '$', '%', '^', '&', '*', '(', ')', '~', '`', '-', '_',
              '/', '\\', '\'', '+', '=', ':', ';', '"', '<', '>', ',', '.', '?']  # list of valid characters for typing


# creating a class for all clickable buttons in the game
class Button:
    def __init__(self, x, y, wid, hgt, text, color, font_size, can_click):
        self.x = x
        self.y = y
        self.wid = wid
        self.hgt = hgt
        self.text = text
        self.color = color
        self.font_size = font_size
        self.rect = pygame.rect.Rect((self.x, self.y), (self.wid + 1, self.hgt))
        self.can_click = can_click
        self.split = not can_click
        self.clicked = False

    def draw(self):  # displays different colors based on mouse position and click status
        if self.rect.collidepoint(mouse_pos) and self.can_click:
            if clicked[0]:
                color = 'light blue'
                self.clicked = True
            else:
                self.clicked = False
                color = 'dark blue'
        else:
            self.clicked = False
            color = 'blue'
        pygame.draw.rect(screen, color, [self.x, self.y, self.wid + 1, self.hgt])
        pygame.draw.rect(screen, 'black', [self.x, self.y, self.wid, self.hgt - 1], 2)
        fnt = pygame.font.Font('freesansbold.ttf', self.font_size)
        if self.split:
            rows = len(self.text) // 10 + 1
            for ind in range(rows):
                txt = fnt.render(self.text[10 * ind:10 * ind + 10], True, 'white')
                screen.blit(txt, (self.x + 5, self.y + 10 + 20 * ind))
        else:
            txt = fnt.render(self.text, True, 'white')
            screen.blit(txt, (self.x + 5, self.y + 15))


# class for the numerical entry boxes on the edit player info screen
class EntryBox:
    def __init__(self, x, y, text, color, font_size, numerical):
        self.x = x
        self.y = y
        self.text = str(text)
        self.color = color
        self.font_size = font_size
        self.rect = None
        self.selected = False
        self.numerical = numerical

    def draw(self):
        global add_it, remove_it
        if self.text == '':
            if self.numerical:
                self.text = '0'
            else:
                self.text = '_'
        fnt = pygame.font.Font('freesansbold.ttf', self.font_size)
        txt = fnt.render(self.text, True, 'white')
        self.rect = txt.get_rect()
        self.rect.topleft = self.x, self.y
        if clicked[0]:
            if self.rect.collidepoint(mouse_pos):
                self.selected = True
            else:
                self.selected = False
        if self.selected:
            bg = 'blue'
            if add_it:
                if not self.numerical:
                    self.text += character
                    if len(self.text) > 1 and self.text[0] == '_':
                        self.text = self.text[1:]
                elif number:
                    if character == '-':
                        if self.text[0] == '-':
                            self.text = self.text[1:]
                        else:
                            self.text = '-' + self.text
                    else:
                        self.text += character
                    if len(self.text) > 1 and self.text[0] == '0':
                        self.text = self.text[1:]
                    elif len(self.text) > 2 and self.text[:2] == '-0':
                        self.text = '-' + self.text[2:]
                add_it = False
            if remove_it:
                self.text = self.text[0:-1]
                if self.numerical:
                    if self.text == '':
                        self.text = '0'
                    elif self.text == '-':
                        self.text = '-0'
                remove_it = False
        else:
            bg = 'black'
        pygame.draw.rect(screen, bg, self.rect, 0, 3)
        screen.blit(txt, (self.x, self.y))


# main program for drawing the primary game area on the screen
def draw_board():
    if mode < 2:  # this means single or double jeopardy use the following system to get questions and display the grid
        for i in range(5):
            for j in range(5):
                my_txt = questions_list[f'category {mode}{i + 1}'][(j + 1) * 200 * (mode + 1)]
                # my_txt has the questions and answers of each question inside it
                if not answered[i][j]:
                    txt = '$ ' + str((j + 1) * 200 * (mode + 1))
                else:
                    txt = ''
                btn = Button(w * i, h * (j + 1), w + 1, h + 1, txt, 'blue', 48, not answered[i][j])
                btn.draw()
            btn = Button(w * i, 0, w + 1, h + 1, questions_list[f'category {mode}{i + 1}']['title'], 'blue', 24, False)
            btn.draw()

        pygame.draw.line(screen, 'black', (0, h - 5), (WIDTH, h - 5), 10)
        pygame.draw.line(screen, 'black', (0, 5 * h - 5), (WIDTH, 5 * h - 5), 10)
    else:  # the only other mode is final jeopardy
        txt = big_font.render(f'FINAL JEOPARDY: ' + questions_list[f'final'][2], True, 'white')
        screen.blit(txt, (5, 5))

        final_question = questions_list[f'final'][0]
        rows = len(final_question) // 40 + 1
        for ind in range(rows):
            txt = big_font.render(final_question[40 * ind:40 * ind + 40], True, 'white')
            screen.blit(txt, (5, 100 + 40 * ind))
        if reveal_final:
            final_answer = questions_list[f'final'][1]
            rows = len(final_answer) // 40 + 1
            for ind in range(rows):
                txt = big_font.render(final_answer[40 * ind:40 * ind + 40], True, 'white')
                screen.blit(txt, (5, 400 + 40 * ind))
        else:
            txt = big_font.render('Click here to reveal answer', True, 'white')
            screen.blit(txt, (5, 400))

    menu = Button(w * 4.5 + 5, h * 6 + 5, 1.5 * w - 10, h - 10, '   MENU', 'blue', 48, True)
    menu.draw()
    return menu


# main navigation menu
def draw_menu():
    pygame.draw.rect(screen, 'gray', [20, 20, WIDTH - 40, HEIGHT - 40], 0, 10)
    pygame.draw.rect(screen, 'black', [20, 20, WIDTH - 40, HEIGHT - 40], 5, 10)
    menu = Button(w * 4.5 - 15, h * 6 - 15, 1.5 * w - 10, h - 5, ' RETURN', 'blue', 48, True)
    menu.draw()
    screen.blit(big_font.render('Trivia Game Menu:', True, 'black'), (WIDTH / 4, 30))
    load = Button(30, 80, WIDTH - 60, 80, 'Load Saved Level', 'blue', 48, True)
    load.draw()
    info = Button(30, 170, WIDTH - 60, 80, 'Edit Player Information', 'blue', 48, True)
    info.draw()
    build = Button(30, 260, WIDTH - 60, 80, 'Create a Level', 'blue', 48, True)
    build.draw()
    leave = Button(30, 530, WIDTH - 60, 80, 'Exit the Program', 'blue', 48, True)
    leave.draw()
    restart = Button(30, 440, WIDTH - 60, 80, 'Restart Current Game', 'blue', 48, True)
    restart.draw()
    rules = Button(30, 350, WIDTH - 60, 80, 'Rules and Instructions', 'blue', 48, True)
    rules.draw()
    return [menu, load, info, build, leave, restart, rules]


# drawing the players names and scores in the bottom of the window
def draw_players():
    for i in range(3):
        btn = Button(w * 1.5 * i + 5, h * 6 + 5, 1.5 * w - 10, h - 10, players[i]['name'], 'blue', 48, True)
        btn.draw()
        if players[i]["score"] >= 0:
            color = 'white'
        else:
            color = 'red'
        screen.blit(font.render(f'$ {players[i]["score"]}', True, color), (w * 1.5 * i + 15, h * 6.5 + 10))


# splitting long strings of text
def parse_text(input_text):
    string_list = []
    current_string = ''
    for i in range(len(input_text)):
        if len(current_string) < 25:
            current_string += input_text[i]
        elif input_text[i] == ' ':
            string_list.append(current_string)
            current_string = ''
        else:
            current_string += input_text[i]
    string_list.append(current_string)
    return string_list


# if there's an active question have the box grow to fill the screen then show the text
def draw_question(coords):
    sev = WIDTH // 7
    col = coords[0]
    row = coords[1]
    cat_txt = f'category {mode}{col + 1}'
    my_txt = questions_list[cat_txt][(row + 1) * 200 * (mode + 1)]
    strings_list = parse_text(my_txt[0])
    for i in range(len(strings_list)):
        screen.blit(big_font.render(strings_list[i], True, 'white'), (50, h + 50 + 50 * i))
    if player_active == 0:
        color = 'white'
    else:
        color = 'light green'
        pygame.draw.rect(screen, 'light green', [w * 1.5 * (player_active - 1) + 5, h * 6 + 5, 1.5 * w - 10, h - 10], 5)
    pct_done = ((countdown_sp - countdown_tmr) / countdown_sp) * 100
    rect_count = int((100 - pct_done) // 25) + 1
    for i in range(rect_count):
        pygame.draw.rect(screen, color, [WIDTH / 2 - 0.5 * sev + sev * i, 5.8 * h, sev, 0.1 * h], 0, 5)
        pygame.draw.rect(screen, color, [WIDTH / 2 - 0.5 * sev - sev * i, 5.8 * h, sev, 0.1 * h], 0, 5)


# logic for the coordinate growth from single question to full screen
def adjust_coords(coords, size):
    if coords[0] > 0:
        coords[0] -= 20
    elif coords[0] != 0:
        coords[0] = 0
    if coords[1] > h:
        coords[1] -= 15
    elif coords[1] != h:
        coords[1] = h
    if size[0] < WIDTH:
        size[0] += 40
    elif size[0] != WIDTH:
        size[0] = WIDTH
    if size[1] < 5 * h:
        size[1] += 20
    elif size[1] != 5 * h:
        size[1] = 5 * h
    return coords, size


# when someone is answering a question, draw yes and no buttons for the game master to click
def draw_yes_no():
    yes = Button(w * 5, h * 5, w / 2, 0.5 * h, 'Right!', 'blue', 18, True)
    no = Button(w * 5.5, h * 5, w / 2, 0.5 * h, 'Wrong :(', 'blue', 18, True)
    yes.draw()
    no.draw()
    return yes, no


# text explaining how to play the game and use the python program
def draw_rules():
    pygame.draw.rect(screen, 'gray', [20, 20, WIDTH - 40, HEIGHT - 40], 0, 10)
    pygame.draw.rect(screen, 'black', [20, 20, WIDTH - 40, HEIGHT - 40], 5, 10)
    return_btn = Button(w * 4.5 - 15, h * 6 - 15, 1.5 * w - 10, h - 5, ' RETURN', 'blue', 48, True)
    return_btn.draw()
    screen.blit(big_font.render('Rules and Instructions:', True, 'black'), (WIDTH / 5, 30))
    screen.blit(font.render("Use the Level Scraper.py function to generate text files", True, 'black'),
                (25, 130))
    screen.blit(font.render("Change the number of text_id in row 16 of main.py to change levels", True,
                            'black'),
                (25, 230))
    screen.blit(
        font.render("Edit player info and adjust scores if mistakes are made", True,
                    'black'),
        (25, 330))
    screen.blit(font.render("Have a 'host' control scoring for players and read the", True,
                            'black'), (25, 430))
    screen.blit(font.render("answers in the python console window", True,
                            'black'), (25, 470))
    screen.blit(font.render("Final Jeopardy have players write down guesses and wagers somewhere", True,
                            'black'), (25, 530))
    screen.blit(font.render("and manually adjust scores after revealing answers", True,
                            'black'), (25, 570))
    return return_btn


# draw the player info and give the ability for changing names and scores
def draw_info():
    pygame.draw.rect(screen, 'gray', [20, 20, WIDTH - 40, HEIGHT - 40], 0, 10)
    pygame.draw.rect(screen, 'black', [20, 20, WIDTH - 40, HEIGHT - 40], 5, 10)
    return_btn = Button(w * 4.5 - 15, h * 6 + 5, 1.5 * w - 10, h - 25, ' RETURN', 'blue', 48, True)
    return_btn.draw()
    screen.blit(big_font.render('Edit Player Info:', True, 'black'), (WIDTH / 5, 30))
    pygame.draw.rect(screen, 'black', [20, 90, WIDTH - 40, 205], 5, 1)
    pygame.draw.rect(screen, 'black', [20, 290, WIDTH - 40, 205], 5, 1)
    pygame.draw.rect(screen, 'black', [20, 490, WIDTH - 40, 200], 5, 1)
    for i in range(3):
        screen.blit(font.render(f'Player {i + 1} Name:', True, 'black'), (30, 200 * i + 110))
        screen.blit(font.render(f'Player {i + 1} Score:', True, 'black'), (30, 200 * i + 180))
    player1.draw()
    play1_score.draw()
    player2.draw()
    play2_score.draw()
    player3.draw()
    play3_score.draw()
    players[0]['name'] = player1.text
    players[1]['name'] = player2.text
    players[2]['name'] = player3.text
    players[0]['score'] = int(play1_score.text)
    players[1]['score'] = int(play2_score.text)
    players[2]['score'] = int(play3_score.text)
    return return_btn


# loading menu I never built (its just not that hard to change the # of the text file you want)
def draw_load():
    pygame.draw.rect(screen, 'gray', [20, 20, WIDTH - 40, HEIGHT - 40], 0, 10)
    pygame.draw.rect(screen, 'black', [20, 20, WIDTH - 40, HEIGHT - 40], 5, 10)
    return_btn = Button(w * 4.5 - 15, h * 6 - 15, 1.5 * w - 10, h - 5, ' RETURN', 'blue', 48, True)
    return_btn.draw()
    screen.blit(big_font.render('Load a Saved Level:', True, 'black'), (WIDTH / 5, 30))
    screen.blit(font.render("Sure would be cool for you to add this yourself :)", True, 'black'),
                (25, 330))
    return return_btn


# build your own level similar to laod menu is just not that hard to do manually. save a text file under a new #
def draw_build():
    pygame.draw.rect(screen, 'gray', [20, 20, WIDTH - 40, HEIGHT - 40], 0, 10)
    pygame.draw.rect(screen, 'black', [20, 20, WIDTH - 40, HEIGHT - 40], 5, 10)
    return_btn = Button(w * 4.5 - 15, h * 6 - 15, 1.5 * w - 10, h - 5, ' RETURN', 'blue', 48, True)
    return_btn.draw()
    screen.blit(big_font.render('Build a New Level:', True, 'black'), (WIDTH / 5, 30))
    screen.blit(font.render("Sure would be cool for you to add this yourself :)", True, 'black'),
                (25, 330))
    return return_btn


# see if all the questions have been answered and if they have, go up one mode
def check_mode(mod, answr):
    done = True
    for i in range(len(answr)):
        for j in range(len(answr[i])):
            if not answr[i][j]:
                done = False
    if done:
        mod += 1
        answr = [[False for _ in range(5)] for _ in range(6)]
    return mod, answr


# entry box definitions
player1 = EntryBox(270, 100, players[0]['name'], 'black', 48, False)
play1_score = EntryBox(270, 180, players[0]['score'], 'black', 48, True)
player2 = EntryBox(270, 300, players[1]['name'], 'black', 48, False)
play2_score = EntryBox(270, 380, players[1]['score'], 'black', 48, True)
player3 = EntryBox(270, 500, players[2]['name'], 'black', 48, False)
play3_score = EntryBox(270, 580, players[2]['score'], 'black', 48, True)

# main game loop
run = True
while run:
    screen.fill('dark gray')
    timer.tick(fps)
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if not menu_active:  # logic for handling ordinary game play (not menus)
        menu_btn = draw_board()
        draw_players()

        if clicked[0] and mode < 2:  # if left mouse button clicked and its single or double jeopardy
            if not active_question:  # if question isnt already active, check where the mouse was when clicking
                player_active = 0
                who_went = [False, False, False]
                countdown_tmr = countdown_sp
                if h < mouse_pos[1] < h * 6:
                    active_id = [int(mouse_pos[0] // w), (int(mouse_pos[1] // h) - 1)]
                    active_coords = [active_id[0] * w, active_id[1] * h]
                    # print(active_id)
                    if not answered[int(active_id[0])][int(active_id[1])]:
                        active_question = True
                        active_size = [w, h]
                        answered[active_id[0]][active_id[1]] = True
                        my_text = questions_list[f'category {mode}{active_id[0] + 1}'][
                            (active_id[1] + 1) * 200 * (mode + 1)]
                        print(my_text[1])
            elif player_active == 0:
                if HEIGHT - h < mouse_pos[1] and mouse_pos[0] < w * 4.5:
                    player_click = (int(mouse_pos[0] // (w * 1.5)))
                    if not who_went[player_click]:
                        player_active = player_click + 1
                        who_went[player_active - 1] = True
                        countdown_tmr = countdown_sp
        elif clicked[0] and mode == 2:  # if its final jeopardy see if the area to reveal the question was clicked
            if 400 < mouse_pos[1] < 500:
                reveal_final = True
        if active_question:  # logic for handling active question logic growing and allowing for yes no answers
            pygame.draw.rect(screen, 'blue', [active_coords[0], active_coords[1], active_size[0], active_size[1]])
            if active_size == [WIDTH, 5 * h] and active_coords == [0, h]:
                draw_question(active_id)
                if countdown_tmr > 0:
                    countdown_tmr -= 1
                else:
                    countdown_tmr = countdown_sp
                    active_question = False
            if player_active != 0:
                right, wrong = draw_yes_no()
            else:
                active_coords, active_size = adjust_coords(active_coords, active_size)
    else:  # some menu is active, handle the menus here
        if not popup:  # if not popup active then base menu is shown
            buttons_list = draw_menu()  # [menu, load, info, build, leave, restart, rules]
            menu_btn = buttons_list[0]
            if buttons_list[1].clicked:
                popup = True
                load_menu = True
            if buttons_list[2].clicked:
                popup = True
                info_menu = True
            if buttons_list[3].clicked:
                popup = True
                build_menu = True
            if buttons_list[4].clicked:
                run = False
            if buttons_list[5].clicked:
                for i in range(3):
                    players[i]['score'] = 0
                answered_count = 0
                answered = [[False for _ in range(5)] for _ in range(5)]
                reset_menu = True
                reveal_final = False
                mode = 0
            if buttons_list[6].clicked:
                popup = True
                rules_menu = True
        else:
            if load_menu:
                leave = draw_load()
                if leave.clicked:
                    reset_popup = True
                    load_menu = False
            if info_menu:
                leave = draw_info()
                if leave.clicked:
                    reset_popup = True
                    info_menu = False
            if build_menu:
                leave = draw_build()
                if leave.clicked:
                    reset_popup = True
                    build_menu = False
            if rules_menu:
                leave = draw_rules()
                if leave.clicked:
                    reset_popup = True
                    rules_menu = False

    for event in pygame.event.get():  # event handling logic for clicking on buttons and other key strokes
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP and player_active != 0 and not menu_active:  # right/wrong + score changes
            if right.clicked:
                players[player_active - 1]['score'] += (active_id[1] + 1) * 200 * (mode + 1)
                active_question = False
                player_active == 0
                mode, answered = check_mode(mode, answered)
            elif wrong.clicked:
                players[player_active - 1]['score'] -= (active_id[1] + 1) * 200 * (mode + 1)
                player_active = 0
                if False in who_went:
                    countdown_tmr = countdown_sp
                else:
                    countdown_tmr = 1
                    mode, answered = check_mode(mode, answered)
            play1_score.text = str(players[0]['score'])
            play2_score.text = str(players[1]['score'])
            play3_score.text = str(players[2]['score'])
        elif event.type == pygame.MOUSEBUTTONUP:  # enter menus, or click on menu buttons
            if menu_btn.clicked or reset_menu:
                if not menu_active:
                    menu_active = True
                else:
                    menu_active = False
                    reset_menu = False
            if reset_popup:
                popup = False
                reset_popup = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                remove_it = True
            elif event.unicode in characters:
                character = event.unicode
                if character in numbers:
                    number = True
                else:
                    number = False
                add_it = True
        elif event.type == pygame.KEYUP:
            add_it = False
            remove_it = False

    pygame.display.flip()  # display everything on the screen
pygame.quit()  # close the program if main game loop is exited
