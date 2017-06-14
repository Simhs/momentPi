#-*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import logging
import time
from threading import Thread

from ExternalDevice import Button
from ExternalDevice import Dial
from ExternalDevice import HyperLapseCam

import os

#import ExternalDevice

logging.basicConfig(level=logging.DEBUG)
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

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

        
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        
        #pygame.init()
        #self.screen = pygame.display.set_mode((w_size, h_size),0,32)

        self.shareIndex = 0

        self.galleryIcon = pygame.image.load('/home/pi/Desktop/momentPi/res/gallery.png')
        self.gallery_rect = self.galleryIcon.get_rect()
        self.gallery_rect.center = (self.w_size - 50, self.h_size - 50)

        self.aimIcon = pygame.image.load('/home/pi/Desktop/momentPi/res/aim.png')
        self.aim_rect = self.aimIcon.get_rect()
        self.aim_rect.center = (self.w_size / 2, self.h_size / 2)

        self.playIcon = pygame.image.load('/home/pi/Desktop/momentPi/res/play.png')
        self.play_rect = self.playIcon.get_rect()
        self.play_rect.center = (self.w_size / 2, self.h_size / 2)

        self.driveIcon = pygame.image.load('/home/pi/Desktop/momentPi/res/drive.png')
        self.drive_rect = self.driveIcon.get_rect()
        self.drive_rect.center = (self.w_size - 50, 40)

        self.larrIcon = pygame.image.load('/home/pi/Desktop/momentPi/res/larr.png')
        self.larr_rect = self.larrIcon.get_rect()
        self.larr_rect.center = (70, self.h_size / 2)

        self.rarrIcon = pygame.image.load('/home/pi/Desktop/momentPi/res/rarr.png')
        self.rarr_rect = self.rarrIcon.get_rect()
        self.rarr_rect.center = (self.w_size - 70, self.h_size / 2)

        self.homeIcon = pygame.image.load('/home/pi/Desktop/momentPi/res/home.png')
        self.home_rect = self.homeIcon.get_rect()
        self.home_rect.center = (self.w_size - 50, self.h_size - 50)

        self.loadingIcon = pygame.image.load('/home/pi/Desktop/momentPi/res/loading.png')
        self.loading_rect = self.loadingIcon.get_rect()
        self.loading_rect.center = (self.w_size/2, self.h_size/2)

        self.streamingState = StreamingState(self)
        self.printingState = PrintingState(self)
        self.recodingState = RecodingState(self)
        self.loadingState = LoadingState(self)
        self.emailSendState = EmailSendState(self)
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
        elif cmd=="EmailSendState":
            self.setState(self.getEmailSendState())
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

    def getEmailSendState(self):
        return self.emailSendState

    def getGalleryState(self):
        return self.galleryState

    def getExitState(self):
        return self.exitState

import os
import time
import io
import pygame
import picamera

class StreamingState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.cmd = None
        self.button = None

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self,cmd):
        self.cmd = cmd

    def displayFlip(self):
        self.button = Button()
        self.button.start()
        logging.debug("1")
        
        with picamera.PiCamera() as camera:
            logging.debug("카메라 객체생석 확인")
            camera.resolution = (320, 240)
            camera.rotation   = 0
            camera.crop       = (0.0, 0.0, 1.0, 1.0)
            rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)
            while True:
                logging.debug("3")
                stream = io.BytesIO()
                camera.capture(stream, use_video_port=True, format='rgb', resize=(320, 240))
                stream.seek(0)
                stream.readinto(rgb)
                stream.close()
                
                self.machine.screen.fill((255, 255, 255))
                
                img = pygame.image.frombuffer(rgb[0:(320 * 240 * 3)], (320, 240), 'RGB')
                img = pygame.transform.scale(img,(480,340))
                self.machine.screen.blit(img, (0,0))
            
                self.machine.screen.blit(self.machine.galleryIcon, self.machine.gallery_rect)
                self.machine.screen.blit(self.machine.aimIcon, self.machine.aim_rect)
                pygame.display.flip()
                

                
                if self.button.getButtonValue() == 1:
                    captureSound = pygame.mixer.Sound("/home/pi/Desktop/momentPi/res/sounds/sound.wav")
                    captureSound.play()    
                    # milliseconds wait for each sound to finish
                    while pygame.mixer.music.get_busy(): 
                        pygame.time.Clock().tick(10)
                    #time.sleep(2)
                    logging.debug("버튼입력")
                    self.setCommand("PrintingState")
                    self.button.close()
                    break

                #logging.debug("스트리밍 화면 재생")
                for evt in pygame.event.get():
                    if evt.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                        # if statement
                        if self.machine.gallery_rect.collidepoint(pos) & pressed1 == 1:
                            self.setCommand("GalleryState")
                            
                            os.system("espeak \"gallery, mode\" ")
                            logging.debug("겔러리버튼입력")
                            self.button.close()
                            return
        
		    if evt.type == pygame.KEYDOWN:
			if evt.key==pygame.K_q:
			    exit()

			

