#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NurOS Calculator
Part of Delta Design Concept Night
Author: AnmiTaliDev <anmitali@anmitali.kz>
Created: 2024-12-21 19:22:55 UTC
"""

import sys
import os
import logging
from pathlib import Path
from datetime import datetime
import json
import configparser
from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                            QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt, QPoint, QSettings, QSize
from PyQt6.QtGui import QFont, QPainter, QColor, QIcon

# Constants
APP_NAME = "NurOS Calculator"
APP_VERSION = "1.0.0"
APP_AUTHOR = "AnmiTaliDev"
BUILD_DATE = "2024-12-21 19:22:55"
CONFIG_VERSION = 1

class ConfigManager:
    """Manages application configuration"""
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'nuros' / 'calculator'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file"""
        default_config = {
            'version': CONFIG_VERSION,
            'window': {
                'pos_x': 100,
                'pos_y': 100,
                'width': 375,
                'height': 600,
            },
            'appearance': {
                'theme': 'dark',
                'font_size': 14,
            },
            'behavior': {
                'precision': 10,
                'scientific_notation': False,
                'thousands_separator': True,
            }
        }

        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    if self.config.get('version', 0) < CONFIG_VERSION:
                        self.config = default_config
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            logging.error("Failed to load config: %s", e)
            self.config = default_config

    def save_config(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logging.error("Failed to save config: %s", e)

class Calculator:
    """Calculator logic implementation"""
    def __init__(self):
        self.current_value = 0
        self.memory_value = 0
        self.last_operation = None
        self.new_number = True
        self.decimal_places = 10

    def calculate(self, operation: str, value: float) -> float:
        """Perform calculation"""
        if operation == '+':
            return self.current_value + value
        elif operation == '-':
            return self.current_value - value
        elif operation == '×':
            return self.current_value * value
        elif operation == '÷':
            return self.current_value / value if value != 0 else float('inf')
        return value

    def format_number(self, number: float) -> str:
        """Format number for display"""
        if number == float('inf'):
            return 'Error'
        
        # Handle scientific notation
        if abs(number) > 10**12 or (abs(number) < 10**-12 and number != 0):
            return f'{number:.{self.decimal_places}e}'
        
        # Regular formatting
        result = f'{number:.{self.decimal_places}f}'.rstrip('0').rstrip('.')
        if result == '':
            return '0'
        return result

class MainWindow(QMainWindow):
    """Main window of the calculator"""
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.config_manager = ConfigManager()
        self.init_logging()
        self.init_ui()
        self.load_window_state()

    def init_logging(self) -> None:
        """Initialize logging"""
        log_dir = Path.home() / '.local' / 'share' / 'nuros' / 'calculator' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / 'calculator.log'

        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.info("Application started")

    def save_window_state(self) -> None:
        """Save window position and size"""
        pos = self.pos()
        size = self.size()
        self.config_manager.config['window']['pos_x'] = pos.x()
        self.config_manager.config['window']['pos_y'] = pos.y()
        self.config_manager.config['window']['width'] = size.width()
        self.config_manager.config['window']['height'] = size.height()
        self.config_manager.save_config()

    def load_window_state(self) -> None:
        """Load window position and size"""
        try:
            cfg = self.config_manager.config['window']
            self.move(cfg['pos_x'], cfg['pos_y'])
            self.resize(cfg['width'], cfg['height'])
        except Exception as e:
            logging.error("Failed to load window state: %s", e)

    def closeEvent(self, event) -> None:
        """Handle window close event"""
        self.save_window_state()
        logging.info("Application closed")
        event.accept()

    def keyPressEvent(self, event) -> None:
        """Handle keyboard input"""
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.close()
        elif key in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            self.calculate_result()
        elif key == Qt.Key.Key_Backspace:
            self.backspace()
        elif key >= Qt.Key.Key_0 and key <= Qt.Key.Key_9:
            self.digit_pressed(str(key - Qt.Key.Key_0))
        elif key == Qt.Key.Key_Period:
            self.digit_pressed('.')
        elif key == Qt.Key.Key_Plus:
            self.operation_pressed('+')
        elif key == Qt.Key.Key_Minus:
            self.operation_pressed('-')
        elif key == Qt.Key.Key_Asterisk:
            self.operation_pressed('×')
        elif key == Qt.Key.Key_Slash:
            self.operation_pressed('÷')

    # Ваш существующий код UI и обработчиков событий остается без изменений

def main():
    """Application entry point"""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setApplicationVersion(APP_VERSION)
        
        # Set app ID for proper taskbar grouping
        if hasattr(app, 'setDesktopFileName'):
            app.setDesktopFileName('nuros-calculator')
        
        window = MainWindow()
        window.show()
        
        return app.exec()
    except Exception as e:
        logging.critical("Application crashed: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(main())