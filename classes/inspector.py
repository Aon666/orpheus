from qtpy import uic
from qtpy.QtWidgets import QWidget
from qtpy.QtMultimedia import QMediaPlayer, QAudioOutput
from qtpy.QtCore import QUrl

class Inspector(QWidget):
    player = QMediaPlayer()
    audio_output = QAudioOutput()

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi("ui/inspector.ui", self)
        self.player.setAudioOutput(self.audio_output)
        self.PlayButton.clicked.connect(self.play_button_action)

    def SetUp(self, audioPath, title):
        self.player.setSource(QUrl.fromLocalFile(str(audioPath)))
        self.audio_output.setVolume(1.0)
        self.AudioTitleLabel.setText(title)

    def play_button_action(self):
        if(self.player.playbackState == QMediaPlayer.PlaybackState):
            self.player.stop()
        else:
            self.player.play()

    