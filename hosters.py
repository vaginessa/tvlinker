#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from qtpy.QtCore import QTimer, QUrl, Qt, Signal as pyqtSignal, Slot as pyqtSlot
from qtpy.QtGui import QCloseEvent, QDesktopServices, QIcon, QPixmap
from qtpy.QtWidgets import (QBoxLayout, QButtonGroup, QDialog, QFrame, QGroupBox, QHBoxLayout, QLabel, QLayout,
                             QProgressBar, QPushButton, QSizePolicy, QSpacerItem, QStyleFactory, QVBoxLayout, qApp)


class HosterLinks(QDialog):
    downloadLink = pyqtSignal(str)
    copyLink = pyqtSignal(str)

    def __init__(self, parent, title=None, f=Qt.WindowCloseButtonHint):
        super(HosterLinks, self).__init__(parent, f)
        self.parent = parent
        self.title = title
        self.setWindowModality(Qt.ApplicationModal)
        self.hosters = []
        self.layout = QVBoxLayout(spacing=0)
        self.setLayout(self.layout)
        self.copy_icon = QIcon(self.parent.get_path('images/copy_icon.png'))
        self.open_icon = QIcon(self.parent.get_path('images/open_icon.png'))
        self.download_icon = QIcon(self.parent.get_path('images/download_icon.png'))
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.copy_group = QButtonGroup(exclusive=False)
        self.copy_group.buttonClicked[int].connect(self.copy_link)
        self.open_group = QButtonGroup(exclusive=False)
        self.open_group.buttonClicked[int].connect(self.open_link)
        self.download_group = QButtonGroup(exclusive=False)
        self.download_group.buttonClicked[int].connect(self.download_link)
        self.setWindowTitle('Hoster Links')
        busy_label = QLabel('Retrieving hoster links...', alignment=Qt.AlignCenter)
        busy_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        busy_indicator = QProgressBar(parent=self, minimum=0, maximum=0)
        if sys.platform.startswith('linux'):
            busy_indicator.setStyle(QStyleFactory.create('Fusion'))
        self.layout.addWidget(busy_label)
        self.layout.addSpacerItem(QSpacerItem(1, 10))
        self.layout.addWidget(busy_indicator)
        self.setMinimumWidth(485)

    def clear_layout(self, layout: QBoxLayout = None) -> None:
        if layout is None:
            layout = self.layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

    def show_hosters(self, hosters: list) -> None:
        self.hosters = hosters
        self.hide()
        self.clear_layout()
        self.setMinimumWidth(650)
        if self.title is not None:
            title_label = QLabel(self.title, alignment=Qt.AlignCenter, objectName='heading')
            title_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
            self.layout.addWidget(title_label)
        index = 0
        for hoster in hosters:
            hoster_logo = QLabel(pixmap=QPixmap(self.parent.get_path('images/hoster_%s' % QUrl(hoster[0]).fileName())),
                                 toolTip=hoster[1])
            hoster_logo.setMinimumWidth(185)
            hoster_logo.setAlignment(Qt.AlignCenter)
            copy_btn = QPushButton(self, icon=self.copy_icon, text=' COPY', toolTip='Copy to clipboard', flat=False,
                                   cursor=Qt.PointingHandCursor)
            copy_btn.setFixedSize(90, 30)
            self.copy_group.addButton(copy_btn, index)
            open_btn = QPushButton(self, icon=self.open_icon, text=' OPEN', toolTip='Open in browser', flat=False,
                                   cursor=Qt.PointingHandCursor)
            open_btn.setFixedSize(90, 30)
            self.open_group.addButton(open_btn, index)
            download_btn = QPushButton(self, icon=self.download_icon, text=' DOWNLOAD', toolTip='Download link',
                                       flat=False, cursor=Qt.PointingHandCursor)
            download_btn.setFixedSize(120, 30)
            self.download_group.addButton(download_btn, index)
            layout = QHBoxLayout(spacing=10)
            layout.addWidget(hoster_logo)
            layout.addWidget(copy_btn, Qt.AlignRight)
            layout.addWidget(open_btn, Qt.AlignRight)
            layout.addWidget(download_btn, Qt.AlignRight)
            groupbox = QGroupBox(self)
            groupbox.setLayout(layout)
            self.layout.addWidget(groupbox)
            index += 1
        qApp.restoreOverrideCursor()
        QTimer.singleShot(800, self.updateGeometry)
        self.show()

    @pyqtSlot(int)
    def copy_link(self, button_id: int) -> None:
        self.copyLink.emit(self.hosters[button_id][1])

    @pyqtSlot(int)
    def open_link(self, button_id: int) -> None:
        QDesktopServices.openUrl(QUrl(self.hosters[button_id][1]))
        self.close()

    @pyqtSlot(int)
    def download_link(self, button_id: int) -> None:
        self.downloadLink.emit(self.hosters[button_id][1])

    def closeEvent(self, event: QCloseEvent) -> None:
        self.deleteLater()
        qApp.restoreOverrideCursor()
        super(QDialog, self).closeEvent(event)
