import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QDialog, QTextEdit
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QMouseEvent, QScreen,QImage,QPainterPath
from PyQt5.QtCore import Qt, QEvent, QTimer
import pyautogui
from pynput import mouse
import time
#подключение библиотек для работы программы
#Создание основного окна
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setFixedSize(400, 200)
        self.setWindowTitle('Обведи, не отрывая пера')

        # Создаем кнопки
        self.easy = QPushButton('Легкий уровень', self)
        self.easy.move(155, 20)
        self.easy.clicked.connect(self.open_easy)

        self.medium = QPushButton('Средний уровень', self)
        self.medium.move(150, 60)
        self.medium.clicked.connect(self.open_medium)

        self.hard = QPushButton('Сложный уровень', self)
        self.hard.move(150, 100)
        self.hard.clicked.connect(self.open_hard)

        self.rule = QPushButton('Правила', self)
        self.rule.move(160, 140)
        self.rule.clicked.connect(self.open_rule)

    #функция открытия окон, подключаемые к кнопкам
    def open_easy(self):
        self.easy_game = EasyWindow()
        self.easy_game.show()

    def open_medium(self):
        self.medium_game = medium_window()
        self.medium_game.show()

    def open_hard(self):
        self.hard_game = hard_window()
        self.hard_game.show()

    def open_rule(self):
        self.rule_game = Rule_okno()
        self.rule_game.show()

#Окно с отображением правил
class Rule_okno(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 550, 150)
        self.setWindowTitle('Правила')

        # Создаем QTextEdit виджет
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 550, 150)

        # Устанавливаем текст в QTextEdit виджет
        self.text_edit.setText('Правила игры таковы:\n'
                               '1) запустив игру, выберете уровень сложности\n'
                               '2) после запуска уровня сложности, в окне будет изображена фигура\n'
                               '3) после этого вам потребуется зажать курсор и провести им по контурам фигуры\n'
                               '4) если вы разожмете кнопку, то игра закончится')


# Окно легкого уровня
class EasyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 400)
        self.setWindowTitle('Легкий уровень')
        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setGeometry(0, 0, self.width(), 50)
        self.message_label.setText("")
        self.startTime = time.time() + 5000
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)
        self.lastPos = None
        self.posMas = []
        self.path = QPainterPath()
        self.expectedPath = QPainterPath()
        self.gameOver = False
    #Правила работы для окна Легкоко уровня

    def mousePressEvent(self, event):
        if not self.gameOver:
            self.startTime = time.time()
            if event.button() == Qt.RightButton:
                self.message_label.setText("Вы проиграли")
                self.setFixedSize(self.size())
                print("Вы зажали правую кнопку мыши")
                self.gameOver = True
                self.timer = QTimer()
                self.timer.timeout.connect(self.close)
                self.timer.start(5000)
                event.ignore()
                #проверка для зажатия ПКМ

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            proverka = 0#элемент лля проверки
            x, y = event.pos().x(), event.pos().y()#Запоминание координат курсора
            if (x >= 195 and x <= 205) and (y >= 100 and y <= 105):
                proverka += 1
            elif (x >= 195 and x <= 205) and (y >= 95 and y <= 105):
                proverka += 1
            elif (x >= 495 and x <= 505) and (y >= 95 and y <= 105):
                proverka += 1
                #проверка прохождения курсором границ круга
            if not self.gameOver:
                print("Левая кнопка мыши была отпущена")

                if len(self.posMas) > 500 and time.time() - self.startTime > 7:
                    #Проверка для
                    if proverka >= 0:
                                self.message_label.setText("Вы выиграли")
                                self.gameOver = True
                                self.timer = QTimer()
                                self.timer.timeout.connect(self.close)
                                self.timer.start(5000)
                                event.ignore()#Выод победы и закрытие окна

                else:
                        self.message_label.setText("Вы проиграли")
                        self.gameOver = True
                        self.timer = QTimer()
                        self.timer.timeout.connect(self.close)
                        self.timer.start(5000)
                        event.ignore()#Вывод поражения и закрытия окна
                check = False

    #Отрисовка линии во время движения ЛКМ
    def mouseMoveEvent(self, event):
        if not self.gameOver:
            if event.buttons() == Qt.LeftButton:
                if self.lastPos is None:
                    self.lastPos = event.pos()
                    self.path.moveTo(self.lastPos)
                else:
                    self.path.lineTo(event.pos())
                    self.lastPos = event.pos()
                self.posMas.append(self.lastPos)
                self.path.addEllipse(event.pos().x(), event.pos().y(), 8, 8)
                self.update()  # Обновляем виджет, чтобы отобразить новое изображение

    #Отрисовка круга
    def paintEvent(self, event):
        super().paintEvent(event)  # Вызываем метод paintEvent() родительского класса
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image)
        pen = QPen(Qt.black, 8, Qt.SolidLine)
        painter.setPen(pen)
        width = self.width()
        height = self.height()
        x = width / 2
        y = height / 2
        #получение данных о размерах окна, для нахождения точки отрисовки
        radius = min(width, height) / 2 - pen.width() / 2
        #print(radius)
        painter.drawEllipse(int(x - radius / 2), int(y - radius / 2), int(2 * radius / 2), int(2 * radius / 2))
        painter.setPen(QPen(Qt.red, 2))
        painter.drawPath(self.path)
        #отрисовка круга
        # Определение координат краев круга
        """left = [x - radius, y]
        top = [x,y - radius]
        right = [x + radius,y]
        bottom = [x,y + radius]
        #print("1:", " ", left, "2:", top, "3:", " ", right, "4: ", " ", bottom)"""
