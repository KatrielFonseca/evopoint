import requests

from PySide6.QtCore import (
    Qt,
    QTimer
)

from PySide6.QtGui import (
    QColor,
    QFont
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QFrame,
    QLineEdit,
    QMessageBox,
    QGridLayout,
    QComboBox,
    QHeaderView,
    QAbstractItemView
)

API_URL = "http://127.0.0.1:8000/employees"
SCALES_URL = "http://127.0.0.1:8000/scales"
SETTINGS_URL = "http://127.0.0.1:8000/settings/"


class EmployeesPage(QWidget):

    def __init__(self):

        super().__init__()

        self.editing_employee_id = None

        self.setup_ui()

        self.load_company()

        self.load_scales()

        self.load_employees()

        # =========================================
        # AUTO REFRESH
        # =========================================

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.safe_reload
        )

        self.timer.start(3000)

    # =====================================================
    # SAFE RELOAD
    # =====================================================

    def safe_reload(self):

        try:

            if self.table.state() == QTableWidget.EditingState:

                return

            self.load_employees()

        except:
            pass

    # =====================================================
    # UI
    # =====================================================

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

        # =====================================================
        # HEADER
        # =====================================================

        header_layout = QHBoxLayout()

        title = QLabel("Funcionários")

        title.setStyleSheet("""

            font-size: 34px;

            font-weight: 800;

            color: #1A1A1A;

            background: transparent;

        """)

        refresh_button = QPushButton(
            "Atualizar"
        )

        refresh_button.clicked.connect(
            self.load_employees
        )

        refresh_button.setFixedHeight(48)

        refresh_button.setCursor(
            Qt.PointingHandCursor
        )

        refresh_button.setStyleSheet(
            self.green_button()
        )

        header_layout.addWidget(title)

        header_layout.addStretch()

        header_layout.addWidget(refresh_button)

        main_layout.addLayout(header_layout)

        # =====================================================
        # FORM CARD
        # =====================================================

        form_container = QFrame()

        form_container.setStyleSheet("""

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

        form_container.setLayout(
            form_layout
        )

        # =====================================================
        # INPUTS
        # =====================================================

        self.registration_input = self.create_input(
            "Matrícula automática"
        )

        self.registration_input.setReadOnly(
            True
        )

        self.registration_input.setStyleSheet("""

            QLineEdit {

                background: #EEF1F4;

                border: 1px solid #E3E6EA;

                border-radius: 14px;

                padding-left: 14px;

                font-size: 13px;

                color: #9CA3AF;
            }

        """)

        self.name_input = self.create_input(
            "Nome"
        )

        self.cpf_input = self.create_input(
            "CPF"
        )

        self.pis_input = self.create_input(
            "PIS"
        )

        self.rg_input = self.create_input(
            "RG"
        )


        # =====================================================
        # COMBOS
        # =====================================================

        self.company_input = self.create_input(
            "Empresa"
        )

        self.company_input.setReadOnly(True)

        self.department_input = self.create_input(
            "Departamento"
        )

        self.role_input = self.create_input(
            "Cargo"
        )

        self.schedule_input = self.create_combo([])

        # =====================================================
        # GRID
        # =====================================================

        form_layout.addWidget(
            self.registration_input,
            0,
            0
        )

        form_layout.addWidget(
            self.name_input,
            0,
            1
        )

        form_layout.addWidget(
            self.cpf_input,
            1,
            0
        )

        form_layout.addWidget(
            self.pis_input,
            1,
            1
        )

        form_layout.addWidget(
            self.rg_input,
            2,
            0
        )

        form_layout.addWidget(
            self.company_input,
            2,
            1
        )

        form_layout.addWidget(
            self.department_input,
            3,
            0
        )

        form_layout.addWidget(
            self.role_input,
            3,
            1
        )

        form_layout.addWidget(
            self.schedule_input,
            4,
            0
        )

        # =====================================================
        # SAVE BUTTON
        # =====================================================

        self.save_button = QPushButton(
            "Cadastrar Funcionário"
        )

        self.save_button.clicked.connect(
            self.create_employee
        )

        self.save_button.setMinimumHeight(50)

        self.save_button.setCursor(
            Qt.PointingHandCursor
        )

        self.save_button.setStyleSheet(
            self.green_button()
        )

        form_layout.addWidget(
            self.save_button,
            4,
            1
        )

        main_layout.addWidget(
            form_container
        )

        # =====================================================
        # TABLE CARD
        # =====================================================

        table_container = QFrame()

        table_container.setStyleSheet("""

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

        table_container.setLayout(
            table_layout
        )

        # =====================================================
        # TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([

            "ID",
            "Nome",
            "CPF",
            "Empresa",
            "Função",
            "Horário",
            "Ações"
        ])

        self.table.setStyleSheet("""

            QTableWidget {

                background: white;

                border: none;

                border-radius: 18px;

                gridline-color: transparent;

                font-size: 12px;

                color: #202020;
            }

            QHeaderView::section {

                background: #F8F9FB;

                border: none;

                border-bottom: 1px solid #ECECEC;

                padding: 14px;

                font-size: 12px;

                font-weight: 700;

                color: #202020;
            }

            QTableWidget::item {

                padding-left: 8px;

                padding-right: 8px;

                border-bottom: 1px solid #F3F3F3;
            }

            QTableWidget::item:selected {

                background: #F5F9FF;

                color: black;
            }

            QScrollBar:vertical {

                border: none;

                background: transparent;

                width: 10px;
            }

            QScrollBar::handle:vertical {

                background: #D1D5DB;

                border-radius: 5px;

                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {

                background: #BDBDBD;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {

                height: 0px;
            }

        """)

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setShowGrid(False)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setFocusPolicy(
            Qt.NoFocus
        )

        self.table.setAlternatingRowColors(
            False
        )

        self.table.setMinimumHeight(520)

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.table.verticalHeader().setDefaultSectionSize(
            58
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.Stretch
        )

        table_layout.addWidget(
            self.table
        )

        main_layout.addWidget(
            table_container
        )

    # =====================================================
    # INPUT
    # =====================================================

    def create_input(self, placeholder):

        field = QLineEdit()

        field.setPlaceholderText(
            placeholder
        )

        field.setMinimumHeight(50)

        field.setStyleSheet("""

            QLineEdit {

                background: #F7F8FA;

                border: 1px solid #E5E7EB;

                border-radius: 14px;

                padding-left: 14px;

                font-size: 13px;
            }

            QLineEdit:focus {

                border: 1px solid #00C853;
            }

        """)

        return field

    # =====================================================
    # COMBO
    # =====================================================

    def create_combo(self, items):

        combo = QComboBox()

        combo.addItems(items)

        combo.setMinimumHeight(50)

        combo.setStyleSheet("""

            QComboBox {

                background: #F7F8FA;

                border: 1px solid #E5E7EB;

                border-radius: 14px;

                padding-left: 14px;

                font-size: 13px;
            }

            QComboBox:hover {

                border: 1px solid #00C853;
            }

        """)

        return combo

    # =====================================================
    # GREEN BUTTON
    # =====================================================

    def green_button(self):

        return """

            QPushButton {

                background: #00C853;

                color: white;

                border: none;

                border-radius: 14px;

                padding: 14px 22px;

                font-size: 13px;

                font-weight: 700;
            }

            QPushButton:hover {

                background: #00B248;
            }

            QPushButton:pressed {

                background: #00963D;
            }

        """

    # =====================================================
    # LOAD EMPLOYEES
    # =====================================================

    def load_company(self):

        try:

            self.company_input.clear()

            response = requests.get(
                SETTINGS_URL
            )

            data = response.json()

            company_name = data.get(
                "company_name",
                ""
            )

            self.company_input.setText(
                company_name
            )

        except Exception as e:

            print(
                "ERRO LOAD COMPANY:",
                str(e)
            )

    def load_scales(self):

        try:

            self.schedule_input.clear()

            response = requests.get(
                SCALES_URL
            )

            scales = response.json()

            for scale in scales:

                self.schedule_input.addItem(
                    scale["name"]
                )

        except Exception as e:

            print(
                "ERRO LOAD SCALES:",
                str(e)
            )


    def load_employees(self):

        try:

            response = requests.get(
                API_URL
            )

            employees = response.json()

            self.table.setRowCount(
                len(employees)
            )

            for row, emp in enumerate(employees):

                values = [

                    str(emp.get("id", "")),
                    emp.get("name", ""),
                    emp.get("cpf", ""),
                    emp.get("company", ""),
                    emp.get("role", ""),
                    emp.get("schedule", "")
                ]

                for col, value in enumerate(values):

                    item = QTableWidgetItem(
                        value
                    )

                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                    item.setFlags(
                        Qt.ItemIsEnabled
                    )

                    self.table.setItem(
                        row,
                        col,
                        item
                    )

                # =====================================================
                # ACTIONS
                # =====================================================

                actions_widget = QWidget()

                actions_widget.setStyleSheet("""
                    background: transparent;
                """)

                actions_layout = QHBoxLayout()

                actions_layout.setContentsMargins(
                    0,
                    0,
                    0,
                    0
                )

                actions_layout.setSpacing(8)

                actions_layout.setAlignment(
                    Qt.AlignCenter
                )

                actions_widget.setLayout(
                    actions_layout
                )

                # =====================================================
                # EDIT BUTTON
                # =====================================================

                edit_button = QPushButton("✏")

                edit_button.setFixedSize(36, 36)

                edit_button.setCursor(
                    Qt.PointingHandCursor
                )

                edit_button.setStyleSheet("""

                    QPushButton {

                        background: #EEF4FF;

                        color: #2563EB;

                        border: none;

                        border-radius: 10px;

                        font-size: 14px;

                        font-weight: bold;
                    }

                    QPushButton:hover {

                        background: #DBEAFE;
                    }

                """)

                edit_button.clicked.connect(

                    lambda checked=False,
                    employee=emp:
                    self.edit_employee(employee)
                )

                # =====================================================
                # DELETE BUTTON
                # =====================================================

                delete_button = QPushButton("🗑")

                delete_button.setFixedSize(36, 36)

                delete_button.setCursor(
                    Qt.PointingHandCursor
                )

                delete_button.setStyleSheet("""

                    QPushButton {

                        background: #FEF2F2;

                        color: #DC2626;

                        border: none;

                        border-radius: 10px;

                        font-size: 13px;

                        font-weight: bold;
                    }

                    QPushButton:hover {

                        background: #FEE2E2;
                    }

                """)

                delete_button.clicked.connect(

                    lambda checked=False,
                    emp_id=emp["id"]:
                    self.delete_employee(emp_id)
                )

                actions_layout.addWidget(
                    edit_button
                )

                actions_layout.addWidget(
                    delete_button
                )

                self.table.setCellWidget(
                    row,
                    6,
                    actions_widget
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # =====================================================
    # CREATE / UPDATE
    # =====================================================

    def create_employee(self):

        try:

            if not self.name_input.text().strip():

                QMessageBox.warning(
                    self,
                    "Atenção",
                    "Digite o nome."
                )

                return

            data = {

                "name":
                self.name_input.text().strip(),

                "cpf":
                self.cpf_input.text().strip(),

                "pis":
                self.pis_input.text().strip(),

                "rg":
                self.rg_input.text().strip(),

                "company":
                self.company_input.text(),

                "department":
                self.department_input.text().strip(),

                "role":
                self.role_input.text().strip(),

                "schedule":
                self.schedule_input.currentText()
            }

            # =====================================================
            # UPDATE
            # =====================================================

            if self.editing_employee_id is not None:

                response = requests.put(

                    f"{API_URL}/{self.editing_employee_id}",

                    json=data
                )

            # =====================================================
            # CREATE
            # =====================================================

            else:

                response = requests.post(
                    API_URL,
                    json=data
                )

            if response.status_code in [200, 201]:

                QMessageBox.information(
                    self,
                    "Sucesso",
                    "Funcionário salvo!"
                )

                self.editing_employee_id = None

                self.save_button.setText(
                    "Cadastrar Funcionário"
                )

                self.clear_fields()

                self.load_employees()

            else:

                QMessageBox.critical(
                    self,
                    "Erro",
                    response.text
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_fields(self):

        self.registration_input.clear()

        self.name_input.clear()

        self.cpf_input.clear()

        self.pis_input.clear()

        self.rg_input.clear()

        self.load_company()

        self.department_input.clear()

        self.role_input.clear()

        self.schedule_input.setCurrentIndex(0)

    # =====================================================
    # DELETE
    # =====================================================

    def delete_employee(self, employee_id):

        confirm = QMessageBox.question(

            self,

            "Confirmar Exclusão",

            "Deseja realmente deletar este funcionário?"
        )

        if confirm != QMessageBox.Yes:
            return

        try:

            response = requests.delete(
                f"{API_URL}/{employee_id}"
            )

            if response.status_code == 200:

                self.load_employees()

                QMessageBox.information(
                    self,
                    "Sucesso",
                    "Funcionário deletado!"
                )

            else:

                QMessageBox.critical(
                    self,
                    "Erro",
                    response.text
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # =====================================================
    # EDIT
    # =====================================================

    def edit_employee(self, employee):

        self.editing_employee_id = employee["id"]

        self.registration_input.setText(
            str(employee.get("registration", ""))
        )

        self.name_input.setText(
            employee.get("name", "")
        )

        self.cpf_input.setText(
            employee.get("cpf", "")
        )

        self.pis_input.setText(
            employee.get("pis", "")
        )

        self.rg_input.setText(
            employee.get("rg", "")
        )

        self.company_input.setText(
            employee.get("company", "")
        )

        self.department_input.setText(
            employee.get("department", "")
        )

        self.role_input.setText(
            employee.get("role", "")
        )

        self.schedule_input.setCurrentText(
            employee.get("schedule", "")
        )

        self.save_button.setText(
            "Salvar Alterações"
        )

        QMessageBox.information(
            self,
            "Modo edição",
            "Funcionário carregado para edição."
        )