import numpy as np
import cv2
import time
import sys
import mss
import keyboard 
import pyautogui
import tkinter
import tkinter.filedialog
import threading
import os.path
import playsound

from PIL import Image
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from playsound import playsound

class SimpleDial(QDial):
    def paintEvent(self, event):
        if not self.value() == self.prevValue:
            playsound("assets/Clack.wav")
        self.firstvalue = self.value()
        # create a QStyleOption for the dial, and initialize it with the basic properties
        # that will be used for the configuration of the painter
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        pixmap = QPixmap('assets/dial.png')
        # construct a QRectF that uses the minimum between width and height, 
        # and adds some margins for better visual separation
        # this is partially taken from the fusion style helper source
        width = opt.rect.width()
        height = opt.rect.height()
        r = min(width, height) / 2
        r -= r / 50

        penColor = self.palette().dark().color()
        qp = QPainter(self)
        qp.setRenderHints(qp.Antialiasing)
        qp.setPen(QPen(penColor, 4))
        value = self.value()
        self.prevValue = self.value()

        # find the "real" value ratio between minimum and maximum
        realValue = (value - self.minimum()) / (self.maximum() - self.minimum())
        # compute the angle at which the dial handle should be placed, assuming
        # a range between 240° and 300° (moving clockwise)
        angle = 240 - 300 * realValue
        pixmap = pixmap.scaled(self.width() - (30 * self.width() / self.originalScale[0]),self.height() - (42 * self.height() / self.originalScale[1]))
        print(self.width())
        pixmap =pixmap.transformed(QTransform().rotate(-angle))
        qp.drawPixmap((self.width() + (20 * self.width() / self.originalScale[0]))/2 - pixmap.width()/2, self.height()/2 - pixmap.height()/2, pixmap)

class SimpleDial2(QDial):
    def paintEvent(self, event):
        if not self.value() == self.prevValue:
            playsound("assets/click.wav")
        # create a QStyleOption for the dial, and initialize it with the basic properties
        # that will be used for the configuration of the painter
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        pixmap = QPixmap('assets/dial2.png')
        # construct a QRectF that uses the minimum between width and height, 
        # and adds some margins for better visual separation
        # this is partially taken from the fusion style helper source
        width = opt.rect.width()
        height = opt.rect.height()
        r = min(width, height) / 2
        r -= r / 50

        penColor = self.palette().dark().color()
        qp = QPainter(self)
        qp.setRenderHints(qp.Antialiasing)
        qp.setPen(QPen(penColor, 4))
        value = np.clip(self.value(),1,2)
        self.prevValue = self.value()
        # find the "real" value ratio between minimum and maximum
        realValue = (value - self.minimum()) / (self.maximum() - self.minimum())
        # compute the angle at which the dial handle should be placed, assuming
        # a range between 240° and 300° (moving clockwise)
        angle = 240 - 300 * realValue
        print(pixmap.width())
        print(self.width())
        pixmap = pixmap.scaled(self.width() - (70 * self.width() / self.originalScale[0]),self.height() - (70 * self.height() / self.originalScale[1]))

        pixmap =pixmap.transformed(QTransform().rotate(-angle + 230))
        qp.drawPixmap((self.width() + (50 * self.width() / self.originalScale[0]))/2 - pixmap.width()/2, (self.height() + (50 * self.height() / self.originalScale[1]))/2 - pixmap.width()/2, pixmap)


