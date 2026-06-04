import requests

from PySide6.QtCore import Qt

from datetime import date

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QHeaderView
)

from PySide6.QtCore import (
    Qt,
    QDate
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

        filters = QFrame()

        filters_layout = QHBoxLayout()

        filters.setLayout(
            filters_layout
        )

        filters_layout.addWidget(
            QLabel("Início:")
        )

        self.start_date = QDateEdit()

        self.start_date.setCalendarPopup(
            True
        )

        today = date.today()

        first_day = date(
            today.year,
            today.month,
            1
        )

        self.start_date.setDate(
            QDate(
                first_day.year,
                first_day.month,
                first_day.day
            )
        )

        filters_layout.addWidget(
            self.start_date
        )

        filters_layout.addWidget(
            QLabel("Fim:")
        )

        self.end_date = QDateEdit()

        self.end_date.setCalendarPopup(
            True
        )

        self.end_date.setDate(
            QDate.currentDate()
        )

        filters_layout.addWidget(
            self.end_date
        )

        self.btn_refresh = QPushButton(
            "Atualizar"
        )

        self.btn_refresh.clicked.connect(
            self.load_data
        )

        filters_layout.addWidget(
            self.btn_refresh
        )

        layout.addWidget(
            filters
        )


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

        start_date = self.start_date.date().toString(
            "yyyy-MM-dd"
        )

        end_date = self.end_date.date().toString(
            "yyyy-MM-dd"
        )

        response = requests.get(

            API_URL,

            params={

                "start_date":
                    start_date,

                "end_date":
                    end_date

            }
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