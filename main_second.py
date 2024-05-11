from PyQt5.QtWidgets import QApplication, QWidget, QSpinBox


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создание QSpinBox
        self.spinBox = QSpinBox(self)
        self.spinBox.move(50, 50)

        # Установка диапазона значений
        self.spinBox.setMinimum(1)  # минимум
        self.spinBox.setMaximum(10)  # максимум

        # Установка шага изменения значения
        self.spinBox.setSingleStep(1)

        # Сигнал изменения значения
        self.spinBox.valueChanged.connect(self.value_changed)

    def value_changed(self, value):
        print(f'Новое значение: {value}')


if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    ex.show()
    app.exec_()
