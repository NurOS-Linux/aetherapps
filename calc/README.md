# NurOS Calculator

<p align="center">
  <img src="src/calculator/resources/icons/logo.svg" alt="NurOS Calculator" width="128"/>
</p>

A modern calculator application built with Delta Design Concept Night theme for NurOS Linux.

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)

## Overview

NurOS Calculator is a sleek, modern calculator application designed with the Delta Design Concept Night theme. It provides a beautiful dark interface while maintaining high functionality and ease of use.

### Features

- Clean, modern interface with Delta Design Concept Night theme
- Basic arithmetic operations
- Memory functions
- Keyboard support
- Configuration saving
- Error handling
- Logging system

## Installation

### Dependencies

First, install the required system packages:

```bash
sudo zypper install python311-setuptools python311-pip python311-devel python311-wheel python311-PyQt6
```

### Development Setup

1. Create and activate virtual environment:
```bash
python3.11 -m venv ~/.venv/calculator
source ~/.venv/calculator/bin/activate
```

2. Install in development mode:
```bash
pip install -e .
```

### System Installation

To install system-wide:

```bash
sudo zypper install nuros-calculator
```

## Usage

### Starting the Calculator

```bash
nuros-calculator
```

### Keyboard Shortcuts

- `0-9`: Number input
- `.`: Decimal point
- `+`: Addition
- `-`: Subtraction
- `*`: Multiplication
- `/`: Division
- `Enter`: Calculate result
- `Esc`: Close calculator
- `Backspace`: Delete last digit

## Development

### Project Structure

```
calculator/
├── src/
│   └── calculator/
│       ├── __init__.py
│       ├── main.py
│       └── resources/
│           ├── icons/
│           └── nuros-calculator.desktop
├── requirements.txt
├── setup.py
├── pyproject.toml
├── MANIFEST.in
└── README.md
```

### Building from Source

1. Clone the repository:
```bash
git clone https://github.com/nuros-linux/ddeapps
cd ddeapps/calculator
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

3. Build the package:
```bash
python -m build
```

### Configuration

Configuration file is stored in:
```
~/.config/nuros/calculator/config.json
```

Logs are stored in:
```
~/.local/share/nuros/calculator/logs/calculator.log
```

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'Add amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

## Technical Details

- **Version:** 1.0.0
- **Created:** 2024-12-21 19:51:55 UTC
- **Author:** AnmiTaliDev
- **Email:** anmitali@anmitali.kz
- **License:** GPL-3.0
- **Python Version:** 3.11+
- **UI Framework:** PyQt6

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- GNOME Calculator team for the application icon
- Qt team for the amazing framework
- NurOS Linux community for support and testing

## Support

If you encounter any problems or have suggestions, please:
1. Check the [issue tracker](https://github.com/nuros-linux/ddeapps/issues)
2. Create a new issue if needed
3. Or contact the developer directly at anmitali@anmitali.kz

---

<p align="center">
Made with ❤️ for NurOS Linux by AnmiTaliDev
</p>
