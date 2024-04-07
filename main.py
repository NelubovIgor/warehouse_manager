import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QTabWidget, QListWidget, QDialog, QHBoxLayout

import PP_Sladosti_warehouse

dried_fruits = PP_Sladosti_warehouse.dried_fruits
nuts = PP_Sladosti_warehouse.nuts
other = PP_Sladosti_warehouse.other
# print(dried_fruits)
def save_product_to_csv(dict_products, name_file):
    with open(name_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for p, w in dict_products.items():
            writer.writerow([p, w[0], w[1]])

class UpdateWeightDialog(QDialog):
    def __init__(self, name_file):
        super().__init__()
        self.setWindowTitle("Пополнение склада (поставка)")
        self.list_update = WarehouseManager()
        self.setGeometry(200, 200, 300, 150)
        self.name_file = name_file

        # Создаем виджеты для ввода веса
        self.weight_labels = {}
        self.old_weight = {}
        self.weight_lineedits = {}
        # print(self.weight_labels)
        # print('----')
        # print(self.weight_lineedits)
        # print(self.products_dict)
        # print(name_file)
        for keys, values in self.name_file.items():
            # print(type(values))
            # print(values)
            for product_name, (weight, translation) in values.items():
                # print(product_name)
                # print(weight)
                # print(translation)
                label = QLabel(f"{translation}:")
                in_warehouse = QLabel(weight)
                lineedit = QLineEdit()
                self.weight_labels[product_name] = label
                self.old_weight[product_name] = in_warehouse
                self.weight_lineedits[product_name] = lineedit

        self.button_update = QPushButton("Обновить вес")
        self.button_update.clicked.connect(self.update_weights)
        self.button_update.clicked.connect(self.list_update.load_products_from_csv)

        # main_layout = QHBoxLayout()
        # Создаем вертикальный контейнер для размещения виджетов
        layout = QVBoxLayout()
        for products in self.name_file.values():
            for product_name in products:
                layout_g = QHBoxLayout()
                layout_g.addWidget(self.weight_labels[product_name])
                layout_g.addWidget(self.old_weight[product_name])
                layout_g.addWidget(self.weight_lineedits[product_name])
                layout.addLayout(layout_g)
        layout.addWidget(self.button_update)

        self.setLayout(layout)
        # print(name_file)
    def update_weights(self):
        # print(name_file)
        # print(type(name_file))
        for name_dict, dicts in self.name_file.items():
            for product_name, lineedit in self.weight_lineedits.items():
                # print(lineedit.text())
                new_weight = lineedit.text()
                if new_weight:
                    # print(new_weight)
                    # print('-----')
                    if dicts.get(product_name):
                        weight = int(new_weight) + int(dicts[product_name][0])
                        # print(int(new_weight))
                        # print(dicts[product_name][1])
                        self.name_file[name_dict][product_name][0] = weight
                        # print(dicts[product_name])
        # Здесь можно добавить логику для сохранения обновленных данных о продуктах
        print("Вес продуктов обновлен.")
        # print(self.name_file)
        self.close()

# class AddProductDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Добавление продукта")
#         self.setGeometry(200, 200, 300, 150)
#
#
#         # Создаем виджеты для ввода продуктов
#         self.label_product = QLabel("Продукт:")
#         self.lineedit_product = QLineEdit()
#         self.label_weight = QLabel("Вес (г):")
#         self.lineedit_weight = QLineEdit()
#         self.button_add = QPushButton("Добавить")
#         self.button_add.clicked.connect(self.add_product)
#
#         # Создаем горизонтальный контейнер для размещения виджетов
#         layout = QHBoxLayout()
#         layout.addWidget(self.label_product)
#         layout.addWidget(self.lineedit_product)
#         layout.addWidget(self.label_weight)
#         layout.addWidget(self.lineedit_weight)
#         layout.addWidget(self.button_add)
#
#         self.setLayout(layout)
#
#     def add_product(self):
#         product = dict()
#         product[self.lineedit_product.text()] = self.lineedit_weight.text()
#
#         save_product_to_csv(product)
#         # Здесь можно добавить логику для сохранения продукта на складе
#         print(f"Добавлен продукт: {self.lineedit_product.text()}, Вес: {self.lineedit_weight.text()} г")
#         self.close()

class WarehouseManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.name_file = {'dried_fruits.csv': dried_fruits, 'nuts.csv': nuts, 'other.csv': other}
        # print(self.name_file, ' - main')
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Менеджер склада")
        self.setGeometry(100, 100, 700, 600)

        # Создаем виджеты для вкладок
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

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
        # self.button_open_dialog.clicked.connect(self.load_products_from_csv)

        # self.button_sorted_products = QPushButton("Сортировать продукты")
        # self.button_sorted_products.clicked.connect(self.sorted_products_in_csv)
        # self.button_sorted_products.clicked.connect(self.load_products_from_csv)

        self.button_append_new_prod = QPushButton("Обновить список продуктов")
        # self.button_append_new_prod.clicked.connect(self.open_dialog)
        self.button_append_new_prod.clicked.connect(self.load_products_from_csv)


        # Создаем вертикальный контейнер для размещения кнопки
        layout = QVBoxLayout()
        layout.addWidget(self.button_open_dialog)

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
        # layout.addWidget(self.button_sorted_products)
        self.tab1.setLayout(layout)
        # self.tab1.setLayout(layout_g)

        # Добавляем вкладки в виджет вкладок
        self.tab_widget.addTab(self.tab1, "Добавление продуктов")
        self.tab_widget.addTab(self.tab2, "Планирование изготовления")

        # Создаем главный виджет и устанавливаем в него вертикальный контейнер
        # central_widget = QWidget()
        # central_widget.setLayout(layout)
        # self.setCentralWidget(central_widget)

        # Устанавливаем виджет вкладок как главный виджет
        self.setCentralWidget(self.tab_widget)

    def open_dialog(self):
        # print('до входа')
        # print(type(self.name_file))
        # print(self.name_file)
        dialog = UpdateWeightDialog(self.name_file)

        # dialog = AddProductDialog()
        dialog.exec_()

    def load_products_from_csv(self):
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
                        object = line.strip()  # Здесь можно обработать строку из файла
                        name, weight, name_rus = object.split(',')
                        object_name = f'{name_rus} - {weight}'
                        if n == 'dried_fruits.csv':
                            PP_Sladosti_warehouse.dried_fruits[name] = [weight, name_rus]
                            self.list_fruits.addItem(object_name)
                        elif n == 'nuts.csv':
                            PP_Sladosti_warehouse.nuts[name] = [weight, name_rus]
                            self.list_nuts.addItem(object_name)
                        elif n == 'other.csv':
                            PP_Sladosti_warehouse.other[name] = [weight, name_rus]
                            self.list_other.addItem(object_name)
        except FileNotFoundError:
            return "Файл nuts.csv не найден. Создайте его."

    # def sorted_products_in_csv(self):
    #     try:
    #         for name_csv, name_prod in self.name_file.items():
    #             with open(name_csv, "r") as csvfile:
    #                 # self.list_fruits.clear()
    #                 dict_products = dict()
    #                 # reader = csv.reader(csvfile)
    #                 for k, v in name_prod.items():
    #                     # name, weight = line
    #                     dict_products[k] = [v[0], v[1]]
    #                 save_product_to_csv(dict_products, name_csv)
    #                 # save_product_to_csv(dict(sorted(dict_products.items())), n_f)
    #     except FileNotFoundError:
    #         return "Файл nuts.csv не найден. Создайте его."

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WarehouseManager()
    window.show()
    sys.exit(app.exec_())
