import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel
from PyQt5.QtGui import QPalette, QBrush, QPixmap

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI() #介面繪製交給InitUi方法
        
    def initUI(self):
        
        pix = QPixmap('background.jpg')

        lb1 = QLabel(self)
        lb1.setGeometry(0,0,300,200)
        lb1.setStyleSheet("border: 2px solid red")
        lb1.setPixmap(pix)

        
        #設定視窗的位置和大小
        self.setGeometry(300, 300, 600, 600)  
        #設定視窗的標題
        self.setWindowTitle('Example')
        
        
        #顯示視窗
        self.show()
        
        
if __name__ == '__main__':
    #建立應用程式和物件
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI()
    sys.exit(app.exec_()) 