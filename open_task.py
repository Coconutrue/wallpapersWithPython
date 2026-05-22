import sqlite3
import sys
from PyQt5 import QtWidgets, QtCore
import tasks
from Cashe import Cache

class ExampleApp(QtWidgets.QMainWindow, tasks.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 500, 400)
        # root.attributes('-topmost', True) - поверх всех окон
        self.setWindowFlags(self.windowFlags())
        self.cache = Cache()

        theme_index = self.cache.get('themeIndex', 0)
        self.theme_index = theme_index

        # кнопки
        self.buttn_close.clicked.connect(self.save_text)
        self.bttn_open_file.clicked.connect(self.open_file)
        self.change_theme.clicked.connect(self.close)

        self.load_text()

    def init_db(self):
        self.conn = sqlite3.connect('notes.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
               CREATE TABLE IF NOT EXISTS notes (
                   id INTEGER PRIMARY KEY,
                   content TEXT
               )
           ''')
        self.conn.commit()

    def save_text(self):
        content = self.textEdit_2.toPlainText()
        self.cursor.execute('DELETE FROM notes')
        self.cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        self.conn.commit()
        self.close()

    def load_text(self):
        self.cursor.execute('SELECT content FROM notes LIMIT 1')
        result = self.cursor.fetchone()
        if result and result[0]:
            self.textEdit_2.setText(result[0])

    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "выбери .txt",
            "",
            "(*.txt)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.textEdit.setText(content)
                    self.tabWidget.setCurrentIndex(1)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")

    """стили"""
    def style1(self):
        self.setStyleSheet("""
                       QMainWindow {
                           background-color: #2b2b2b;
                       }
                   """)

        self.centralwidget.setStyleSheet("""
                       QWidget {
                           background-color: #2b2b2b;
                       }
                   """)

        self.textEdit.setStyleSheet("""
                       QTextEdit {
                           background-color: #3c3c3c;
                           color: #ffffff;
                           font-family: 'Arial';
                           font-size: 14px;
                           border: 2px solid #555555;
                           border-radius: 5px;
                           padding: 10px;
                       }
                       QTextEdit:focus {
                           border: 2px solid #0078d4;
                       }
                   """)

        self.setStyleSheet("""
                       QPushButton {
                           background-color: #555555;
                           color: white;
                           border: none;
                           border-radius: 5px;
                           padding: 8px;
                           font-size: 12px;
                           font-weight: bold;
                       }
                       QPushButton:hover {
                           background-color: #777777;
                       }
                       QPushButton:pressed {
                           background-color: #333333;
                       }
                   """)
    def style2(self):
        self.setStyleSheet("""
                       QMainWindow {
                           background-color: #2b2b2b;
                       }
                   """)

        self.centralwidget.setStyleSheet("""
                       QWidget {
                           background-color: #2b2b2b;
                       }
                   """)

        self.textEdit.setStyleSheet("""
                       QTextEdit {
                           background-color: #3c3c3c;
                           color: #ffffff;
                           font-family: 'Arial';
                           font-size: 14px;
                           border: 2px solid #555555;
                           border-radius: 5px;
                           padding: 10px;
                       }
                       QTextEdit:focus {
                           border: 2px solid #0078d4;
                       }
                   """)

        self.setStyleSheet("""
                       QPushButton {
                           background-color: #555555;
                           color: white;
                           border: none;
                           border-radius: 5px;
                           padding: 8px;
                           font-size: 12px;
                           font-weight: bold;
                       }
                       QPushButton:hover {
                           background-color: #777777;
                       }
                       QPushButton:pressed {
                           background-color: #333333;
                       }
                   """)
    def style3(self):
        self.setStyleSheet("""
                       QMainWindow {
                           background-color: #2b2b2b;
                       }
                   """)

        self.centralwidget.setStyleSheet("""
                       QWidget {
                           background-color: #2b2b2b;
                       }
                   """)

        self.textEdit.setStyleSheet("""
                       QTextEdit {
                           background-color: #3c3c3c;
                           color: #ffffff;
                           font-family: 'Arial';
                           font-size: 14px;
                           border: 2px solid #555555;
                           border-radius: 5px;
                           padding: 10px;
                       }
                       QTextEdit:focus {
                           border: 2px solid #0078d4;
                       }
                   """)

        self.setStyleSheet("""
                       QPushButton {
                           background-color: #555555;
                           color: white;
                           border: none;
                           border-radius: 5px;
                           padding: 8px;
                           font-size: 12px;
                           font-weight: bold;
                       }
                       QPushButton:hover {
                           background-color: #777777;
                       }
                       QPushButton:pressed {
                           background-color: #333333;
                       }
                   """)

    def style4(self):
        self.setStyleSheet("""
                       QMainWindow {
                           background-color: #2b2b2b;
                       }
                   """)

        self.centralwidget.setStyleSheet("""
                       QWidget {
                           background-color: #2b2b2b;
                       }
                   """)

        self.textEdit.setStyleSheet("""
                       QTextEdit {
                           background-color: #3c3c3c;
                           color: #ffffff;
                           font-family: 'Arial';
                           font-size: 14px;
                           border: 2px solid #555555;
                           border-radius: 5px;
                           padding: 10px;
                       }
                       QTextEdit:focus {
                           border: 2px solid #0078d4;
                       }
                   """)

        self.setStyleSheet("""
                       QPushButton {
                           background-color: #555555;
                           color: white;
                           border: none;
                           border-radius: 5px;
                           padding: 8px;
                           font-size: 12px;
                           font-weight: bold;
                       }
                       QPushButton:hover {
                           background-color: #777777;
                       }
                       QPushButton:pressed {
                           background-color: #333333;
                       }
                   """)



