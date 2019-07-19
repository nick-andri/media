import sys
from PySide2.QtWidgets import QApplication, QMainWindow,QFileDialog,QListWidgetItem
from ui_media import Ui_MainWindow
from PySide2.QtMultimedia import  QMediaPlayer,QMediaContent
from PySide2.QtCore import QUrl,QTime,QFileInfo





class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Connection du decodeur et lecteur
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.ecranWidget)

        #chargement du media
        mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        self.mediaPlayer.setMedia(mediaContent)

       #connect push boutons
        self.ui.pbLecture.clicked.connect(self.lectureClicked)
        self.ui.pbPause.clicked.connect(self.pauseClicked)
        self.ui.pbStop.clicked.connect(self.stopClicked)
        self.ui.dialVolume.valueChanged.connect(self.volControl)
        self.ui.nivoVolume.setText(str(self.ui.dialVolume.value()))
        self.ui.nivoVolume.setText('{}%'.format(str(self.ui.dialVolume.value())))
        self.mediaPlayer.durationChanged.connect(self.affTemp)
        self.mediaPlayer.positionChanged.connect(self.avanceTemp)
        self.ui.barreLect.valueChanged.connect(self.avanceSlider)
        self.ui.pbPlus.clicked.connect(self.pbPlusCtrl)
        self.ui.pbMoins.clicked.connect(self.pbMoinsCtrl)
        self.ui.listWidget.itemDoubleClicked.connect(self.mediaSelected)
        self.ui.pbSuivant.clicked.connect(self.suivantBouton)
        self.ui.pbPrecedent.clicked.connect(self.precedentBouton)



    #fonction qui gere les click
    def lectureClicked(self):
        self.mediaPlayer.play()

    def pauseClicked(self):

      if  self.mediaPlayer.state() == QMediaPlayer.PausedState :
          self.mediaPlayer.play()
      else :
        self.mediaPlayer.pause()

    def stopClicked(self):
        self.mediaPlayer.stop()

    def volControl(self):
        self.mediaPlayer.setVolume(self.ui.dialVolume.value())
        self.ui.nivoVolume.setText('{}%'.format(str(self.ui.dialVolume.value())))

    def affTemp(self):
        tempTotl = QTime(0, 0, 0)
        tempTotl = tempTotl.addMSecs(self.mediaPlayer.duration() - self.mediaPlayer.position())

        posTemp = QTime(0, 0, 0)
        posTemp = posTemp.addMSecs((self.mediaPlayer.position()))

        self.ui.tempRestant.setText("- {}".format(tempTotl.toString("HH:mm:ss")))
        self.ui.tempLecture.setText(posTemp.toString("HH:mm:ss"))
        self.ui.barreLect.setRange(0,self.mediaPlayer.duration())

    def avanceTemp(self):
        tempTotl= QTime(0,0,0)
        tempTotl = tempTotl.addMSecs(self.mediaPlayer.duration()-self.mediaPlayer.position())


        posTemp= QTime(0,0,0)
        posTemp = posTemp.addMSecs((self.mediaPlayer.position()))

        self.ui.tempRestant.setText("-{}".format(tempTotl.toString("HH:mm:ss")))
        self.ui.tempLecture.setText(posTemp.toString("HH:mm:ss"))
        self.ui.barreLect.setSliderPosition(self.mediaPlayer.position())

    def avanceSlider(self):
        self.mediaPlayer.setPosition(self.ui.barreLect.sliderPosition())

    def pbPlusCtrl(self):

        fileName = QFileDialog.getOpenFileName(self,"choix film","/home","Film(*.avi *.mp4)")
        fInfo = QFileInfo(fileName[0])
        fShortName = fInfo.baseName()
        item = QListWidgetItem(fShortName)
        item.setToolTip(fileName[0])
        self.ui.listWidget.addItem(item)
        print(item.toolTip().title())

    def pbMoinsCtrl(self):
        rowItem= self.ui.listWidget.currentRow()
        if rowItem != -1:
            self.ui.listWidget.takeItem(rowItem)

    def mediaSelected(self):
        currentItem = self.ui.listWidget.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile(currentItem.toolTip()))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()

    def suivantBouton(self):

        if self.ui.listWidget.count() != 0 :
            self.ui.listWidget.setCurrentRow((self.ui.listWidget.currentRow()+1) % self.ui.listWidget.count() )
            mediaContent = QMediaContent(QUrl.fromLocalFile(self.ui.listWidget.currentItem().toolTip()))
            self.mediaPlayer.setMedia(mediaContent)
            self.lectureClicked()

    def precedentBouton(self):

        if self.ui.listWidget.count() != 0 :
            self.ui.listWidget.setCurrentRow((self.ui.listWidget.currentRow()-1) % self.ui.listWidget.count() )
            mediaContent = QMediaContent(QUrl.fromLocalFile(self.ui.listWidget.currentItem().toolTip()))
            self.mediaPlayer.setMedia(mediaContent)
            self.lectureClicked()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())