class WidgetGallery(QWidget):
    def __init__(self):
        
        QFontDatabase.addApplicationFont("./assets/impact.ttf")
        QFontDatabase.addApplicationFont("./assets/impactR.ttf")
        QWidget.__init__(self)
        layout = QVBoxLayout()
        self.label = QLabel(self)
        self.pixmap = QPixmap('assets/image2.png')
        self.label.setPixmap(self.pixmap.scaled(960,540))
        self.setWindowTitle('Open World Shutter')
        self.setLayout(layout)
        layout.addWidget(self.label)
        self.label.setScaledContents(True)        

        self.widgetcollection = []
        
        self.dial = SimpleDial(self)
        self.dial.prevValue = 1
        self.dial.setMinimum(1)
        self.dial.setMaximum(70)
        self.dial.setValue(1)
        self.dial.setWrapping(False)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.sliderMoved)
        self.dial.resize(275,275)
        p = QPoint(165,157)
        self.dial.move(p)
        self.dial.originalScale = (275,275)
        self.dial.originalPos = (165,157) 
        self.widgetcollection.append(self.dial)


        self.dial2 = SimpleDial2(self)
        self.dial2.prevValue = 1
        self.dial2.setMinimum(1)
        self.dial2.setMaximum(8)
        self.dial2.setValue(1)
        self.dial2.setWrapping(False)
        self.dial2.setNotchesVisible(True)
        self.dial2.valueChanged.connect(self.slider2Moved)
        self.dial2.resize(230,230)
        p = QPoint(792,120)
        self.dial2.move(p)
        self.dial2.setToolTip('LOW quality processes images during capture. HI quality takes more images and processes after capture.')
        self.dial2.originalScale = (230,230)
        self.dial2.originalPos = (792,120) 
        self.widgetcollection.append(self.dial2)
        
        self.l1 = QLabel(self)
        self.l1.resize(360,24)
        p1 = QPoint(200,530)
        self.l1.move(p1)
        font = QFont('impact', 24)
        self.l1.setFont(font)
        self.l1.setStyleSheet("QLabel { background-color: white; font-family: 'Impact Label';}")
        self.l1.setText("Exposure Length: " + str(self.dial.value()) + "s ")
        self.l1.originalScale = (360, 24)
        self.l1.originalPos = (200,530) 
        self.widgetcollection.append(self.l1)

        self.l2 = QLabel(self)
        self.l2.resize(228,24)
        p1 = QPoint(200,570)
        self.l2.move(p1)
        font = QFont('impact', 24)
        self.l2.setFont(font)
        self.l2.setStyleSheet("QLabel { background-color: white; font-family: 'Impact Label';}")
        self.l2.setText("Quality: LOW")
        self.l2.originalScale = (228,24)
        self.l2.originalPos = (200,570) 
        self.widgetcollection.append(self.l2)


        self.qualityHigh = False
        self.l3 = QLabel(self)
        self.l3.resize(500,24)
        p1 = QPoint(200,610)
        self.l3.move(p1)
        font = QFont('impact', 24)
        self.l3.setFont(font)
        self.l3.setStyleSheet("QLabel { background-color: white; font-family: 'Impact Label';}")
        self.l3.setText("Shutter start/stop key: F1 ")
        self.l3.originalScale = (500,24)
        self.l3.originalPos = (200,610) 
        self.widgetcollection.append(self.l3)
        

        self.push_button = QPushButton("START" +'\n'+"(F1)", self)
        self.push_button.setDefault(True)
        self.push_button.resize(100,100)
        font2 = QFont('impact', 18)
        self.push_button.setFont(font2)
        self.push_button.setStyleSheet("QPushButton { background-color: #000000; color: #FFFFFF; font-family: 'Impact Label Reversed';} QPushButton:hover {background-color: rgb(40, 40, 40);}")
        p2 = QPoint(1034,570)
        self.push_button.move(p2)
        self.push_button.clicked.connect(self.setupPicture)
        self.push_button.originalScale = (100,100)
        self.push_button.originalPos = (1034,570) 
        self.widgetcollection.append(self.push_button)
       
       
        self.key = "F1"
        self.push_buttonShutterKey = QPushButton("BIND KEY ", self)
        self.push_buttonShutterKey.setDefault(True)
        self.push_buttonShutterKey.resize(150,50)
        font2 = QFont('impact', 18)
        self.push_buttonShutterKey.setFont(font2)
        self.push_buttonShutterKey.setStyleSheet("QPushButton { background-color: #000000; color: #FFFFFF; font-family: 'Impact Label Reversed';} QPushButton:hover {background-color: rgb(40, 40, 40);}")
        p3 = QPoint(200,658)
        self.push_buttonShutterKey.move(p3)
        self.push_buttonShutterKey.clicked.connect(lambda: self.map_key(self.push_buttonShutterKey, self.l3))
        keyboard.on_release_key("F1", self.setupPicture)
        self.push_buttonShutterKey.originalScale = (150,50)
        self.push_buttonShutterKey.originalPos = (200,658) 
        self.widgetcollection.append(self.push_buttonShutterKey)
        
        self.cb = QComboBox(self)
        self.cb.resize(300,25)
        self.cb.move(QPoint(630,585))
        for x in pyautogui.getAllWindows():
            print(x)
            if(x.title != ""):
                self.cb.addItem(str(x.title))
        
        self.cb.currentIndexChanged.connect(self.selectionchange)
        self.cb.originalScale = (300,25)
        self.cb.originalPos = (630,585) 
        self.widgetcollection.append(self.cb)


        self.l4 = QLabel(self)
        self.l4.resize(320,24)
        self.l4.move(QPoint(630,535))
        font = QFont('impact', 24)
        self.l4.setFont(font)
        self.l4.setStyleSheet("QLabel {  background-color: white;font-family: 'Impact Label';}")
        self.l4.setText("Window To Capture ")
        self.l4.originalScale = (320,24)
        self.l4.originalPos = (630,535) 
        self.widgetcollection.append(self.l4)

        self.cb1 = QCheckBox(self)
        self.cb1.setChecked(True)
        self.cb1.stateChanged.connect(self.setSaveVideo)
        self.cb1.resize(100,200)
        self.cb1.move(QPoint(850,575))
        self.saveVideo = True
        self.cb1.originalScale = (100,200)
        self.cb1.originalPos = (850,575) 
        self.widgetcollection.append(self.cb1)

        self.l5 = QLabel(self)
        self.l5.resize(190,24)
        self.l5.move(QPoint(630,660))
        font = QFont('impact', 24)
        self.l5.setFont(font)
        self.l5.setStyleSheet("QLabel { background-color: white; font-family: 'Impact Label';}")
        self.l5.setText("Save Video ")
        self.l5.originalScale = (190,24)
        self.l5.originalPos = (630,660) 
        self.widgetcollection.append(self.l5)

        self.final_pic_true_average = None
        self.final_pic_min_eighty = None
        self.final_pic_max_eighty = None
        self.final_pic_max_only = None
        self.final_pic_min_only = None

        self.qImgAvg = None
        self.qImgMin80 = None
        self.qImgMax80 = None

        self.root = None
        self.running = False
        self.CaptureWindow = self.cb.currentText()
        self.CaptureWindowObject = pyautogui.getWindowsWithTitle(self.CaptureWindow)[0]
        self.setFixedSize(1280, 720)
        self.event = threading.Event()


    def closePicsWindow(self):
        self.savebutton.setHidden(True)
        self.backbutton.setHidden(True)
        self.cameraBack.setHidden(True)
        self.picsBox.setHidden(True)
        self.mainLabel.setHidden(True)
        keyboard.on_release_key(self.key, self.setupPicture)

    def setSaveVideo(self):
        self.saveVideo = not self.saveVideo
    
    def switchPic(self, num,event):
        print("event is " + str(event))
        p = QPixmap(self.qImgAvg)
        if(num == 0):
            print("iszero")
            p = QPixmap(self.qImgAvg)
        elif(num == 2):
            p = QPixmap(self.qImgMin80)
        elif(num == 3):
            p = QPixmap(self.qImgMax80)
        self.currentImgIndex = num
        widthval = min(500, p.width())
        p = p.scaledToWidth(widthval)
        self.mainLabel.setPixmap(p)


    def saveImg(self, index):
        keyboard.unhook_all()
        imToSave = None
        self.root = tkinter.Tk()
        if(index == 0):
            imToSave = self.final_pic_true_average
        elif(index == 2):
            imToSave = self.final_pic_min_eighty
        elif(index == 3):
            imToSave = self.final_pic_max_eighty
        file = tkinter.filedialog.asksaveasfilename(defaultextension=".png")
        if file:
            f = open(file, 'a')
            cv2.imwrite(str(file),imToSave)
            f.close()
            self.root.destroy()
        else:
            self.root.destroy()
        keyboard.on_release_key(self.key, self.setupPicture)
        

    
    def selectionchange(self,i):
      self.CaptureWindow = self.cb.currentText()
      print(self.cb.currentText())
      self.CaptureWindowObject = pyautogui.getWindowsWithTitle(self.CaptureWindow)[0]

    def sliderMoved(self):
        if(self.dial.value() == 70):
            self.l1.setText("Exposure Length: M ")
        else:
            self.l1.setText("Exposure Length: "  + str(self.dial.value()) + "s ")
    
    def slider2Moved(self):
        if(self.dial2.value() == 2):
            self.l2.setText("Quality: HI ")
            self.pixmap = QPixmap('assets/image2HQ.png')
            self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height()))
            self.qualityHigh = True
        else:
            self.l2.setText("Quality: LOW")
            self.pixmap = QPixmap('assets/image2.png')
            self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height()))
            self.qualityHigh = False
    
    def map_key(self, b, l):
        k  = keyboard.read_key()
        l.setText("Shutter start/stop key: " + str(k) + " ")
        self.push_button.setText("START" +'\n'+"(" + str(k) + ")")
        keyboard.unhook_all()
        self.key = str(k)
        thread = Thread(target = self.bindKey)
        thread.start()
        

    def bindKey(self):
        time.sleep(0.5)
        keyboard.on_release_key(self.key, self.setupPicture)     

    def setupPicture(self, event):
        if not self.event.is_set():
            picThread = Thread(target = self.take_picture)
            picThread.start()
            self.event.set()
            time.sleep(2)
            keyboard.on_release_key(self.key, self.setupPicture)     
        return

    def setKeyHook(self):
        time.sleep(1)
        playsound('assets/finished.mp3')
        keyboard.on_release_key(self.key, self.setupPicture)     
        return

    def take_picture(self):
        keyboard.unhook_all()
        playsound('assets/start.mp3')
        exposureTime = self.dial.value()
        if(self.dial.value() == 70):
            exposureTime = 100
        self.final_pic_max_eighty = None
        self.final_pic_min_eighty = None
        self.final_pic_true_average = None
            
        if(self.qualityHigh == True):
            start = time.time()
            (rAvg,gAvg,bAvg) = (None,None,None)
            total = 0
            images = []
            if self.saveVideo:
                gifImagesLight = []
                gifImagesDark = []
                gifImages = []
            with mss.mss() as sct:
                mon = sct.monitors[1]
                print(self.CaptureWindowObject.left)
                if(self.CaptureWindowObject is not None):
                    monitor = {
                        "top": self.CaptureWindowObject.top,  # 0px from the top
                        "left": self.CaptureWindowObject.left + 8,  # 0px from the left
                        "width": self.CaptureWindowObject.width - 16,
                        "height": self.CaptureWindowObject.height - 8,
                        "mon": 0,
                        }
                else:
                    screen = app.primaryScreen()
                    monitor = {
                    "top": 0,  # 0px from the top
                    "left": 0,  # 0px from the left
                    "width": screen.size().width(),
                    "height": screen.size().height(),
                    "mon": 0,
                    }
                while time.time() - start < exposureTime :
                    if(keyboard.is_pressed(self.key)):
                        break
                    sct_img = sct.grab(monitor)
                    images.append(sct_img)
                playsound('assets/stop.mp3')
                time.sleep(1)
                self.event.clear()

            gifImagesLight = []
            gifImagesDark = []
            gifImages = []
            for f in images:
                img = Image.frombytes("RGB", f.size, f.bgra, "raw", "BGRX")
                
                img_np = np.array(img)

                frame = cv2.cvtColor(img_np,cv2.COLOR_BGR2RGB)
                frame1 = frame.astype("float")
                (R,G,B) = cv2.split(frame1)
                if total == 0:
                    maxavg = frame1
                    minavg = frame1
                    rAvg = R
                    bAvg = B
                    gAvg = G
                else:
                    maxavg = np.maximum(maxavg, frame1)
                    minavg = np.minimum(minavg, frame1)
                    rAvg = ((total * rAvg) + (1*R)) / (total + 1.0)
                    gAvg = ((total * gAvg) + (1*G)) / (total + 1.0)
                    bAvg = ((total * bAvg) + (1*B)) / (total + 1.0)

                total += 1
                main_avg = cv2.merge([rAvg,gAvg,bAvg])
                if self.saveVideo:
                    gifImagesLight.append(maxavg.astype("uint8"))
                    gifImagesDark.append(minavg.astype("uint8"))
                    gifImages.append(main_avg.astype("uint8"))
            video = cv2.VideoWriter("testLight.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 60, (self.CaptureWindowObject.width,self.CaptureWindowObject.height))
            for f in gifImagesLight:
                video.write(f)
            video2 = cv2.VideoWriter("testDark.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 60, (self.CaptureWindowObject.width,self.CaptureWindowObject.height))
            for f in gifImagesDark:
                video2.write(f)
            video3 = cv2.VideoWriter("testAvg.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 60, (self.CaptureWindowObject.width,self.CaptureWindowObject.height))
            for f in gifImages:
                video3.write(f)
            self.final_pic_max_eighty = (main_avg + 4*maxavg) / 5.0
            self.final_pic_min_eighty = (main_avg + 4*minavg) / 5.0
            self.final_pic_true_average = main_avg
            self.final_pic_true_average = self.final_pic_true_average.astype("uint8")
            self.final_pic_min_eighty = self.final_pic_min_eighty.astype("uint8")
            self.final_pic_max_eighty = self.final_pic_max_eighty.astype("uint8")
            print("total number of frames for high quality exposure is")
            print(total)
        else:
            print("entering low quality mode")
            start = time.time()
            (rAvg,gAvg,bAvg) = (None,None,None)
            total = 0
            frame = None
            frame1 = None
            maxavg = None
            minavg = None
            if self.saveVideo:
                gifImagesLight = []
                gifImagesDark = []
                gifImages = []
            with mss.mss() as sct:

                mon = sct.monitors[1]

                if(self.CaptureWindowObject is not None):
                    monitor = {
                        "top": self.CaptureWindowObject.top,  # 0px from the top
                        "left": self.CaptureWindowObject.left + 8,  # 0px from the left
                        "width": self.CaptureWindowObject.width - 16,
                        "height": self.CaptureWindowObject.height - 8,
                        "mon": 0,
                        }
                else:
                    screen = app.primaryScreen()
                    monitor = {
                    "top": 0,  # 0px from the top
                    "left": 0,  # 0px from the left
                    "width": screen.size().width(),
                    "height": screen.size().height(),
                    "mon": 0,
                    }
                while time.time() - start < exposureTime :
                    if(keyboard.is_pressed(self.key)):
                        break
                    sct_img = sct.grab(monitor)
                    if(keyboard.is_pressed(self.key)):
                        break
                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                    img_np = np.array(img)
                    if(keyboard.is_pressed(self.key)):
                        break
                    
                    frame = cv2.cvtColor(img_np,cv2.COLOR_BGR2RGB)
                    frame1 = frame.astype("float")
                    if(keyboard.is_pressed(self.key)):
                        break
                    (R,G,B) = cv2.split(frame1)
                    if total == 0:
                        maxavg = frame1
                        minavg = frame1
                        rAvg = R
                        bAvg = B
                        gAvg = G
                    else:
                        maxavg = np.maximum(maxavg, frame1)
                        minavg = np.minimum(minavg, frame1)
                        rAvg = ((total * rAvg) + (1*R)) / (total + 1.0)
                        gAvg = ((total * gAvg) + (1*G)) / (total + 1.0)
                        bAvg = ((total * bAvg) + (1*B)) / (total + 1.0)

                    total += 1
                    main_avg = cv2.merge([rAvg,gAvg,bAvg])
                    if self.saveVideo:
                        gifImagesLight.append(np.copy(maxavg.astype("uint8")))
                        gifImagesDark.append(np.copy(minavg.astype("uint8")))
                        gifImages.append(np.copy(main_avg.astype("uint8")))
                    if(keyboard.is_pressed(self.key)):
                        break
            playsound('assets/stop.mp3')
            time.sleep(1)
            self.event.clear()

            print("total number of frames for low quality exposure is")
            print(total)
            self.final_pic_max_eighty = (main_avg + 4*maxavg) / 5.0
            self.final_pic_min_eighty = (main_avg + 4*minavg) / 5.0
            self.final_pic_true_average = main_avg

            self.final_pic_true_average = self.final_pic_true_average.astype("uint8")
            self.final_pic_min_eighty = self.final_pic_min_eighty.astype("uint8")
            self.final_pic_max_eighty = self.final_pic_max_eighty.astype("uint8")
        
        index = 0
        darkstring= "Exposure" + str(index) + "Min.png"
        avgstring= "Exposure" + str(index) + "Avg.png"
        lightstring= "Exposure" + str(index) + "Max.png"

        file_existsDark = os.path.exists(darkstring)
        file_existsAvg = os.path.exists(avgstring)
        file_existsLight = os.path.exists(lightstring)
        while(file_existsDark or file_existsAvg or file_existsLight):
            index = index + 1
            darkstring= "Exposure" + str(index) + "Min.png"
            avgstring= "Exposure" + str(index) + "Avg.png"
            lightstring= "Exposure" + str(index) + "Max.png"
            file_existsDark = os.path.exists(darkstring)
            file_existsAvg = os.path.exists(avgstring)
            file_existsLight = os.path.exists(lightstring)
        cv2.imwrite(darkstring,self.final_pic_min_eighty)
        cv2.imwrite(lightstring,self.final_pic_max_eighty)
        cv2.imwrite(avgstring,self.final_pic_true_average)

        if(self.saveVideo):
            height, width, channels = gifImages[0].shape
            FrameRate = 30
            if(self.qualityHigh == True == True):
                FrameRate = 60
            video = cv2.VideoWriter("ExposureVideo" + str(index) + "Max.mp4", cv2.VideoWriter_fourcc(*'avc1'), FrameRate, (width,height))
            for f in gifImagesLight:
                video.write(f)
            video.release()

            video2 = cv2.VideoWriter("ExposureVideo" + str(index) + "Min.mp4", cv2.VideoWriter_fourcc(*'avc1'), FrameRate, (width,height))
            for f in gifImagesDark:
                video2.write(f)
            video2.release()

            video3 = cv2.VideoWriter("ExposureVideo" + str(index) + "Avg.mp4", cv2.VideoWriter_fourcc(*'avc1'), FrameRate, (width,height))
            for f in gifImages:
                video3.write(f)
            video3.release()

        self.setKeyHook()
        return

def appExec():
    
    app.exec_()
    print("goodbye")
    
if __name__ == '__main__':
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):  
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(appExec())
    
