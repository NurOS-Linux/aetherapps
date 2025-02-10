import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
import subprocess

class NetworkManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Manager")
        self.setFixedSize(800, 700)
        self.setup_ui()
        
        self.prev_rx_bytes = self.get_network_bytes('rx')
        self.prev_tx_bytes = self.get_network_bytes('tx')
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitoring)

    def get_network_bytes(self, direction):
        try:
            with open('/proc/net/dev', 'r') as f:
                total_bytes = 0
                for line in f.readlines()[2:]:
                    if not line.strip().startswith('lo:'):
                        values = line.split(':')[1].split()
                        total_bytes += int(values[0] if direction == 'rx' else values[8])
                return total_bytes
        except: return 0

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.tab_widget = QTabWidget()
        tabs = [
            (self.create_network_tab(), "Сеть"),
            (self.create_firewall_tab(), "Брандмауэр"),
            (self.create_connections_tab(), "Подключения"),
            (self.create_monitoring_tab(), "Мониторинг")
        ]
        for tab, name in tabs:
            self.tab_widget.addTab(tab, name)
        layout.addWidget(self.tab_widget)
        self.apply_styles()

    def create_network_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Статус
        self.connection_status = QLabel("Статус: проверка...")
        self.ip_address = QLabel("IP: проверка...")
        for label in [self.connection_status, self.ip_address]:
            layout.addWidget(label)

        # Кнопки
        btn_layout = QHBoxLayout()
        buttons = [
            ("Обновить", self.refresh_network_status),
            ("Включить", self.enable_network),
            ("Отключить", self.disable_network)
        ]
        for text, slot in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        # Таблица интерфейсов
        self.interfaces_table = QTableWidget()
        self.interfaces_table.setColumnCount(4)
        self.interfaces_table.setHorizontalHeaderLabels(
            ["Интерфейс", "Статус", "IP", "MAC"]
        )
        self.interfaces_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.interfaces_table)
        
        self.refresh_network_status()
        return tab

    def create_firewall_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.firewall_status = QLabel("Статус: проверка...")
        layout.addWidget(self.firewall_status)

        # Таблица правил
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(5)
        self.rules_table.setHorizontalHeaderLabels(
            ["Порт", "Протокол", "Направление", "Действие", "Описание"]
        )
        layout.addWidget(self.rules_table)

        # Управление
        controls = QHBoxLayout()
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["TCP", "UDP"])
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["Входящий", "Исходящий"])
        self.action_combo = QComboBox()
        self.action_combo.addItems(["Разрешить", "Запретить"])
        
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_firewall_rule)

        for w in [self.port_input, self.protocol_combo, 
                 self.direction_combo, self.action_combo, add_btn]:
            controls.addWidget(w)
        layout.addLayout(controls)

        self.refresh_firewall_status()
        return tab

    def create_connections_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.connections_table = QTableWidget()
        self.connections_table.setColumnCount(5)
        self.connections_table.setHorizontalHeaderLabels(
            ["Протокол", "Локальный", "Удаленный", "Статус", "PID"]
        )
        layout.addWidget(self.connections_table)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("Обновить")
        kill_btn = QPushButton("Завершить")
        refresh_btn.clicked.connect(self.refresh_connections)
        kill_btn.clicked.connect(self.kill_connection)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(kill_btn)
        layout.addLayout(btn_layout)

        self.refresh_connections()
        return tab

    def create_monitoring_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.download_speed = QLabel("Загрузка: 0 B/s")
        self.upload_speed = QLabel("Отдача: 0 B/s")
        self.total_traffic = QLabel("Всего: 0 B")
        
        for label in [self.download_speed, self.upload_speed, self.total_traffic]:
            layout.addWidget(label)

        # Настройки
        settings = QHBoxLayout()
        self.auto_refresh = QCheckBox("Автообновление")
        self.auto_refresh.setChecked(True)
        self.refresh_interval = QSpinBox()
        self.refresh_interval.setRange(1, 60)
        self.refresh_interval.setValue(5)
        settings.addWidget(self.auto_refresh)
        settings.addWidget(self.refresh_interval)
        layout.addLayout(settings)

        self.start_monitoring()
        return tab

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {background-color: #1a1a1a;}
            QLabel, QCheckBox {color: white;}
            QPushButton {
                background-color: #5c90ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QTableWidget {
                background-color: #2d2d2d;
                color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #3d3d3d;
                color: white;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
        """)

    # Методы управления сетью
    def refresh_network_status(self):
        try:
            result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            if 'inet ' in result.stdout:
                self.ip_address.setText(f"IP: {result.stdout.split('inet ')[1].split('/')[0]}")
            
            result = subprocess.run(['nmcli', 'connection', 'show', '--active'], 
                                 capture_output=True, text=True)
            self.connection_status.setText(
                "Статус: Подключено" if result.stdout.strip() else "Статус: Отключено"
            )
            
            # Обновление таблицы интерфейсов
            self.update_interfaces_table()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def update_interfaces_table(self):
        try:
            result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            self.interfaces_table.setRowCount(0)
            current_interface = None
            
            for line in result.stdout.split('\n'):
                if not line.startswith(' '):
                    if ': ' in line:
                        current_interface = line.split(': ')[1].split('@')[0]
                elif current_interface and 'inet ' in line:
                    ip = line.split('inet ')[1].split('/')[0]
                    row = self.interfaces_table.rowCount()
                    self.interfaces_table.insertRow(row)
                    self.interfaces_table.setItem(row, 0, QTableWidgetItem(current_interface))
                    self.interfaces_table.setItem(row, 2, QTableWidgetItem(ip))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def enable_network(self):
        try:
            subprocess.run(['sudo', 'nmcli', 'networking', 'on'], check=True)
            self.refresh_network_status()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def disable_network(self):
        try:
            subprocess.run(['sudo', 'nmcli', 'networking', 'off'], check=True)
            self.refresh_network_status()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def refresh_firewall_status(self):
        try:
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
            self.firewall_status.setText(f"Статус: {result.stdout.split()[0]}")
            self.update_firewall_rules()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def update_firewall_rules(self):
        try:
            result = subprocess.run(['ufw', 'status', 'numbered'], 
                                 capture_output=True, text=True)
            self.rules_table.setRowCount(0)
            for rule in result.stdout.split('\n')[1:]:
                if rule.strip():
                    parts = rule.split()
                    if len(parts) >= 4:
                        row = self.rules_table.rowCount()
                        self.rules_table.insertRow(row)
                        self.rules_table.setItem(row, 0, QTableWidgetItem(parts[1]))
                        self.rules_table.setItem(row, 1, QTableWidgetItem(parts[2]))
                        self.rules_table.setItem(row, 3, QTableWidgetItem(parts[3]))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def add_firewall_rule(self):
        try:
            cmd = [
                'sudo', 'ufw',
                'allow' if self.action_combo.currentText() == "Разрешить" else 'deny',
                'in' if self.direction_combo.currentText() == "Входящий" else 'out',
                str(self.port_input.value()),
                'proto',
                self.protocol_combo.currentText().lower()
            ]
            subprocess.run(cmd, check=True)
            self.refresh_firewall_status()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def refresh_connections(self):
        try:
            result = subprocess.run(['netstat', '-tunapl'], capture_output=True, text=True)
            self.connections_table.setRowCount(0)
            for line in result.stdout.split('\n')[2:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 7:
                        row = self.connections_table.rowCount()
                        self.connections_table.insertRow(row)
                        for i, val in enumerate([parts[0], parts[3], parts[4], parts[5], parts[6]]):
                            self.connections_table.setItem(row, i, QTableWidgetItem(val))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def kill_connection(self):
        selected = self.connections_table.selectedItems()
        if not selected:
            return
        try:
            pid = self.connections_table.item(selected[0].row(), 4).text()
            if pid and pid.isdigit():
                subprocess.run(['sudo', 'kill', '-9', pid], check=True)
                self.refresh_connections()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def start_monitoring(self):
        self.monitor_timer.start(self.refresh_interval.value() * 1000)

    def update_monitoring(self):
        if not self.auto_refresh.isChecked():
            return
        try:
            curr_rx = self.get_network_bytes('rx')
            curr_tx = self.get_network_bytes('tx')
            
            rx_speed = (curr_rx - self.prev_rx_bytes) / self.refresh_interval.value()
            tx_speed = (curr_tx - self.prev_tx_bytes) / self.refresh_interval.value()
            
            self.download_speed.setText(f"Загрузка: {self.format_bytes(rx_speed)}/s")
            self.upload_speed.setText(f"Отдача: {self.format_bytes(tx_speed)}/s")
            self.total_traffic.setText(f"Всего: {self.format_bytes(curr_rx + curr_tx)}")
            
            self.prev_rx_bytes = curr_rx
            self.prev_tx_bytes = curr_tx
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def format_bytes(self, bytes_value):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.2f} TB"

def main():
    app = QApplication(sys.argv)
    window = NetworkManager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()