#-*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import logging
import time

logging.basicConfig(level=logging.DEBUG)

class State:
    def getCommand(self):
        pass
    def setCommand(self):
        pass
    def changeState(self,cmd):
        pass
    def displayFlip(self):
        pass

class Machine:
    def __init__(self,w_size, h_size):
        # self.screen = pygame.display.set_mode((w_size, h_size), pygame.FULLSCREEN)
        self.w_size = w_size
        self.h_size = h_size
        self.screen = pygame.display.set_mode((w_size, h_size))

        self.galleryIcon = pygame.image.load('./res/gallery.png')
        self.gallery_rect = self.galleryIcon.get_rect()
        self.gallery_rect.center = (self.w_size - 50, self.h_size - 50)

        self.aimIcon = pygame.image.load('./res/aim.png')
        self.aim_rect = self.aimIcon.get_rect()
        self.aim_rect.center = (self.w_size / 2, self.h_size / 2)

        self.playIcon = pygame.image.load('./res/play.png')
        self.play_rect = self.playIcon.get_rect()
        self.play_rect.center = (self.w_size / 2, self.h_size / 2)

        self.driveIcon = pygame.image.load('./res/drive.png')
        self.drive_rect = self.driveIcon.get_rect()
        self.drive_rect.center = (self.w_size - 50, 40)

        self.larrIcon = pygame.image.load('./res/larr.png')
        self.larr_rect = self.larrIcon.get_rect()
        self.larr_rect.center = (70, self.h_size / 2)

        self.rarrIcon = pygame.image.load('./res/rarr.png')
        self.rarr_rect = self.rarrIcon.get_rect()
        self.rarr_rect.center = (self.w_size - 70, self.h_size / 2)

        self.homeIcon = pygame.image.load('./res/home.png')
        self.home_rect = self.homeIcon.get_rect()
        self.home_rect.center = (self.w_size - 50, self.h_size - 50)

        self.streamingState = StreamingState(self)
        self.printingState = PrintingState(self)
        self.recodingState = RecodingState(self)
        self.loadingState = LoadingState(self)
        self.galleryState = GalleryState(self)
        self.exitState = ExitState(self)
        self.state = StreamingState(self)

    def getCommand(self):
        return  self.state.getCommand()

    def changeState(self,cmd):
        if cmd=="StreamingState":
            self.setState(self.getStreamingState())
        elif cmd=="PrintingState":
            self.setState(self.getPrintingState())
        elif cmd=="RecodingState":
            self.setState(self.getRecodingState())
        elif cmd=="LoadingState":
            self.setState(self.getLoadingState())
        elif cmd=="GalleryState":
            self.setState(self.getGalleryState())
        elif cmd=="ExitState":
            self.setState((self.getExitState()))


    def displayFlip(self):
        self.state.displayFlip()

    def setState(self,state):
        self.state = state

    def getState(self):
        return self.state

    def getStreamingState(self):
        return self.streamingState

    def getPrintingState(self):
        return self.printingState

    def getRecodingState(self):
        return self.recodingState

    def getLoadingState(self):
        return self.loadingState

    def getGalleryState(self):
        return self.galleryState

    def getExitState(self):
        return self.exitState


class StreamingState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.cmd = None

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self,cmd):
        self.cmd = cmd


    def displayFlip(self):
        #logging.debug("스트리밍 화면 재생")
        for evt in pygame.event.get():
            if evt.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                # if statement
                if self.machine.gallery_rect.collidepoint(pos) & pressed1 == 1:
                    self.setCommand("GalleryState")
                    logging.debug("겔러리버튼입력")


        self.machine.screen.fill((255, 255, 255))
        pygame.font.init()
        text = "streaming screen"
        font = pygame.font.Font(None, 50)
        imgText = font.render(text, True, (255, 0, 0))
        rect = imgText.get_rect()
        self.machine.screen.blit(imgText, rect)
        self.machine.screen.blit(self.machine.galleryIcon, self.machine.gallery_rect)
        self.machine.screen.blit(self.machine.aimIcon, self.machine.aim_rect)
        pygame.display.flip()

class PrintingState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.cmd = None

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self,cmd):
        self.cmd = cmd

    def printPicture(self):
        pass

    def checkDialValue(self):
        return 30


    def displayFlip(self):
        logging.debug("사진 출력 화면 재생")
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        if self.checkDialValue() >0:
            self.setCommand("RecodingState")
        else:
            self.setCommand("StreamingState")

        self.machine.screen.fill((255, 255, 255))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])

        pygame.font.init()
        text = "printing... screen"
        font = pygame.font.Font(None, 50)
        imgText = font.render(text, True, (255, 0, 0))
        rect = imgText.get_rect()
        # rect.center = text_space.center
        self.machine.screen.blit(imgText, rect)
        pygame.display.flip()

        self.printPicture()


