import requests

from PySide6.QtCore import Qt

from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QLineEdit,
    QMessageBox,
    QGridLayout,
    QComboBox,
    QHeaderView,
    QAbstractItemView
)


JUSTIFICATIONS_URL = "http://127.0.0.1:8000/justifications/"
EMPLOYEES_URL = "http://127.0.0.1:8000/employees"


class JustificationsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load_employees()

        self.load_justifications()

        self.current_month = datetime.now().month

        self.current_year = datetime.now().year

    # =========================================
    # UI
    # =========================================

    def setup_ui(self):

        self.setStyleSheet("""

            QWidget {

                background: #F4F6F8;

                color: #1E1E1E;

                font-family: 'Segoe UI';

                font-size: 13px;
            }

        """)

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            35,
            20,
            35,
            35
        )

        main_layout.setSpacing(24)

        self.setLayout(main_layout)

        # =========================================
        # HEADER
        # =========================================

        title = QLabel(
            "Justificativas"
        )

        title.setStyleSheet("""

            font-size: 34px;

            font-weight: 800;

            color: #1A1A1A;

        """)

        main_layout.addWidget(title)

        # =========================================
        # FILTROS
        # =========================================

        filter_card = QFrame()

        filter_card.setStyleSheet("""

        QFrame{

            background:white;

            border-radius:24px;

        }

        """)

        filter_layout = QHBoxLayout()

        filter_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        filter_layout.setSpacing(15)

        filter_card.setLayout(filter_layout)

        # Funcionário

        self.filter_employee = QComboBox()

        self.filter_employee.setMinimumHeight(45)

        self.filter_employee.setStyleSheet(
            self.combo_style()
        )

        self.filter_employee.addItem(
            "Todos",
            None
        )

        # Mês

        self.filter_month = QComboBox()

        self.filter_month.setMinimumHeight(45)

        self.filter_month.setStyleSheet(
            self.combo_style()
        )

        meses = [

            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro"

        ]

        for i, nome in enumerate(meses, start=1):

            self.filter_month.addItem(
                nome,
                i
            )

        # Ano

        self.filter_year = QComboBox()

        self.filter_year.setMinimumHeight(45)

        self.filter_year.setStyleSheet(
            self.combo_style()
        )

        for ano in range(2024, 2036):

            self.filter_year.addItem(
                str(ano)
            )

        hoje = datetime.now()

        self.filter_month.setCurrentIndex(
            hoje.month - 1
        )

        self.filter_year.setCurrentText(
            str(hoje.year)
        )

        # Botão

        self.search_button = QPushButton(
            "Pesquisar"
        )

        self.search_button.setMinimumHeight(45)

        self.search_button.setStyleSheet(
            self.green_button()
        )

        self.search_button.clicked.connect(
            self.search_month
        )

        filter_layout.addWidget(
            self.filter_employee,
            3
        )

        filter_layout.addWidget(
            self.filter_month,
            1
        )

        filter_layout.addWidget(
            self.filter_year,
            1
        )

        filter_layout.addWidget(
            self.search_button,
            1
        )

        main_layout.addWidget(
            filter_card
        )

        # =========================================
        # FORM CARD
        # =========================================

        form_card = QFrame()

        form_card.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 24px;

            }

        """)

        form_layout = QGridLayout()

        form_layout.setContentsMargins(
            22,
            22,
            22,
            22
        )

        form_layout.setHorizontalSpacing(16)

        form_layout.setVerticalSpacing(16)

        form_card.setLayout(
            form_layout
        )

        self.employee_input = QComboBox()

        self.employee_input.setMinimumHeight(
            50
        )

        self.employee_input.setStyleSheet(
            self.combo_style()
        )

        self.type_input = QComboBox()

        self.type_input.addItems([

            "Atestado Médico",

            "Declaração de Comparecimento",

            "Falta Justificada",

            "Folga Compensatória",

            "Férias",

            "Licença Médica",

            "Licença Maternidade",

            "Licença Paternidade",

            "Suspensão",

            "Outro"

        ])
        
        self.mode_input = QComboBox()

        self.mode_input.addItems([

            "Por Dia",

            "Por Hora"

        ])


        self.mode_input.currentTextChanged.connect(
            self.toggle_hour_fields
        )



        self.mode_input.setMinimumHeight(
            50
        )

        self.mode_input.setStyleSheet(
            self.combo_style()
        )

        self.type_input.setMinimumHeight(
            50
        )

        self.type_input.setStyleSheet(
            self.combo_style()
        )

        self.start_date_input = self.create_input(
            "Data Inicial (AAAA-MM-DD)"
        )

        self.end_date_input = self.create_input(
            "Data Final (AAAA-MM-DD)"
        )

        self.start_time_input = self.create_input(
            "Hora Inicial (08:00)"
        )

        self.end_time_input = self.create_input(
            "Hora Final (12:00)"
        )

        self.description_input = self.create_input(
            "Descrição"
        )

        form_layout.addWidget(
            self.employee_input,
            0,
            0
        )

        form_layout.addWidget(
            self.type_input,
            0,
            1
        )

        form_layout.addWidget(
            self.mode_input,
            0,
            2
        )

        form_layout.addWidget(
            self.start_date_input,
            1,
            0
        )

        form_layout.addWidget(
            self.end_date_input,
            1,
            1
        )

        form_layout.addWidget(
            self.start_time_input,
            1,
            2
        )

        form_layout.addWidget(
            self.end_time_input,
            1,
            3
        )

        form_layout.addWidget(
            self.description_input,
            2,
            0,
            1,
            2
        )

        self.save_button = QPushButton(
            "Salvar Justificativa"
        )

        self.save_button.setMinimumHeight(
            50
        )

        self.save_button.clicked.connect(
            self.create_justification
        )

        self.save_button.setStyleSheet(
            self.green_button()
        )

        form_layout.addWidget(
            self.save_button,
            3,
            0,
            1,
            2
        )

        main_layout.addWidget(
            form_card
        )


        # =========================================
        # TABLE CARD
        # =========================================

        table_card = QFrame()

        table_card.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 24px;

            }

        """)

        table_layout = QVBoxLayout()

        table_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        table_card.setLayout(
            table_layout
        )

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([

            "ID",

            "Funcionário",

            "Tipo",

            "Início",

            "Fim",

            "Descrição",

            "Ações"

        ])

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setMinimumHeight(
            450
        )

        table_layout.addWidget(
            self.table
        )

        main_layout.addWidget(
            table_card
        )
        

    

        self.toggle_hour_fields()


    # =========================================
    # INPUT
    # =========================================

    def create_input(self, placeholder):

        field = QLineEdit()

        field.setPlaceholderText(
            placeholder
        )

        field.setMinimumHeight(
            50
        )

        field.setStyleSheet("""

            QLineEdit {

                background: #F7F8FA;

                border: 1px solid #E5E7EB;

                border-radius: 14px;

                padding-left: 14px;

            }

        """)

        return field

    # =========================================
    # COMBO STYLE
    # =========================================

    def combo_style(self):

        return """

            QComboBox {

                background: #F7F8FA;

                border: 1px solid #E5E7EB;

                border-radius: 14px;

                padding-left: 14px;

            }

        """

    # =========================================
    # BUTTON
    # =========================================

    def green_button(self):

        return """

            QPushButton {

                background: #00C853;

                color: white;

                border: none;

                border-radius: 14px;

                font-weight: bold;

            }

            QPushButton:hover {

                background: #00B248;

            }

        """

    # =========================================
    # EMPLOYEES
    # =========================================

    def load_employees(self):

        try:

            response = requests.get(
                EMPLOYEES_URL
            )

            employees = response.json()

            self.employee_input.clear()

            for emp in employees:

                self.employee_input.addItem(

                    emp["name"],

                    emp["id"]

                )

            self.filter_employee.clear()

            self.filter_employee.addItem(
                "Todos",
                None
            )

            for emp in employees:

                self.filter_employee.addItem(

                    emp["name"],

                    emp["id"]

                )

        except Exception as e:

            print(e)

    # =========================================
    # CREATE
    # =========================================

    def create_justification(self):

        try:

            requests.post(

                JUSTIFICATIONS_URL,

               json={

                "employee_id":
                self.employee_input.currentData(),

                "start_date":
                self.start_date_input.text(),

                "end_date":
                self.end_date_input.text(),

                "justification_type":
                self.type_input.currentText(),

                "description":
                self.description_input.text(),

                "attachment":
                "",

                "mode":

                    "hour"

                    if self.mode_input.currentText()
                    == "Por Hora"

                    else

                    "day",

                "start_time":

                    self.start_time_input.text()

                    if self.mode_input.currentText()
                    == "Por Hora"

                    else

                    None,

                "end_time":

                    self.end_time_input.text()

                    if self.mode_input.currentText()
                    == "Por Hora"

                    else

                    None

            }

            )

            QMessageBox.information(

                self,

                "Sucesso",

                "Justificativa cadastrada."

            )

            self.load_justifications()

        except Exception as e:

            QMessageBox.critical(

                self,

                "Erro",

                str(e)

            )

    # =========================================
    # LOAD
    # =========================================

    def load_justifications(self):

        try:

            response = requests.get(
                JUSTIFICATIONS_URL
            )

            records = response.json()

            self.table.setRowCount(
                len(records)
            )

            for row, item in enumerate(records):

                self.table.setItem(
                    row,
                    0,
                    QTableWidgetItem(
                        str(item["id"])
                    )
                )

                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        str(item["employee_name"])
                    )
                )

                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        item["justification_type"]
                    )
                )

                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        item["start_date"]
                    )
                )

                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem(
                        item["end_date"]
                    )
                )

                self.table.setItem(
                    row,
                    5,
                    QTableWidgetItem(
                        item["description"] or ""
                    )
                )

                delete_button = QPushButton(
                    "🗑"
                )

                delete_button.clicked.connect(

                    lambda checked=False,
                    item_id=item["id"]:
                    self.delete_justification(
                        item_id
                    )

                )

                delete_button.setStyleSheet("""

                    QPushButton {

                        background: #FEE2E2;

                        border: none;

                        border-radius: 10px;

                    }

                """)

                self.table.setCellWidget(
                    row,
                    6,
                    delete_button
                )

        except Exception as e:

            print(e)

    # =========================================
    # DELETE
    # =========================================

    def delete_justification(self, item_id):

        requests.delete(

            f"{JUSTIFICATIONS_URL}{item_id}"

        )

        self.load_justifications()
    

    def search_month(self):

        month = self.filter_month.currentData()

        year = int(
            self.filter_year.currentText()
        )

        employee_id = self.filter_employee.currentData()

        url = f"http://127.0.0.1:8000/justifications/month/{year}/{month}"

        if employee_id:

            url += f"?employee_id={employee_id}"

        try:

            response = requests.get(url)

            records = response.json()

            self.table.setRowCount(len(records))

            for row, item in enumerate(records):

                self.table.setItem(
                    row, 0,
                    QTableWidgetItem(str(item["id"]))
                )

                self.table.setItem(
                    row, 1,
                    QTableWidgetItem(item["employee_name"])
                )

                self.table.setItem(
                    row, 2,
                    QTableWidgetItem(item["type"])
                )

                self.table.setItem(
                    row, 3,
                    QTableWidgetItem(item["start_date"])
                )

                self.table.setItem(
                    row, 4,
                    QTableWidgetItem(item["end_date"])
                )

                self.table.setItem(
                    row, 5,
                    QTableWidgetItem(item["description"] or "")
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    
    def toggle_hour_fields(self):

        show = (
            self.mode_input.currentText()
            == "Por Hora"
        )

        self.start_time_input.setVisible(
            show
        )

        self.end_time_input.setVisible(
            show
        )

    