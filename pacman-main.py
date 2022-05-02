import subprocess
import tkinter, copy, time, sys, pygame, json, os, platform
from tkinter import messagebox

from pygame.locals import *


# class responsible for initial main menu with all methods it needs
click = False

class mainMenu():
    # Setup pygame/window ---------------------------------------- #

    def __init__(self):
        self.mainClock = pygame.time.Clock()

        pygame.init()
        pygame.display.init()
        pygame.display.set_caption('Game base')
        self.screen = pygame.display.set_mode((500, 600), 0, 32)

        self.font = pygame.font.SysFont('freesansbold.ttf', 20)

        self.level = 0
        self.running = True
        self.mainLoop = True
        self.balance = 0

    # method used for drawing text on pygame canvas
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    # displaying main menu and handling actions in order to let user choose different menu options
    def main_menu(self):
        global click
        while self.mainLoop:

            self.screen.fill((0, 0, 0))
            self.draw_text('Main Menu', self.font, (255, 255, 255), self.screen, 20, 20)

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(150, 50, 200, 50)
            button_2 = pygame.Rect(150, 125, 200, 50)
            button_3 = pygame.Rect(150, 125, 200, 50)
            button_4 = pygame.Rect(150, 200, 200, 50)
            button_5 = pygame.Rect(150, 275, 200, 50)
            button_6 = pygame.Rect(150, 350, 200, 50)

            if button_1.collidepoint((mx, my)):
                if click:
                    self.game()
            # if button_2.collidepoint((mx, my)):
            #     if click:
            #         self.options()
            if button_3.collidepoint((mx, my)):
                if click:
                    self.store()
            if button_4.collidepoint((mx, my)):
                if click:
                    self.highscore()
            if button_5.collidepoint((mx, my)):
                if click:
                    self.help()
            if button_6.collidepoint((mx, my)):
                if click:
                    self.exit_game()
            pygame.draw.rect(self.screen, (255, 255, 0), button_1)
            self.draw_text("Play!", self.font, (0, 0, 0), self.screen, (150 + 80), (50 + (50 / 2)))
            # pygame.draw.rect(self.screen, (255, 255, 0), button_2)
            # self.draw_text("Options", self.font, (0, 0, 0), self.screen, (150 + 80), (125 + (50 / 2)))
            pygame.draw.rect(self.screen, (255, 255, 0), button_3)
            self.draw_text("Store", self.font, (0, 0, 0), self.screen, (150 + 80), (125 + (50 / 2)))
            pygame.draw.rect(self.screen, (255, 255, 0), button_4)
            self.draw_text("Highscore", self.font, (0, 0, 0), self.screen, (150 + 80), (200 + (50 / 2)))
            pygame.draw.rect(self.screen, (255, 255, 0), button_5)
            self.draw_text("Help", self.font, (0, 0, 0), self.screen, (150 + 80), (275 + (50 / 2)))
            pygame.draw.rect(self.screen, (255, 255, 0), button_6)
            self.draw_text("Exit", self.font, (0, 0, 0), self.screen, (150 + 80), (350 + (50 / 2)))

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.mainClock.tick(60)
        pygame.display.quit()
        return

    # allows players to choose from available levels and runs the game
    def game(self):
        global click, level, runGame
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            self.draw_text('Game', self.font, (255, 255, 255), self.screen, 20, 20)
            self.draw_text('Select level', pygame.font.SysFont('freesansbold.ttf', 50), (255, 255, 255), self.screen,
                           70, 40)

            mx, my = pygame.mouse.get_pos()

            level_1_button = pygame.Rect(150, 125, 200, 50)
            level_2_button = pygame.Rect(150, 200, 200, 50)

            if level_1_button.collidepoint((mx, my)):
                if click:
                    self.level = 1
                    runGame = True
                    self.mainLoop = False
                    break
            if level_2_button.collidepoint((mx, my)):
                if click:
                    self.level = 2
                    runGame = True
                    self.mainLoop = False
                    break

            pygame.draw.rect(self.screen, (255, 255, 0), level_1_button)
            self.draw_text("Level 1", self.font, (0, 0, 0), self.screen, (150 + 80), (125 + (50 / 2)))
            pygame.draw.rect(self.screen, (255, 255, 0), level_2_button)
            self.draw_text("Level 2", self.font, (0, 0, 0), self.screen, (150 + 80), (200 + (50 / 2)))

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.mainClock.tick(60)

    def options(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            self.draw_text('Options', self.font, (255, 255, 255), self.screen, 20, 20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            self.mainClock.tick(60)

    # handles displaying the store items, logic behind economy and purchases, also allows players to equip purchased skins
    def store(self):
        global click, equippedSkin
        running = True
        # loads data from json files
        jsonFile = open("storeItems.json", "r")
        jsonObject = json.load(jsonFile)
        jsonFile.close()
        playerFile = open('player_info.json', 'r')
        jsonObjectPlayer = json.load(playerFile)
        playerFile.close()
        self.balance = jsonObjectPlayer["money"]
        x = 0
        y = 100

        number = 50

        self.screen.fill((0, 0, 0))

        self.draw_text('Store', self.font, (255, 255, 255), self.screen, 20, 20)
        self.draw_text('Current balance: ' + str(self.balance), self.font, (255, 255, 255), self.screen, 20, 40)
        # display store items
        for key in jsonObject:
            print(key)
            # itemRect = pygame.Rect(x + number, y, 100, 50)
            image = pygame.image.load('images/doprava1-' + key + '.gif').convert()
            if (key != 'yellow'):
                image = pygame.transform.scale(image, (250, 190))
                self.screen.blit(image, (x + number - 80, y-60))
            else:
                self.screen.blit(image, (93, 125))
            number += 110

        buy_1 = pygame.Rect(x + 50, y + 60, 100, 30)
        buy_2 = pygame.Rect(x + 160, y + 60, 100, 30)
        buy_3 = pygame.Rect(x + 270, y + 60, 100, 30)
        buy_4 = pygame.Rect(x + 380, y + 60, 100, 30)

        equip_1 = pygame.Rect(x + 50, y + 100, 100, 30)
        equip_2 = pygame.Rect(x + 160, y + 100, 100, 30)
        equip_3 = pygame.Rect(x + 270, y + 100, 100, 30)
        equip_4 = pygame.Rect(x + 380, y + 100, 100, 30)

        # based on data from json display correct buttons and options for users
        pygame.draw.rect(self.screen, (255, 255, 255), buy_1)
        if jsonObject['yellow'][0]['purchased'] == 'false':
            self.draw_text(str(jsonObject['yellow'][0]['cost']), self.font, (0, 0, 0), self.screen, (x + 50 + 30),
                           (y + 70))
        else:
            self.draw_text('Purchased', self.font, (0, 0, 0), self.screen, (x + 50 + 20), (y + 70))
            pygame.draw.rect(self.screen, (255, 255, 255), equip_1)
            if (jsonObjectPlayer['skin'] == 'yellow'):
                self.draw_text('Equipped', self.font, (0, 0, 0), self.screen, (x + 50 + 20), (y + 110))
            else:
                self.draw_text('Equip', self.font, (0, 0, 0), self.screen, (x + 50 + 20), (y + 110))
        pygame.draw.rect(self.screen, (255, 255, 255), buy_2)
        if jsonObject['blue'][0]['purchased'] == 'false':
            self.draw_text(str(jsonObject['blue'][0]['cost']), self.font, (0, 0, 0), self.screen, (x + 160 + 30),
                           (y + 60 + 10))
        else:
            self.draw_text('Purchased', self.font, (0, 0, 0), self.screen, (x + 160 + 20), (y + 70))
            pygame.draw.rect(self.screen, (255, 255, 255), equip_2)
            if (jsonObjectPlayer['skin'] == 'blue'):
                self.draw_text('Equipped', self.font, (0, 0, 0), self.screen, (x + 160 + 20), (y + 110))
            else:
                self.draw_text('Equip', self.font, (0, 0, 0), self.screen, (x + 160 + 20), (y + 110))
        pygame.draw.rect(self.screen, (255, 255, 255), buy_3)
        if jsonObject['green'][0]['purchased'] == 'false':
            self.draw_text(str(jsonObject['green'][0]['cost']), self.font, (0, 0, 0), self.screen, (x + 270 + 30),
                           (y + 60 + 10))
        else:
            self.draw_text('Purchased', self.font, (0, 0, 0), self.screen, (x + 270 + 20), (y + 70))
            pygame.draw.rect(self.screen, (255, 255, 255), equip_3)
            if (jsonObjectPlayer['skin'] == 'green'):
                self.draw_text('Equipped', self.font, (0, 0, 0), self.screen, (x + 270 + 20), (y + 110))
            else:
                self.draw_text('Equip', self.font, (0, 0, 0), self.screen, (x + 270 + 20), (y + 110))
        pygame.draw.rect(self.screen, (255, 255, 255), buy_4)
        if jsonObject['pink'][0]['purchased'] == 'false':
            self.draw_text(str(jsonObject['pink'][0]['cost']), self.font, (0, 0, 0), self.screen, (x + 380 + 30),
                           (y + 60 + 10))
        else:
            self.draw_text('Purchased', self.font, (0, 0, 0), self.screen, (x + 380 + 20), (y + 70))
            pygame.draw.rect(self.screen, (255, 255, 255), equip_4)
            if (jsonObjectPlayer['skin'] == 'pink'):
                self.draw_text('Equipped', self.font, (0, 0, 0), self.screen, (x + 380 + 20), (y + 110))
            else:
                self.draw_text('Equip', self.font, (0, 0, 0), self.screen, (x + 380 + 20), (y + 110))

        while running:
            mx, my = pygame.mouse.get_pos()

            purchase = False

            # handles purchase actions and economy, modify json files according to user actions
            if buy_1.collidepoint((mx, my)):
                if click:
                    if jsonObject["yellow"][0]["purchased"] == "false":
                        yellowCost = jsonObject["yellow"][0]["cost"]
                        if int(yellowCost) > self.balance:
                            messagebox.showinfo('Not enough money', 'OK')
                        else:
                            self.balance = self.balance - int(yellowCost)
                            jsonObject['yellow'][0]['purchased'] = 'true'
                            jsonFile = open('storeItems.json', 'w')
                            json.dump(jsonObject, jsonFile)
                            purchase = True

            if buy_2.collidepoint((mx, my)):
                if click:
                    if jsonObject["blue"][0]["purchased"] == "false":
                        yellowCost = jsonObject["blue"][0]["cost"]
                        if int(yellowCost) > self.balance:
                            messagebox.showinfo('Not enough money', 'OK')
                        else:
                            self.balance = self.balance - int(yellowCost)
                            jsonObject['blue'][0]['purchased'] = 'true'
                            jsonFile = open('storeItems.json', 'w')
                            json.dump(jsonObject, jsonFile)
                            purchase = True

            if buy_3.collidepoint((mx, my)):
                if click:
                    if jsonObject["green"][0]["purchased"] == "false":
                        yellowCost = jsonObject["green"][0]["cost"]
                        if int(yellowCost) > self.balance:
                            messagebox.showinfo('Not enough money', 'OK')
                        else:
                            self.balance = self.balance - int(yellowCost)
                            jsonObject['green'][0]['purchased'] = 'true'
                            jsonFile = open('storeItems.json', 'w')
                            json.dump(jsonObject, jsonFile)
                            purchase = True

            if buy_4.collidepoint((mx, my)):
                if click:
                    if jsonObject["pink"][0]["purchased"] == "false":
                        yellowCost = jsonObject["pink"][0]["cost"]
                        if int(yellowCost) > self.balance:
                            messagebox.showinfo('Not enough money', 'OK')
                        else:
                            self.balance = self.balance - int(yellowCost)
                            jsonObject['pink'][0]['purchased'] = 'true'
                            jsonFile = open('storeItems.json', 'w')
                            json.dump(jsonObject, jsonFile)
                            purchase = True
            # handles equip actions
            if equip_1.collidepoint((mx, my)):
                if click:
                    if jsonObjectPlayer["skin"] != "yellow":
                        jsonObjectPlayer["skin"] = "yellow"
                        jsonFile = open('player_info.json', 'w')
                        json.dump(jsonObjectPlayer, jsonFile)
                        jsonFile.close()
                        self.store()

            if equip_2.collidepoint((mx, my)):
                if click:
                    if jsonObjectPlayer["skin"] != "blue":
                        jsonObjectPlayer["skin"] = "blue"
                        jsonFile = open('player_info.json', 'w')
                        json.dump(jsonObjectPlayer, jsonFile)
                        jsonFile.close()
                        self.store()

            if equip_3.collidepoint((mx, my)):
                if click:
                    if jsonObjectPlayer["skin"] != "green":
                        jsonObjectPlayer["skin"] = "green"
                        jsonFile = open('player_info.json', 'w')
                        json.dump(jsonObjectPlayer, jsonFile)
                        jsonFile.close()
                        self.store()

            if equip_4.collidepoint((mx, my)):
                if click:
                    if jsonObjectPlayer["skin"] != "pink":
                        jsonObjectPlayer["skin"] = "pink"
                        jsonFile = open('player_info.json', 'w')
                        json.dump(jsonObjectPlayer, jsonFile)
                        jsonFile.close()
                        self.store()

            # changes data in storeItems.json based on user actions
            if (purchase):
                jsonFile.close()
                playerFile = open("player_info.json", "w")
                jsonObjectPlayer['money'] = self.balance
                json.dump(jsonObjectPlayer, playerFile)
                playerFile.close()
                self.store()

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            self.mainClock.tick(60)

    # method for displaying the highscores from the json file
    def highscore(self):
        running = True
        self.screen.fill((0, 0, 0))
        y = 50
        self.draw_text('Highscore', self.font, (255, 255, 255), self.screen, 20, 20)
        jsonFile = json.load(open('highscores.json', 'r'))
        for key in jsonFile:
            print(str(key) + ' ' + str(jsonFile[key]))
            self.draw_text(str(key) + '. ' + str(jsonFile[key]), self.font, (255, 255, 255), self.screen, 20, y)
            y += 30
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            self.mainClock.tick(60)

    # displays help page with instructions
    def help(self):
        running = True
        self.screen.fill((0, 0, 0))

        self.draw_text('Help', self.font, (255, 255, 255), self.screen, 20, 20)
        self.draw_text('The movement is provided by up, '
                       'down, left and right keys.', self.font, (255, 255, 255), self.screen, 20, 100)
        self.draw_text('Player gets 3 lives each game. After hitting a ghost player loses '
                       'life.', self.font, (255, 255, 255), self.screen, 20, 120)
        self.draw_text('However, if player collects special point '
                       'he will be able', self.font, (255, 255, 255), self.screen, 20, 140)
        self.draw_text('to eat ghosts for a short period of time and earn points for it.', self.font, (255, 255, 255),
                       self.screen,
                       20,
                       160)
        while running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            self.mainClock.tick(60)

    # exits the game and system, option in main menu
    def exit_game(self):
        pygame.quit()
        sys.exit()


# player class that represents the pacman and all of its necessary fields and update actions
class player(object):
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.body = c.create_image(x * cell + cell // 2, y * cell + cell // 2, image=self.image)
        self.smer = 0
        self.changesmer = 0
        self.smerx = -1
        self.smery = 0
        self.zivoty = 3
        self.startx = x
        self.starty = y
        self.resetWait = False
        self.mv = 0

    # changes image as part of pacman animation
    def change_image(self, importimage):
        c.itemconfig(self.body, image=importimage)

    # handles action of losing a life and checks for number of lives in case the end of the game takes places
    def lose_life(self):
        self.zivoty -= 1

        if self.zivoty == 0:
            end_game(False)
        self.update_lives()

    # updates the canvas based on the number of player lives
    def update_lives(self):
        c.delete('bodky')
        for i in range(self.zivoty):
            c.create_image(cell + i * 27, cell * yy - 14, image=img3, tags='bodky')

    # changes direction of the pacman
    def changeDirection(self, changesmer):
        self.changesmer = changesmer

    # main update method that is recurring during the time the game is played
    def update(self):
        if self.mv == 0:
            global cell, score_count, superpower, stars
            dx = [-1, 0, 1, 0]
            dy = [0, -1, 0, 1]
            if self.smer != self.changesmer:
                short = pole[self.x + dx[self.changesmer]][self.y + dy[self.changesmer]]
                if short == '*' or short == 'O' or short == '.':
                    self.smer = self.changesmer
            self.smerx = dx[self.smer]
            self.smery = dy[self.smer]

            if pole[self.x + self.smerx][self.y + self.smery] == '*':
                score_count += 10
                update_score()
                pole[self.x + self.smerx][self.y + self.smery] = '.'
                c.itemconfig(obrazky[self.x + self.smerx][self.y + self.smery], image=blank)
                self.move()
                stars -= 1
                if stars == 0:
                    end_game(True)
            elif pole[self.x + self.smerx][self.y + self.smery] == 'O':
                score_count += 100
                update_score()
                pole[self.x + self.smerx][self.y + self.smery] = '.'
                c.itemconfig(obrazky[self.x + self.smerx][self.y + self.smery], image=blank)
                if superpower == False:
                    c.after(6000, bonus)
                superpower = True
                # print('O',end='')
                self.move()
            elif pole[self.x + self.smerx][self.y + self.smery] == '.':
                # print('.',end='')
                self.move()
            pac_man_colission()
        else:
            self.mv -= 1
            c.move(self.body, self.smerx * 4, self.smery * 4)

        if self.resetWait:
            c.after(3000, self.update)
            self.resetWait = False
        else:
            c.after(20, self.update)

    # handles pacman movement
    def move(self):
        self.mv = 3
        self.x += self.smerx
        self.y += self.smery
        c.move(self.body, self.smerx * 4, self.smery * 4)

    # resets pacman to its original position
    def reset(self):
        self.mv = 0
        self.resetWait = True
        self.x = self.startx
        self.y = self.starty
        c.delete(self.body)
        self.body = c.create_image(self.x * cell + cell // 2, self.y * cell + cell // 2, image=self.image)


# handles all actions regarding ghost actions
class ghost(object):

    def __init__(self, image, x, y, rot, speed, color):
        global navigation_map
        self.color = color
        self.image = image
        self.x = x
        self.y = y
        self.body = c.create_image(x * cell + cell // 2, y * cell + cell // 2, image=self.image)
        self.map = copy.deepcopy(navigation_map)
        self.startx = x
        self.starty = y
        self.rotation = rot
        self.avoid = []
        self.endX = 1
        self.endY = 5
        self.speed = speed
        self.mv = 0
        self.resetWait = False
        # c.after(1000, self.update)

    # sets direction for ghost movement
    def direction(self, endX, endY, avoid):
        self.endX = endX
        self.endY = endY
        self.avoid = avoid

    def path(self, endX, endY):
        global pole
        self.map = copy.deepcopy(pole)
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1]
        sym = ['>', 'v', '<', '^']
        table = [[endX, endY]]
        self.map[endX][endY] = 'G'

        loop = True
        if endX == self.x and endY == self.y:
            loop = False
        while (loop):
            new_table = []
            for tile in table:
                for i in range(4):
                    tilex = tile[0] + dx[i]
                    tiley = tile[1] + dy[i]
                    if check_tile(self.map, tilex, tiley):
                        new_table.append([tilex, tiley])
                        self.map[tilex][tiley] = sym[i]
                        if tilex == self.x and tiley == self.y:
                            loop = False
            table = new_table
            if not table:
                loop = False

    # calculates the path for the ghost
    def navigate(self):
        global navigation_map
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1]
        sym = ['<', '^', '>', 'v']

        possible_ways = 0
        for rot in [+1, 0, +3]:
            rotation = (self.rotation + rot) % 4
            tileX = self.x + dx[rotation]
            tileY = self.y + dy[rotation]
            if navigation_map[tileX][tileY] == '.':
                possible_ways += 1
                self.map[self.x][self.y] = sym[rotation]

        if possible_ways == 1 or (self.endX == self.x and self.endY == self.y):
            pass

        elif possible_ways > 1:
            endX = self.endX
            endY = self.endY

            avoidTails = self.avoid
            for nothing in range(len(avoidTails) + 1):
                self.map = copy.deepcopy(navigation_map)
                for avoid in avoidTails:
                    self.map[avoid[0]][avoid[1]] = 'H'

                table = [[self.x, self.y, self.rotation]]
                SeekPath = True
                while table and SeekPath:
                    new_table = []
                    for tile in table:
                        for rot in [+1, 0, +3]:
                            rotation = (tile[2] + rot) % 4
                            tileX = tile[0] + dx[rotation]
                            tileY = tile[1] + dy[rotation]
                            if self.map[tileX][tileY] == '.':
                                new_table.append([tileX, tileY, rotation])
                                self.map[tileX][tileY] = sym[rotation]
                                if tileX == endX and tileY == endY:
                                    SeekPath = False
                    table = new_table
                if SeekPath == False:
                    break
                else:
                    if avoidTails:
                        # print('Dropping: '+str(avoidTails[-1]))
                        del avoidTails[-1]

            if not SeekPath:
                new_map = copy.deepcopy(navigation_map)
                symReversed = ['>', 'v', '<', '^']
                while (not (endX == self.x and endY == self.y)):
                    for i in range(4):
                        if self.map[endX][endY] == symReversed[i]:
                            endX += dx[i]
                            endY += dy[i]
                            new_map[endX][endY] = symReversed[i]
                            break
                self.map = new_map
        else:
            pass
            # print('I AM STUCK!')

    # update the ghost position, movement and calculates path, this is running recurringly during the time of game
    def update(self):
        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0, 1]
        sym = ['<', '^', '>', 'v']
        if self.mv == 0:
            global cell
            self.navigate()
            for i in range(4):
                if self.map[self.x][self.y] == sym[i]:
                    c.move(self.body, dx[i] * 4, dy[i] * 4)
                    self.rotation = i
                    self.x += dx[i]
                    self.y += dy[i]
                    self.mv = 3
                    break
        else:
            self.mv -= 1
            c.move(self.body, dx[self.rotation] * 4, dy[self.rotation] * 4)

        if self.resetWait:
            c.after(3000, self.update)
            self.resetWait = False
        else:
            c.after(self.speed, self.update)

    def showpath(self):
        global xx, yy
        for y in range(yy):
            for x in range(xx):
                print(str(self.map[x][y]), end + '')
            print('')

    # used for testing and debugging purposes, displays path for a ghost
    def drawpath(self):
        c.delete(str(self.color))
        global xx, yy, cell
        for y in range(yy):
            for x in range(xx):
                ch = str(self.map[x][y])
                if ch == '<' or ch == '>' or ch == '^' or ch == 'v':
                    c.create_text(x * cell + cell // 2, y * cell + cell // 2, tags=str(self.color),
                                  text=str(self.map[x][y]), fill=self.color, font='Arial 15 bold')

    # resets the ghost to its starting position and sets timer for its release
    def reset(self, val):
        self.mv = 0
        self.resetWait = val
        self.x = self.startx
        self.y = self.starty
        c.delete(self.body)
        self.body = c.create_image(self.x * cell + cell // 2, self.y * cell + cell // 2, image=self.image)

    # changes image of the ghost when special effect takes place
    def change_image(self, importimage):
        c.itemconfigure(self.body, image=importimage)


# Contoller in form of static methods

# updates score real time
def update_score():
    global score_count, highscore
    c.delete('body')
    c.create_text(16 * 7, 32, text='Score: ' + str(score_count), fill='white', tags='body', font='Courier 20 bold')
    c.create_text(16 * 20, 32, text='Highscore: ' + str(highscore), fill='white', tags='body', font='Courier 20 bold')


# handles end of game event and returns player to main menu
def end_game(win):
    global score_count, highscore, game_no
    c.delete('all')

    if win == True:
        c.create_text(xx * cell // 2, yy * cell // 5 * 1, text='YOU WIN', fill='white', font='Courier 35 bold')
        c.create_text(xx * cell // 2, yy * cell // 5 * 2, text='Your Score:' + str(score_count), fill='white',
                      font='Courier 35 bold')
        c.create_text(xx * cell // 2, yy * cell // 5 * 3, text='Highscore:' + str(highscore), fill='white',
                      font='Courier 35 bold')
    else:
        c.create_text(xx * cell // 2, yy * cell // 2, text='THE END', fill='white', font='Arial 40')
        c.create_text(xx * cell // 2, yy * cell // 5 * 2, text='Your Score:' + str(score_count), fill='white',
                      font='Courier 35 bold')
        c.create_text(xx * cell // 2, yy * cell // 5 * 3, text='Highscore:' + str(highscore), fill='white',
                      font='Courier 35 bold')

    evaluate_score()
    c.update()
    time.sleep(3)
    c.delete(playerOne.body)
    c.update()
    c.delete('all')
    c.update()
    test.destroy()

    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

    # start_game(False)
    # game_loop()


# evaluates score in regard to the highscore file, and updates it if necessary
def evaluate_score():
    global score_count
    jsonFile = open('highscores.json', 'r')
    jsonObject = json.load(jsonFile)
    jsonFile.close()
    moneyFile = open('player_info.json', 'r')
    playerObject = json.load(moneyFile)
    moneyFile.close()

    run = True
    while run:
        for key in jsonObject:
            if score_count > int(jsonObject[key]):
                score = score_count
                score_count = int(jsonObject[key])
                jsonObject[key] = score
                break
            if score_count == int(jsonObject[key]) or key == "10":
                run = False

    if score_count > 10:
        playerObject['money'] = playerObject['money'] + (score_count // 10)
        moneyAdd = open('player_info.json','w')
        json.dump(playerObject, moneyAdd)
        moneyAdd.close()

    jsonFile = open('highscores.json', 'w')
    json.dump(jsonObject, jsonFile)
    jsonFile.close()


def double_field(xx, yy):
    pole = []
    for x in range(xx):
        pole2 = []
        for y in range(yy):
            pole2.append("X")
        pole.append(pole2)
    return (pole)


# handles key call backs as user inputs
def callback_key(event):
    # print(event)
    if event.char == 'r':
        pinky.showpath()
    global direction
    direction = ['Left', 'Up', 'Right', 'Down']
    for i in range(len(direction)):
        if event.keysym == direction[i]:
            playerOne.changeDirection(i)


# updates the map with visual representation
def update_all():
    global xx, yy, debug
    val = ['X', '.', '#', '*', 'O', '-']
    col = [blank, blank, wall, coin, bodka, blank]
    if debug:
        col = [blank, blank, wall, blank, bodka, blank]

    for x in range(xx):
        for y in range(yy):
            for i in range(len(val)):
                if pole[x][y] == val[i]:
                    obrazky[x][y] = c.create_image(x * cell + cell // 2, y * cell + cell // 2, image=col[i])


# reads map.txt file in order to implement it as a map visual
def read(filename):
    y = 0
    global stars
    with open(filename) as fileobj:
        for line in fileobj:
            x = -1
            for ch in line:
                x += 1
                if ch != '\n':
                    pole[x][y] = ch
                    if ch == '*':
                        stars += 1
            y += 1


# used for testing and debugging purposes to find the current position of the mouse on click
def mouse(event):
    print(event.x // cell, event.y // cell)


# checks for the object on tile on the map
def check_tile(mapa, x, y):
    if mapa[x][y] == '*' or mapa[x][y] == '.' or mapa[x][y] == 'O':
        return True
    else:
        return False


# handles the collision between pacman and ghost
def colission(hrac, poleobjektov):
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]
    for objekt in poleobjektov:
        one = objekt.x == hrac.x and objekt.y == hrac.y
        two = objekt.x == hrac.x + dx[(hrac.smer + 2) % 4] and objekt.y == hrac.y + dy[(hrac.smer + 2) % 4]
        if one or two:
            return objekt
    return False


# used for debugging purposes, deprecated now
def close_doors():
    global navigation_map
    navigation_map[13][16] = '='
    navigation_map[14][16] = '='


# used for debugging purposes, deprecated now
def open_doors():
    global navigation_map
    navigation_map[13][16] = '.'
    navigation_map[14][16] = '.'


# handles bonus action after hitting special effect tile
def bonus():
    global superpower
    superpower = False
    blinky.change_image(blinky.image)
    pinky.change_image(pinky.image)
    inky.change_image(inky.image)
    clyde.change_image(clyde.image)


# handles animation of the pacman movement
def animation():
    global pacman, imgvalue
    imgvalue += 1
    imgvalue = imgvalue % 3
    playerOne.change_image(pacman[playerOne.smer][imgvalue])
    c.after(70, animation)


# handles the collision between pacman and ghost
def pac_man_colission():
    global score_count, superpower, debug
    if superpower == False:
        blinky.direction(playerOne.x, playerOne.y, [[13, 33], [13, 9]])
        pinky.direction(playerOne.x, playerOne.y, [[blinky.x, blinky.y]])
        inky.direction(playerOne.x, playerOne.y, [[blinky.x, blinky.y], [pinky.x, pinky.y]])
        clyde.direction(pinky.x, pinky.y, [[playerOne.x, playerOne.y], [inky.x, inky.y], [blinky.x, blinky.y]])
        if colission(playerOne, [blinky, pinky, inky, clyde]) and debug == False:
            clyde.reset(True)
            blinky.reset(True)
            inky.reset(True)
            pinky.reset(True)
            playerOne.lose_life()
            playerOne.reset()
            # close_doors()
            # c.after(3000, open_doors)
    else:
        blinky.change_image(bonusimg)
        pinky.change_image(bonusimg)
        inky.change_image(bonusimg)
        clyde.change_image(bonusimg)

        blinky.direction(1, 5, [])
        pinky.direction(26, 5, [])
        inky.direction(1, 33, [])
        clyde.direction(26, 33, [])
        hit = colission(playerOne, [blinky, pinky, inky, clyde])
        if hit:
            score_count += 200
            update_score()
            hit.reset(True)


# used for testing purposes, shows path of the ghosts
def path_debug():
    for ghost in [pinky, inky, clyde, blinky]:
        ghost.drawpath()
        c.tag_raise(ghost.body)
    c.after(200, path_debug)


# main game loop
def game_loop():
    playerOne.update_lives()

    update_score()

    c.bind_all("<Key>", callback_key)
    c.bind_all("<Button-1>", mouse)

    # c.after(3000, open_doors)
    animation()

    if debug:
        path_debug()

    tkinter.mainloop()


# initial setup and actions taking place in order for game to start
def start_game(first_game):
    global xx, yy, cell, score_count, superpower, stars, map_number, debug, highscore, c, pacman, imgvalue, bonusimg, wall, playerOne, playery
    global blank, coin, bodka, obrazky, blinky, pinky, inky, clyde, pole, navigation_map, img3, plocha, game_no, equippedSkin, tkinterItem
    xx = 28
    yy = 37
    cell = 16
    score_count = 0
    superpower = False
    stars = 0
    map_number = menu.level
    debug = False
    highscore_file = open('highscores.json', 'r')
    highscore = json.load(highscore_file)['1']
    highscore_file.close()

    # View is managed by TKinter canvas
    # tkinter.Tk().title("Pac-Man")
    c = tkinter.Canvas(width=cell * xx, height=cell * yy, bg='black')
    c.pack()

    # dx = [-1, 0, 1, 0]
    # dy = [0, -1, 0, 1]
    # sym = ['l', 'u', 'r', 'd']

    player_file = open('player_info.json', 'r')
    playerSkin = json.load(player_file)['skin']
    player_file.close()

    img1 = tkinter.PhotoImage(file='images/img1-' + playerSkin + '.gif')
    img2 = tkinter.PhotoImage(file='images/img2-' + playerSkin + '.gif')
    img3 = tkinter.PhotoImage(file='images/img3-' + playerSkin + '.gif')
    hore1 = tkinter.PhotoImage(file='images/hore1-' + playerSkin + '.gif')
    hore2 = tkinter.PhotoImage(file='images/hore2-' + playerSkin + '.gif')
    hore3 = tkinter.PhotoImage(file='images/hore3-' + playerSkin + '.gif')
    doprava1 = tkinter.PhotoImage(file='images/doprava1-' + playerSkin + '.gif')
    doprava2 = tkinter.PhotoImage(file='images/doprava2-' + playerSkin + '.gif')
    doprava3 = tkinter.PhotoImage(file='images/doprava3-' + playerSkin + '.gif')
    dole1 = tkinter.PhotoImage(file='images/dole1-' + playerSkin + '.gif')
    dole2 = tkinter.PhotoImage(file='images/dole2-' + playerSkin + '.gif')
    dole3 = tkinter.PhotoImage(file='images/dole3-' + playerSkin + '.gif')
    pacman = [[img1, img2, img3], [hore1, hore2, hore3], [doprava1, doprava2, doprava3], [dole1, dole2, dole3]]
    imgvalue = 0

    redimg = tkinter.PhotoImage(file='images/red.gif')
    blueimg = tkinter.PhotoImage(file='images/blue.gif')
    orangeimg = tkinter.PhotoImage(file='images/orange.gif')
    pinkimg = tkinter.PhotoImage(file='images/pink.gif')
    bonusimg = tkinter.PhotoImage(file='images/bonus.gif')

    pole = double_field(xx, yy)

    if map_number == 1:
        wall = tkinter.PhotoImage(file='images/blank.gif')
        plocha = tkinter.PhotoImage(file='images/mapa.png')
        c.create_image(xx * cell // 2, yy * cell // 2, image=plocha)
        playery = 21
    if map_number == 2 or map_number == 3:
        wall = tkinter.PhotoImage(file='images/wall.gif')
        playery = 23


    blank = tkinter.PhotoImage(file='images/blank.gif')
    coin = tkinter.PhotoImage(file='images/x.gif')
    bodka = tkinter.PhotoImage(file='images/bodka.gif')
    obrazky = double_field(xx, yy)

    read('maps/map' + str(map_number) + '.txt')
    navigation_map = double_field(xx, yy)
    for x in range(xx):
        for y in range(yy):
            if pole[x][y] == '*' or pole[x][y] == '.' or pole[x][y] == 'O':
                navigation_map[x][y] = '.'
            else:
                navigation_map[x][y] = pole[x][y]

    update_all()

    playerOne = player(img1, 13, playery)

    blinky = ghost(redimg, 13, 18, 1, 120 // 4, 'red')
    pinky = ghost(pinkimg, 15, 18, 1, 93 // 4, 'pink')
    inky = ghost(blueimg, 14, 18, 1, 131 // 4, 'cyan')
    clyde = ghost(orangeimg, 12, 18, 1, 84 // 3, 'orange')

    c.after(1000, playerOne.update)

    c.after(1000, blinky.update)
    c.after(1000, pinky.update)
    c.after(1000, inky.update)
    c.after(1000, clyde.update)


# start of the program code, equivalent to a main function
test = tkinter.Tk()
test.title('Pac-Man')

runGame = False

menu = mainMenu()

menu.main_menu()

if runGame == True:
    start_game(True)

    game_loop()
