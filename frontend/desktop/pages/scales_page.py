import requests

from PySide6.QtCore import (
    Qt,
    QTimer
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
    QCheckBox,
    QHeaderView,
    QAbstractItemView,
    QDialog,
    QTableWidget,
    QTableWidgetItem
)

API_URL = "http://127.0.0.1:8000/scales"
SCALE_DAYS_URL = "http://127.0.0.1:8000/scale-days"



class ScaleDaysDialog(QDialog):

    def __init__(
        self,
        scale_id,
        scale_name,
        parent=None
    ):


        self.scale_id = scale_id

        self.scale_name = scale_name

        super().__init__(parent)

        self.setWindowTitle(
            "Configuração Individual de Dias"
        )

        self.resize(900, 500)

        layout = QVBoxLayout()

        self.setLayout(layout)

        title = QLabel(
            f"Configuração dos Dias - {scale_name}"
        )

        title.setStyleSheet(
            "font-size:22px;font-weight:bold;"
        )

        layout.addWidget(title)

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([

            "Dia",
            "Entrada 1",
            "Saída 1",
            "Entrada 2",
            "Saída 2",
            "Entrada 3",
            "Saída 3"

        ])

        self.table.setRowCount(7)

        for row in range(7):

            for col in range(1, 7):

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem("")
                )

        dias = [
            "SEG",
            "TER",
            "QUA",
            "QUI",
            "SEX",
            "SAB",
            "DOM"
        ]

        for row, dia in enumerate(dias):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(dia)
            )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(
            self.table
        )

        salvar = QPushButton(
            "Salvar Dias"
        )

        salvar.clicked.connect(
            self.save_days
        )

        layout.addWidget(
            salvar
        )


        self.load_days()


    def save_days(self):

        try:

            dias = [
                "MONDAY",
                "TUESDAY",
                "WEDNESDAY",
                "THURSDAY",
                "FRIDAY",
                "SATURDAY",
                "SUNDAY"
            ]

            for row, day_name in enumerate(dias):

                data = {

                    "scale_id": self.scale_id,

                    "day_name": day_name,

                    "entry_1": self.get_text(row, 1),

                    "exit_1": self.get_text(row, 2),

                    "entry_2": self.get_text(row, 3),

                    "exit_2": self.get_text(row, 4),

                    "entry_3": self.get_text(row, 5),

                    "exit_3": self.get_text(row, 6)

                }

                response = requests.post(
                    SCALE_DAYS_URL,
                    json=data
                )

                print("STATUS:", response.status_code)
                print("RESPOSTA:", response.text)

            QMessageBox.information(
                self,
                "Sucesso",
                "Dias salvos com sucesso."
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )


    def get_text(self, row, col):

        item = self.table.item(
            row,
            col
        )

        if item:

            return item.text().strip()

        return None
    

    def load_days(self):

        try:

            response = requests.get(
                f"{SCALE_DAYS_URL}/{self.scale_id}"
            )

            if response.status_code != 200:

                return

            days = response.json()

            row_map = {

                "MONDAY": 0,
                "TUESDAY": 1,
                "WEDNESDAY": 2,
                "THURSDAY": 3,
                "FRIDAY": 4,
                "SATURDAY": 5,
                "SUNDAY": 6

            }

            for day in days:

                row = row_map.get(
                    day["day_name"]
                )

                if row is None:

                    continue

                self.table.item(
                    row,
                    1
                ).setText(
                    day.get("entry_1") or ""
                )

                self.table.item(
                    row,
                    2
                ).setText(
                    day.get("exit_1") or ""
                )

                self.table.item(
                    row,
                    3
                ).setText(
                    day.get("entry_2") or ""
                )

                self.table.item(
                    row,
                    4
                ).setText(
                    day.get("exit_2") or ""
                )

                self.table.item(
                    row,
                    5
                ).setText(
                    day.get("entry_3") or ""
                )

                self.table.item(
                    row,
                    6
                ).setText(
                    day.get("exit_3") or ""
                )

        except Exception as e:

            print("ERRO LOAD DAYS:", e)


