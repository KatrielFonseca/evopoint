from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSizePolicy
    
)

from PySide6.QtCore import Qt, QTimer, QMargins

import requests

from PySide6.QtCharts import *

from PySide6.QtGui import QColor, QPainter



API_URL = "http://127.0.0.1:8000"


# =====================================================
# CARD
# =====================================================

class DashboardCard(QFrame):

    def __init__(self, titulo, valor, color):

        super().__init__()

        self.setFixedHeight(120)

        self.setStyleSheet("""

            QFrame{

                background:white;

                border-radius:20px;

            }

        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            22,
            18,
            22,
            18
        )

        self.value = QLabel(valor)

        self.value.setAlignment(
            Qt.AlignLeft
        )

        self.value.setStyleSheet(f"""

            font-size:34px;

            font-weight:800;

            color:{color};

            background:transparent;

        """)

        title = QLabel(titulo)

        title.setStyleSheet("""

            font-size:14px;

            color:#666;

            background:transparent;

        """)

        layout.addWidget(self.value)

        layout.addWidget(title)


# =====================================================
# DASHBOARD
# =====================================================

class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        root = QVBoxLayout(self)

        root.setContentsMargins(
            0,
            0,
            0,
            0
        )

        root.setSpacing(20)

        # ==========================================
        # CARDS
        # ==========================================

        cards = QHBoxLayout()

        cards.setSpacing(20)

        self.card_funcionarios = DashboardCard(

            "Funcionários",

            "0",

            "#222222"

        )

        self.card_presentes = DashboardCard(

            "Presentes Hoje",

            "0",

            "#00C853"

        )

        self.card_ausentes = DashboardCard(

            "Ausentes",

            "0",

            "#E53935"

        )

        self.card_justificativas = DashboardCard(

            "Justificativas",

            "0",

            "#1E88E5"

        )

        self.card_ativos = DashboardCard(

            "Ativos Agora",

            "0",

            "#F9A825"

        )

        cards.addWidget(
            self.card_funcionarios
        )

        cards.addWidget(
            self.card_presentes
        )

        cards.addWidget(
            self.card_ausentes
        )

        cards.addWidget(
            self.card_justificativas
        )

        cards.addWidget(
            self.card_ativos
        )

        root.addLayout(cards)

        # ==========================================
        # PAINEL PRINCIPAL
        # ==========================================

        painel = QFrame()

        painel.setStyleSheet("""

            QFrame{

                background:white;

                border-radius:24px;

            }

        """)

        painel_layout = QVBoxLayout(painel)

        titulo = QLabel("Dashboard")

        titulo.setStyleSheet("""

            font-size:28px;

            font-weight:800;

            background:transparent;

        """)

        painel_layout.addWidget(titulo)

        grid = QGridLayout()

        grid.setSpacing(20)

        self.graph_panel = self.create_panel(
            "📈 Batidas do Dia"
        )

        graph_layout = self.graph_panel.layout()

        self.chart = QChart()

        self.chart.legend().hide()

        self.chart.setBackgroundVisible(False)

        self.chart.setMargins(QMargins(5, 5, 5, 5))

        self.chart.setMargins(
            QMargins(
                0,
                0,
                0,
                0
            )
        )

        self.chart_view = QChartView(
            self.chart
        )

        self.chart_view.setMinimumHeight(520)

        self.chart_view.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )


        self.chart_view.setMinimumHeight(320)
        self.chart_view.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.chart_view.setRenderHint(
            QPainter.Antialiasing
        )

        graph_layout.addWidget(
            self.chart_view,
            1
        )

        self.load_chart()



        self.status_panel = self.create_panel(
            "🟢 Status do Sistema"
        )

       

       

        grid.addWidget(
            self.graph_panel,
            0,
            0
        )

        grid.addWidget(
            self.status_panel,
            0,
            1
        )


        grid.setColumnStretch(
            0,
            1
        )

        grid.setColumnStretch(
            1,
            1
        )

        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 2)

        grid.setRowStretch(0, 1)

        painel_layout.addLayout(grid)

        root.addWidget(painel)

        # ==========================================
        # STATUS
        # ==========================================

        status_layout = self.status_panel.layout()

        self.api_label = QLabel()

        self.database_label = QLabel()

        self.evo_label = QLabel()

        self.capture_label = QLabel()

        self.sync_label = QLabel()

        status_layout.addWidget(self.api_label)

        status_layout.addWidget(self.database_label)

        status_layout.addWidget(self.evo_label)

        status_layout.addWidget(self.capture_label)

        status_layout.addWidget(self.sync_label)

        # ==========================================
        # CARREGA
        # ==========================================

        self.load_dashboard()

        self.load_status()

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.load_dashboard
        )

        self.timer.timeout.connect(
            self.load_status
        )

        self.timer.timeout.connect(
            self.load_chart
        )

        self.timer.start(5000)

    # =====================================================
    # PAINEL
    # =====================================================

    def create_panel(self, title):

        frame = QFrame()

        frame.setStyleSheet("""

            QFrame{

                background:white;

                border:1px solid #E5E7EB;

                border-radius:20px;

            }

        """)

        layout = QVBoxLayout(frame)

        layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        titulo = QLabel(title)

        titulo.setStyleSheet("""

            font-size:18px;

            font-weight:700;

            background:transparent;

        """)

        layout.addWidget(titulo)

        layout.setSpacing(10)

        layout.setStretch(
            0,
            0
        )

        return frame

    # =====================================================
    # DASHBOARD
    # =====================================================

    def load_dashboard(self):

        try:

            response = requests.get(

                f"{API_URL}/dashboard",

                timeout=5

            )

            if response.status_code != 200:

                return

            data = response.json()

            # =====================================
            # CARDS
            # =====================================

            self.card_funcionarios.value.setText(

                str(

                    data.get(

                        "employees",

                        0

                    )

                )

            )

            self.card_presentes.value.setText(

                str(

                    data.get(

                        "presentes",

                        0

                    )

                )

            )

            self.card_ausentes.value.setText(

                str(

                    data.get(

                        "ausentes",

                        0

                    )

                )

            )

            self.card_justificativas.value.setText(

                str(

                    data.get(

                        "justificativas",

                        0

                    )

                )

            )

            self.card_ativos.value.setText(

                str(

                    data.get(

                        "ativos",

                        0

                    )

                )

            )

        except Exception as e:

            print("================================")

            print("ERRO DASHBOARD")

            print(str(e))

            print("================================")


    # =====================================================
    # STATUS
    # =====================================================

    def load_status(self):

        try:

            response = requests.get(

                f"{API_URL}/dashboard/status",

                timeout=5

            )

            if response.status_code != 200:

                return

            data = response.json()

            self.api_label.setText(

                "🟢 API Online"

                if data.get("api")

                else "🔴 API Offline"

            )

            self.database_label.setText(

                "🟢 Banco Online"

                if data.get("database")

                else "🔴 Banco Offline"

            )

            self.evo_label.setText(

                "🟢 EVO Online"

                if data.get("evo")

                else "🔴 EVO Offline"

            )

            self.capture_label.setText(

                "🟢 Captura Ativa"

                if data.get("capture")

                else "🔴 Captura Parada"

            )

            self.sync_label.setText(

                "Última atualização: "

                + data.get(

                    "time",

                    "--:--:--"

                )

            )

        except Exception as e:

            print("================================")

            print("ERRO STATUS")

            print(str(e))

            print("================================")


  


    # =====================================================
    # FUTURO - ÚLTIMOS REGISTROS
    # =====================================================

    def load_last_records(self):

        pass


    # =====================================================
    # FUTURO - ALERTAS
    # =====================================================

    def load_alerts(self):

        pass
    

    def load_chart(self):

        try:

            response = requests.get(

                f"{API_URL}/dashboard/chart"

            )

            if response.status_code != 200:

                return

            dados = response.json()

            self.chart.removeAllSeries()

            serie = QBarSeries()

            serie.setBarWidth(0.85)

            conjunto = QBarSet(
                "Batidas"
            )

            conjunto.setColor(
                QColor("#00C853")
            )

            categorias = []

            for item in dados:

                conjunto.append(
                    item["count"]
                )

                categorias.append(
                    f"{item['hour']:02d}"
                )

            serie.append(
                conjunto
            )

            self.chart.addSeries(
                serie
            )

            eixo_x = QBarCategoryAxis()

            eixo_x.append(
                categorias
            )

            eixo_x.setLabelsAngle(0)

            eixo_y = QValueAxis()

            eixo_y.setTickCount(2)

            eixo_y.setMin(0)

            # Esconde o eixo Y
            eixo_y.setVisible(False)

            eixo_y.setGridLineVisible(False)

            self.chart.removeAxis(
                self.chart.axisX()
            ) if self.chart.axisX() else None

            self.chart.removeAxis(
                self.chart.axisY()
            ) if self.chart.axisY() else None

            self.chart.addAxis(
                eixo_x,
                Qt.AlignBottom
            )

            self.chart.addAxis(
                eixo_y,
                Qt.AlignLeft
            )

            serie.attachAxis(eixo_x)

            serie.attachAxis(eixo_y)

            self.chart.setBackgroundVisible(False)

            self.chart.setBackgroundRoundness(0)

            self.chart.layout().setContentsMargins(
                0,
                0,
                0,
                0
            )


            self.chart.setTitle("Batidas por Hora")

            self.chart.setTitleBrush(
                QColor("#333333")
            )

            self.chart.legend().hide()

            self.chart.setTitle(
                "Batidas por Hora"
            )

            self.chart.setBackgroundVisible(False)

            self.chart.setPlotAreaBackgroundVisible(False)

            self.chart.setBackgroundRoundness(0)

            self.chart.legend().hide()

            self.chart.setMargins(QMargins(0,0,0,0))

            self.chart.layout().setContentsMargins(
                0,
                0,
                0,
                0
            )

        except Exception as e:

            print(e)