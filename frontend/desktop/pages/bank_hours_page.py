import requests

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QHeaderView
)

API_URL = "http://127.0.0.1:8000/bank-hours"


class BankHoursPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load_data()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.setLayout(layout)

        title = QLabel("Banco de Horas")

        title.setStyleSheet("""

            font-size: 32px;
            font-weight: bold;

        """)

        layout.addWidget(title)

        card = QFrame()

        card.setStyleSheet("""

            QFrame {

                background: white;
                border-radius: 20px;

            }

        """)

        card_layout = QVBoxLayout()

        card.setLayout(card_layout)

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([

            "Funcionário",
            "Normais",
            "Extras",
            "Faltas",
            "Saldo"

        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        card_layout.addWidget(
            self.table
        )

        layout.addWidget(card)

    def load_data(self):

        response = requests.get(
            API_URL
        )

        data = response.json()

        self.table.setRowCount(
            len(data)
        )

        for row, item in enumerate(data):

            values = [

                item["name"],
                item["normal_hours"],
                item["extra_hours"],
                item["missing_hours"],
                item["balance"]

            ]

            for col, value in enumerate(values):

                table_item = QTableWidgetItem(
                    str(value)
                )

                table_item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    col,
                    table_item
                )