import datetime   
import picamera

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

    def printPicture(self,isSave):
        nowPicName = str(datetime.datetime.now()).replace(" ","-")
        with picamera.PiCamera() as picam:
            picam.capture('/home/pi/Desktop/momentPi/image/savedImage/'+nowPicName+'.jpg')
            time.sleep(1)
            os.system("espeak \"printing, picture\" ")
            os.system("lpr -o fit-to-page /home/pi/Desktop/momentPi/image/savedImage/"+nowPicName+".jpg")
        if not isSave:
            os.system("rm -rf /home/pi/Desktop/momentPi/image/savedImage/"+nowPicName+".jpg")
            pass
    

    def displayFlip(self):
        dial = Dial()
        self.machine.screen.fill((255, 255, 255))
        pygame.draw.rect(self.machine.screen, (200, 200, 200), [0, 0, 50, 50])

        pygame.font.init()
        text = "printing... screen"
        font = pygame.font.Font(None, 50)
        imgText = font.render(text, True, (255, 0, 0))
        rect = imgText.get_rect()
        
        # rect.center = text_space.center
        self.machine.screen.blit(imgText, rect)
        pygame.display.flip()
        
        if dial.getValue() >0:
            self.printPicture(False)
            self.setCommand("RecodingState")
                
            
        else:
            self.printPicture(True)
            self.setCommand("StreamingState")
                
        time.sleep(2)
        dial.close()


        
import time
import cv2
import picamera

