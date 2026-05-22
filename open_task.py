import sqlite3
import sys
from PyQt5 import QtWidgets, QtCore
import tasks
from Cashe import Cache
from Color import Color


class ExampleApp(QtWidgets.QMainWindow, tasks.Ui_MainWindow):
    def __init__(self, theme=None, theme_index=None):
        super().__init__()
        self.init_db()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 500, 400)

        self.cache = Cache()

        if theme is not None and theme_index is not None:
            self.theme_index = theme_index
            self.theme = theme
        else:
            self.theme_index = self.cache.get('themeIndex', 0)
            self.theme = Color.getTheme(self.theme_index)

        self.buttn_close.clicked.connect(self.save_text)
        self.bttn_open_file.clicked.connect(self.open_file)
        self.change_theme.clicked.connect(self.change_theme_style)

        self.load_text()
        self.apply_theme_style()

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

    def rgb_to_hex(self, rgb):
        """Преобразует RGB кортеж в HEX строку"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def apply_theme_style(self):
        bg_color = self.rgb_to_hex(self.theme['bg'])
        fg_color = self.rgb_to_hex(self.theme['fg'])
        text_color = self.rgb_to_hex(self.theme['text'])

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {bg_color};
            }}
            QWidget#centralwidget {{
                background-color: {bg_color};
            }}
            QTextEdit {{
                background-color: {bg_color};
                color: {text_color};
                font-family: 'Arial';
                font-size: 14px;
                border: 2px solid {fg_color};
                border-radius: 5px;
                padding: 10px;
            }}
            QTextEdit:focus {{
                border: 2px solid {text_color};
            }}
            QPushButton {{
                background-color: {fg_color};
                color: {bg_color};
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {text_color};
                color: {fg_color};
            }}
            QPushButton:pressed {{
                background-color: {bg_color};
                color: {fg_color};
                border: 1px solid {fg_color};
            }}
            QTabWidget::pane {{
                border: 1px solid {fg_color};
                background-color: {bg_color};
            }}
            QTabBar::tab {{
                background-color: {fg_color};
                color: {bg_color};
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }}
            QTabBar::tab:selected {{
                background-color: {text_color};
                color: {fg_color};
            }}
            QTabBar::tab:hover {{
                background-color: {text_color};
                color: {fg_color};
            }}
            QScrollBar:vertical {{
                background-color: {bg_color};
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {fg_color};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {text_color};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                background-color: {bg_color};
                height: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {fg_color};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {text_color};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)

    def change_theme_style(self):
        self.theme_index += 1
        themes = Color.getThemeList()
        if self.theme_index >= len(themes):
            self.theme_index = 0
        self.theme = Color.getTheme(self.theme_index)
        self.cache.put('themeIndex', self.theme_index)
        self.apply_theme_style()

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
                    self.tabWidget.setCurrentIndex(0)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")