#окно игры среднего уровня
class medium_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Создаем метку с сообщением
        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setGeometry(0, 0, self.width(), 50)
        self.message_label.setText("")
        self.lastPos = None
        self.posMas = []
        self.path = QPainterPath()
        self.expectedPath = QPainterPath()
        self.gameOver = False
        # Устанавливаем обработчик события нажатия кнопки
        self.mousePressEvent = self.mousePressEvent

    def mousePressEvent(self, event):
        if not self.gameOver:
            self.startTime = time.time()
            if event.button() == Qt.RightButton:
                self.message_label.setText("Вы проиграли")
                self.setFixedSize(self.size())
                print("Вы зажали правую кнопку мыши")
                self.gameOver = True
                self.timer = QTimer()
                self.timer.timeout.connect(self.close)
                self.timer.start(5000)
                event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.gameOver:
                print("Левая кнопка мыши была отпущена")
                check = False
                for pos in self.posMas:
                    path = QPainterPath()
                    path.addEllipse(pos.x(), pos.y(), 8, 8)

                    if not path.intersects(self.expectedPath):
                        check = True

                try:
                    path1 = QPainterPath()
                    path2 = QPainterPath()
                    path1.addEllipse(self.posMas[0].x(), self.posMas[0].y(), 8, 8)
                    path2.addEllipse(self.posMas[len(self.posMas) - 1].x(), self.posMas[len(self.posMas) - 1].y(), 8, 8)
                    if not path1.intersects(path2):
                        check = True
                except:
                    pass
                if not check:
                    self.message_label.setText("Вы победили ")
                else:
                    self.message_label.setText("Вы проиграли ")
                self.gameOver = True
                self.setFixedSize(self.size())
                self.timer = QTimer()
                self.timer.timeout.connect(self.close)
                self.timer.start(5000)
    def initUI(self):
        self.setFixedSize(400, 300)
        self.setWindowTitle('Средний уровень')

    def mouseMoveEvent(self, event):
        if not self.gameOver:
            if event.buttons() == Qt.LeftButton:
                if self.lastPos is None:
                    self.lastPos = event.pos()
                    self.path.moveTo(self.lastPos)
                else:
                    self.path.lineTo(event.pos())
                    self.lastPos = event.pos()
                self.posMas.append(self.lastPos)
                self.path.addEllipse(event.pos().x(), event.pos().y(), 8, 8)

                self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Установка параметров рисования границ
        pen = QPen(Qt.black, 6, Qt.SolidLine)
        painter.setPen(pen)

        # Вычисление координат и радиуса круга
        width = self.width()
        height = self.height()
        x = width / 2
        y = height / 2
        radius = min(width, height) / 2 - pen.width() / 2

        # Рисование большой окружности окружности
        painter.drawEllipse(int(x - radius / 2), int(y - radius / 2), int(2 * radius / 2), int(2 * radius / 2))
        # Рисование средней окружности
        painter.drawEllipse(int(x - radius / 4), int(y - radius / 4), int(radius / 2), int (radius / 2))
        #Рисование линии
        painter.drawLine(130, 130, 165, 165)
        painter.setPen(QPen(Qt.red, 2))
        self.expectedPath.moveTo(245,245)
        self.expectedPath.lineTo(195,195)
        self.expectedPath.addEllipse(int(x - radius / 2), int(y - radius / 2), int(2 * radius / 2), int(2 * radius / 2))
        self.expectedPath.addEllipse(int(x - radius / 4), int(y - radius / 4), int(radius / 2), int (radius / 2))
        painter.drawPath(self.path)
