import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QTabWidget,
                             QListWidget, QDialog, QHBoxLayout, QSpinBox, QScrollArea)
from PyQt5.QtCore import Qt
import PP_Sladosti_warehouse

dried_fruits = PP_Sladosti_warehouse.dried_fruits
nuts = PP_Sladosti_warehouse.nuts
other = PP_Sladosti_warehouse.other


planning = dict()

def save_product_to_csv(dict_products, name_file):
    with open(name_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for p, w in dict_products.items():
            writer.writerow([p, w[0], w[1]])


class UpdateWeightDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пополнение склада (поставка)")
        self.list_update = WarehouseManager()
        self.setGeometry(200, 200, 300, 150)

        # Создаем виджеты для ввода веса
        self.weight_labels = {}
        self.old_weight = {}
        self.weight_lineedits = {}
        for product_name, (weight, translation) in self.list_update.current_dict.items():
            label = QLabel(f"{translation}:")
            in_warehouse = QLabel(weight)
            lineedit = QLineEdit()
            self.weight_labels[product_name] = label
            self.old_weight[product_name] = in_warehouse
            self.weight_lineedits[product_name] = lineedit

        self.button_update = QPushButton("Обновить вес")
        self.button_update.clicked.connect(self.update_weights)

        # Создаем вертикальный контейнер для размещения виджетов
        layout = QVBoxLayout()
        for products in self.list_update.name_file.values():
            for product_name in products:
                layout_g = QHBoxLayout()
                layout_g.addWidget(self.weight_labels[product_name])
                layout_g.addWidget(self.old_weight[product_name])
                layout_g.addWidget(self.weight_lineedits[product_name])
                layout.addLayout(layout_g)
        layout.addWidget(self.button_update)

        self.setLayout(layout)

    def update_weights(self):
        for product_name, lineedit in self.weight_lineedits.items():
            new_weight = lineedit.text()
            if new_weight:
                weight = int(new_weight) + int(self.old_weight[product_name].text())
                self.list_update.current_dict[product_name] = [weight, self.weight_labels[product_name].text()]
        for name_file in self.list_update.name_file.keys():
            with open(name_file, "r+", newline="") as csvfile:
                csv_reader = csv.reader(csvfile)
                rows = list(csv_reader)  # Преобразуем в список списков
                for row in rows:
                    product, weight_prod, rus_name = row
                    weight_p = self.list_update.current_dict[product][0]
                    row[1] = weight_p
                # Возвращаемся в начало файла перед записью
                csvfile.seek(0)

                # Создаем объект writer для записи обновленных данных
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(rows)

        # Здесь можно добавить логику для сохранения обновленных данных о продуктах
        # self.list_update.load_products_from_csv()
        print("Вес продуктов обновлен.")

        self.close()


class CounterWidget(QWidget):
    def __init__(self, mix_name):
        super().__init__()
        self.mix_name = mix_name
        self.initUI()

    def initUI(self):
        self.main = QVBoxLayout()
        self.layout = QHBoxLayout()

        self.label = QLabel(self.mix_name, self)
        self.layout.addWidget(self.label)

        self.spinBox = QSpinBox(self)
        self.layout.addWidget(self.spinBox)

        self.addButton = QPushButton('+', self)
        self.addButton.clicked.connect(lambda: self.spinBox.setValue(self.spinBox.value() + 1))
        self.layout.addWidget(self.addButton)

        self.subtractButton = QPushButton('-', self)
        self.subtractButton.clicked.connect(lambda: self.spinBox.setValue(self.spinBox.value() - 1))
        self.layout.addWidget(self.subtractButton)

        self.spinBox.valueChanged.connect(self.value_changed)

        self.main.addLayout(self.layout)
        self.setLayout(self.main)

    def value_changed(self, value):
        planning[self.mix_name] = value
        print(f'Новое значение {self.mix_name}: {value}')


class PlanningTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.monos1 = ['кешью', 'миндаль', 'фундук']
        self.monos2 = ['манго', 'инжир', 'клюква']
        self.monos3 = ['банан', 'ананас', 'курага']
        self.monos4 = ['красная слива', 'чернослив', 'дыня']
        self.monos5 = ['кокос', 'апельсин']
        self.monos6 = ['чернослив конфета', 'дыня конфета', 'курага конфета']
        self.mixes = {
            'mix1': self.monos1,
            'mix2': self.monos2,
            'mix3': self.monos3,
            'mix4': self.monos4,
            'mix5': self.monos5,
            'mix6': self.monos6,
        }

        for mix in self.mixes.keys():
            self.layout.addWidget(CounterWidget(mix))

        for monos in self.mixes.values():
            for mono in monos:
                self.layout.addWidget(CounterWidget(mono))

        self.setLayout(self.layout)


class WarehouseManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name_file = {'dried_fruits.csv': dried_fruits, 'nuts.csv': nuts, 'other.csv': other}
        self.current_dict = dict()
        self.plan_dict = dict()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Менеджер склада")
        self.setGeometry(100, 100, 900, 800)

        # Создаем виджеты для вкладок
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        # self.tab2 = PlanningTab()

        # Создаем виджет для текста
        self.dried_fruits = QLabel('Сухофрукты')
        self.list_fruits = QListWidget()
        self.nuts = QLabel('Орехи')
        self.list_nuts = QListWidget()
        self.other = QLabel('Дополнения')
        self.list_other = QListWidget()
        self.load_products_from_csv()

        # Создаем кнопку для открытия диалогового окна
        self.button_open_dialog = QPushButton("Добавить продукты поставки")
        self.button_open_dialog.clicked.connect(self.open_dialog)

        self.button_append_new_prod = QPushButton("Обновить список продуктов")
        self.button_append_new_prod.clicked.connect(self.load_products_from_csv)

        # Создаем вертикальный контейнер для размещения кнопки
        main_layout = QHBoxLayout()
        layout = QVBoxLayout()
        right_side = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.planning_layout = PlanningTab()
        self.scroll_area.setWidget(self.planning_layout)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(self.button_open_dialog)

        self.right_label = QLabel('Планирование')
        right_side.addWidget(self.right_label)
        right_side.addWidget(self.scroll_area)

        self.result_button = QPushButton('Посчитать')
        self.result_button.clicked.connect(self.result_plan_func)
        right_side.addWidget(self.result_button)

        main_layout.addLayout(layout)
        main_layout.addLayout(right_side)

        # Создаем горизонтальный контейнер для размещения виджетов
        layout_g = QHBoxLayout()
        layout_g.addWidget(self.dried_fruits)
        layout_g.addWidget(self.list_fruits)
        layout_g.addWidget(self.nuts)
        layout_g.addWidget(self.list_nuts)
        layout_g.addWidget(self.other)
        layout_g.addWidget(self.list_other)
        layout.addLayout(layout_g)
        layout.addWidget(self.button_append_new_prod)

        self.tab1.setLayout(main_layout)

        # Добавляем вкладки в виджет вкладок
        self.tab_widget.addTab(self.tab1, "Добавление продуктов")
        # self.tab_widget.addTab(self.tab2, "Планирование изготовления")

        # Устанавливаем виджет вкладок как главный виджет
        self.setCentralWidget(self.tab_widget)

    def open_dialog(self):
        dialog = UpdateWeightDialog()
        dialog.exec_()

    def result_plan_func(self):

        print(f'значения словаря сейчас: {self.current_dict}')
        print(f'посчитал {planning}')

    def load_products_from_csv(self):
        # print('before')
        # print(self.current_dict)
        try:
            for n in self.name_file.keys():
                with open(n, "r") as csvfile:
                    if n == 'dried_fruits.csv':
                        self.list_fruits.clear()
                    elif n == 'nuts.csv':
                        self.list_nuts.clear()
                    elif n == 'other.csv':
                        self.list_other.clear()
                    for line in csvfile:
                        objects = line.strip()  # Здесь можно обработать строку из файла
                        name, weight, name_rus = objects.split(',')
                        object_name = f'{name_rus} - {weight}'
                        if n == 'dried_fruits.csv':
                            self.current_dict[name] = [weight, name_rus]
                            self.list_fruits.addItem(object_name)
                        elif n == 'nuts.csv':
                            self.current_dict[name] = [weight, name_rus]
                            self.list_nuts.addItem(object_name)
                        elif n == 'other.csv':
                            self.current_dict[name] = [weight, name_rus]
                            self.list_other.addItem(object_name)
            # print('after')
            # print(self.current_dict)
        except FileNotFoundError:
            return "Файл nuts.csv не найден. Создайте его."


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WarehouseManager()
    window.show()
    sys.exit(app.exec_())
