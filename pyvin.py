import pylast
import time
import os
#import json
import ast
import urllib.request
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest

class Ui_Dialog(object):
    def __init__(self):
        with open('dict.txt') as f: 
            data = f.read() 
        self.albumDict = ast.literal_eval(data)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(557, 367)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(90, 10, 151, 23))
        self.comboBox.setObjectName("comboBox")

        for key, value in self.albumDict.items():
            self.comboBox.addItem(key) 
        #label 2 (Currently srobbling)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 10, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Not scrobbling anything right now")
        #label 3
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(340, 80, 125, 21))
        self.label_3.setObjectName("label_3")
        #label 5 (name and artist)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(260, 100, 281, 61))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        #label 1 (Picture)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 60, 221, 211))
        self.label.setText("")
                #1
        self.label.setScaledContents(True)
        self.label.setObjectName("label") 
        #label 6  (on etc)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(270, 160, 251, 20))
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")

        
        #label 7        (track number)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(350, 182, 91, 20))
        self.label_7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(250, 10, 41, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start)

        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(250, 220, 291, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def start(self):
        API_KEY = "94e0533e6b7f8d733455fbed379b7543"
        API_SECRET = "db4c15d2158771d31b8540a1e9aa2905"
        username = "temp"
        password_hash = pylast.md5("temp")
        network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
            username=username,
            password_hash=password_hash,
        )
        
        self.label_3.setText("Currently Scrobbling: ") 
        data = self.albumDict.get(self.comboBox.currentText())
        songs = data[0]
        length = data[1]
        albumArtist = self.comboBox.currentText().split(" - ")
        artist = albumArtist[0]
        album = albumArtist[1]
        print(artist, album)
        print(os.path.exists(".covers/"+self.comboBox.currentText()+".jpg"))
        if not os.path.exists(".covers/"+self.comboBox.currentText()+".jpg"):
            try:
                cover = network.get_album(artist, album)
                cover = cover.get_cover_image()
                print(cover)
                abc = '.covers/'+self.comboBox.currentText()+".jpg"
                urllib.request.urlretrieve(cover, abc)
            except:
                print("Error fetching cover") 
        self.label.setPixmap(QtGui.QPixmap(".covers/"+self.comboBox.currentText()+".jpg"))
        print(songs, length, artist, album)
        self.label_6.setText("On " + album)
        x = 0
        z = -1
        for song in songs:
            x += 1
            z += 1
            time2 = length[z]
            seconds = time2.split(":")
            seconds = int(seconds[0])*60 + int(seconds[1])
            a = 0.01 * float(seconds)
            a = a * 1000
            print(song, artist, x)
            self.setSong(song, artist, x, len(songs))
            
            network.update_now_playing(artist=artist, album=album, title=song, duration=a)

            for percent in range(101):
                print(a, percent)
                self.progressBar.setValue(percent)
                QtTest.QTest.qWait(int(a))
            network.scrobble(artist=artist, album=album, title=song, timestamp=int(time.time()))
        self.label_3.setText("No Longer Scrobbling") 
        self.label_2.setText("")
        self.label_5.setText("")
        self.label_6.setText("")
        self.label_7.setText("")


    def setSong(self, song, artist, track, allTrack):
        self.label_5.setText(song + " by " + artist)
        self.label_7.setText(str(track) + "/" + str(allTrack))
        QtGui.QGuiApplication.processEvents()



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PyVin"))
        self.pushButton.setText(_translate("Dialog", "Start"))
        self.label_2.setText(_translate("Dialog", "Album:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


