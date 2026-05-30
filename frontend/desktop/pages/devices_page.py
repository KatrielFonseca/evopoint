from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox
)

import requests


class DevicesPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setStyleSheet("""

            QWidget {

                background: #F4F6F8;

                color: #1E1E1E;

                font-family: 'Segoe UI';

            }

        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            35,
            20,
            35,
            35
        )

        layout.setSpacing(20)

        self.setLayout(layout)

        # ==========================
        # TÍTULO
        # ==========================

        title = QLabel(
            "Dispositivos"
        )

        title.setStyleSheet("""

            font-size: 34px;

            font-weight: 800;

        """)

        layout.addWidget(title)

        # ==========================
        # CARD
        # ==========================

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

        self.status_label = QLabel(
            "Status: Não verificado"
        )

        self.status_label.setStyleSheet("""

            font-size: 18px;

            font-weight: bold;

        """)

        card_layout.addWidget(
            self.status_label
        )

        # ==========================
        # BOTÕES
        # ==========================

        self.status_button = QPushButton(
            "Testar Conexão"
        )

        self.info_button = QPushButton(
            "Informações do Equipamento"
        )

        self.capacity_button = QPushButton(
            "Capacidade"
        )

        self.sync_time_button = QPushButton(
            "Sincronizar Hora"
        )

        self.clear_logs_button = QPushButton(
            "Limpar Logs"
        )

        buttons = [

            self.status_button,

            self.info_button,

            self.capacity_button,

            self.sync_time_button,

            self.clear_logs_button

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

            card_layout.addWidget(
                button
            )

        layout.addWidget(card)

        layout.addStretch()

        # ==========================
        # EVENTOS
        # ==========================

        self.status_button.clicked.connect(
            self.check_status
        )

        self.info_button.clicked.connect(
            self.device_info
        )

        self.capacity_button.clicked.connect(
            self.device_capacity
        )

        self.sync_time_button.clicked.connect(
            self.sync_time
        )

        self.clear_logs_button.clicked.connect(
            self.clear_logs
        )

    # ==========================
    # STATUS
    # ==========================

    def check_status(self):

        try:

            response = requests.get(
                "http://127.0.0.1:8000/device/status"
            )

            data = response.json()

            if data.get("online"):

                self.status_label.setText(
                    "Status: ONLINE"
                )

            else:

                self.status_label.setText(
                    "Status: OFFLINE"
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # ==========================
    # INFO
    # ==========================

    def device_info(self):

        try:

            response = requests.get(
                "http://127.0.0.1:8000/device/info"
            )

            data = response.json()

            info = f"""
    MODELO: EVO Facial

    NÚMERO DE SÉRIE:
    {data.get('sn', 'N/A')}

    ID DO DISPOSITIVO:
    {data.get('deviceid', 'N/A')}

    IDIOMA:
    {data.get('language', 'N/A')}

    VOLUME:
    {data.get('volume', 'N/A')}

    FORMATO DE DATA:
    {data.get('date_format', 'N/A')}

    FORMATO DE HORA:
    {data.get('time_format', 'N/A')}

    WEB SERVER:
    {data.get('webserverport', 'N/A')}

    USUÁRIOS MÁXIMOS:
    {data.get('managers', 'N/A')}

    RESULTADO:
    {"ONLINE" if data.get("result") else "OFFLINE"}
            """

            QMessageBox.information(

                self,

                "Informações do Equipamento",

                info

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Erro",

                str(e)

            )
    # ==========================
    # CAPACIDADE
    # ==========================

    def device_capacity(self):

        try:

            response = requests.get(
                "http://127.0.0.1:8000/device/capacity"
            )

            QMessageBox.information(

                self,

                "Capacidade",

                str(response.json())

            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # ==========================
    # SINCRONIZAR HORA
    # ==========================

    def sync_time(self):

        try:

            requests.post(
                "http://127.0.0.1:8000/device/sync-time"
            )

            QMessageBox.information(

                self,

                "Sucesso",

                "Hora sincronizada."

            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # ==========================
    # LIMPAR LOGS
    # ==========================

    def clear_logs(self):

        try:

            requests.post(
                "http://127.0.0.1:8000/device/clear-logs"
            )

            QMessageBox.information(

                self,

                "Sucesso",

                "Logs removidos."

            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )