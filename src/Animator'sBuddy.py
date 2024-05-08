import maya.cmds as mc
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog
from PySide2.QtGui import QColor, QPainter, QBrush

class KeyFrameManager:
    
    def setFrame(self):
        mc.setKeyframe()

    def setKeyFrameColors(self, color):
        mc.displayRGBColor("timeControlKey",color.redF(), color.greenF(), color.blueF())

    def setInbetweenColors(self, color:QColor):
        mc.displayRGBColor("timeControlTickDrawSpecial",color.redF(), color.greenF(), color.blueF())
        
    #def clear_selection(self):
        #mc.selectKey(clear=True)

    def SetCurrentKeyToSpecial(self):
        currentFame = mc.currentTime(q=True)
        mc.selectKey(cl=True)
        mc.keyframe(tds=True, time=(currentFame, currentFame))

class ColorPicker(QWidget):
    onColorChanged = Signal(QColor) # this adds a built in class member called onColorChanged.
    def __init__(self, width = 80, height = 20):
        super().__init__()
        self.setFixedSize(width, height)
        self.color = QColor()

    def mousePressEvent(self, event):
        color = QColorDialog().getColor(self.color) 
        self.color = color
        self.onColorChanged.emit(self.color)
        self.update()#update the widget

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0,0,self.width(), self.height())

class AnimBuddyUI(QWidget):
    def __init__(self):
        self.keyframemanager = KeyFrameManager()
        super().__init__() # needed to call if you are inheriting from a parent class
        self.setWindowTitle("AnimBuddy V1.0") # set the title of the window 
        self.masterLayout = QVBoxLayout() # creates a vertical layout         
        self.setLayout(self.masterLayout)

        self.materialLayout = QHBoxLayout()#material layout is horizontal
        self.masterLayout.addLayout(self.materialLayout)
        keyFramecolorPicker = ColorPicker()
        keyFramecolorPicker.onColorChanged.connect(self.keyframemanager.setKeyFrameColors)
        self.materialLayout.addWidget(keyFramecolorPicker)

        setKeyFrame = QPushButton("Set Key Frame")
        setKeyFrame.clicked.connect(self.setKeyFrameBtnClicked)
        self.materialLayout.addWidget(setKeyFrame)

        self.materialLayout = QHBoxLayout()#material layout is horizontal
        self.masterLayout.addLayout(self.materialLayout)
        inbetweenColorPicker = ColorPicker()
        inbetweenColorPicker.onColorChanged.connect(self.keyframemanager.setInbetweenColors)
        self.materialLayout.addWidget(inbetweenColorPicker)

        setInbetweenFrame = QPushButton("Set Inbetween")
        setInbetweenFrame.clicked.connect(self.setInbetweenFrameBtnClicked)
        self.materialLayout.addWidget(setInbetweenFrame)

    def setKeyFrameBtnClicked(self):
        self.keyframemanager.setFrame()
        self.keyframemanager.setKeyFrameColors(self.keyframemanager.color)

    def setInbetweenFrameBtnClicked(self):
        self.keyframemanager.setFrame()
        self.keyframemanager.SetCurrentKeyToSpecial()

animBuddyUI = AnimBuddyUI()
animBuddyUI.show()