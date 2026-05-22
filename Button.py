class Button:
    def __init__(self):
        self.buttons = []

    def addButton(self, cord, function, update):
        self.buttons.append({
            'cord': cord,  # Прямоугольная область кнопки
            'function': function,  # Callback функция
            'update': update  # Флаг необходимости обновления
        })