class RecodingState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.dialValue = Dial()
        self.cmd = None
        self.rgb = None
        
        self.finish = False

        self.gotoState = False

        self.picam = None
        #self.camera = HyperLapseCam(100)


    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self, cmd):
        self.cmd = cmd

    def saveImg(self):
        pass
        #self.camera.startCapture(2,2)

        
    
    def capture(self,totaltime):
        totaltime = float(totaltime)
        timer = totaltime*60.0/750.0
        #print timer
        for i in range(750):
            if self.finish == True:
                return
            self.picam.capture('/home/pi/Desktop/momentPi/image/tempImage/image'+str(i)+'.jpg')
            time.sleep(timer)
        self.finish = True
        return
    
            
    

    def cvimage_to_pygame(self,image):
        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cvimg =pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"RGB")
        except:
            return False
        return cvimg
    
        
    def preview(self):
        while not self.finish:
            for evt in pygame.event.get():
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                    # if statement
                    if self.machine.home_rect.collidepoint(pos) & pressed1 == 1:
                        logging.debug("홈 버튼 눌러짐")
                        self.finish = True
                        self.gotoState = True
                        return
        
            stream = io.BytesIO()
            self.picam.capture(stream, use_video_port=True, format='rgb', resize=(320, 240))
            stream.seek(0)
            stream.readinto(self.rgb)
            stream.close()
                
            self.machine.screen.fill((255, 255, 255))
            img = pygame.image.frombuffer(self.rgb[0:(320 * 240 * 3)], (320, 240), 'RGB')
            img = pygame.transform.scale(img,(480,340))
            self.machine.screen.blit(img, (0,0))
            self.machine.screen.blit(self.machine.homeIcon, self.machine.home_rect)
            pygame.display.flip()

            
                
    def displayFlip(self):
        logging.debug("녹화중")
        
        time.sleep(1)
        os.system("espeak \"starting, recode\" ")
        os.system("sudo rm -rf /home/pi/Desktop/momentPi/image/tempImage/*")
        dial = Dial()
        dialValue = int(dial.getValue())
        logging.debug(dialValue)      
        dial.close()
        with picamera.PiCamera() as self.picam:
            # self.picam.resolution = (1920, 1080)
            self.picam.rotation   = 180
            self.picam.crop       = (0.0, 0.0, 1.0, 1.0)
            self.rgb = bytearray(self.picam.resolution[0] * self.picam.resolution[1] * 3)
            # self.picam = picamera.PiCamera()
            self.picam.resolution = (1920, 1080) #okay
            
            
            self.thread1 = Thread(target=self.capture,args=(dialValue,))
            self.thread2 = Thread(target=self.preview,args=())
            self.thread1.start()
            self.thread2.start()

            self.thread1.join()
            self.thread2.join()

            if not self.gotoState:
                self.setCommand("LoadingState")
            else:
                self.setCommand("StreamingState")
                os.system("espeak \"cancel\" ")
                
            self.finish = False
            self.gotoState = False

import datetime
class LoadingState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.barValue = None
        self.cmd = None
        self.convertOver = False

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self,cmd):
        self.cmd = cmd

    def convertToMP4(self):
        
        os.system("espeak \"convert, file\" ")
        os.system("ffmpeg -y -f image2 -i /home/pi/Desktop/momentPi/image/tempImage/image%d.jpg -preset fast /home/pi/Desktop/momentPi/image/savedImage/"+str(datetime.datetime.now()).replace(" ","-")+".mp4")
        self.convertOver = True


    def animation(self):
        angle = -20
        spd = 2
        while True:
            if not self.convertOver:
                clock = pygame.time.Clock()
                self.machine.screen.fill((0, 0, 0))
                pygame.draw.rect(self.machine.screen, (200, 200, 200), [0, 0, self.machine.w_size, self.machine.h_size])
                pygame.font.init()
                text = "loading..."
                font = pygame.font.Font(None, 50)
                imgText = font.render(text, True, (255, 0, 0))
                rect = imgText.get_rect()
                self.machine.screen.blit(imgText, rect)
                image = pygame.transform.rotate(self.machine.loadingIcon, angle)
                rect = image.get_rect()
                rect.center = self.machine.loading_rect.center
                self.machine.screen.blit(image,rect)
                pygame.display.flip()
                time.sleep(0.01)
                if angle < -160:
                    angle -= spd
                    spd -= 0.19
                else:
                    angle -= spd
                    spd += 0.2
                if angle < -380:
                    angle = -20
                    spd = 3
            else:
                break


    def displayFlip(self):
        self.setCommand("StreamingState")
        self.thread = Thread(target=self.animation, )
        self.thread.start()
        self.convertToMP4()
        self.thread.join()
        self.convertOver = False


import httplib2
import os
from apiclient import discovery
import apiclient.http
import datetime
from oauth2client import *
from oauth2client.file import Storage
import argparse


