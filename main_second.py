from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

class UpdateWeightDialog(QDialog):
    def __init__(self, products_dict):
        super().__init__()
        self.setWindowTitle("Обновление веса продуктов")
        self.setGeometry(200, 200, 300, 150)

        self.products_dict = products_dict

        # Создаем виджеты для ввода веса
        self.weight_labels = {}
        self.weight_lineedits = {}
        for product_name, (weight, translation) in self.products_dict.items():
            label = QLabel(f"{translation}:")
            lineedit = QLineEdit(str(weight))
            self.weight_labels[product_name] = label
            self.weight_lineedits[product_name] = lineedit

        self.button_update = QPushButton("Обновить вес")
        self.button_update.clicked.connect(self.update_weights)

        # Создаем вертикальный контейнер для размещения виджетов
        layout = QVBoxLayout()
        for product_name in self.products_dict:
            layout.addWidget(self.weight_labels[product_name])
            layout.addWidget(self.weight_lineedits[product_name])
        layout.addWidget(self.button_update)

        self.setLayout(layout)

    def update_weights(self):
        for product_name, lineedit in self.weight_lineedits.items():
            new_weight = lineedit.text()
            self.products_dict[product_name][0] = int(new_weight)

        # Здесь можно добавить логику для сохранения обновленных данных о продуктах
        print("Вес продуктов обновлен.")
        self.close()

# Пример использования:
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = UpdateWeightDialog(dried_fruits)
    dialog.exec_()
