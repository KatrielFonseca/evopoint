from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox
)

import webbrowser


class ReportsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

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

        # =====================================
        # TÍTULO
        # =====================================

        title = QLabel("Relatórios")

        title.setStyleSheet("""

            font-size: 34px;

            font-weight: 800;

            color: #1A1A1A;

        """)

        main_layout.addWidget(title)

        # =====================================
        # CARD
        # =====================================

        card = QFrame()

        card.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 24px;

            }

        """)

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        card_layout.setSpacing(16)

        card.setLayout(card_layout)

        info = QLabel(
            "Selecione o relatório desejado."
        )

        info.setStyleSheet("""

            font-size: 16px;

            color: #666;

        """)

        card_layout.addWidget(info)

        # =====================================
        # BOTÕES
        # =====================================

        self.employees_button = QPushButton(
            "Relatório de Funcionários"
        )

        self.bank_hours_button = QPushButton(
            "Relatório de Banco de Horas"
        )

        self.extra_hours_button = QPushButton(
            "Relatório de Horas Extras"
        )

        self.absence_button = QPushButton(
            "Relatório de Faltas"
        )

        buttons = [

            self.employees_button,

            self.bank_hours_button,

            self.extra_hours_button,

            self.absence_button,


        ]

        for button in buttons:

            button.setMinimumHeight(52)

            button.setStyleSheet("""

                QPushButton {

                    background: #00C853;

                    color: white;

                    border: none;

                    border-radius: 14px;

                    font-size: 14px;

                    font-weight: bold;

                }

                QPushButton:hover {

                    background: #00B248;

                }

            """)

            card_layout.addWidget(button)

        main_layout.addWidget(card)

        main_layout.addStretch()

        # =====================================
        # EVENTOS
        # =====================================

        self.employees_button.clicked.connect(
            self.generate_employees_report
        )

        self.bank_hours_button.clicked.connect(
            self.generate_bank_hours_report
        )

        self.extra_hours_button.clicked.connect(
            self.generate_extra_hours_report
        )

        self.absence_button.clicked.connect(
            self.generate_absence_report
        )


    # =========================================
    # RELATÓRIO FUNCIONÁRIOS
    # =========================================

    def generate_employees_report(self):

        try:

            webbrowser.open(
                "http://127.0.0.1:8000/reports/employees"
            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Erro",

                str(e)

            )

    # =========================================
    # RELATÓRIO BANCO DE HORAS
    # =========================================

    def generate_bank_hours_report(self):

        try:

            webbrowser.open(

                "http://127.0.0.1:8000/reports/bank-hours"

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Erro",

                str(e)

            )

    # =========================================
    # RELATÓRIO HORAS EXTRAS
    # =========================================

    def generate_extra_hours_report(self):

        try:

            webbrowser.open(

                "http://127.0.0.1:8000/reports/extra-hours"

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Erro",

                str(e)

            )

    # =========================================
    # RELATÓRIO FALTAS
    # =========================================

    def generate_absence_report(self):

        try:

            webbrowser.open(

                "http://127.0.0.1:8000/reports/absences"

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Erro",

                str(e)

            )

   