class ScalesPage(QWidget):

    def __init__(self):

        super().__init__()

        self.editing_scale_id = None

        self.setup_ui()

        self.load_scales()

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.safe_reload
        )

        self.timer.start(3000)

    # =========================================
    # SAFE RELOAD
    # =========================================

    def safe_reload(self):

        try:

            if self.table.state() == QTableWidget.EditingState:

                return

            self.load_scales()

        except:
            pass

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

        header_layout = QHBoxLayout()

        title = QLabel("Escalas")

        title.setStyleSheet("""

            font-size: 34px;

            font-weight: 800;

            color: #1A1A1A;

        """)

        refresh_button = QPushButton(
            "Atualizar"
        )

        refresh_button.clicked.connect(
            self.load_scales
        )

        refresh_button.setStyleSheet(
            self.green_button()
        )

        refresh_button.setFixedHeight(48)

        header_layout.addWidget(title)

        header_layout.addStretch()

        header_layout.addWidget(refresh_button)

        main_layout.addLayout(
            header_layout
        )

        # =========================================
        # CARD
        # =========================================

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

        form_container.setLayout(
            form_layout
        )

        self.name_input = self.create_input(
            "Nome da Escala"
        )

        form_layout.addWidget(
            self.name_input,
            0,
            0,
            1,
            4
        )

        # =========================================
        # DIAS
        # =========================================

        self.monday = QCheckBox("SEG")
        self.tuesday = QCheckBox("TER")
        self.wednesday = QCheckBox("QUA")
        self.thursday = QCheckBox("QUI")
        self.friday = QCheckBox("SEX")
        self.saturday = QCheckBox("SAB")
        self.sunday = QCheckBox("DOM")

        for day in [

            self.monday,
            self.tuesday,
            self.wednesday,
            self.thursday,
            self.friday,
            self.saturday,
            self.sunday

        ]:

            day.setChecked(True)

        self.saturday.setChecked(False)
        self.sunday.setChecked(False)

        days_layout = QHBoxLayout()

        days_layout.addWidget(self.monday)
        days_layout.addWidget(self.tuesday)
        days_layout.addWidget(self.wednesday)
        days_layout.addWidget(self.thursday)
        days_layout.addWidget(self.friday)
        days_layout.addWidget(self.saturday)
        days_layout.addWidget(self.sunday)

        form_layout.addLayout(
            days_layout,
            1,
            0,
            1,
            4
        )

        # =========================================
        # HORÁRIOS
        # =========================================

        self.entry1 = self.create_input("Entrada 1")
        self.exit1 = self.create_input("Saída 1")

        self.entry2 = self.create_input("Entrada 2")
        self.exit2 = self.create_input("Saída 2")

        self.entry3 = self.create_input("Entrada 3")
        self.exit3 = self.create_input("Saída 3")

        form_layout.addWidget(self.entry1, 2, 0)
        form_layout.addWidget(self.exit1, 2, 1)

        form_layout.addWidget(self.entry2, 2, 2)
        form_layout.addWidget(self.exit2, 2, 3)

        form_layout.addWidget(self.entry3, 3, 0)
        form_layout.addWidget(self.exit3, 3, 1)

        self.save_button = QPushButton(
            "Cadastrar Escala"
        )


        self.days_button = QPushButton(
            "Configurar Dias"
        )

        self.days_button.setMinimumHeight(50)

        self.days_button.setStyleSheet(
            self.green_button()
        )

        self.days_button.clicked.connect(
            self.configure_days
        )



        self.save_button.clicked.connect(
            self.save_scale
        )

        self.save_button.setStyleSheet(
            self.green_button()
        )

        self.save_button.setMinimumHeight(50)

        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(
            self.save_button
        )

        buttons_layout.addWidget(
            self.days_button
        )

        form_layout.addLayout(
            buttons_layout,
            3,
            2,
            1,
            2
        )

        main_layout.addWidget(
            form_container
        )

        # =========================================
        # TABELA
        # =========================================

        table_container = QFrame()

        table_container.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 24px;
            }

        """)

        table_layout = QVBoxLayout()

        table_container.setLayout(
            table_layout
        )

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([

            "ID",
            "Escala",
            "Dias",
            "Horários",
            "Ações"

        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setShowGrid(False)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        table_layout.addWidget(
            self.table
        )

        main_layout.addWidget(
            table_container
        )

    # =========================================
    # INPUT
    # =========================================

    def create_input(self, placeholder):

        field = QLineEdit()

        field.setPlaceholderText(
            placeholder
        )

        field.setMinimumHeight(48)

        return field

    # =========================================
    # BUTTON STYLE
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

        """

        # =========================================
    # LOAD SCALES
    # =========================================

    def load_scales(self):

        try:

            response = requests.get(
                API_URL
            )

            scales = response.json()

            self.table.setRowCount(
                len(scales)
            )

            for row, scale in enumerate(scales):

                days = []

                if scale.get("monday"):
                    days.append("SEG")

                if scale.get("tuesday"):
                    days.append("TER")

                if scale.get("wednesday"):
                    days.append("QUA")

                if scale.get("thursday"):
                    days.append("QUI")

                if scale.get("friday"):
                    days.append("SEX")

                if scale.get("saturday"):
                    days.append("SAB")

                if scale.get("sunday"):
                    days.append("DOM")

                horarios = []

                if scale.get("entry_1"):

                    horarios.append(
                        f"{scale.get('entry_1')} - {scale.get('exit_1')}"
                    )

                if scale.get("entry_2"):

                    horarios.append(
                        f"{scale.get('entry_2')} - {scale.get('exit_2')}"
                    )

                if scale.get("entry_3"):

                    horarios.append(
                        f"{scale.get('entry_3')} - {scale.get('exit_3')}"
                    )

                values = [

                    str(scale.get("id", "")),

                    scale.get("name", ""),

                    " ".join(days),

                    " | ".join(horarios)

                ]

                for col, value in enumerate(values):

                    item = QTableWidgetItem(
                        str(value)
                    )

                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                    self.table.setItem(
                        row,
                        col,
                        item
                    )

                # =====================================
                # ACTIONS
                # =====================================

                actions_widget = QWidget()

                actions_layout = QHBoxLayout()

                actions_layout.setContentsMargins(
                    0,
                    0,
                    0,
                    0
                )

                actions_layout.setSpacing(8)

                actions_widget.setLayout(
                    actions_layout
                )
                
                days_button = QPushButton("📅")

                days_button.setFixedSize(
                    36,
                    36
                )

                days_button.clicked.connect(

                    lambda checked=False,
                    scale=scale:
                    self.configure_scale_days(scale)

                )

                edit_button = QPushButton("✏")

                edit_button.setFixedSize(
                    36,
                    36
                )

                edit_button.clicked.connect(

                    lambda checked=False,
                    scale=scale:
                    self.edit_scale(scale)

                )

                delete_button = QPushButton("🗑")

                delete_button.setFixedSize(
                    36,
                    36
                )

                delete_button.clicked.connect(

                    lambda checked=False,
                    scale_id=scale["id"]:
                    self.delete_scale(scale_id)

                )

                actions_layout.addWidget(
                    days_button
                )

                actions_layout.addWidget(
                    edit_button
                )

                actions_layout.addWidget(
                    delete_button
                )

                self.table.setCellWidget(
                    row,
                    4,
                    actions_widget
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # =========================================
    # SAVE SCALE
    # =========================================

    def save_scale(self):

        try:

            data = {

                "name":
                self.name_input.text().strip(),

                "monday":
                self.monday.isChecked(),

                "tuesday":
                self.tuesday.isChecked(),

                "wednesday":
                self.wednesday.isChecked(),

                "thursday":
                self.thursday.isChecked(),

                "friday":
                self.friday.isChecked(),

                "saturday":
                self.saturday.isChecked(),

                "sunday":
                self.sunday.isChecked(),

                "entry_1":
                self.entry1.text().strip(),

                "exit_1":
                self.exit1.text().strip(),

                "entry_2":
                self.entry2.text().strip(),

                "exit_2":
                self.exit2.text().strip(),

                "entry_3":
                self.entry3.text().strip() or None,

                "exit_3":
                self.exit3.text().strip() or None
            }

            if self.editing_scale_id:

                response = requests.put(

                    f"{API_URL}/{self.editing_scale_id}",

                    json=data
                )

            else:

                response = requests.post(
                    API_URL,
                    json=data
                )

            if response.status_code in [200, 201]:

                QMessageBox.information(
                    self,
                    "Sucesso",
                    "Escala salva!"
                )

                self.clear_fields()

                self.load_scales()

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

    # =========================================
    # EDIT SCALE
    # =========================================

    def edit_scale(self, scale):

        self.editing_scale_id = scale["id"]

        self.name_input.setText(
            scale.get("name", "")
        )

        self.monday.setChecked(
            scale.get("monday", False)
        )

        self.tuesday.setChecked(
            scale.get("tuesday", False)
        )

        self.wednesday.setChecked(
            scale.get("wednesday", False)
        )

        self.thursday.setChecked(
            scale.get("thursday", False)
        )

        self.friday.setChecked(
            scale.get("friday", False)
        )

        self.saturday.setChecked(
            scale.get("saturday", False)
        )

        self.sunday.setChecked(
            scale.get("sunday", False)
        )

        self.entry1.setText(
            scale.get("entry_1", "")
        )

        self.exit1.setText(
            scale.get("exit_1", "")
        )

        self.entry2.setText(
            scale.get("entry_2", "")
        )

        self.exit2.setText(
            scale.get("exit_2", "")
        )

        self.entry3.setText(
            scale.get("entry_3") or ""
        )

        self.exit3.setText(
            scale.get("exit_3") or ""
        )

        self.save_button.setText(
            "Salvar Alterações"
        )

    # =========================================
    # DELETE SCALE
    # =========================================

    def delete_scale(self, scale_id):

        confirm = QMessageBox.question(

            self,

            "Excluir",

            "Deseja remover esta escala?"
        )

        if confirm != QMessageBox.Yes:

            return

        try:

            response = requests.delete(

                f"{API_URL}/{scale_id}"

            )

            if response.status_code == 200:

                self.load_scales()

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

    # =========================================
    # CLEAR
    # =========================================

    def clear_fields(self):

        self.editing_scale_id = None

        self.name_input.clear()

        self.entry1.clear()
        self.exit1.clear()

        self.entry2.clear()
        self.exit2.clear()

        self.entry3.clear()
        self.exit3.clear()

        self.monday.setChecked(True)
        self.tuesday.setChecked(True)
        self.wednesday.setChecked(True)
        self.thursday.setChecked(True)
        self.friday.setChecked(True)

        self.saturday.setChecked(False)
        self.sunday.setChecked(False)

        self.save_button.setText(
            "Cadastrar Escala"
        )
    
    def configure_days(self):

        QMessageBox.information(
            self,
            "AVAPoint",
            "Use o botão 📅 da escala desejada."
        )
    
    def configure_scale_days(self, scale):

        dialog = ScaleDaysDialog(
            scale["id"],
            scale["name"],
            self
        )

        dialog.exec()