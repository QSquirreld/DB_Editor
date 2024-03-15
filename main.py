import sys
from PyQt5.QtWidgets import *
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self, nedelya):
        self.nedelya = nedelya
        super().__init__()

        self.con()

        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Расписание')
        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(100, 30)
        self.btn.move(120, 230)
        self.btn.clicked.connect(self.upd)

        self.numb = QLineEdit(self)
        self.numb.resize(100, 30)
        self.numb.move(20, 200)

        self.ti = QLineEdit(self)
        self.ti.resize(100, 30)
        self.ti.move(120, 200)

        self.pre = QLineEdit(self)
        self.pre.resize(100, 30)
        self.pre.move(220, 200)

        self.kab = QLineEdit(self)
        self.kab.resize(100, 30)
        self.kab.move(320, 200)

        self.tip = QLineEdit(self)
        self.tip.resize(100, 30)
        self.tip.move(420, 200)

        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(100, 30)
        self.btn.move(220, 230)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(100, 30)
        self.btn.move(320, 230)
        self.btn.clicked.connect(self.dels)

    # соединение с базой данных

    def con(self):
        self.conn = psycopg2.connect(database="raspisanie",
                                     user="postgres",
                                     password="Roots1234",
                                     host="localhost",
                                     port="5432")
        self.cur = self.conn.cursor()

        # обновить таблицу и поля

    def upd(self):
        self.conn.commit()
        # self.numbb.setText('')
        self.numb.setText('')
        self.ti.setText('')
        self.pre.setText('')
        self.kab.setText('')
        self.tip.setText('')

        # добавить таблицу новую строку

    def ins(self):
        numb, ti, pre, kab, tip = self.numb.text(), self.ti.text(), self.pre.text(), self.kab.text(), self.tip.text()
        self.cur.execute(
            f"INSERT INTO {self.nedelya} ( numb, ti, pre, kab, tip ) VALUES ('{str(numb)}', '{str(ti)}','{str(pre)}','{str(kab)}','{str(tip)}');")

        # удалить из таблицы строку

    def dels(self):
        numbb = int(self.numb.text())
        self.cur.execute(f"DELETE FROM {self.nedelya}  WHERE  numb='{str(numbb)}';")
        # изменить  данные

    def esm(self):
        numb, ti, pre, kab, tip = self.numb.text(), self.ti.text(), self.pre.text(), self.kab.text(), self.tip.text()
        numbb = int(self.numb.text())
        self.cur.execute(
            f"UPDATE {self.nedelya} SET numb='{str(numb)}', ti='{str(ti)}', pre='{str(pre)}', kab='{str(kab)}', tip='{str(tip)}';")


