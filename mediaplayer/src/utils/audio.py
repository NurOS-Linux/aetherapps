"""
NurOS Media Player - Audio System
~~~~~~~~~~~~~~~~~~~~~~~~~~
DeltaDesign Concept Night Audio Processing System

Created: 2024-12-22 11:02:18 UTC
Author: AnmiTaliDev
License: GPL 3
"""

import wave
import array
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from PyQt6.QtMultimedia import (
    QAudioFormat, QMediaDevices, 
    QAudioSink, QAudioSource
)

from .. import logger

class AudioSystem:
    """
    Система обработки аудио для DeltaDesign Concept Night.
    Обеспечивает работу с аудиоустройствами и обработку аудиопотока.
    """

    # Настройки аудио по умолчанию
    DEFAULT_SAMPLE_RATE = 44100
    DEFAULT_CHANNEL_COUNT = 2
    DEFAULT_SAMPLE_SIZE = 16
    BUFFER_SIZE = 4096

    def __init__(self):
        """Инициализация аудиосистемы."""
        self.format = QAudioFormat()
        self.audio_input: Optional[QAudioSource] = None
        self.audio_output: Optional[QAudioSink] = None
        self.devices = QMediaDevices()
        
        # Состояние системы
        self.is_initialized = False
        self.current_device = None
        self.volume_level = 1.0
        
        # Настройки эквалайзера
        self.equalizer_bands = [
            60, 170, 310, 600, 1000, 
            3000, 6000, 12000, 14000, 16000
        ]
        self.equalizer_values = [0.0] * len(self.equalizer_bands)
        
        logger.info("Audio system created")

    def initialize(self) -> bool:
        """Инициализация аудиосистемы."""
        try:
            # Настройка формата
            self.format.setSampleRate(self.DEFAULT_SAMPLE_RATE)
            self.format.setChannelCount(self.DEFAULT_CHANNEL_COUNT)
            self.format.setSampleFormat(QAudioFormat.SampleFormat.Int16)
            
            # Проверка поддержки формата
            if not self.format.isValid():
                logger.error("Invalid audio format")
                return False

            # Инициализация устройств
            self._init_devices()
            self.is_initialized = True
            logger.info("Audio system initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Audio system initialization failed: {e}")
            return False

    def _init_devices(self):
        """Инициализация аудиоустройств."""
        # Получение списка устройств
        self.input_devices = self.devices.audioInputs()
        self.output_devices = self.devices.audioOutputs()
        
        # Установка устройств по умолчанию
        if self.output_devices:
            self.current_device = self.output_devices[0]
            self.audio_output = QAudioSink(self.current_device, self.format)
            self.audio_output.setVolume(self.volume_level)

        if self.input_devices:
            self.audio_input = QAudioSource(
                self.input_devices[0], 
                self.format
            )

    def get_devices(self) -> Dict[str, List[str]]:
        """Получение списка доступных устройств."""
        return {
            'input': [d.description() for d in self.input_devices],
            'output': [d.description() for d in self.output_devices]
        }

    def set_device(self, device_name: str, is_input: bool = False) -> bool:
        """Установка активного устройства."""
        try:
            devices = (
                self.input_devices if is_input 
                else self.output_devices
            )
            
            for device in devices:
                if device.description() == device_name:
                    if is_input:
                        self.audio_input = QAudioSource(device, self.format)
                    else:
                        self.audio_output = QAudioSink(device, self.format)
                        self.audio_output.setVolume(self.volume_level)
                    self.current_device = device
                    return True
                    
            return False
            
        except Exception as e:
            logger.error(f"Failed to set audio device: {e}")
            return False

    def set_volume(self, volume: float):
        """Установка громкости (0.0 - 1.0)."""
        self.volume_level = max(0.0, min(1.0, volume))
        if self.audio_output:
            self.audio_output.setVolume(self.volume_level)

    def set_equalizer(self, band: int, value: float):
        """Установка значения полосы эквалайзера."""
        if 0 <= band < len(self.equalizer_bands):
            self.equalizer_values[band] = max(-12.0, min(12.0, value))

    def get_equalizer(self) -> List[Tuple[int, float]]:
        """Получение настроек эквалайзера."""
        return list(zip(self.equalizer_bands, self.equalizer_values))

    def analyze_audio(self, file_path: Path) -> Dict[str, Any]:
        """Анализ аудиофайла."""
        try:
            with wave.open(str(file_path), 'rb') as wav:
                # Получение параметров
                params = wav.getparams()
                frames = wav.readframes(wav.getnframes())
                
                # Преобразование в массив
                audio_data = array.array('h', frames)
                
                # Анализ
                return {
                    'channels': params.nchannels,
                    'sample_rate': params.framerate,
                    'sample_width': params.sampwidth,
                    'frames': params.nframes,
                    'duration': params.nframes / params.framerate,
                    'max_amplitude': max(abs(min(audio_data)), 
                                      abs(max(audio_data)))
                }
                
        except Exception as e:
            logger.error(f"Audio analysis failed: {e}")
            return {}

    def cleanup(self):
        """Очистка ресурсов."""
        if self.audio_input:
            self.audio_input.stop()
        if self.audio_output:
            self.audio_output.stop()
        logger.info("Audio system cleaned up")