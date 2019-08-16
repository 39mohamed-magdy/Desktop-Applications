# import pyqt5
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*

import os
from os import path
import sys
import urllib.request
import pafy
import humanize

from main import Ui_MainWindow

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.Handel_Buttons()

    def Handel_UI(self):
        self.setWindowTitle("Py Downloader")
        self.setFixedSize(620, 350)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)
        self.pushButton_13.clicked.connect(self.Download_Youtube_Video)
        self.pushButton_4.clicked.connect(self.Get_Youtube_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_5.clicked.connect(self.Save_Browse)
        self.pushButton_6.clicked.connect(self.Playlist_Download)

    def Handel_Browse(self):
        save_place = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files (*.*)")
        text = str(save_place)
        name = (text[2:].split(',')[0].replace("'", ''))
        self.lineEdit_2.setText(name)

    def Handel_Progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize

        if totalsize > 0:

            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()  # Not Responding

    def Download(self):

        # url --save location -- progress--
        url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        try:

            urllib.request.urlretrieve(url, save_location, self.Handel_Progress)
        except Exception:

            QMessageBox.information(self, "Download Error", "The Download  Faild")
            return
        QMessageBox.information(self, "Download Completed", "The Download Finished")
        self.progressBar.setValue(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

    def Save_Browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_4.setText(save)
        self.lineEdit_5.setText(save)

    def Get_Youtube_Video(self):
        video_link = self.lineEdit_3.text()
        v = pafy.new(video_link)
        st = v.videostreams
        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data = '{} {} {} {}'.format(s.mediatype, s.extension, s.quality, size)
            self.comboBox.addIteam(data)

    def Download_Youtube_Video(self):
        video_link = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()
        v = pafy.new(video_link)
        st = v.videostreams
        quality = self.comboBox.currentIndex()
        down = st[quality].download(filepath=save_location)
        QMessageBox.information(self, "Download Completed", "The Video Download Finished")

    def Playlist_Download(self):
        playlist_url = self.lineEdit_6.text()
        save_location = self.lineEdit_5.text()
        platlist = pafy.get_playlist(playlist_url)
        videos = platlist['items']
        os.chdir(save_location)
        if os.path.exists(str(platlist['title'])):
            os.chdir(str(platlist['title']))
        else:
            os.mkdir(str(platlist['title']))
            os.chdir(str(platlist['title']))

        for video in videos:
            p = video['pafy']
            best = p.getbest(preftype='mp4')
            best.download()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  #infinte loop


if __name__ == '__main__':
    main()