# класс - таблица
class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg

        super().__init__(wg)
        self.setGeometry(20, 20, 700, 600)
        self.setColumnCount(5)
        self.verticalHeader().hide()
        self.updt()  # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cellClicked.connect(self.cellClick)

    # обновление таблицы
    def updt(self):
        self.clear()

        self.setColumnCount(5)
        self.setRowCount(5)
        self.setHorizontalHeaderLabels(["numb", "ti", "pre", "kab", "tip"])

        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        # self.horizontalHeaderItem(5).setTextAlignment(Qt.AlignHCenter)

        self.wg.cur.execute(f"select * from {self.wg.nedelya} ORDER BY numb")

        rows = self.wg.cur.fetchall()
        i = 0
        for records in rows:
            self.setItem(i, 0, QTableWidgetItem(f"{records[0]}"))
            self.setItem(i, 1, QTableWidgetItem(f"{records[1]}"))
            self.setItem(i, 2, QTableWidgetItem(f"{records[2]}"))
            self.setItem(i, 3, QTableWidgetItem(f"{records[3]}"))
            self.setItem(i, 4, QTableWidgetItem(f"{records[4]}"))
            # self.setItem(i, 5, QTableWidgetItem(f"{records[5]}"))

            i += 1

    # обработка щелчка мыши по таблице
    def cellClick(self, row, col):
        # self.wg.numbb.setText(self.item(row, 0).text().strip())
        self.wg.numb.setText(self.item(row, 0).text().strip())
        self.wg.ti.setText(self.item(row, 1).text().strip())
        self.wg.pre.setText(self.item(row, 2).text().strip())
        self.wg.kab.setText(self.item(row, 3).text().strip())
        self.wg.tip.setText(self.item(row, 4).text().strip())


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.secondWin = ''

    def initUI(self):
        self.setGeometry(400, 400, 500, 500)
        self.setWindowTitle('расписание')

        self.btn = QPushButton('Понедельник_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 100)
        self.btn.clicked.connect(lambda: self.openWin('понедельник_1'))

        self.btn = QPushButton('Понедельник_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 100)
        self.btn.clicked.connect(lambda: self.openWin('понедельник_2'))

        self.btn = QPushButton('Вторник_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 150)
        self.btn.clicked.connect(lambda: self.openWin('вторник_1'))

        self.btn = QPushButton('Вторник_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 150)
        self.btn.clicked.connect(lambda: self.openWin('вторник_2'))

        self.btn = QPushButton('Среда_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 200)
        self.btn.clicked.connect(lambda: self.openWin('среда_1'))

        self.btn = QPushButton('Среда_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 200)
        self.btn.clicked.connect(lambda: self.openWin('среда_2'))

        self.btn = QPushButton('Четверг_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 250)
        self.btn.clicked.connect(lambda: self.openWin('четверг_1'))

        self.btn = QPushButton('Четверг_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 250)
        self.btn.clicked.connect(lambda: self.openWin('четверг_2'))

        self.btn = QPushButton('Пятница_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 300)
        self.btn.clicked.connect(lambda: self.openWin('пятница_1'))

        self.btn = QPushButton('Пятница_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 300)
        self.btn.clicked.connect(lambda: self.openWin('пятница_2'))

        self.btn = QPushButton('Суббота_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 350)
        self.btn.clicked.connect(lambda: self.openWin('суббота_1'))

        self.btn = QPushButton('Суббота_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 350)
        self.btn.clicked.connect(lambda: self.openWin('суббота_2'))

    # ===========================================================================

    def openWin(self, op):
        nedelya = ''
        if op == 'среда_1':
            nedelya = 'sre1'
        elif op == 'среда_2':
            nedelya = 'sre2'
        elif op == 'понедельник_1':
            nedelya = 'pon1'
        elif op == 'понедельник_2':
            nedelya = 'pon2'
        elif op == 'вторник_1':
            nedelya = 'vto1'
        elif op == 'вторник_2':
            nedelya = 'vto2'
        elif op == 'четверг_1':
            nedelya = 'che1'
        elif op == 'четверг_2':
            nedelya = 'che2'
        elif op == 'пятница_1':
            nedelya = 'pia1'
        elif op == 'пятница_2':
            nedelya = 'pia2'
        elif op == 'суббота_1':
            nedelya = 'sub1'
        elif op == 'суббота_2':
            nedelya = 'sub2'

        self.secondWin = MyWidget(nedelya)
        self.secondWin.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())import sys
from PyQt5.QtWidgets import *
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self, nedelya):
        self.nedelya = nedelya
        super().__init__()

        self.con()

        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Расписание')
        self.tb = Tb(self)
        # кнопка "обновить"
        self.btn = QPushButton('Обновить', self)
        self.btn.resize(100, 30)
        self.btn.move(120, 230)
        self.btn.clicked.connect(self.upd)

        self.numb = QLineEdit(self)
        self.numb.resize(100, 30)
        self.numb.move(20, 200)

        self.ti = QLineEdit(self)
        self.ti.resize(100, 30)
        self.ti.move(120, 200)

        self.pre = QLineEdit(self)
        self.pre.resize(100, 30)
        self.pre.move(220, 200)

        self.kab = QLineEdit(self)
        self.kab.resize(100, 30)
        self.kab.move(320, 200)

        self.tip = QLineEdit(self)
        self.tip.resize(100, 30)
        self.tip.move(420, 200)

        # кнопка добавить запись
        self.btn = QPushButton('Добавить', self)
        self.btn.resize(100, 30)
        self.btn.move(220, 230)
        self.btn.clicked.connect(self.ins)
        # кнопка удалить запись
        self.btn = QPushButton('Удалить', self)
        self.btn.resize(100, 30)
        self.btn.move(320, 230)
        self.btn.clicked.connect(self.dels)

    # соединение с базой данных


    def con(self):
        self.conn = psycopg2.connect(database="raspisanie",
                                     user="postgres",
                                     password="Roots1234",
                                     host="localhost",
                                     port="5432")
        self.cur = self.conn.cursor()

        # обновить таблицу и поля


    def upd(self):
        self.conn.commit()
        #self.numbb.setText('')
        self.numb.setText('')
        self.ti.setText('')
        self.pre.setText('')
        self.kab.setText('')
        self.tip.setText('')

        # добавить таблицу новую строку

    def ins(self):
        numb, ti, pre, kab, tip = self.numb.text(), self.ti.text(), self.pre.text(), self.kab.text(), self.tip.text()
        self.cur.execute(
            f"INSERT INTO {self.nedelya} ( numb, ti, pre, kab, tip ) VALUES ('{str(numb)}', '{str(ti)}','{str(pre)}','{str(kab)}','{str(tip)}');")

        # удалить из таблицы строку


    def dels(self):
        numbb = int(self.numb.text())
        self.cur.execute(f"DELETE FROM {self.nedelya}  WHERE  numb='{str(numbb)}';")
        # изменить  данные


    def esm(self):
        numb, ti, pre, kab, tip = self.numb.text(), self.ti.text(), self.pre.text(), self.kab.text(), self.tip.text()
        numbb = int(self.numb.text())
        self.cur.execute(
            f"UPDATE {self.nedelya} SET numb='{str(numb)}', ti='{str(ti)}', pre='{str(pre)}', kab='{str(kab)}', tip='{str(tip)}';")


# класс - таблица
class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg

        super().__init__(wg)
        self.setGeometry(20, 20, 700, 600)
        self.setColumnCount(5)
        self.verticalHeader().hide()
        self.updt()  # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cellClicked.connect(self.cellClick)

    # обновление таблицы
    def updt(self):
        self.clear()

        self.setColumnCount(5)
        self.setRowCount(5)
        self.setHorizontalHeaderLabels(["numb", "ti", "pre", "kab", "tip"])

        self.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
        self.horizontalHeaderItem(4).setTextAlignment(Qt.AlignHCenter)
        #self.horizontalHeaderItem(5).setTextAlignment(Qt.AlignHCenter)

        self.wg.cur.execute(f"select * from {self.wg.nedelya} ORDER BY numb")

        rows = self.wg.cur.fetchall()
        i = 0
        for records in rows:

            self.setItem(i, 0, QTableWidgetItem(f"{records[0]}"))
            self.setItem(i, 1, QTableWidgetItem(f"{records[1]}"))
            self.setItem(i, 2, QTableWidgetItem(f"{records[2]}"))
            self.setItem(i, 3, QTableWidgetItem(f"{records[3]}"))
            self.setItem(i, 4, QTableWidgetItem(f"{records[4]}"))
            #self.setItem(i, 5, QTableWidgetItem(f"{records[5]}"))

            i += 1

    # обработка щелчка мыши по таблице
    def cellClick(self, row, col):
        #self.wg.numbb.setText(self.item(row, 0).text().strip())
        self.wg.numb.setText(self.item(row, 0).text().strip())
        self.wg.ti.setText(self.item(row, 1).text().strip())
        self.wg.pre.setText(self.item(row, 2).text().strip())
        self.wg.kab.setText(self.item(row, 3).text().strip())
        self.wg.tip.setText(self.item(row, 4).text().strip())


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.secondWin = ''

    def initUI(self):
        self.setGeometry(400, 400, 500, 500)
        self.setWindowTitle('расписание')



        self.btn = QPushButton('Понедельник_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 100)
        self.btn.clicked.connect(lambda: self.openWin('понедельник_1'))

        self.btn = QPushButton('Понедельник_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 100)
        self.btn.clicked.connect(lambda: self.openWin('понедельник_2'))

        self.btn = QPushButton('Вторник_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 150)
        self.btn.clicked.connect(lambda: self.openWin('вторник_1'))

        self.btn = QPushButton('Вторник_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 150)
        self.btn.clicked.connect(lambda: self.openWin('вторник_2'))

        self.btn = QPushButton('Среда_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 200)
        self.btn.clicked.connect(lambda: self.openWin('среда_1'))

        self.btn = QPushButton('Среда_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 200)
        self.btn.clicked.connect(lambda: self.openWin('среда_2'))

        self.btn = QPushButton('Четверг_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 250)
        self.btn.clicked.connect(lambda: self.openWin('четверг_1'))

        self.btn = QPushButton('Четверг_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 250)
        self.btn.clicked.connect(lambda: self.openWin('четверг_2'))

        self.btn = QPushButton('Пятница_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 300)
        self.btn.clicked.connect(lambda: self.openWin('пятница_1'))

        self.btn = QPushButton('Пятница_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 300)
        self.btn.clicked.connect(lambda: self.openWin('пятница_2'))

        self.btn = QPushButton('Суббота_1', self)
        self.btn.resize(120, 50)
        self.btn.move(100, 350)
        self.btn.clicked.connect(lambda: self.openWin('суббота_1'))

        self.btn = QPushButton('Суббота_2', self)
        self.btn.resize(120, 50)
        self.btn.move(220, 350)
        self.btn.clicked.connect(lambda: self.openWin('суббота_2'))
#===========================================================================

    def openWin(self, op):
        nedelya = ''
        if op == 'среда_1':
            nedelya = 'sre1'
        elif op == 'среда_2':
            nedelya = 'sre2'
        elif op == 'понедельник_1':
            nedelya = 'pon1'
        elif op == 'понедельник_2':
            nedelya = 'pon2'
        elif op == 'вторник_1':
            nedelya = 'vto1'
        elif op == 'вторник_2':
            nedelya = 'vto2'
        elif op == 'четверг_1':
            nedelya = 'che1'
        elif op == 'четверг_2':
            nedelya = 'che2'
        elif op == 'пятница_1':
            nedelya = 'pia1'
        elif op == 'пятница_2':
            nedelya = 'pia2'
        elif op == 'суббота_1':
            nedelya = 'sub1'
        elif op == 'суббота_2':
            nedelya = 'sub2'


        self.secondWin = MyWidget(nedelya)
        self.secondWin.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())