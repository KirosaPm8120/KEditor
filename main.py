import sys

import requests
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QUrl, QTimer,QPropertyAnimation
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QMainWindow, QDialog, QWidget, QVBoxLayout, QGraphicsOpacityEffect


api = "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"
prompt = ''
model = "openai/gpt-oss-120b:free"
style = 1
theme = 0

class Startup(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setGeometry(0, 0, 1920, 1080)
        self.showFullScreen()



        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)
        self.media_player.setAudioOutput(self.audio_output)

        self.media_player.setVideoOutput(self.video_widget)
        self.setLayout(layout)
        self.media_player.setSource(QUrl.fromLocalFile("Main_1.mp4"))
        self.media_player.play()




class Ui_MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        uic.loadUi("AiEdit.ui", self)
        self.setWindowIcon(QIcon('k_redactor_logo.png'))

        self.showPopUp()

        self.sound = QMediaPlayer()
        self.audio_out = QAudioOutput()
        self.sound.setAudioOutput(self.audio_out)

        self.StyleEdit.clicked.connect(self.openStyle)
        self.APISettings.clicked.connect(self.openAPI)
        self.ModelSelect.clicked.connect(self.openModel)
        self.AskAIButton.clicked.connect(self.redact)
        self.Edit.clicked.connect(self.edit)
        self.theme.clicked.connect(self.change_theme)

        self.setStyleSheet("""
        QMainWindow {
            background-color: #0f172a;
        }

        QTextEdit {
            background-color: #1e293b;
            color: #e2e8f0;
            border-radius: 12px;
            padding: 10px;
            font-size: 14px;
        }

        QLineEdit {
            background-color: #1e293b;
            color: #e2e8f0;
            border-radius: 10px;
            padding: 8px;
        }

        QPushButton {
            background-color: #22c55e;
            color: white;
            border-radius: 10px;
            padding: 8px 16px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #16a34a;
        }

        QPushButton:pressed {
            background-color: #15803d;
        }

        QLabel {
            color: #cbd5f5;
            font-size: 14px;
        }
        """)

    def showPopUp(self):
        self.splash = Startup()
        self.splash.show()

        QTimer.singleShot(1,self.playsound)
        QTimer.singleShot(3000,self.closepopup)

    def playsound(self):
        self.sound.setSource(QUrl.fromLocalFile("Sound.mp3"))
        self.sound.play()

    def closepopup(self):
        self.splash.close()
        self.show()
        self.fade_in()

    def openStyle (self):
        style_dialog = StyleDialog()
        style_dialog.exec()

    def openAPI (self):
        api_dialog = ApiDialog()
        api_dialog.exec()

    def openModel (self):
        model_dialog = ModelDialog()
        model_dialog.exec()


    def redact (self):
        global style
        global model
        print(model)

        self.UserPrompt = self.AskAILine.text().strip()
        self.UserText = self.Text.toPlainText()
        print(self.UserText)
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",  # ← правильный эндпоинт
            headers={
                "Authorization": f"Bearer {api}",  # ← обязательно Bearer
                "Content-Type": "application/json",
            },
            json={
                "model":f"{model}",
                "messages": [  # ← messages вместо input
                    {"role": "user", "content": f"Ты — помощник по редактированию текста. Выполни строго то, что просит пользователь в запросе({self.UserPrompt}), применив это к тексту текст({self.UserText}). Запрещено добавлять комментарии, пояснения, списки изменений или любой другой текст. Выведи только результат редактирования."}
                ],
                "max_tokens": 9000,  # ← max_tokens, а не max_output_tokens
            }
        )

        if response.status_code == 200:
            result = response.json()
            otvet = result['choices'][0]['message']['content']
            print(result['choices'][0]['message']['content'])
            self.Text.clear()
            self.Text.append(otvet)
        else:
            print(response.json())


    def edit(self):
        global style
        global model
        print(style)
        if style == 1:
            self.UserText = self.Text.toPlainText()
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",  # ← правильный эндпоинт
                headers={
                    "Authorization": f"Bearer {api}",  # ← обязательно Bearer
                    "Content-Type": "application/json",
                },
                json={
                    "model": f"{model}",
                    "messages": [  # ← messages вместо input
                        {"role": "user",
                         "content": f"Ты — редактор деловой документации. Перепиши текст указанный в скобках ({self.UserText}) в строгом официально-деловом стиле. Требования: исключи разговорную лексику, метафоры, эмоциональные оценки и личные местоимения (где возможно). Используй канцелярские обороты, пассивные конструкции, чёткую логику и нейтральный тон. Выведи только готовый отредактированный текст без кавычек, пояснений и комментариев."}
                    ],
                    "max_tokens": 9000,  # ← max_tokens, а не max_output_tokens
                }
            )

        elif style == 2:
            self.UserText = self.Text.toPlainText()
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",  # ← правильный эндпоинт
                headers={
                    "Authorization": f"Bearer {api}",  # ← обязательно Bearer
                    "Content-Type": "application/json",
                },
                json={
                    "model": f"{model}",
                    "messages": [  # ← messages вместо input
                        {"role": "user",
                         "content": f"Ты — редактор научных текстов. Перепиши текст({self.UserText}) в научном стиле. Требования: используй терминологию по предмету, безличные или пассивные конструкции, логическую последовательность (тезис — аргумент — вывод), избегай разговорных выражений, метафор, эмоциональной окраски и местоимений первого/второго лица. Сохрани точность исходного смысла. Выведи только готовый отредактированный текст без кавычек, пояснений и комментариев."}
                    ],
                    "max_tokens": 9000,  # ← max_tokens, а не max_output_tokens
                }
            )

        elif style == 3:
            self.UserText = self.Text.toPlainText()
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",  # ← правильный эндпоинт
                headers={
                    "Authorization": f"Bearer {api}",  # ← обязательно Bearer
                    "Content-Type": "application/json",
                },
                json={
                    "model": f"{model}",
                    "messages": [  # ← messages вместо input
                        {"role": "user",
                         "content": f"Ты — редактор текстов в разговорном стиле. Перепиши текст({self.UserText}) так, чтобы он звучал естественно, живо и неформально, как в устной беседе. Требования: используй простые и короткие предложения, разговорную лексику, допустимы междометия, обращения, сокращения (типа «не», «вот», «ну», «давай»), личные местоимения («я», «ты», «мы»), эмоциональные оттенки. Избегай канцеляризмов, сложных конструкций и абстрактных терминов. Сохрани исходный смысл. Выведи только готовый отредактированный текст без кавычек, пояснений и комментариев."}
                    ],
                    "max_tokens": 9000,  # ← max_tokens, а не max_output_tokens
                }
            )

        if response.status_code == 200:
            result = response.json()
            otvet = result['choices'][0]['message']['content']
            print(result['choices'][0]['message']['content'])
            self.Text.clear()
            self.Text.append(otvet)
        else:
            print(response.json())



    def fade_in (self):
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)

        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def change_theme(self):
        global theme
        if theme == 0:
            self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }

            QTextEdit {
                background-color: #1e293b;
                color: #e2e8f0;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }

            QLineEdit {
                background-color: #1e293b;
                color: #e2e8f0;
                border-radius: 10px;
                padding: 8px;
            }

            QPushButton {
                background-color: #22c55e;
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #16a34a;
            }

            QPushButton:pressed {
                background-color: #15803d;
            }

            QLabel {
                color: #cbd5f5;
                font-size: 14px;
            }
            """)
            theme = 1
        else:
            self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }

            QTextEdit {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }

            QLineEdit {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton:pressed {
                background-color: #1e40af;
            }

            QLabel {
                color: #334155;
                font-size: 14px;
            }

            QFrame {
                background-color: #ffffff;
                border-radius: 14px;
                border: 1px solid #e2e8f0;
            }
            """)

            theme = 0

