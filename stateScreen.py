#-*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import logging
logging.basicConfig(level=logging.DEBUG)
class State:
    def clickedPushButton(self):
        pass

    def clickedGalleryBox(self):
        pass

    def checkDialValue(self,dialValue):
        pass

    def clickedHomeBox(self):
        pass

    def finishedRecoding(self):
        pass

    def reached100percent(self):
        pass

    def clickedSendEmail(self):
        pass

    def systemShutdown(self):
        pass

    def displayFlip(self):
        pass

class Machine:
    def __init__(self,w_size, h_size):
        # self.screen = pygame.display.set_mode((w_size, h_size), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((w_size, h_size))

        self.streamingState = StreamingState(self)
        self.printingState = PrintingState(self)
        self.recodingState = RecodingState(self)
        self.loadingState = LoadingState(self)
        self.galleryState = GalleryState(self)
        self.exitState = ExitState(self)
        self.state = StreamingState(self)

    def buttonCliked(self):
        pass

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

    def clickedPushButton(self):
        logging.debug("푸시버튼 눌러짐")
        self.machine.setState(self.machine.getPrintingState())

    def clickedGalleryBox(self):
        logging.debug("겔러리 버튼 눌러짐")
        self.machine.setState(self.machine.getGalleryState())

    def systemShutdown(self):
        logging.debug("시스템 종료 버튼 눌러짐")
        self.machine.setState(self.machine.getExitState())

    def displayFlip(self):
        logging.debug("스트리밍 화면 재생")
        text = "streaming screen"
        text_space = pygame.draw.rect(self.machine.screen, (255, 0, 0), (0,0, 100, 30))

        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_q:
                    logging.debug("키보드 q")
        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])
        '''
        font = pygame.font.Font(None, 10)
        imgText = font.render(text, True, (255, 0, 0))
        rect = imgText.get_rect()
        rect.center = text_space.center
        self.machine.screen.blit(imgText, rect)
        '''
        pygame.display.flip()

class PrintingState(State):
    def __init__(self,Machine):
        self.machine = Machine

    def checkDialValue(self,dialValue):
        logging.debug("다이얼 번호 책크")
        if type(dialValue) is not int:
            logging.error("type err : PrintingState.checkDialValue parameter is not tpye of int")
            return -1
        if dialValue == 0:
            self.machine.setState(self.machine.getStreamingState())
        else:
            self.machine.setState(self.machine.recodingState())

    def displayFlip(self):
        logging.debug("사진 출력 화면 재생")
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_q:
                    logging.debug("키보드 q")
        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])
        pygame.display.flip()


class RecodingState(State):
    def __init__(self,Machine):
        self.machine = Machine

    def clickedHomeBox(self):
        logging.debug("홈 버튼 눌러짐")
        self.machine.setState(self.machine.getStreamingState())

    def finishedRecoding(self):
        logging.debug("녹화 완료")
        self.machine.setState(self.machine.getLoadingState())

    def displayFlip(self):
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_q:
                    logging.debug("키보드 q")
        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])
        pygame.display.flip()

class LoadingState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.barValue = None

    def reached100percent(self):
        logging.debug("프로그래스바가 100퍼센트 됨")
        self.machine.setState(self.machine.getStreamingState())

    def setProgressBar(self,barValue):
        if type(barValue) is not int:
            logging.error("type err : LoadingState.setProgressBar parameter is not tpye of int")
            return -1
        elif 0 <= barValue and barValue <= 100:
            logging.error("value range err : LoadingState.setProgressBar parameter is not in 0<= barValue <= 100 ")
            return -1
        else:
            self.barValue = barValue

    def getBarValue(self):
        return  self.barValue

    def displayFlip(self):
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_q:
                    logging.debug("키보드 q")
        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])
        pygame.display.flip()


class GalleryState(State):
    def __init__(self,Machine):
        self.machine = Machine

    def clickedHomeBox(self):
        logging.debug("홈 버튼 눌러짐")
        self.machine.setState(self.machine.getStreamingState())

    def clickedSendEmail(self):
        logging.debug("이메일 버튼 눌러짐")
        self.machine.setState(self.machine.getLoadingState())

    def displayFlip(self):
        logging.debug("겔러리 화면 재생")
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_q:
                    logging.debug("키보드 q")
        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])
        pygame.display.flip()

class ExitState(State):
    def __init__(self,Machine):
        self.machine = Machine

    def exit(self):
        logging.debug("시스템 종료...")


    def displayFlip(self):
        BLUE = (100, 230, 255)
        GRAY = (200, 200, 200)
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_q:
                    logging.debug("키보드 q")
        self.machine.screen.fill((0, 0, 0))
        pygame.draw.rect(self.machine.screen, GRAY, [0, 0, 50, 50])
        pygame.display.flip()

import time

if __name__ == '__main__':
    machine = Machine(480,320)
    machine.state.displayFlip()
    time.sleep(1)
    machine.state.clickedGalleryBox()
    time.sleep(1)
    machine.state.clickedHomeBox()
    while True:
        pass