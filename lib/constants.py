__all__ = ['SKIP_FRAMES', 'PEAK_RATE', 'PEAK_HIST_COUNT', 'PEAK_MIN_COUNT', 'TEST_WINDOWS', 'OUTPUT_FOLDER',
           'INPUT_FOLDER', 'SAVE_LOG', 'WHISPER_MODEL']

"""Настройки распознавания"""
SKIP_FRAMES = 10    # Количество кадров для пропуска
PEAK_RATE = 10      # Какая кратность превышения числа пикселей дельты приводит к записи кадра
PEAK_HIST_COUNT = 20 # Глубина анализа среднего для вычисления пика
PEAK_MIN_COUNT = 5   # Минимальное количество кадров для начала анализа пиков

"""Настройки тестирования"""
TEST_WINDOWS = False   # Показывать тестовые окна
SAVE_LOG = False       # Сохранять файл журнала с таймингом

"""Папки входных и выходных данных"""
OUTPUT_FOLDER = './output/'   # Директория выходных данных
INPUT_FOLDER = './input/'     # Директория входных данных

"""Настройки речевой модели"""
WHISPER_MODEL = 'base'       #  Модель распознавания звука
#WHISPER_MODEL = 'large-v3'  #
#WHISPER_MODEL = './ggml-small.bin'