class ModelDialog(QDialog):
    def __init__(self):
        super().__init__()


        global model
        model = "openai/gpt-oss-120b:free"
        uic.loadUi("ModelSelect.ui", self)
        self.Qwen.clicked.connect(self.set_model_qwen)
        self.Llama.clicked.connect(self.set_model_llama)
        self.GPT.clicked.connect(self.set_model_GPT)

    def set_model_qwen(self):
        global model
        model = "openai/gpt-oss-120b:free"
        print(model)

    def set_model_llama(self):
        global model
        model = "openrouter/elephant-alpha"
        print(model)

    def set_model_GPT(self):
        global model
        model = "nvidia/nemotron-3-super-120b-a12b:free"
        print(model)

class ApiDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("APIKey.ui",self)

        self.Key.textChanged.connect(self.setApi)

    def setApi(self):
        global api
        api = self.Key.text()


class StyleDialog(QDialog):
    def __init__(self):
        global style
        super().__init__()
        uic.loadUi("StyleSelect.ui", self)
        self.Official.clicked.connect(self.set_style_off)
        self.Science.clicked.connect(self.set_style_sci)
        self.Simple.clicked.connect(self.set_style_simple)

    def set_style_off(self):
        global style
        style = 1
        print(style)
    def set_style_sci(self):
        global style
        style = 2
        print(style)
    def set_style_simple(self):
        global style
        style = 3
        print(style)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ui_MainWindow()
    sys.exit(app.exec())