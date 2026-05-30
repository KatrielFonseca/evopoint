import sys

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QFrame,
    QStackedWidget,
    QSizePolicy
)

from pages.employees_page import EmployeesPage
from pages.records_page import RecordsPage
from pages.scales_page import ScalesPage
from pages.bank_hours_page import BankHoursPage
from pages.reports_page import ReportsPage
from pages.devices_page import DevicesPage

# =========================================
# SIDEBAR BUTTON
# =========================================

class SidebarButton(QPushButton):

    def __init__(self, text):

        super().__init__(text)

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setFixedHeight(56)

        self.setStyleSheet("""

            QPushButton {

                background: transparent;

                border: none;

                border-radius: 16px;

                padding-left: 22px;

                text-align: left;

                font-size: 15px;

                font-weight: 600;

                color: #E8F5E9;
            }

            QPushButton:hover {

                background: rgba(255,255,255,0.12);
            }

            QPushButton:pressed {

                background: rgba(255,255,255,0.20);
            }

        """)


# =========================================
# MAIN WINDOW
# =========================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "EVOPoint"
        )

        self.resize(1500, 920)

        self.setMinimumSize(1280, 720)

        # =====================================
        # CENTRAL
        # =====================================

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        # =====================================
        # GLOBAL STYLE
        # =====================================

        self.setStyleSheet("""

            QWidget {

                background: #F4F6F8;

                color: #1E1E1E;

                font-family: 'Segoe UI';

                font-size: 14px;
            }

        """)

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(0)

        central_widget.setLayout(
            main_layout
        )

        # =====================================
        # SIDEBAR
        # =====================================

        sidebar = QFrame()

        sidebar.setFixedWidth(285)

        sidebar.setStyleSheet("""

            QFrame {

                background: qlineargradient(
                    x1:0,
                    y1:0,
                    x2:0,
                    y2:1,

                    stop:0 #00C853,

                    stop:1 #009624
                );

                border-top-right-radius: 28px;

                border-bottom-right-radius: 28px;
            }

        """)

        sidebar_layout = QVBoxLayout()

        sidebar_layout.setContentsMargins(
            22,
            22,
            22,
            22
        )

        sidebar_layout.setSpacing(12)

        sidebar.setLayout(
            sidebar_layout
        )

        # =====================================
        # LOGO
        # =====================================

        logo = QLabel("EVOPoint")

        logo.setStyleSheet("""

            color: white;

            font-size: 38px;

            font-weight: 800;

            margin-bottom: 28px;

            background: transparent;

        """)

        sidebar_layout.addWidget(
            logo
        )

        # =====================================
        # MENU LABEL
        # =====================================

        menu_label = QLabel("MENU")

        menu_label.setStyleSheet("""

            color: rgba(255,255,255,0.7);

            font-size: 12px;

            font-weight: bold;

            letter-spacing: 2px;

            margin-bottom: 10px;

            background: transparent;

        """)

        sidebar_layout.addWidget(
            menu_label
        )

        # =====================================
        # BUTTONS
        # =====================================

        self.dashboard_button = SidebarButton(
            "Dashboard"
        )

        self.employees_button = SidebarButton(
            "Funcionários"
        )

        self.records_button = SidebarButton(
            "Registros"
        )

        self.scales_button = SidebarButton(
            "Escalas"
        )

        self.hours_button = SidebarButton(
            "Banco de Horas"
        )

        self.reports_button = SidebarButton(
            "Relatórios"
        )

        self.devices_button = SidebarButton(
            "Dispositivos"
        )

        self.settings_button = SidebarButton(
            "Configurações"
        )
        
        buttons = [

            self.dashboard_button,

            self.employees_button,

            self.records_button,

            self.scales_button,

            self.hours_button,

            self.reports_button,

            self.devices_button,

            self.settings_button
        ]

        for button in buttons:

            sidebar_layout.addWidget(
                button
            )

        sidebar_layout.addStretch()

        # =====================================
        # VERSION
        # =====================================

        version = QLabel(
            "EVOPoint v1.0"
        )

        version.setStyleSheet("""

            color: rgba(255,255,255,0.7);

            font-size: 12px;

            background: transparent;

        """)

        sidebar_layout.addWidget(
            version
        )

        # =====================================
        # CONTENT
        # =====================================

        content = QFrame()

        content.setStyleSheet("""

            QFrame {

                background: #F4F6F8;
            }

        """)

        content_layout = QVBoxLayout()

        content_layout.setContentsMargins(
            35,
            30,
            35,
            30
        )

        content_layout.setSpacing(20)

        content.setLayout(
            content_layout
        )

        # =====================================
        # TOP BAR
        # =====================================

        top_bar = QFrame()

        top_bar.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 24px;
            }

        """)

        top_bar_layout = QHBoxLayout()

        top_bar_layout.setContentsMargins(
            28,
            20,
            28,
            20
        )

        top_bar.setLayout(
            top_bar_layout
        )

        # =====================================
        # TITLE AREA
        # =====================================

        title_container = QVBoxLayout()

        title = QLabel("EVOPoint")

        title.setStyleSheet("""

            font-size: 34px;

            font-weight: 800;

            color: #1E1E1E;

            background: transparent;

        """)

        subtitle = QLabel(
            "Sistema inteligente de ponto facial"
        )

        subtitle.setStyleSheet("""

            font-size: 15px;

            color: #757575;

            background: transparent;

        """)

        title_container.addWidget(
            title
        )

        title_container.addWidget(
            subtitle
        )

        top_bar_layout.addLayout(
            title_container
        )

        top_bar_layout.addStretch()

        # =====================================
        # STATUS
        # =====================================

        online_status = QLabel(
            "● Sistema Online"
        )

        online_status.setStyleSheet("""

            color: #00C853;

            font-size: 14px;

            font-weight: bold;

            background: #E8F5E9;

            padding: 12px 18px;

            border-radius: 14px;

        """)

        top_bar_layout.addWidget(
            online_status
        )

        content_layout.addWidget(
            top_bar
        )

        # =====================================
        # STACK
        # =====================================

        self.stack = QStackedWidget()

        self.stack.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # =====================================
        # DASHBOARD PAGE
        # =====================================

        dashboard_page = QWidget()

        dashboard_layout = QVBoxLayout()

        dashboard_layout.setContentsMargins(
            0,
            20,
            0,
            0
        )

        dashboard_layout.setSpacing(20)

        dashboard_page.setLayout(
            dashboard_layout
        )

        welcome_card = QFrame()

        welcome_card.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 28px;
            }

        """)

        welcome_layout = QVBoxLayout()

        welcome_layout.setContentsMargins(
            35,
            35,
            35,
            35
        )

        welcome_card.setLayout(
            welcome_layout
        )

        dashboard_title = QLabel(
            "Bem-vindo ao EVOPoint"
        )

        dashboard_title.setStyleSheet("""

            font-size: 32px;

            font-weight: 800;

            color: #1E1E1E;

        """)

        dashboard_info = QLabel("""

Sistema moderno de ponto facial online
com reconhecimento facial, banco de horas,
escalas, registros em tempo real e integração EVO.

        """)

        dashboard_info.setStyleSheet("""

            font-size: 18px;

            color: #555555;

            line-height: 30px;

        """)

        welcome_layout.addWidget(
            dashboard_title
        )

        welcome_layout.addSpacing(10)

        welcome_layout.addWidget(
            dashboard_info
        )

        dashboard_layout.addWidget(
            welcome_card
        )

        dashboard_layout.addStretch()

        # =====================================
        # REAL PAGES
        # =====================================

        self.employees_page = EmployeesPage()

        self.records_page = RecordsPage()

        # =====================================
        # PLACEHOLDERS
        # =====================================

        self.scales_page = ScalesPage()

        self.bank_hours_page = BankHoursPage()

        self.reports_page = ReportsPage()

        self.devices_page = DevicesPage()

        settings_page = self.create_placeholder(
            "Configurações"
        )

        # =====================================
        # ADD STACK
        # =====================================

        self.stack.addWidget(
            dashboard_page
        )

        self.stack.addWidget(
            self.employees_page
        )

        self.stack.addWidget(
            self.records_page
        )

        self.stack.addWidget(
            self.scales_page
        )

        self.stack.addWidget(
            self.bank_hours_page
        )

        self.stack.addWidget(
            self.reports_page
        )

        self.stack.addWidget(
            self.devices_page
        )

        self.stack.addWidget(
            settings_page
        )

        content_layout.addWidget(
            self.stack
        )

        # =====================================
        # BUTTON EVENTS
        # =====================================

        self.dashboard_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(0)
        )

        self.employees_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(1)
        )

        self.records_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(2)
        )

        self.scales_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(3)
        )

        self.hours_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(4)
        )

        self.reports_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(5)
        )

        self.devices_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(6)
        )

        self.settings_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(7)
        )

        # =====================================
        # ADD LAYOUT
        # =====================================

        main_layout.addWidget(
            sidebar
        )

        main_layout.addWidget(
            content
        )

    # =========================================
    # PLACEHOLDER
    # =========================================

    def create_placeholder(self, title_text):

        page = QWidget()

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            20,
            0,
            0
        )

        page.setLayout(
            layout
        )

        card = QFrame()

        card.setStyleSheet("""

            QFrame {

                background: white;

                border-radius: 28px;
            }

        """)

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            35,
            35,
            35,
            35
        )

        card.setLayout(
            card_layout
        )

        title = QLabel(title_text)

        title.setStyleSheet("""

            font-size: 30px;

            font-weight: 800;

            color: #1E1E1E;

        """)

        subtitle = QLabel(
            f"Módulo {title_text} em desenvolvimento."
        )

        subtitle.setStyleSheet("""

            font-size: 16px;

            color: #757575;

        """)

        card_layout.addWidget(
            title
        )

        card_layout.addSpacing(10)

        card_layout.addWidget(
            subtitle
        )

        layout.addWidget(
            card
        )

        layout.addStretch()

        return page


# =========================================
# RUN
# =========================================

app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())