class EmailSendState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.barValue = None
        self.cmd = None
        self.convertOver = False

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def setCommand(self,cmd):
        self.cmd = cmd


    def sendEmail(self):
        os.system("espeak \"upload, file\" ")
        index = self.machine.shareIndex
        fileList = os.listdir("/home/pi/Desktop/momentPi/image/savedImage/")
        
        SCOPES = "https://www.googleapis.com/auth/drive"
        CLIENT_SECRET_FILE = "/home/pi/Desktop/momentPi/lib/client_secret.json"
        APPLICATION_NAME = 'Drive API Python Quickstart'
        if "mp4" in fileList[index]:
            MIMETYPE = 'video/mp4'
        else:
            MIMETYPE = 'image/jpeg'
        
        FILENAME = "/home/pi/Desktop/momentPi/image/savedImage/"+str(fileList[index])
        TITLE = str(datetime.datetime.now())
        DESCRIPTION = 'A shiny new text document about hello world.'
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

        credentials = None
        
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
                print('Storing credentials to ' + credential_path)
        
        http = credentials.authorize(httplib2.Http())
        drive_service = apiclient.discovery.build('drive', 'v2', http=http)
        media_body = apiclient.http.MediaFileUpload(FILENAME,mimetype=MIMETYPE,resumable=True)
        body = {'title': TITLE,'description': DESCRIPTION,}
        

        new_file = drive_service.files().insert(body=body, media_body=media_body).execute()
        self.convertOver = True

        
    def animation(self):
        angle = -20
        spd = 2
        while True:
            if not self.convertOver:
                clock = pygame.time.Clock()
                self.machine.screen.fill((0, 0, 0))
                pygame.draw.rect(self.machine.screen, (200, 200, 200), [0, 0, self.machine.w_size, self.machine.h_size])
                pygame.font.init()
                text = "loading..."
                font = pygame.font.Font(None, 50)
                imgText = font.render(text, True, (255, 0, 0))
                rect = imgText.get_rect()
                self.machine.screen.blit(imgText, rect)
                image = pygame.transform.rotate(self.machine.loadingIcon, angle)
                rect = image.get_rect()
                rect.center = self.machine.loading_rect.center
                self.machine.screen.blit(image,rect)
                pygame.display.flip()
                time.sleep(0.01)
                if angle < -160:
                    angle -= spd
                    spd -= 0.19
                else:
                    angle -= spd
                    spd += 0.2
                if angle < -380:
                    angle = -20
                    spd = 3
            else:
                break


    def displayFlip(self):
        logging.debug("sendemail state!!")
        self.setCommand("StreamingState")
        sendEmailThread = Thread(target=self.sendEmail,args=())
        self.thread = Thread(target=self.animation, )
        self.thread.start()
        sendEmailThread.start()
        
        self.thread.join()
        sendEmailThread.join()
        self.convertOver = False


import os
import cv2

