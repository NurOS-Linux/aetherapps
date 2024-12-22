# NurOS Media Player
#### DeltaDesign Concept Night Edition

![NurOS Media Player](docs/images/preview.png)

## Overview

NurOS Media Player is a modern audio player built with DeltaDesign Concept Night - a sleek, dark-themed design language optimized for night-time use. It combines powerful audio playback capabilities with an elegant user interface.

### Key Features

- 🎨 DeltaDesign Concept Night theme
- 🎵 Support for multiple audio formats (MP3, WAV, OGG, FLAC)  
- 🔊 10-band equalizer with presets
- 📋 Playlist management with drag & drop
- 🎚️ Volume normalization and fade effects
- 🔄 Gapless playback
- 🌙 Night mode optimized interface

## Installation

### From RPM Package
```bash
sudo dnf install nuros-mediaplayer-1.0.0-1.fc*.noarch.rpm
```

### From Source
```bash
# Clone repository
git clone https://github.com/AnmiTaliDev/nuros-mediaplayer.git
cd nuros-mediaplayer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python -m mediaplayer
```

## Dependencies

Core:
- Python 3.8+
- PyQt6
- Mutagen
- NumPy
- SoundDevice

Development:
- Black
- isort
- Pylint
- Pytest
- Sphinx

## Usage

### Basic Controls
- Space: Play/Pause
- Left/Right: Seek backward/forward
- Up/Down: Volume control
- Ctrl+O: Open file
- Ctrl+Q: Quit

### Playlist Management
- Drag & drop files into playlist
- Right-click for context menu
- Double-click to play
- Ctrl+drag to reorder

### Equalizer
- 10 customizable frequency bands
- Save/load presets
- Reset to default

## Configuration

Configuration file location: `~/.config/nuros-mediaplayer/config.json`

Example configuration:
```json
{
    "volume": 0.7,
    "equalizer": {
        "enabled": true,
        "preset": "Rock",
        "bands": [4, 3, 2, 0, -2, -1, 2, 3, 2, 1]
    },
    "theme": {
        "accent_color": "#00A5B8",
        "background": "dark"
    }
}
```

## Development

### Project Structure
```
nuros-mediaplayer/
├── mediaplayer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── player.py
│   ├── playlist.py
│   ├── ui/
│   └── utils/
├── tests/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

### Building
```bash
# Build RPM package
./build_rpm.sh

# Build documentation
cd docs
make html
```

### Testing
```bash
pytest tests/
```

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Design: DeltaDesign Concept Night
- Icons: [Phosphor Icons](https://phosphoricons.com)
- Font: [Segoe UI](https://docs.microsoft.com/en-us/typography/font-list/segoe-ui)

## Support

- Issues: GitHub Issues
- Wiki: Project Wiki
- Email: anmitalidev@example.com

---
*Built with ❤️ using DeltaDesign Concept Night*