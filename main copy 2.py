import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from transformers import AutoModelForCausalLM, AutoTokenizer
from diffusers import DiffusionPipeline
from PIL import Image
import numpy as np

import Ui_interfaceUi
import Ui_loginui

user_now = ''

class ImageGenerationThread(QThread):
    image_generated = pyqtSignal(QPixmap)

   
    def __init__(self, description):
        super().__init__()
        self.description = description

    def run(self):
        pipeline = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
           # 这里假设 pipeline 以正确配置
        pipeline.to("cuda")  # 或 "cpu"，根据您的设置

        # 生成图像
        generated_images = pipeline(self.description).images
        generated_image = generated_images[0]  # 获取第一张图像

        # 将 PIL 图像转换为 QImage
        qimage = self.pil2pixmap(generated_image)
        self.image_generated.emit(qimage)

    @staticmethod
    def pil2pixmap(img):
        """ 将 PIL 图像转换为 QPixmap """
        if img.mode == "RGB":
            r, g, b = img.split()
            img = Image.merge("RGB", (b, g, r))
        elif img.mode == "RGBA":
            r, g, b, a = img.split()
            img = Image.merge("RGBA", (b, g, r, a))
        elif img.mode == "L":
            img = img.convert("RGBA")

        # PIL 图像转换为 QImage
        im2 = img.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
        return QPixmap.fromImage(qim)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.description_input = QTextEdit(self)
        self.description_input.setGeometry(10, 10, 280, 100)

        self.generate_button = QPushButton('Generate Image', self)
        self.generate_button.setGeometry(10, 120, 280, 40)
        self.generate_button.clicked.connect(self.on_generate_clicked)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 170, 280, 280)

    def on_generate_clicked(self):
        description = self.description_input.toPlainText()
        self.thread = ImageGenerationThread(description)
        self.thread.image_generated.connect(self.display_image)
        self.thread.start()

    def display_image(self, qimage):
        pixmap = qimage.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
