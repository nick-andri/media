import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_media import Ui_MainWindow
from PySide2.QtMultimedia import  QMediaPlayer,QMediaContent
from PySide2.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Connection du decodeur et lecteur
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.ecranWidget)

       #connect push boutons
        self.ui.pbLecture.clicked.connect(self.lectureClicked)
        self.ui.pbPause.clicked.connect(self.pauseClicked)
        self.ui.pbStop.clicked.connect(self.stopClicked)
        self.ui.dialVolume.valueChanged.connect(self.volControl)
        self.ui.nivoVolume.setText(str(self.ui.dialVolume.value()))
        self.ui.nivoVolume.setText('{}%'.format(str(self.ui.dialVolume.value())))
        # self.ui.pbLecture.clicked.connect(self.bLectContrl)
        # self.ui.pbLecture.clicked.connect(self.bLectContrl)


        mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        self.mediaPlayer.setMedia(mediaContent)

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



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())