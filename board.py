import pygame

from levelGeneration import *
from window import Window
import sprites
import mark
import random
from tiles import Tile

TILE_SIZE = 16


class Board:
    def __init__(self, window: Window, textures: pygame.image, spriteBank: dict, mark: mark.Mark,
                 texts: text.Texts, player):
        self.mark = mark
        self.window = window
        self.textures = textures
        self.rows = window.heigthScaled // TILE_SIZE
        self.cols = window.widthScaled // TILE_SIZE
        self.maxHeight = self.rows * TILE_SIZE
        self.maxWidth = self.cols * TILE_SIZE
        self.spriteBank = spriteBank
        self.tilesGroup = sprites.GameSpriteGroup()
        self.boardGrid = []
        self.texts = texts
        self.player = player

    def initBoard(self, width, height, size):

        self.boardGrid = [[None for x in range(width)] for y in range(height)]

        self.boardGrid[0][0] = SpawnTopLeftBorder(self.textures, size, 0, 0, self.texts, self.player)
        self.boardGrid[0][0].generateLevel(self.spriteBank, self.mark)

        self.boardGrid[0][len(self.boardGrid) - 1] = TopRightBorder(self.textures, size, 0, len(self.boardGrid[0]) - 1, self.texts, self.player)
        self.boardGrid[0][len(self.boardGrid) - 1].generateLevel(self.spriteBank, self.mark)

        self.boardGrid[len(self.boardGrid[0]) - 1][0] = BottomLeftBorder(self.textures, size, len(self.boardGrid) - 1, 0, self.texts, self.player)
        self.boardGrid[len(self.boardGrid[0]) - 1][0].generateLevel(self.spriteBank, self.mark)

        self.boardGrid[len(self.boardGrid[0])- 1][len(self.boardGrid) - 1] = BottomRightBorder(self.textures, size, len(self.boardGrid) - 1, len(self.boardGrid) - 1, self.texts, self.player)
        self.boardGrid[len(self.boardGrid[0])- 1][len(self.boardGrid) - 1].generateLevel(self.spriteBank, self.mark)

        for z in range(1, height - 1):
            self.boardGrid[z][0] = LeftBorder(self.textures, size, z, 0, self.texts, self.player)
            self.boardGrid[z][0].generateLevel(self.spriteBank, self.mark)
            self.boardGrid[z][len(self.boardGrid) - 1] = RightBorder(self.textures, size, z, len(self.boardGrid) - 1, self.texts, self.player)
            self.boardGrid[z][len(self.boardGrid) - 1].generateLevel(self.spriteBank, self.mark)

        for w in range(1, width - 1):
            self.boardGrid[0][w] = TopBorder(self.textures, size, 0, w, self.texts, self.player)
            self.boardGrid[0][w].generateLevel(self.spriteBank, self.mark)
            self.boardGrid[len(self.boardGrid[0]) - 1][w] = BotBorder(self.textures, size,len(self.boardGrid[0]) - 1  , w, self.texts, self.player)
            self.boardGrid[len(self.boardGrid[0]) - 1][w].generateLevel(self.spriteBank, self.mark)

        w2 = width // 2
        h2 = height // 2
        w3 = w2
        h3 = h2 + 1


        self.boardGrid[h2][w2] = CastleCenterRoom(self.textures, size, h2, w2, self.texts, self.player)
        self.boardGrid[h2][w2].generateLevel(self.spriteBank, self.mark)
        self.boardGrid[h3][w3] = CastleEntrance(self.textures, size, h3, w3, self.texts, self.player)
        self.boardGrid[h3][w3].generateLevel(self.spriteBank, self.mark)

        for y in range(1, width - 1):
            for x in range(1, height - 1):
                if not (y == h2 and x == w2) and not (y == h3 and x == w3):
                    room = self.generateRoom(y, x, size)
                    self.boardGrid[y][x] = room



    def generateRoom(self, line, column, size):
        #TODO stuff
        #like LevelMAnager.getArray

        rooms = [BasicRoom, VCorridorWallRoom,RuinedWildRoom, HCorridorWallRoom, CossWallRoom, VCorridorWallRoom];
        newRoom = rooms[randint(0, len(rooms) - 1)](self.textures, size, line, column, self.texts, self.player)

        possibleTop = Adjacency.ALL in newRoom.adjacencies or (((Adjacency.TOP in newRoom.adjacencies and
                                                                not (line == 0)) and (
                                                                           self.boardGrid[line - 1][column] is None or
                                                                           Adjacency.ALL in self.boardGrid[line - 1][
                                                                               column].adjacencies or Adjacency.BOTTOM in
                                                                           self.boardGrid[line - 1][
                                                                               column].adjacencies))
                                                               or not (Adjacency.TOP in newRoom.adjacencies) and (
                                                                           (not (line == len(self.boardGrid) - 1))
                                                                           and ((self.boardGrid[line + 1][
                                                                                     column] is None or not Adjacency.BOTTOM in
                                                                                                            self.boardGrid[
                                                                                                                line + 1][
                                                                                                                column].adjacencies))))

        possibleBottom = Adjacency.ALL in newRoom.adjacencies or (((Adjacency.BOTTOM in newRoom.adjacencies and
                                                                  not (line == len(self.boardGrid) - 1)) and (
                                                                          self.boardGrid[line + 1][
                                                                              column] is None
                                                                          or Adjacency.ALL in
                                                                          self.boardGrid[line + 1][
                                                                              column].adjacencies or Adjacency.TOP in
                                                                          self.boardGrid[line + 1][
                                                                              column].adjacencies))
                                                                  or not (Adjacency.BOTTOM in newRoom.adjacencies) and (
                                                                              (not (line == 0))
                                                                              and (
                                                                              (self.boardGrid[line - 1][column] is None
                                                                               or Adjacency.ALL in
                                                                               self.boardGrid[line - 1][
                                                                                   column].adjacencies))))

        possibleLEFT = Adjacency.ALL in newRoom.adjacencies or (((Adjacency.LEFT in newRoom.adjacencies and
                                                                not (column == 0)) and (
                                                                        self.boardGrid[line][column - 1] is None
                                                                        or Adjacency.ALL in
                                                                        self.boardGrid[line][
                                                                            column - 1].adjacencies or Adjacency.RIGHT in
                                                                        self.boardGrid[line][
                                                                            column - 1].adjacencies))
                                                                or not (Adjacency.LEFT in newRoom.adjacencies) and (
                                                                            not (column == len(self.boardGrid[0]) - 1)
                                                                            and ((self.boardGrid[line][
                                                                                      column + 1] is None or not Adjacency.RIGHT in
                                                                                                                             self.boardGrid[
                                                                                                                                 line][
                                                                                                                                 column + 1].adjacencies or Adjacency.ALL in
                                                                                  self.boardGrid[line][
                                                                                      column + 1].adjacencies
                                                                                  ))))

        possibleRight = Adjacency.ALL in newRoom.adjacencies or (((Adjacency.RIGHT in newRoom.adjacencies and
                                                                 not (column == len(self.boardGrid[0]) - 1)) and (
                                                                         self.boardGrid[line][
                                                                             column + 1] is None or
                                                                         Adjacency.ALL in self.boardGrid[line][
                                                                             column + 1].adjacencies or Adjacency.LEFT in
                                                                         self.boardGrid[line][
                                                                             column + 1].adjacencies))
                                                                 or not (Adjacency.RIGHT in newRoom.adjacencies)
                                                                 and ((column == 0)
                                                                      and ((
                                    self.boardGrid[line][column - 1] is None or not Adjacency.RIGHT in
                                                                                    self.boardGrid[line][
                                                                                        column - 1].adjacencies
                                    or Adjacency.ALL in self.boardGrid[line][column - 1].adjacencies))))




        while not (possibleTop and possibleBottom and possibleLEFT and possibleRight):

            newRoom = rooms[randint(0, len(rooms) - 1)](self.textures, size, line, column, self.texts, self.player)

            possibleTop = Adjacency.ALL in newRoom.adjacencies or (((Adjacency.TOP in newRoom.adjacencies and
                                                                     not (line == 0)) and (
                                                                            self.boardGrid[line - 1][column] is None or
                                                                            Adjacency.ALL in self.boardGrid[line - 1][
                                                                                column].adjacencies or Adjacency.BOTTOM in
                                                                            self.boardGrid[line - 1][
                                                                                column].adjacencies))
                                                                   or not (Adjacency.TOP in newRoom.adjacencies) and (
                                                                           (not (line == len(self.boardGrid) - 1))
                                                                           and ((self.boardGrid[line + 1][
                                                                                     column] is None or not Adjacency.BOTTOM in
                                                                                                            self.boardGrid[
                                                                                                                line + 1][
                                                                                                                column].adjacencies))))

            possibleBottom = Adjacency.ALL in newRoom.adjacencies or (((Adjacency.BOTTOM in newRoom.adjacencies and
                                                                        not (line == len(self.boardGrid) - 1)) and (
                                                                               self.boardGrid[line + 1][
                                                                                   column] is None
                                                                               or Adjacency.ALL in
                                                                               self.boardGrid[line + 1][
                                                                                   column].adjacencies or Adjacency.TOP in
                                                                               self.boardGrid[line + 1][
                                                                                   column].adjacencies))
                                                                      or not (
                                Adjacency.BOTTOM in newRoom.adjacencies) and (
                                                                              (not (line == 0))
                                                                              and (
                                                                                  (self.boardGrid[line - 1][
                                                                                       column] is None
                                                                                   or Adjacency.ALL in
                                                                                   self.boardGrid[line - 1][
                                                                                       column].adjacencies))))

            possibleLEFT = Adjacency.ALL in newRoom.adjacencies or (((Adjacency.LEFT in newRoom.adjacencies and
                                                                      not (column == 0)) and (
                                                                             self.boardGrid[line][column - 1] is None
                                                                             or Adjacency.ALL in
                                                                             self.boardGrid[line][
                                                                                 column - 1].adjacencies or Adjacency.RIGHT in
                                                                             self.boardGrid[line][
                                                                                 column - 1].adjacencies))
                                                                    or not (Adjacency.LEFT in newRoom.adjacencies) and (
                                                                            not (column == len(self.boardGrid[0]) - 1)
                                                                            and ((self.boardGrid[line][
                                                                                      column + 1] is None or not Adjacency.RIGHT in
                                                                                                                 self.boardGrid[
                                                                                                                     line][
                                                                                                                     column + 1].adjacencies or Adjacency.ALL in
                                                                                  self.boardGrid[line][
                                                                                      column + 1].adjacencies
                                                                                  ))))

            possibleRight = Adjacency.ALL in newRoom.adjacencies or (((Adjacency.RIGHT in newRoom.adjacencies and
                                                                       not (column == len(self.boardGrid[0]) - 1)) and (
                                                                              self.boardGrid[line][
                                                                                  column + 1] is None or
                                                                              Adjacency.ALL in self.boardGrid[line][
                                                                                  column + 1].adjacencies or Adjacency.LEFT in
                                                                              self.boardGrid[line][
                                                                                  column + 1].adjacencies))
                                                                     or not (Adjacency.RIGHT in newRoom.adjacencies)
                                                                     and ((column == 0)
                                                                          and ((
                                    self.boardGrid[line][column - 1] is None or not Adjacency.RIGHT in
                                                                                    self.boardGrid[line][
                                                                                        column - 1].adjacencies
                                    or Adjacency.ALL in self.boardGrid[line][column - 1].adjacencies))))

        newRoom.generateLevel(self.spriteBank, self.mark)
        return newRoom;


    def update(self):
        for line in self.boardGrid:
            for col in line:
                if config.CANVASWIDTH + config.CANVASWIDTH/2 > col.xStart - self.mark.x > - config.CANVASWIDTH - config.CANVASWIDTH/2 and \
                        config.CANVASHEIGHT + config.CANVASHEIGHT/2 > col.yStart - self.mark.y > - config.CANVASHEIGHT - config.CANVASHEIGHT/2:
                    config.Rendered += 1
                    col.update()


    def render(self):
        surface = self.window.get()

        for line in self.boardGrid:
            for col in line:
                if config.CANVASWIDTH + config.CANVASWIDTH / 2 > col.xStart - self.mark.x > - config.CANVASWIDTH - config.CANVASWIDTH / 2 and \
                        config.CANVASHEIGHT + config.CANVASHEIGHT / 2 > col.yStart - self.mark.y > - config.CANVASHEIGHT - config.CANVASHEIGHT / 2:
                    col.render(surface)