class GalleryState(State):
    def __init__(self,Machine):
        self.machine = Machine
        self.cmd = None
        self.fileList = os.listdir("/home/pi/Desktop/momentPi/image/savedImage/")
        #self.fileList.reverse()
        print self.fileList
        self.index = 0

    def getCommand(self):
        command = self.cmd
        self.setCommand(None)
        return command

    def addIndex(self):
        os.system("espeak \"next\" ")
        self.fileList = os.listdir("/home/pi/Desktop/momentPi/image/savedImage/")
        #self.fileList.reverse()
        numlist = len(self.fileList)
        if numlist == 0:
            return False
        else:
            self.index += 1
            self.index = self.index%numlist
            
    def subIndex(self):
        os.system("espeak \"before\" ")
        self.fileList = os.listdir("/home/pi/Desktop/momentPi/image/savedImage/")
        #self.fileList.reverse()
        numlist = len(self.fileList)
        if numlist == 0:
            return False
        else:
            self.index -= 1
            self.index = self.index%numlist

    def setCommand(self, cmd):
        self.cmd = cmd


    def cvimage_to_pygame(self,image):
        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cvimg =pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"RGB")
        except:
            return False
        return cvimg
    
    def displayFlip(self):
        logging.debug("gallery겔러리 화면 재생")
        if "mp4" in self.fileList[self.index]:
            self.cap = cv2.VideoCapture("/home/pi/Desktop/momentPi/image/savedImage/"+str(self.fileList[self.index]))
            
            while True:
                for evt in pygame.event.get():
                    if evt.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                        # if statement
                        if self.machine.drive_rect.collidepoint(pos) & pressed1 == 1:
                            logging.debug("이베일 버튼 눌러짐")
                            self.setCommand("EmailSendState")
                            self.machine.shareIndex = self.index
                            self.cap.release()
                            return
                        if self.machine.larr_rect.collidepoint(pos) & pressed1 == 1:
                            logging.debug("좌 버튼 눌러짐")
                            self.subIndex()
                            self.cap.release()
                            return
                        if self.machine.rarr_rect.collidepoint(pos) & pressed1 == 1:
                            logging.debug("우 버튼 눌러짐")
                            self.addIndex()
                            self.cap.release()
                            return
                        if self.machine.play_rect.collidepoint(pos) & pressed1 == 1:
                            logging.debug("실행 버튼 눌러짐")
                            self.cap.release()
                            return                            
                        if self.machine.home_rect.collidepoint(pos) & pressed1 == 1:
                            os.system("espeak \"cancel\" ")
                            logging.debug("홈 버튼 눌러짐")
                            self.setCommand("StreamingState")
                            self.cap.release()
                            return


                ret,cvimg = self.cap.read()
                cvimg = cv2.resize(cvimg,(480,340), interpolation=cv2.INTER_AREA)
                
                self.machine.screen.fill((255, 255, 255))
                
                #cv2.imshow("test",cvimg)
                
                img = self.cvimage_to_pygame(cvimg)
                img = pygame.transform.scale(img, (480, 340))
                    
                self.machine.screen.blit(img,(0,0))
                self.machine.screen.blit(self.machine.playIcon, self.machine.play_rect)
                self.machine.screen.blit(self.machine.driveIcon, self.machine.drive_rect)
                self.machine.screen.blit(self.machine.larrIcon, self.machine.larr_rect)
                self.machine.screen.blit(self.machine.rarrIcon, self.machine.rarr_rect)
                self.machine.screen.blit(self.machine.homeIcon, self.machine.home_rect)
                pygame.display.flip()
        else:
            cvimg = cv2.imread("/home/pi/Desktop/momentPi/image/savedImage/"+str(self.fileList[self.index]),cv2.IMREAD_COLOR)
            self.machine.screen.fill((255, 255, 255))
            img = self.cvimage_to_pygame(cvimg)
            img = pygame.transform.scale(img, (480, 340))
            self.machine.screen.blit(img,(0,0))
            self.machine.screen.blit(self.machine.playIcon, self.machine.play_rect)
            self.machine.screen.blit(self.machine.driveIcon, self.machine.drive_rect)
            self.machine.screen.blit(self.machine.larrIcon, self.machine.larr_rect)
            self.machine.screen.blit(self.machine.rarrIcon, self.machine.rarr_rect)
            self.machine.screen.blit(self.machine.homeIcon, self.machine.home_rect)
            pygame.display.flip()
            while True:
                for evt in pygame.event.get():
                        if evt.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
                            # if statement
                            if self.machine.drive_rect.collidepoint(pos) & pressed1 == 1:
                                logging.debug("이베일 버튼 눌러짐")
                                self.setCommand("EmailSendState")
                                self.machine.shareIndex = self.index
                                return
                            if self.machine.larr_rect.collidepoint(pos) & pressed1 == 1:
                                logging.debug("좌 버튼 눌러짐")
                                self.subIndex()
                                return
                            if self.machine.rarr_rect.collidepoint(pos) & pressed1 == 1:
                                logging.debug("우 버튼 눌러짐")
                                self.addIndex()
                                return
                            if self.machine.play_rect.collidepoint(pos) & pressed1 == 1:
                                logging.debug("실행 버튼 눌러짐")
                                return                            
                            if self.machine.home_rect.collidepoint(pos) & pressed1 == 1:
                                logging.debug("홈 버튼 눌러짐")
                                os.system("espeak \"cancel\" ")
                                self.setCommand("StreamingState")
                                return
                            
        

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
