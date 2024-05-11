import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QFileDialog, QSpinBox
from PyQt5.QtCore import Qt, QAbstractTableModel

class FruitTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.headers = ["Название", "Количество"]

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None

class FruitInventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Склад сухофруктов")
        self.setGeometry(100, 100, 800, 600)

        self.table_view = QTableView()
        self.load_button = QPushButton("Загрузить данные из CSV")
        self.load_button.clicked.connect(self.load_data)

        self.spinboxes = {}  # Словарь для хранения QSpinBox'ов

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.table_view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            with open(file_name, "r") as csv_file:
                reader = csv.reader(csv_file)
                data = [row for row in reader]
                model = FruitTableModel(data)
                self.table_view.setModel(model)

                # Создаем QSpinBox для каждого сухофрукта
                for row in data:
                    fruit_name = row[0]
                    spinbox = QSpinBox()
                    spinbox.setMinimum(0)
                    spinbox.setMaximum(1000)  # Установите максимальное значение по вашему усмотрению
                    self.spinboxes[fruit_name] = spinbox

                    # Добавляем QSpinBox в таблицу
                    self.table_view.setIndexWidget(model.index(data.index(row), 1), spinbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FruitInventoryApp()
    window.show()
    sys.exit(app.exec_())
