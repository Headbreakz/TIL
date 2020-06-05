from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QPushButton, QStyle

videoWidget = QVideoWidget()

self.playButton = QPushButton()
self.playButton.setEnabled(False)
self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
self.playButton.clicked.connect(self.play)