import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import win32clipboard
from io import BytesIO
from PIL import Image
import pytesseract

# Tesseract 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageTextExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Windows 클립보드 이미지 텍스트 추출기')
        self.setGeometry(100, 100, 600, 500)
        
        layout = QVBoxLayout()
        
        self.captureBtn = QPushButton('클립보드에서 이미지 가져오기')
        self.captureBtn.clicked.connect(self.getClipboardImage)
        layout.addWidget(self.captureBtn)
        
        self.imageLabel = QLabel('캡처된 이미지가 여기에 표시됩니다.')
        self.imageLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.imageLabel)
        
        self.extractBtn = QPushButton('텍스트 추출')
        self.extractBtn.clicked.connect(self.extractText)
        layout.addWidget(self.extractBtn)
        
        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)
        
        self.setLayout(layout)
        
    def getClipboardImage(self):
        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                image = Image.open(BytesIO(data[14:]))  # Skip the BITMAPINFO header
                self.displayImage(image)
                self.current_image = image
            else:
                self.imageLabel.setText('클립보드에 이미지가 없습니다.')
        finally:
            win32clipboard.CloseClipboard()
    
    def displayImage(self, image):
        qimage = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB32)
        pixmap = QPixmap.fromImage(qimage)
        self.imageLabel.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio))
    
    def extractText(self):
        if hasattr(self, 'current_image'):
            text = pytesseract.image_to_string(self.current_image, lang='kor+eng')
            self.textEdit.setText(text)
        else:
            self.textEdit.setText('먼저 이미지를 가져와주세요.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageTextExtractor()
    ex.show()
    sys.exit(app.exec_())