import pygame

from levelGeneration import *
from window import Window
import sprites
import mark
import random
from tiles import Tile
import text

TILE_SIZE = 16


class Board:
    def __init__(self, window: Window, textures: pygame.image, spriteBank: dict, mark: mark.Mark,
                 texts: text.Texts):
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


    def initBoard(self, width, height,size):
        self.boardGrid = [[None for x in range(width)] for y in range(height)]
        v = 0
        for y in range(width):
            v += 1
            for x in range(height):
                room = self.generateRoom(y, x, size)
                self.boardGrid[x][y] = room

    def generateRoom(self, line, column, size):
        #TODO stuff
        #like LevelMAnager.getArray
        rooms = [BasicRoom,HCorridorWallRoom,VCorridorWallRoom,VCorridorWallRoom,VCorridorWallRoom,HCorridorWallRoom,HCorridorWallRoom,HCorridorWallRoom,HCorridorWallRoom,VCorridorWallRoom,VCorridorWallRoom];
        newRoom = rooms[randint(0, len(rooms) - 1)](self.textures, size, line, column, self.texts)

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


        if(column == 0 and line == 0):
            #
            print("haut :" + str(self.boardGrid[3][4]))
            print("g :" + str(self.boardGrid[4][3]))
            print("b: " + str(self.boardGrid[5][4]))
            print("d : " + str(self.boardGrid[4][5]))
            print(Adjacency.ALL in newRoom.adjacencies or (((Adjacency.TOP in newRoom.adjacencies and
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
                                                                                                                column].adjacencies)))))
            print((((Adjacency.TOP in newRoom.adjacencies and
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
                                                                                                        column].adjacencies)))))
            print(newRoom)
            print(possibleLEFT)
            print(possibleRight)
            print(possibleBottom)
            print(possibleTop)
            print(Adjacency.ALL in newRoom.adjacencies)
            print(newRoom.adjacencies)
            #print(self.boardGrid[line - 1][column].adjacencies)

        while not (possibleTop and possibleBottom and possibleLEFT and possibleRight):

            newRoom = rooms[randint(0, len(rooms) - 1)](self.textures, size, line, column, self.texts)

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