#окно игры высокого уровня
class hard_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Создаем метку с сообщением
        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setGeometry(0, 0, self.width(), 50)
        self.message_label.setText("")
        self.lastPos = None
        self.posMas = []
        self.path = QPainterPath()
        self.expectedPath = QPainterPath()
        self.gameOver = False
        # Устанавливаем обработчик события нажатия кнопки
        self.mousePressEvent = self.mousePressEvent

    def mousePressEvent(self, event):
        if not self.gameOver:
            self.startTime = time.time()
            if event.button() == Qt.RightButton:
                self.message_label.setText("Вы проиграли")
                self.setFixedSize(self.size())
                print("Вы зажали правую кнопку мыши")
                self.gameOver = True
                self.timer = QTimer()
                self.timer.timeout.connect(self.close)
                self.timer.start(5000)
                event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.gameOver:
                print("Левая кнопка мыши была отпущена")
                check = False
                for pos in self.posMas:
                    path = QPainterPath()
                    path.addEllipse(pos.x(), pos.y(), 8, 8)

                    if not path.intersects(self.expectedPath):
                        check = True

                try:
                    path1 = QPainterPath()
                    path2 = QPainterPath()
                    path1.addEllipse(self.posMas[0].x(), self.posMas[0].y(), 8, 8)
                    path2.addEllipse(self.posMas[len(self.posMas) - 1].x(), self.posMas[len(self.posMas) - 1].y(), 8, 8)
                    if not path1.intersects(path2):
                        check = True
                except:
                    pass
                if not check:
                    self.message_label.setText("Вы победили ")
                else:
                    self.message_label.setText("Вы проиграли ")
                self.gameOver = True
                self.setFixedSize(self.size())
                self.timer = QTimer()
                self.timer.timeout.connect(self.close)
                self.timer.start(5000)
    def initUI(self):
        self.setFixedSize(600, 600)
        self.setWindowTitle('Сложный уровень')
    def mouseMoveEvent(self, event):
        if not self.gameOver:
            if event.buttons() == Qt.LeftButton:
                if self.lastPos is None:
                    self.lastPos = event.pos()
                    self.path.moveTo(self.lastPos)
                else:
                    self.path.lineTo(event.pos())
                    self.lastPos = event.pos()
                self.posMas.append(self.lastPos)
                self.path.addEllipse(event.pos().x(), event.pos().y(), 8, 8)

                self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Установка параметров рисования границ
        pen = QPen(Qt.black, 8, Qt.SolidLine)
        painter.setPen(pen)

        # Вычисление координат и радиуса круга
        width = self.width()
        height = self.height()
        x = width / 2
        y = height / 2
        radius = min(width, height) / 2 - pen.width() / 2

        # Рисование   большой окружности
        painter.drawEllipse(int(x - radius / 2), int(y - radius / 2), int(2 * radius / 2), int(2 * radius / 2))
        # Рисование средней окружности
        painter.drawEllipse(int(x - radius / 4), int(y - radius / 4), int(radius / 2), int(radius / 2))
        #Рисование малой окружности
        painter.drawEllipse(int(x - radius / 8), int(y - radius / 8), int(radius / 4), int(radius / 4))
        #
        painter.drawRect(50, 50, 400, 400)
        #
        painter.drawRect(50, 50, 100, 100)
        #
        painter.drawRect(100, 50, 400, 100)
        #
        painter.drawLine(245, 245, 195, 195)
        #
        painter.drawLine(245, 245,273, 273)
        self.expectedPath.moveTo(245,245)
        self.expectedPath.addRect(50,50,400,400)
        self.expectedPath.addRect(50,50,100,100)
        self.expectedPath.addRect(100,50,400,100)
        self.expectedPath.moveTo(245,245)
        self.expectedPath.lineTo(195,195)
        self.expectedPath.moveTo(245,245)
        self.expectedPath.lineTo(273,273)
        self.expectedPath.addEllipse(int(x - radius / 2), int(y - radius / 2), int(2 * radius / 2), int(2 * radius / 2))
        self.expectedPath.addEllipse(int(x - radius / 4), int(y - radius / 4), int(radius / 2), int(radius / 2))
        self.expectedPath.addEllipse(int(x - radius / 8), int(y - radius / 8), int(radius / 4), int(radius / 4))
        painter.setPen(QPen(Qt.red, 2))
        painter.drawPath(self.path)


#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())