class RecodingState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.dialValue = None

        self.cmd = None

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self, cmd):
        self.cmd = cmd


    def displayFlip(self):
        logging.debug("녹화중")
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        for evt in pygame.event.get():
            if evt.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                # if statement
                if self.machine.home_rect.collidepoint(pos) & pressed1 == 1:
                    logging.debug("홈 버튼 눌러짐")
                    self.setCommand("StreamingState")

        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])

        pygame.font.init()
        text = "recoding screen"
        font = pygame.font.Font(None, 50)
        imgText = font.render(text, True, (255, 0, 0))
        rect = imgText.get_rect()
        # rect.center = text_space.center
        self.machine.screen.blit(imgText, rect)

        pygame.display.flip()

class LoadingState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.barValue = None
        self.cmd = None

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self,cmd):
        self.cmd = cmd

    def convertToMP4(self):
        pass

    def sendEmail(self):
        pass

    def displayFlip(self):
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)

        self.setCommand("StreamingState")

        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])
        pygame.font.init()
        text = "loading screen"
        font = pygame.font.Font(None, 50)
        imgText = font.render(text, True, (255, 0, 0))
        rect = imgText.get_rect()
        # rect.center = text_space.center
        self.machine.screen.blit(imgText, rect)
        pygame.display.flip()
        if 1:
            self.convertToMP4()
        else:
            self.sendEmail()



class GalleryState(State):
    def __init__(self,Machine):
        self.machine = Machine

        self.playIcon = pygame.image.load('./res/play.png')
        self.play_rect = self.playIcon.get_rect()
        self.play_rect.center = (self.machine.w_size / 2, self.machine.h_size / 2)

        self.driveIcon = pygame.image.load('./res/drive.png')
        self.drive_rect = self.driveIcon.get_rect()
        self.drive_rect.center = (self.machine.w_size - 50, 40)

        self.larrIcon = pygame.image.load('./res/larr.png')
        self.larr_rect = self.larrIcon.get_rect()
        self.larr_rect.center = (70, self.machine.h_size / 2)

        self.rarrIcon = pygame.image.load('./res/rarr.png')
        self.rarr_rect = self.rarrIcon.get_rect()
        self.rarr_rect.center = (self.machine.w_size - 70, self.machine.h_size / 2)

        self.homeIcon = pygame.image.load('./res/home.png')
        self.home_rect = self.homeIcon.get_rect()
        self.home_rect.center = (self.machine.w_size - 50, self.machine.h_size - 50)

        self.cmd = None

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self, cmd):
        self.cmd = cmd



    def displayFlip(self):
        #logging.debug("겔러리 화면 재생")
        for evt in pygame.event.get():
            if evt.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                # if statement
                if self.drive_rect.collidepoint(pos) & pressed1 == 1:
                    logging.debug("이베일 버튼 눌러짐")
                    self.setCommand("email")
                if self.larr_rect.collidepoint(pos) & pressed1 == 1:
                    logging.debug("좌 버튼 눌러짐")
                if self.rarr_rect.collidepoint(pos) & pressed1 == 1:
                    logging.debug("우 버튼 눌러짐")
                if self.play_rect.collidepoint(pos) & pressed1 == 1:
                    logging.debug("실행 버튼 눌러짐")
                if self.home_rect.collidepoint(pos) & pressed1 == 1:
                    logging.debug("홈 버튼 눌러짐")
                    self.setCommand("StreamingState")

        self.machine.screen.fill((255, 255, 255))

        pygame.font.init()
        text = "gallery screen"
        font = pygame.font.Font(None, 50)
        imgText = font.render(text, True, (255, 0, 0))
        rect = imgText.get_rect()
        # rect.center = text_space.center
        self.machine.screen.blit(imgText, (0,0))
        self.machine.screen.blit(self.playIcon, self.play_rect)
        self.machine.screen.blit(self.driveIcon, self.drive_rect)
        self.machine.screen.blit(self.larrIcon, self.larr_rect)
        self.machine.screen.blit(self.rarrIcon, self.rarr_rect)
        self.machine.screen.blit(self.homeIcon, self.home_rect)
        pygame.display.flip()

class ExitState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.name = "ExitState"

    def exit(self):
        logging.debug("시스템 종료...")


    def displayFlip(self):
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])
        pygame.font.init()
        text = "exit screen"
        font = pygame.font.Font(None, 50)
        imgText = font.render(text, True, (255, 0, 0))
        rect = imgText.get_rect()
        # rect.center = text_space.center
        self.machine.screen.blit(imgText, rect)

        pygame.display.flip()
