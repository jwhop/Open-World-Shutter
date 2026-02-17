import numpy as np
import cv2
import time
import sys
import mss
import keyboard 
import pyautogui
import threading
import os.path
import playsound

from PIL import Image
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from playsound import playsound
import cgitb
cgitb.enable(format = 'text')

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
        pixmap = pixmap.scaled(self.width() - (30 * self.width() / self.originalScale[0]),self.height() - (42 * self.height() / self.originalScale[1]))

        pixmap =pixmap.transformed(QTransform().rotate(-angle + 230))
        qp.drawPixmap((self.width() + (30 * self.width() / self.originalScale[0]))/2 - pixmap.width()/2, self.height()/2 - pixmap.height()/2, pixmap)


class MainWindow(QMainWindow):
    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
    def setupUi(self, MainWindow):
        print("setting things up")
        self.setWindowIcon(QIcon('icon.ico'))
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(376, 550)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        font = QFont()
        font.setFamily(u"Impact Label")
        font.setPointSize(36)
        self.label_7.setScaledContents(False)
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.resize(380,200)
        self.label_7.setStyleSheet( "background-image: url(\"assets/CameraBackPatternWithText.png\"); background-repeat: no-repeat; background-position: center;")
        
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 10, 20, 20)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

    #exposure settings
        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(99)
        self.spinBox.setEnabled(True)
        self.spinBox.setValue(5)        
        self.spinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBox.valueChanged.connect(self.changeExposureLength)
        self.horizontalLayout_2.addWidget(self.spinBox)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.stateChanged.connect(self.setManual)
        self.checkBox.setChecked(False)
        self.manual = False

        self.horizontalLayout_2.addWidget(self.checkBox)


        self.horizontalLayout.addLayout(self.horizontalLayout_2)

    #quality settings
        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.horizontalLayout_4.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_4.addWidget(self.radioButton_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.label_3)

    #shutter key settings
        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_6.addWidget(self.label_5)
        self.key = "F1"
        self.pushButton = QPushButton(self.groupBox_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.clicked.connect(lambda: self.map_key(self.pushButton, self.label_5))
        self.horizontalLayout_6.addWidget(self.pushButton)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)

    #capture window

        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_8.addWidget(self.label_6)

        self.comboBox = QComboBox(self.groupBox_4)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(125,100))
        for x in pyautogui.getAllWindows():
            if(x.title != "" and x.width > 0 and x.height > 0):
                self.comboBox.addItem(str(x.title))
        self.comboBox.setEnabled(False)
        self.comboBox.currentIndexChanged.connect(self.selectionchange)


        self.horizontalLayout_8.addWidget(self.comboBox)

        self.pushButton_4 = QPushButton(self.groupBox_4)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.clicked.connect(self.refreshComboBox)

        self.horizontalLayout_8.addWidget(self.pushButton_4)

        self.checkBox_2 = QCheckBox(self.groupBox_4)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)
        self.CaptureWholeScreen = True
        self.checkBox_2.stateChanged.connect(self.setWholeScreenCapture)
        self.horizontalLayout_8.addWidget(self.checkBox_2)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        
        self.checkBox_3 = QCheckBox(self.groupBox_5)
        self.saveVideo = False
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.stateChanged.connect(self.setVideoSave)

        self.horizontalLayout_10.addWidget(self.checkBox_3)


        self.checkBox_4 = QCheckBox(self.groupBox_5)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setChecked(False)
        self.checkBox_4.stateChanged.connect(self.setCropTop)
        self.cropTop = False

        self.horizontalLayout_10.addWidget(self.checkBox_4)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_10)

        self.verticalLayout.addWidget(self.groupBox_5)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.clicked.connect(self.setupPicture)
        self.verticalLayout.addWidget(self.pushButton_2)
        keyboard.on_release_key("F1", self.setupPicture)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(False)
        self.menubar.setGeometry(QRect(0, 0, 376, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(False)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        self.ExposureTime = self.spinBox.value()
        self.final_pic_true_average = None
        self.final_pic_min_eighty = None
        self.final_pic_max_eighty = None
        self.final_pic_max_only = None
        self.final_pic_min_only = None
        self.CaptureWindow = self.comboBox.currentText()
        self.CaptureWindowObject = pyautogui.getWindowsWithTitle(self.CaptureWindow)[0]
        self.event = threading.Event()        

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Open World Shutter", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Exposure Settings", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Exposure Length (seconds):", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Quality Settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Quality:", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"LOW", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"HIGH ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"*warning: expect processing times of ~5x exposure length on high quality*", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Shutter Key", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Shutter Key: ", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"F1", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Bind Key", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Capture Window", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Window:", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))

        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Capture Whole Screen", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Misc Settings", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Save Video", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"Crop Top Window Header", None))

        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"START CAPTURE (F1)", None))
    # retranslateUi

    def changeExposureLength(self):
        self.ExposureTime = self.spinBox.value()
    def setManual(self):
        self.manual = not self.manual
        if self.manual:
            self.spinBox.setEnabled(False)
        else:
            self.spinBox.setEnabled(True)
    
    def map_key(self, b, l):
        k  = keyboard.read_key()
        l.setText(str(k))
        self.pushButton_2.setText("START CAPTURE" +'\n'+"(" + str(k) + ")")
        keyboard.unhook_all()
        self.key = str(k)
        thread = Thread(target = self.bindKey)
        thread.start()

    def bindKey(self):
        time.sleep(0.5)
        keyboard.on_release_key(self.key, self.setupPicture)     
    
    def setWholeScreenCapture(self):
        self.CaptureWholeScreen = not self.CaptureWholeScreen
        if self.CaptureWholeScreen:
            self.comboBox.setEnabled(False)
        else:
            self.comboBox.setEnabled(True)
    
    def setVideoSave(self):
        self.saveVideo = not self.saveVideo
    
    def refreshComboBox(self):
        self.comboBox.clear()
        for x in pyautogui.getAllWindows():
            if(x.title != "" and x.width > 0 and x.height > 0):
                self.comboBox.addItem(str(x.title))
    
    def selectionchange(self,i):
      self.CaptureWindow = self.comboBox.currentText()
      self.CaptureWindowObject = pyautogui.getWindowsWithTitle(self.CaptureWindow)[0]
    
    def setCropTop(self):
        self.cropTop = not self.cropTop

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
        timeValue = 1000
        if not self.manual:
            if(self.ExposureTime is not None):
                timeValue = self.ExposureTime
            else:
                timeValue = 5


        self.final_pic_max_eighty = None
        self.final_pic_min_eighty = None
        self.final_pic_true_average = None
        print("about to start capture")
        if(self.radioButton_2.isChecked() == True):
            print("starting capture on high quality mode")
            print("exposure time will be " + str(timeValue))
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
                if not (self.CaptureWholeScreen): 
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
                if(self.cropTop):
                    monitor["top"] += 31
                    monitor["height"] -= 31
                while time.time() - start < timeValue :
                    if(keyboard.is_pressed(self.key)):
                        break
                    sct_img = sct.grab(monitor)
                    images.append(sct_img)
                playsound('assets/stop.mp3')
                totalTime = time.time() - start

                time.sleep(1)
                self.event.clear()
            
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
            print("exposure time will be " + str(timeValue))
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

                if not (self.CaptureWholeScreen): 
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
                if(self.cropTop):
                    monitor["top"] += 31
                    monitor["height"] -= 31
                while time.time() - start < timeValue :
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
            totalTime = time.time() - start

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
        print("exposure took " + str(totalTime) + " seconds")
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
            if(self.radioButton_2.isChecked() == True):
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
    gallery = MainWindow()
    gallery.setupUi(gallery)
    gallery.show()
    sys.exit(appExec())
    
