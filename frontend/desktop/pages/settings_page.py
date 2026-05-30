import requests

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QMessageBox,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QScrollArea
)

SETTINGS_URL = "http://127.0.0.1:8000/settings/"
HOLIDAYS_URL = "http://127.0.0.1:8000/holidays"


class SettingsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load_settings()

        self.load_holidays()

    # =====================================
    # INPUT
    # =====================================

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

    # =====================================
    # CARD
    # =====================================

    def create_card(self, title):

        card = QFrame()

        card.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 24px;

            }

        """)

        layout = QGridLayout()

        layout.setContentsMargins(
            22,
            22,
            22,
            22
        )

        layout.setHorizontalSpacing(16)

        layout.setVerticalSpacing(16)

        card.setLayout(layout)

        title_label = QLabel(title)

        title_label.setStyleSheet("""

            font-size: 18px;

            font-weight: 700;

            color: #1A1A1A;

        """)

        layout.addWidget(
            title_label,
            0,
            0,
            1,
            2
        )

        return card, layout

    # =====================================
    # GREEN BUTTON
    # =====================================

    def green_button(self):

        return """

            QPushButton {

                background: #00C853;

                color: white;

                border: none;

                border-radius: 14px;

                padding: 14px;

                font-size: 13px;

                font-weight: 700;

            }

            QPushButton:hover {

                background: #00B248;

            }

        """

    # =====================================
    # UI
    # =====================================

    def setup_ui(self):

        self.setStyleSheet("""

            QWidget {

                background: #F4F6F8;

                color: #1E1E1E;

                font-family: 'Segoe UI';

            }

        """)

        root = QVBoxLayout(self)

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setFrameShape(QFrame.NoFrame)

        root.addWidget(scroll)

        content = QWidget()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(content)

        main_layout.setContentsMargins(
            35,
            20,
            35,
            35
        )

        main_layout.setSpacing(24)

        title = QLabel("Configurações")

        title.setStyleSheet("""

            font-size: 34px;

            font-weight: 800;

            color: #1A1A1A;

        """)

        main_layout.addWidget(title)

        # =====================================
        # EMPRESA
        # =====================================

        company_card, company = self.create_card(
            "🏢 Dados da Empresa"
        )

        self.company_name = self.create_input(
            "Razão Social"
        )

        self.trade_name = self.create_input(
            "Nome Fantasia"
        )

        self.cnpj = self.create_input(
            "CNPJ"
        )

        self.state_registration = self.create_input(
            "Inscrição Estadual"
        )

        self.municipal_registration = self.create_input(
            "Inscrição Municipal"
        )

        company.addWidget(self.company_name,1,0)
        company.addWidget(self.trade_name,1,1)
        company.addWidget(self.cnpj,2,0)
        company.addWidget(self.state_registration,2,1)
        company.addWidget(self.municipal_registration,3,0)

        main_layout.addWidget(company_card)

        # =====================================
        # CONTATO
        # =====================================

        contact_card, contact = self.create_card(
            "📞 Contato"
        )

        self.phone = self.create_input(
            "Telefone"
        )

        self.email = self.create_input(
            "E-mail"
        )

        self.responsible = self.create_input(
            "Responsável"
        )

        contact.addWidget(self.phone,1,0)
        contact.addWidget(self.email,1,1)
        contact.addWidget(self.responsible,2,0)

        main_layout.addWidget(contact_card)

        # =====================================
        # ENDEREÇO
        # =====================================

        address_card, address = self.create_card(
            "📍 Endereço"
        )

        self.address = self.create_input(
            "Endereço"
        )

        self.number = self.create_input(
            "Número"
        )

        self.district = self.create_input(
            "Bairro"
        )

        self.city = self.create_input(
            "Cidade"
        )

        self.state = self.create_input(
            "Estado"
        )

        self.zip_code = self.create_input(
            "CEP"
        )

        address.addWidget(self.address,1,0)
        address.addWidget(self.number,1,1)
        address.addWidget(self.district,2,0)
        address.addWidget(self.city,2,1)
        address.addWidget(self.state,3,0)
        address.addWidget(self.zip_code,3,1)

        main_layout.addWidget(address_card)

        # =====================================
        # EVO
        # =====================================

        evo_card, evo = self.create_card(
            "🖥 EVO Facial"
        )

        self.evo_ip = self.create_input(
            "IP do EVO"
        )

        self.evo_port = self.create_input(
            "Porta"
        )

        self.evo_password = self.create_input(
            "Senha"
        )

        evo.addWidget(self.evo_ip,1,0)
        evo.addWidget(self.evo_port,1,1)
        evo.addWidget(self.evo_password,2,0)

        self.test_button = QPushButton(
            "Testar Conexão"
        )

        self.test_button.setStyleSheet(
            self.green_button()
        )

        evo.addWidget(
            self.test_button,
            2,
            1
        )

        main_layout.addWidget(evo_card)

        # =====================================
        # SERVIDOR
        # =====================================

        server_card, server = self.create_card(
            "🌐 Servidor EVOPoint"
        )

        self.server_ip = self.create_input(
            "IP do Servidor"
        )

        self.server_port = self.create_input(
            "Porta"
        )

        server.addWidget(
            self.server_ip,
            1,
            0
        )

        server.addWidget(
            self.server_port,
            1,
            1
        )

        main_layout.addWidget(server_card)

                # =====================================
        # FERIADOS
        # =====================================

        holiday_card, holiday = self.create_card(
            "🎉 Feriados"
        )

        self.holiday_date = self.create_input(
            "AAAA-MM-DD"
        )

        self.holiday_description = self.create_input(
            "Descrição do feriado"
        )

        holiday.addWidget(
            self.holiday_date,
            1,
            0
        )

        holiday.addWidget(
            self.holiday_description,
            1,
            1
        )

        self.add_holiday_button = QPushButton(
            "Adicionar"
        )

        self.add_holiday_button.setStyleSheet(
            self.green_button()
        )

        holiday.addWidget(
            self.add_holiday_button,
            2,
            0
        )

        self.delete_holiday_button = QPushButton(
            "Excluir Selecionado"
        )

        self.delete_holiday_button.setStyleSheet(
            self.green_button()
        )

        holiday.addWidget(
            self.delete_holiday_button,
            2,
            1
        )

        self.holiday_table = QTableWidget()

        self.holiday_table.setColumnCount(3)

        self.holiday_table.setHorizontalHeaderLabels([
            "ID",
            "Data",
            "Descrição"
        ])

        self.holiday_table.verticalHeader().setVisible(
            False
        )

        self.holiday_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.holiday_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.holiday_table.setMinimumHeight(
            250
        )

        holiday.addWidget(
            self.holiday_table,
            3,
            0,
            1,
            2
        )

        main_layout.addWidget(
            holiday_card
        )

        # =====================================
        # BANCO DE HORAS
        # =====================================

        bank_card, bank = self.create_card(
            "⏱ Banco de Horas"
        )

        self.recalculate_button = QPushButton(
            "Recalcular Banco"
        )

        self.recalculate_button.setStyleSheet(
            self.green_button()
        )

        self.reset_button = QPushButton(
            "Zerar Banco"
        )

        self.reset_button.setStyleSheet(
            self.green_button()
        )

        bank.addWidget(
            self.recalculate_button,
            1,
            0
        )

        bank.addWidget(
            self.reset_button,
            1,
            1
        )

        main_layout.addWidget(
            bank_card
        )

        # =====================================
        # SALVAR
        # =====================================

        self.save_button = QPushButton(
            "Salvar Configurações"
        )

        self.save_button.setMinimumHeight(
            54
        )

        self.save_button.setStyleSheet(
            self.green_button()
        )

        main_layout.addWidget(
            self.save_button
        )

        # =====================================
        # EVENTOS
        # =====================================

        self.save_button.clicked.connect(
            self.save_settings
        )

        self.add_holiday_button.clicked.connect(
            self.add_holiday
        )

        self.delete_holiday_button.clicked.connect(
            self.delete_holiday
        )

        self.test_button.clicked.connect(
            self.test_connection
        )

        self.recalculate_button.clicked.connect(
            self.recalculate_bank
        )

        self.reset_button.clicked.connect(
            self.reset_bank
        )

    # =====================================
    # LOAD SETTINGS
    # =====================================

    def load_settings(self):

        try:

            response = requests.get(
                SETTINGS_URL
            )

            data = response.json()

            self.company_name.setText(
                data.get("company_name", "")
            )

            self.trade_name.setText(
                data.get("trade_name", "")
            )

            self.cnpj.setText(
                data.get("cnpj", "")
            )

            self.state_registration.setText(
                data.get("state_registration", "")
            )

            self.municipal_registration.setText(
                data.get("municipal_registration", "")
            )

            self.phone.setText(
                data.get("phone", "")
            )

            self.email.setText(
                data.get("email", "")
            )

            self.responsible.setText(
                data.get("responsible", "")
            )

            self.address.setText(
                data.get("address", "")
            )

            self.number.setText(
                data.get("number", "")
            )

            self.district.setText(
                data.get("district", "")
            )

            self.city.setText(
                data.get("city", "")
            )

            self.state.setText(
                data.get("state", "")
            )

            self.zip_code.setText(
                data.get("zip_code", "")
            )

            self.evo_ip.setText(
                data.get("evo_ip", "")
            )

            self.evo_password.setText(
                data.get("evo_password", "")
            )

            self.evo_port.setText(
                data.get("evo_port", "")
            )

            self.server_ip.setText(
                data.get("server_ip", "")
            )

            self.server_port.setText(
                data.get("server_port", "")
            )

        except Exception as e:

            print(e)

    # =====================================
    # SAVE SETTINGS
    # =====================================

    def save_settings(self):

        try:

            requests.post(

                SETTINGS_URL,

                json={

                    "company_name": self.company_name.text(),
                    "trade_name": self.trade_name.text(),
                    "cnpj": self.cnpj.text(),
                    "state_registration": self.state_registration.text(),
                    "municipal_registration": self.municipal_registration.text(),
                    "phone": self.phone.text(),
                    "email": self.email.text(),
                    "responsible": self.responsible.text(),
                    "address": self.address.text(),
                    "number": self.number.text(),
                    "district": self.district.text(),
                    "city": self.city.text(),
                    "state": self.state.text(),
                    "zip_code": self.zip_code.text(),
                    "evo_ip": self.evo_ip.text(),
                    "evo_password": self.evo_password.text(),
                    "evo_port": self.evo_port.text(),
                    "server_ip": self.server_ip.text(),
                    "server_port": self.server_port.text()

                }

            )

            QMessageBox.information(
                self,
                "Sucesso",
                "Configurações salvas."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # =====================================
    # HOLIDAYS
    # =====================================

    def load_holidays(self):

        try:

            response = requests.get(
                HOLIDAYS_URL
            )

            holidays = response.json()

            self.holiday_table.setRowCount(
                len(holidays)
            )

            for row, holiday in enumerate(holidays):

                self.holiday_table.setItem(
                    row,
                    0,
                    QTableWidgetItem(
                        str(holiday["id"])
                    )
                )

                self.holiday_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        holiday["date"]
                    )
                )

                self.holiday_table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        holiday["description"]
                    )
                )

        except Exception as e:

            print(e)

    def add_holiday(self):

        try:

            requests.post(

                HOLIDAYS_URL,

                json={

                    "date":
                    self.holiday_date.text(),

                    "description":
                    self.holiday_description.text()

                }

            )

            self.load_holidays()

            self.holiday_date.clear()

            self.holiday_description.clear()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    def delete_holiday(self):

        row = self.holiday_table.currentRow()

        if row < 0:

            return

        holiday_id = self.holiday_table.item(
            row,
            0
        ).text()

        requests.delete(
            f"{HOLIDAYS_URL}/{holiday_id}"
        )

        self.load_holidays()

    # =====================================
    # EVO
    # =====================================

    def test_connection(self):

        QMessageBox.information(
            self,
            "EVO",
            "Conexão testada."
        )

    # =====================================
    # BANCO
    # =====================================

    def recalculate_bank(self):

        requests.post(
            "http://127.0.0.1:8000/bank-hours/recalculate"
        )

        QMessageBox.information(
            self,
            "Banco",
            "Banco recalculado."
        )

    def reset_bank(self):

        confirm = QMessageBox.question(
            self,
            "Confirmação",
            "Deseja zerar o banco?"
        )

        if confirm != QMessageBox.Yes:

            return

        requests.post(
            "http://127.0.0.1:8000/bank-hours/reset"
        )

        QMessageBox.information(
            self,
            "Banco",
            "Banco zerado."
        )