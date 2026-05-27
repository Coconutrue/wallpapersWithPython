import sys
from PyQt5 import QtWidgets, QtCore
import timer
from Cashe import Cache
from Color import Color


class Timer(QtWidgets.QMainWindow, timer.Ui_MainWindow):
    def __init__(self, theme=None, theme_index=None):
        super().__init__()
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

        self.time_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        # Таймер и переменные состояния
        self.countdown_timer = QtCore.QTimer()
        self.countdown_timer.timeout.connect(self.update_timer)
        self.remaining_seconds = 0
        self.is_running = False
        self.hour.setRange(0, 99)
        self.hour.setValue(0)
        self.min.setRange(0, 59)
        self.min.setValue(0)
        self.second.setRange(0, 59)
        self.second.setValue(0)

        self.start.clicked.connect(self.start_timer)
        self.pause.clicked.connect(self.pause_timer)
        self.pause.setEnabled(False)
        self.stop.clicked.connect(self.stop_timer)
        self.stop.setEnabled(False)
        self.setup.clicked.connect(self.set_time_from_spinboxes)
        self.pushButton.clicked.connect(self.change_theme_style)
        self.close_btn.clicked.connect(self.close)


        self.apply_theme_style()

    def set_time_from_spinboxes(self):
        self.stop_timer()
        hours = self.hour.value()
        minutes = self.min.value()
        seconds = self.second.value()
        self.remaining_seconds = hours * 3600 + minutes * 60 + seconds
        self.update_display()
        if hasattr(self, 'status_label'):
            self.status_label.setText(f"Установлено: {self.format_time(self.remaining_seconds)}")

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_display(self):
        self.time_label.setText(self.format_time(self.remaining_seconds))

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            if self.remaining_seconds == 0:
                self.timer_finished()
        else:
            self.timer_finished()

    def timer_finished(self):
        self.countdown_timer.stop()
        self.is_running = False
        self.start.setEnabled(True)
        self.pause.setEnabled(False)
        self.stop.setEnabled(False)
        self.time_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #ff4444;")

        QtWidgets.QMessageBox.information(
            self, "Таймер завершён",
            f"Время вышло\n{self.format_time(self.remaining_seconds)}"
        )
        self.time_label.setStyleSheet("font-size: 48px; font-weight: bold;")

        if hasattr(self, 'status_label'):
            self.status_label.setText("Таймер завершён")

    def start_timer(self):
        if self.remaining_seconds > 0 and not self.is_running:
            self.countdown_timer.start(1000)
            self.is_running = True
            self.start.setEnabled(False)
            self.pause.setEnabled(True)
            self.stop.setEnabled(True)
            self.time_label.setStyleSheet("font-size: 48px; font-weight: bold;")

            if hasattr(self, 'status_label'):
                self.status_label.setText("Таймер работает...")

    def pause_timer(self):
        if self.is_running:
            self.countdown_timer.stop()
            self.is_running = False
            self.start.setEnabled(True)
            self.pause.setEnabled(False)
            self.start.setText("Продолжить")
            self.time_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #ffaa00;")

            if hasattr(self, 'status_label'):
                self.status_label.setText("На паузе")

    def stop_timer(self):
        self.countdown_timer.stop()
        self.is_running = False
        self.start.setEnabled(True)
        self.start.setText("Старт")
        self.pause.setEnabled(False)
        self.stop.setEnabled(False)
        self.time_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.update_display()
        if hasattr(self, 'status_label'):
            self.status_label.setText("Остановлен")

    def rgb_to_hex(self, rgb):
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
            QLabel {{
                color: {text_color};
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
            QPushButton:disabled {{
                background-color: #555555;
                color: #888888;
            }}
            QSpinBox {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {fg_color};
                border-radius: 3px;
                padding: 2px;
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Timer()
    window.show()
    sys.exit(app.exec_())