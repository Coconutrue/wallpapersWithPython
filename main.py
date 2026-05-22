import ctypes
import os
import time
import datetime
from tkinter import Menu
from tkinter import ttk
from tkinter import *
from open_task import *
from PIL import Image, ImageDraw, ImageFont
import win32gui
import tkinter as tk
from Button import Button
from Cashe import Cache
from Color import Color
from Cord import Cord
from Date import Date
import threading


class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_ulong), ('y', ctypes.c_ulong)]


def queryMousePosition():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return {'x': pt.x, 'y': pt.y}


cache = Cache()
button = Button()



class Main:
    def __init__(self):
        user32 = ctypes.windll.user32
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)

        # Состояние левой кнопки мыши
        self.mBuffer = 0
        self.mDown = False
        self.lastClickTime = 0
        self.clickDelay = 0.3  # Задержка между кликами (секунды)

        self.path = os.getcwd()
        self.indexTheme = cache.get('themeIndex', 0)
        self.theme = Color.getTheme(self.indexTheme)

        self.font = ImageFont.load_default()
        self.cashFonts = {}

        self.bg = False
        self.bgLastColor = False

        # Флаг для обновления обоев
        self.needsUpdate = True

    def genEmpty(self):
        """Создает пустое изображение для фона"""
        if not self.bg or self.theme['bg'] != self.bgLastColor:
            color = self.theme['bg']
            img = Image.new('RGB', (self.width, self.height), color)
            self.orig = img
            self.bgLastColor = self.theme['bg']
        img = self.orig.copy()
        self.object = img
        self.draw = ImageDraw.Draw(img)

    def getTextSize(self, text):
        bbox = self.draw.textbbox((0, 0), text, font=self.font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def setFont(self, name, size):
        id = f'{name}x{size}'
        if id not in self.cashFonts:
            try:
                self.cashFonts[id] = ImageFont.truetype(f'resources/fonts/{name}', size)
            except Exception:
                self.font = ImageFont.load_default()
                return
        self.font = self.cashFonts[id]

    def setText(self, x, y, text, color=(255, 255, 255)):
        self.draw.text((x, y), text, font=self.font, fill=color)
        w, h = self.getTextSize(text)
        return Cord(x, y, w, h)

    def setMindText(self, x, y, text, color=(255, 255, 255)):
        w, h = self.getTextSize(text)
        return self.setText(int(x - w / 2), y, text, color)

    def setWallpaper(self, filename):
        ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, self.path + f'\\{filename}', 2)

    def onUpdate(self):
        """события мать его мыши"""
        current_time = time.time()
        # Проверяем, прошло ли достаточно времени с последнего клика
        if current_time - self.lastClickTime < self.clickDelay:
            return False

        # Получаем состояние левой кнопки мыши
        current_state = ctypes.windll.user32.GetKeyState(0x01) & 0x8000
        # Определяем момент нажатия (переход из 0 в 1)
        if current_state and not self.mBuffer:
            self.mBuffer = True
            # Проверяем активное окно
            try:
                focus = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            except:
                focus = ''

            # Только если активен рабочий стол
            if focus in {'Program Manager', ''}:
                x, y = queryMousePosition()['x'], queryMousePosition()['y']

                # Перебираем кнопки в обратном порядке (верхние имеют приоритет)
                for butt in reversed(button.buttons):
                    if butt['cord'].isInside(x, y):
                        # Вызываем функцию кнопки в отдельном потоке, чтобы не блокировать
                        threading.Thread(target=butt['function'], daemon=True).start()
                        self.lastClickTime = current_time
                        return butt['update']  # Возвращаем, нужно ли обновление
        elif not current_state:
            self.mBuffer = False

        return False

    def update(self):
        """
        Основная функция отрисовки
        """
        button.buttons = []
        # Создаем фон
        self.genEmpty()
        d_m_Y = Date.get('%d.%m.%Y')
        day_name = Date.getDay()
        w = self.width / 2
        theme = self.theme

        self.setFont('font.otf', 100)
        c = self.setMindText(w, self.height / 3 - 100, day_name, theme['fg'])

        self.draw.line(
            (c.x - 10, c.y2 + 15, c.x2 + 10, c.y2 + 15),
            fill=theme['fg'],
            width=5
        )

        self.setFont('font.otf', 80)
        c_date = self.setMindText(w, c.y2 + 50, d_m_Y, theme['fg'])

        def newTheme():
            self.indexTheme += 1
            if self.indexTheme >= len(Color.getThemeList()):
                self.indexTheme = 0
            self.theme = Color.getTheme(self.indexTheme)
            cache.put('themeIndex', self.indexTheme)
            self.needsUpdate = True

        def open_tasks():
            # def change_theme():
            #     self.theme = Color.getTheme_hex(self.indexTheme)
            #     text_field['bg'] = self.theme['bg']
            #     text_field['fg'] = self.theme['fg']
            #     # text_field['insertbackground'] = view_colors[theme]['cursor']
            #     text_field['selectbackground'] = self.theme['selectbackground']
            #
            # self.theme = Color.getTheme_hex(self.indexTheme)
            # root = tk.Tk()
            # root.title("Фоновое приложение")
            # root.geometry("300x400")
            # root.overrideredirect(True)  # Убирает рамку окна
            #
            # main_menu = tk.Menu(root)
            # close_button = ttk.Button(root, text="Закрыть", command=root.destroy)
            # close_button.pack()
            #
            # #файл
            # file_menu = tk.Menu(main_menu, tearoff=0)
            # file_menu.add_command(label='открыть')
            # file_menu.add_command(label='сохранить')
            # file_menu.add_separator()
            # file_menu.add_command(label='закрыть')
            # root.config(menu=file_menu)
            #
            # #вид
            # viev_menu = Menu(main_menu, tearoff=0)
            # viev_menu_sub = Menu(viev_menu, tearoff=0)
            # font_menu_sub = Menu(viev_menu, tearoff=0)
            # viev_menu_sub.add_command(label='соответствие', command=lambda: change_theme())
            # viev_menu.add_cascade(label='Тема', menu=viev_menu_sub)
            #
            # root.config(menu=viev_menu)
            #
            #
            # #добавление списков в меню
            # main_menu.add_cascade(label='файл', menu=file_menu)
            # main_menu.add_cascade(label='вид', menu=viev_menu)
            #
            # root.config(menu=main_menu)
            #
            # f_text = tk.Frame(root)
            # f_text.pack(expand=1)
            #
            # text_field = tk.Text(f_text,
            #                      bg = self.theme['bg'],
            #                      fg=self.theme['fg'],
            #                      padx=10,
            #                      pady=10,
            #                      insertbackground='brown',
            #                      selectbackground=self.theme['selectbackground'],
            #                      spacing3=10,
            #                      font='Arial 14 bold'
            #                      )
            # text_field.pack(expand=1)
            # scroll = tk.Scrollbar(f_text, command=text_field.yview)
            # scroll.pack(side=tk.LEFT)
            # text_field.config(yscrollcommand=scroll.set)
            #
            # # root.attributes('-topmost', True)  # Всегда поверх всех окон
            #
            # root.mainloop()
            app = QtWidgets.QApplication(sys.argv)
            window = ExampleApp()
            window.show()
            app.exec_()



        self.setFont('font.ttf', 20)
        w1, h1 = self.getTextSize('Сменить тему')
        s = self.setText(
            self.width - 5 - w1,
            self.height - 48 - h1,
            'Сменить тему',
            theme['fg']
        )
        button.addButton(s, newTheme, True)
        s1 = self.setText(
            15,
            15,
            'Открыть задачи',
            theme['fg']
        )
        button.addButton(s1, open_tasks, True)

        try:
            temp_path = 'resources/tmp/temp.png'
            # Создаем папку если не существует
            os.makedirs('resources/tmp', exist_ok=True)

            if os.path.exists(temp_path):
                os.remove(temp_path)
            self.object.save(temp_path)
            self.setWallpaper(temp_path)
            self.needsUpdate = False
        except Exception as e:
            print(f"Ошибка при работе с файлом обоев: {e}")

    def start(self):
        print("Приложение запущено. Нажмите Ctrl+C для остановки.")
        self.update()  # Первоначальная отрисовка

        last_update_check = time.time()
        update_interval = 60  # Проверяем обновление каждые 60 секунд

        while True:
            try:
                # Обрабатываем клики с высокой частотой
                if self.onUpdate():
                    self.update()

                # Маленькая задержка для снижения нагрузки на CPU
                time.sleep(0.01)

            except KeyboardInterrupt:
                print("\nПриложение остановлено.")
                break
            except Exception as e:
                print(f"Ошибка в основном цикле: {e}")
                time.sleep(1)


if __name__ == "__main__":
    app = Main()
    app.start()