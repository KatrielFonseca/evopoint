import requests

from PySide6.QtCore import (
    Qt,
    QTimer
)

from PySide6.QtGui import (
    QColor,
    QFont
)

import webbrowser
import tempfile
import os

from urllib.parse import quote

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QFrame,
    QMessageBox,
    QComboBox,
    QHeaderView,
    QAbstractItemView,
    QDateEdit,
    QDialog,
    QFormLayout,
    QLineEdit
    )

API_URL = "http://127.0.0.1:8000"


class RecordsPage(QWidget):

    def __init__(self):

        super().__init__()

        # =====================================
        # CONTROLE
        # =====================================

        self.loading_table = False

        # =====================================
        # UI
        # =====================================

        self.setup_ui()

        # =====================================
        # LOAD
        # =====================================

        self.load_employees()

        self.load_records()

        # =====================================
        # EVENTOS
        # =====================================

        self.table.cellChanged.connect(
            self.on_cell_changed
        )

        

        # =====================================
        # AUTO REFRESH
        # =====================================

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.safe_reload
        )

        self.timer.start(3000)

    # =================================================
    # UI
    # =================================================

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

        main_layout.setSpacing(22)

        self.setLayout(main_layout)

        # =================================================
        # HEADER
        # =================================================

        header_layout = QHBoxLayout()

        title = QLabel(
            "Registros de Ponto"
        )

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
            self.load_records
        )

        refresh_button.setCursor(
            Qt.PointingHandCursor
        )

        refresh_button.setMinimumHeight(48)

        refresh_button.setStyleSheet("""

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

        """)

        header_layout.addWidget(title)

        header_layout.addStretch()

        header_layout.addWidget(refresh_button)

        self.whatsapp_button = QPushButton(
            "Enviar WhatsApp"
        )

        self.whatsapp_button.setMinimumHeight(48)

        self.whatsapp_button.setStyleSheet("""

            QPushButton {

                background: #25D366;
                color: white;

                border: none;
                border-radius: 14px;

                padding: 14px 22px;

                font-size: 13px;
                font-weight: 700;
            }

            QPushButton:hover {

                background: #20BD5A;
            }

        """)

        self.whatsapp_button.clicked.connect(
            self.send_whatsapp
        )

        header_layout.addWidget(
            self.whatsapp_button
        )

        add_punch_button = QPushButton(
            "Adicionar Batida"
        )

        add_punch_button.clicked.connect(
            self.add_manual_punch
        )

        add_punch_button.setMinimumHeight(48)

        add_punch_button.setStyleSheet("""

            QPushButton {

                background: #1565C0;
                color: white;

                border: none;
                border-radius: 14px;

                padding: 14px 22px;

                font-size: 13px;
                font-weight: 700;
            }

        """)

        header_layout.addWidget(
            add_punch_button
        )

        main_layout.addLayout(header_layout)

        # =================================================
        # TOP CARD
        # =================================================

        top_card = QFrame()

        top_card.setStyleSheet("""

            QFrame {

                background: white;
                border-radius: 24px;
            }

        """)

        top_layout = QHBoxLayout()

        top_layout.setContentsMargins(
            22,
            22,
            22,
            22
        )

        top_layout.setSpacing(18)

        top_card.setLayout(top_layout)

        # =================================================
        # COMBO
        # =================================================

        self.employee_combo = QComboBox()
        from PySide6.QtCore import QDate

        self.start_date = QDateEdit()

        self.start_date.setCalendarPopup(
            True
        )

        self.start_date.setDate(
            QDate.currentDate().addMonths(-1)
        )

        self.start_date.setMinimumHeight(
            50
        )

        self.end_date = QDateEdit()

        self.end_date.setCalendarPopup(
            True
        )

        self.end_date.setDate(
            QDate.currentDate()
        )

        self.end_date.setMinimumHeight(
            50
        )

        self.employee_combo.setMinimumHeight(50)

        self.employee_combo.currentIndexChanged.connect(
            self.load_records
        )

        self.employee_combo.setStyleSheet("""

            QComboBox {

                background: #F7F8FA;

                border: 1px solid #E5E7EB;

                border-radius: 14px;

                padding-left: 14px;

                font-size: 13px;

                min-height: 50px;
            }

            QComboBox:hover {

                border: 1px solid #00C853;
            }

            QComboBox:focus {

                border: 1px solid #00C853;
            }

        """)

        top_layout.addWidget(
            self.employee_combo
        )

        top_layout.addWidget(
            self.start_date
        )

        top_layout.addWidget(
            self.end_date
        )

        # =================================================
        # PDF BUTTON
        # =================================================

        pdf_button = QPushButton(
            "Gerar PDF"
        )
        pdf_all_button = QPushButton(
            "PDF Todos"
        )

        pdf_all_button.setMinimumHeight(50)

        pdf_all_button.setCursor(
            Qt.PointingHandCursor
        )

        pdf_all_button.clicked.connect(
            self.generate_all_pdfs
        )

        pdf_all_button.setStyleSheet("""

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

        """)

        pdf_button.clicked.connect(
            self.generate_pdf
        )

        pdf_button.setMinimumHeight(50)

        pdf_button.setCursor(
            Qt.PointingHandCursor
        )

        pdf_button.setStyleSheet("""

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

        """)

        top_layout.addWidget(pdf_button)

        top_layout.addWidget(
            pdf_all_button
        )

        main_layout.addWidget(top_card)

        # =================================================
        # TABLE CARD
        # =================================================

        table_card = QFrame()

        table_card.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 24px;
            }

        """)

        table_layout = QVBoxLayout()

        table_layout.setContentsMargins(
            22,
            22,
            22,
            22
        )

        table_card.setLayout(table_layout)

        # =================================================
        # TABLE
        # =================================================

        self.table = QTableWidget()

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels([

            "Data",
            "Funcionário",
            "Entrada 1",
            "Saída 1",
            "Entrada 2",
            "Saída 2",
            "Entrada 3",
            "Saída 3",
            "Horas"
        ])

        self.table.setStyleSheet("""

            QTableWidget {

                background: white;

                border: none;

                border-radius: 18px;

                gridline-color: #EEEEEE;

                font-size: 12px;

                color: #1E1E1E;
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

                padding: 10px;
            }

            QTableWidget::item:selected {

                background: #E8F5E9;

                color: black;
            }

            QScrollBar:vertical {

                border: none;

                background: transparent;

                width: 10px;

                margin: 0px;
            }

            QScrollBar::handle:vertical {

                background: #D8D8D8;

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

        self.table.setShowGrid(True)

        self.table.setGridStyle(
            Qt.SolidLine
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked
        )

        self.table.setFocusPolicy(
            Qt.StrongFocus
        )

        self.table.keyPressEvent = self.table_key_press

        self.table.setAlternatingRowColors(
            False
        )

        self.table.setMinimumHeight(0)

        self.table.setMaximumHeight(450)

        self.table.setFixedHeight(450)

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.table.verticalHeader().setDefaultSectionSize(
            58
        )

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.Stretch
        )

        table_layout.addWidget(self.table)

        main_layout.addWidget(
            table_card,
            1
        )

    # =================================================
    # SAFE RELOAD
    # =================================================

    def safe_reload(self):

        try:

            if self.table.state() == QTableWidget.EditingState:
                return

            self.load_employees()

            self.load_records()

        except:
            pass

    # =================================================
    # LOAD EMPLOYEES
    # =================================================

    def load_employees(self):

        try:

            current = self.employee_combo.currentData()

            response = requests.get(
                f"{API_URL}/employees"
            )

            employees = response.json()

            self.employee_combo.blockSignals(True)

            self.employee_combo.clear()

            selected_index = 0

            for index, emp in enumerate(employees):

                self.employee_combo.addItem(

                    emp["name"],
                    emp["registration"]
                )

                if emp["registration"] == current:

                    selected_index = index

            self.employee_combo.setCurrentIndex(
                selected_index
            )

            self.employee_combo.blockSignals(False)

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # =================================================
    # LOAD RECORDS
    # =================================================

    def load_records(self):

        try:

            self.loading_table = True

            self.table.blockSignals(True)

            registration = (
                self.employee_combo.currentData()
            )

            if not registration:

                self.table.setRowCount(0)

                return

            response = requests.get(

                f"{API_URL}/timesheet/{registration}",

                params={

                    "start_date": self.start_date.date().toString("yyyy-MM-dd"),

                    "end_date": self.end_date.date().toString("yyyy-MM-dd")

                }

            )

            print(response.status_code)
            print(response.text)

            records = response.json()

            self.table.setRowCount(
                len(records)
            )

            for row, record in enumerate(records):

                # =====================================
                # DATA
                # =====================================

                item_data = QTableWidgetItem(
                    str(record["date"])
                )

                item_data.setFlags(
                    Qt.ItemIsEnabled
                )

                item_data.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(row, 0, item_data)

                # =====================================
                # FUNCIONARIO
                # =====================================

                item_employee = QTableWidgetItem(
                    str(record["employee"])
                )

                item_employee.setFlags(
                    Qt.ItemIsEnabled
                )

                item_employee.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    1,
                    item_employee
                )

                # =====================================
                # CAMPOS
                # =====================================

                campos = [

                    "entrada_1",
                    "saida_1",

                    "entrada_2",
                    "saida_2",

                    "entrada_3",
                    "saida_3"
                ]

                coluna = 2

                for campo in campos:

                    registro = record.get(campo)

                    texto = ""

                    record_id = None

                    if registro:

                        texto = registro["time"]

                        record_id = registro["id"]

                    item = QTableWidgetItem(
                        texto
                    )

                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                    item.setFlags(

                        Qt.ItemIsSelectable |
                        Qt.ItemIsEnabled |
                        Qt.ItemIsEditable
                    )

                    item.setData(

                        Qt.UserRole,

                        {

                            "record_id": record_id,

                            "campo": campo,

                            "date": record["date"],

                            "row": row,

                            "column": coluna
                        }
                    )

                    self.table.setItem(
                        row,
                        coluna,
                        item
                    )

                    coluna += 1

                # =====================================
                # HORAS
                # =====================================

                horas = str(
                    record["worked_hours"]
                )

                horas_item = QTableWidgetItem(
                    horas
                )

                horas_item.setFlags(
                    Qt.ItemIsEnabled
                )

                horas_item.setTextAlignment(
                    Qt.AlignCenter
                )

                horas_item.setFont(
                    QFont("Segoe UI", 11, QFont.Bold)
                )

                if horas >= "08:00":

                    horas_item.setBackground(
                        QColor("#00C853")
                    )

                    horas_item.setForeground(
                        QColor("white")
                    )

                else:

                    horas_item.setBackground(
                        QColor("#FF5252")
                    )

                    horas_item.setForeground(
                        QColor("white")
                    )

                self.table.setItem(
                    row,
                    8,
                    horas_item
                )

                


        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

        finally:

            self.table.blockSignals(False)

            self.loading_table = False

    # =================================================
    # CELL CHANGED
    # =================================================

    def on_cell_changed(self, row, column):

        if self.loading_table:
            return

        if column < 2 or column > 7:
            return

        try:

            item = self.table.item(
                row,
                column
            )

            if not item:
                return

            metadata = item.data(
                Qt.UserRole
            )

            if not metadata:
                return

            horario = item.text().strip()

            if len(horario) != 8:
                return

            record_id = metadata["record_id"]

            campo = metadata["campo"]

            date = metadata["date"]

            registration = (
                self.employee_combo.currentData()
            )

            employee_name = (
                self.employee_combo.currentText()
            )

            inout = 0

            if "saida" in campo:
                inout = 1

            self.timer.stop()

            # =====================================
            # UPDATE
            # =====================================

            if record_id:

                response = requests.put(

                    f"{API_URL}/time-records/{record_id}",

                    params={

                        "time": horario,
                        "inout": inout
                    }
                )

            # =====================================
            # CREATE
            # =====================================

            else:

                response = requests.post(

                    f"{API_URL}/time-records/manual",

                    params={

                        "registration":
                            registration,

                        "employee_name":
                            employee_name,

                        "date":
                            date,

                        "time":
                            horario,

                        "inout":
                            inout
                    }
                )

            if response.status_code != 200:

                QMessageBox.warning(
                    self,
                    "Erro",
                    response.text
                )

                return

            data = response.json()

            if not record_id:

                metadata["record_id"] = data["id"]

                item.setData(
                    Qt.UserRole,
                    metadata
                )

            self.recalculate_row(row)

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

        finally:

            self.timer.start(3000)

    # =================================================
    # RECALCULA
    # =================================================

    def recalculate_row(self, row):

        try:

            pares = [

                (2, 3),
                (4, 5),
                (6, 7)
            ]

            total_seconds = 0

            for entrada_col, saida_col in pares:

                entrada_item = self.table.item(
                    row,
                    entrada_col
                )

                saida_item = self.table.item(
                    row,
                    saida_col
                )

                if not entrada_item or not saida_item:
                    continue

                entrada = entrada_item.text().strip()

                saida = saida_item.text().strip()

                if len(entrada) != 8:
                    continue

                if len(saida) != 8:
                    continue

                h1, m1, s1 = map(
                    int,
                    entrada.split(":")
                )

                h2, m2, s2 = map(
                    int,
                    saida.split(":")
                )

                entrada_seg = (
                    h1 * 3600 +
                    m1 * 60 +
                    s1
                )

                saida_seg = (
                    h2 * 3600 +
                    m2 * 60 +
                    s2
                )

                diferenca = (
                    saida_seg -
                    entrada_seg
                )

                if diferenca > 0:

                    total_seconds += diferenca

            horas = total_seconds // 3600

            minutos = (
                total_seconds % 3600
            ) // 60

            resultado = (
                f"{horas:02}:{minutos:02}"
            )

            horas_item = QTableWidgetItem(
                resultado
            )

            horas_item.setFlags(
                Qt.ItemIsEnabled
            )

            horas_item.setTextAlignment(
                Qt.AlignCenter
            )

            horas_item.setFont(
                QFont("Segoe UI", 11, QFont.Bold)
            )

            if total_seconds >= 28800:

                horas_item.setBackground(
                    QColor("#00C853")
                )

                horas_item.setForeground(
                    QColor("white")
                )

            else:

                horas_item.setBackground(
                    QColor("#FF5252")
                )

                horas_item.setForeground(
                    QColor("white")
                )

            self.table.setItem(
                row,
                8,
                horas_item
            )

        except:
            pass

    # =================================================
    # PDF
    # =================================================

    def generate_pdf(self):

        try:

            registration = (
                self.employee_combo.currentData()
            )

            if not registration:

                QMessageBox.warning(
                    self,
                    "Atenção",
                    "Selecione um funcionário."
                )

                return

            start_date = self.start_date.date().toString(
                "yyyy-MM-dd"
            )

            end_date = self.end_date.date().toString(
                "yyyy-MM-dd"
            )

            response = requests.get(

            f"{API_URL}/timesheet/pdf/{registration}",

            params={

                "start_date": self.start_date.date().toString("yyyy-MM-dd"),

                "end_date": self.end_date.date().toString("yyyy-MM-dd")

            }

        )

            if response.status_code != 200:

                QMessageBox.warning(
                    self,
                    "Erro",
                    response.text
                )

                return

            import tempfile
            import os
            import webbrowser

            pdf_path = os.path.join(
                tempfile.gettempdir(),
                f"espelho_ponto_{registration}.pdf"
            )

            with open(pdf_path, "wb") as pdf_file:

                pdf_file.write(response.content)

            webbrowser.open(pdf_path)

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )


    def send_whatsapp(self):

        try:

            registration = (
                self.employee_combo.currentData()
            )

            if not registration:

                QMessageBox.warning(

                    self,

                    "WhatsApp",

                    "Selecione um funcionário."

                )

                return

            # ==========================
            # BUSCA FUNCIONÁRIO
            # ==========================

           

            employee = requests.get(
                f"{API_URL}/employees/{registration}"
            ).json()

            if not employee:

                QMessageBox.warning(

                    self,

                    "WhatsApp",

                    "Funcionário não encontrado."

                )

                return

            whatsapp = employee.get(
                "whatsapp"
            )

            if not whatsapp:

                QMessageBox.warning(

                    self,

                    "WhatsApp",

                    "Funcionário sem WhatsApp cadastrado."

                )

                return

            # ==========================
            # GERA PDF
            # ==========================

            start_date = self.start_date.date().toString(
                "yyyy-MM-dd"
            )

            end_date = self.end_date.date().toString(
                "yyyy-MM-dd"
            )

            pdf_response = requests.get(

                f"{API_URL}/timesheet/pdf/{registration}",

                params={

                    "start_date": start_date,

                    "end_date": end_date

                }

            )

            if pdf_response.status_code != 200:

                QMessageBox.warning(

                    self,

                    "Erro",

                    pdf_response.text

                )

                return

            pasta = os.path.join(

                tempfile.gettempdir(),

                "AVAPoint_PDFs"

            )

            os.makedirs(

                pasta,

                exist_ok=True

            )

            nome_arquivo = f"{registration}.pdf"

            pdf_path = os.path.join(

                pasta,

                nome_arquivo

            )

            with open(pdf_path, "wb") as f:

                f.write(
                    pdf_response.content
                )

            # ==========================
            # ABRE PASTA
            # ==========================

            os.startfile(pasta)

            # ==========================
            # ABRE WHATSAPP
            # ==========================

            mensagem = quote(

                "Olá, segue sua folha de ponto."

            )

            numero = "".join(

                c for c in whatsapp

                if c.isdigit()
            )

            webbrowser.open(

                f"https://wa.me/55{numero}?text={mensagem}"

            )

            QMessageBox.information(

                self,

                "WhatsApp",

                f"PDF gerado em:\n\n{pdf_path}\n\nArraste o arquivo para o WhatsApp."

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Erro",

                str(e)

            )
    
    # =================================================
    # PDF TODOS
    # =================================================

    def generate_all_pdfs(self):

        try:

            response = requests.get(
                f"{API_URL}/employees"
            )

            employees = response.json()

            if not employees:

                QMessageBox.warning(
                    self,
                    "AVAPoint",
                    "Nenhum funcionário encontrado."
                )

                return

            import tempfile
            import os
            import webbrowser

            from datetime import datetime

            nome_pasta = datetime.now().strftime(
                "PDFS_%d%m%Y_%H%M"
            )

            pasta = os.path.join(
                tempfile.gettempdir(),
                nome_pasta
            )

            os.makedirs(
                pasta,
                exist_ok=True
            )

            start_date = self.start_date.date().toString(
                "yyyy-MM-dd"
            )

            end_date = self.end_date.date().toString(
                "yyyy-MM-dd"
            )

            total = 0

            for employee in employees:

                registration = employee["registration"]

                pdf_response = requests.get(

                    f"{API_URL}/timesheet/pdf/{registration}",

                    params={

                        "start_date": start_date,

                        "end_date": end_date

                    }

                )

                if pdf_response.status_code == 200:

                    caminho = os.path.join(

                        pasta,

                        f"{registration}.pdf"

                    )

                    with open(
                        caminho,
                        "wb"
                    ) as f:

                        f.write(
                            pdf_response.content
                        )

                    total += 1

            QMessageBox.information(

                self,

                "AVAPoint",

                f"{total} PDFs gerados em:\n\n{pasta}"

            )

            webbrowser.open(pasta)

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )
    def delete_day(self, record):

        confirm = QMessageBox.question(

            self,

            "Excluir",

            f"Excluir todos os registros de {record['date']} ?"

        )

        if confirm != QMessageBox.Yes:
            return

        QMessageBox.information(

            self,

            "AVAPoint",

            "Backend de exclusão já está pronto.\nAgora vamos ligar o botão à API."

        )            

    # =================================================
    # DELETE REGISTRO
    # =================================================

    def delete_record(self, record_id):

        try:

            response = requests.delete(

                f"{API_URL}/time-records/{record_id}"

            )

            if response.status_code != 200:

                QMessageBox.warning(

                    self,

                    "Erro",

                    response.text

                )

                return

            self.load_records()

            QMessageBox.information(

                self,

                "Sucesso",

                "Registro excluído."

            )

        except Exception as e:

            QMessageBox.critical(

                self,

                "Erro",

                str(e)

            )    
    def table_key_press(self, event):

        if event.key() == Qt.Key_Delete:

            row = self.table.currentRow()
            col = self.table.currentColumn()

            if row < 0:
                return

            if col < 2 or col > 7:
                return

            item = self.table.item(row, col)

            if not item:
                return

            metadata = item.data(Qt.UserRole)

            if not metadata:
                return

            record_id = metadata.get("record_id")

            if not record_id:
                return

            confirm = QMessageBox.question(

                self,

                "Excluir Registro",

                f"Excluir o registro {item.text()} ?"

            )

            if confirm == QMessageBox.Yes:

                self.delete_record(record_id)

        else:

            QTableWidget.keyPressEvent(
                self.table,
                event
            )

    def add_manual_punch(self):

        dialog = QDialog(self)

        dialog.setWindowTitle(
            "Adicionar Batida"
        )

        layout = QFormLayout(dialog)

        date_edit = QDateEdit()

        date_edit.setCalendarPopup(True)

        date_edit.setDate(
            self.start_date.date()
        )

        time_edit = QLineEdit()

        time_edit.setPlaceholderText(
            "08:00:00"
        )

        layout.addRow(
            "Data:",
            date_edit
        )

        layout.addRow(
            "Hora:",
            time_edit
        )

        save_button = QPushButton(
            "Salvar"
        )

        layout.addWidget(
            save_button
        )

        def salvar():

            registration = (
                self.employee_combo.currentData()
            )

            employee_name = (
                self.employee_combo.currentText()
            )

            response = requests.post(

                f"{API_URL}/time-records/manual",

                params={

                    "registration":
                        registration,

                    "employee_name":
                        employee_name,

                    "date":
                        date_edit.date().toString(
                            "yyyy-MM-dd"
                        ),

                    "time":
                        time_edit.text(),

                    "inout":
                        0
                }
            )

            if response.status_code == 200:

                dialog.accept()

                self.load_records()

            else:

                QMessageBox.warning(
                    self,
                    "Erro",
                    response.text
                )

        save_button.clicked.connect(
            salvar
        )

        dialog.exec()