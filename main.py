#coding = 'utf-8'

import sys
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QApplication, QMainWindow,QFileDialog,QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from diffusers import DiffusionPipeline
from PIL import Image

import Ui_interfaceUi
import Ui_loginui

import requests

user_now = ''
 
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# 


class ImageGenerationThread(QThread):
    image_generated = pyqtSignal(QPixmap)

   
    def __init__(self, description):
        super().__init__()
        self.description = description

    def run(self):
        # 调用Stable Diffusion模型生成图像,下载
        # model_id = "runwayml/stable-diffusion-v1-5"
        # pipeline = DiffusionPipeline.from_pretrained(model_id, cache_dir="model")

        pipeline = DiffusionPipeline.from_pretrained(r"model\models--runwayml--stable-diffusion-v1-5\snapshots\1d0c4ebf6ff58a5caecab40fa1406526bca4b5b9")

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
        """将 PIL 图像转换为 QPixmap"""
        if img.mode == "RGB":
            r, g, b = img.split()
            img = Image.merge("RGB", (r, g, b))
            img = img.convert("RGBA")  # 转换为 RGBA
        elif img.mode == "RGBA":
            r, g, b, a = img.split()
            img = Image.merge("RGBA", (r, g, b, a))
        elif img.mode == "L":
            img = img.convert("RGBA")  # 灰度图像转换为 RGBA

        # PIL 图像转换为 QImage
        data = img.tobytes("raw", "RGBA")
        qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap
    
    


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(10)
        self.shadow.setYOffset(10)
        self.shadow.setColor(QColor(0, 0, 0, 110))
        self.setGraphicsEffect(self.shadow)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = Ui_loginui.Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda:buttonClicked(self.ui))
        self.ui.pushButton_Register.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_Login.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentIndex(1))

        # 点击pushButton_L_sure进入MainWindow
        self.ui.pushButton_L_sure.clicked.connect(self.Login_in)
                                               
        self.show()
    
    def Login_in(self):
        # 获取用户名和密码
        username = self.ui.lineEdit_L_account.text()
        password = self.ui.lineEdit_L_password.text()
        # 进行登录验证
        if username == "admin" and password == "123456":
            self.w = MainWindow()
            
            self.close()
        else:
            
            self.ui.lineEdit_L_account.clear()
            self.ui.lineEdit_L_password.clear()
            self.ui.lineEdit_L_account.setFocus()

    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = Ui_interfaceUi.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.on_generate_clicked)
        self.ui.pushButton_logout.clicked.connect(self.logout)
        self.ui.pushButton_3.clicked.connect(self.download_image)
        self.fetch_data()
                                               
        self.show()

        
    
    def logout(self):
        global user_now
        self.close()
        self.login = LoginWindow()
        user_now = ""
    
    def on_generate_clicked(self):
        description = self.ui.textEdit.toPlainText()
        self.thread = ImageGenerationThread(description)
        self.thread.image_generated.connect(self.display_image)
        self.thread.start()

    def fetch_data(self):
        url = 'http://127.0.0.1:8188/object_info'  # 示例 API
        response = requests.get(url)
        print(response)
        self.ui.label.setText(response.text)

    def display_image(self, qimage):
        pixmap = qimage.scaled(self.ui.label.width(), self.ui.label.height(), Qt.KeepAspectRatio)
        self.ui.label.setPixmap(pixmap)

    # 把生成的qimage图片下载到本地
    def download_image(self):
        # 在您的类或函数中使用文件对话框
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图像", "", "图像文件 (*.png *.jpg *.jpeg)")
        if file_path:
            self.ui.label.pixmap().save(file_path)
            QMessageBox.information(self, "Success", "图像保存成功!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LoginWindow()

    sys.exit(app.exec_())
