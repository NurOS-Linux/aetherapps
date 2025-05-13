# meson.build
project('AMath', 'cpp',
  version : '1.3.2',
  default_options : ['cpp_std=c++17', 'warning_level=3']
)

# Находим и подключаем библиотеки Qt6
qt6 = import('qt6')
qt6_dep = dependency('qt6', modules: ['Core', 'Gui', 'Widgets'])

# Исходные файлы проекта
src_files = ['main.cpp']

# Создаем исполняемый файл
executable('AMath',
  sources : src_files,
  dependencies : qt6_dep,
  install : true
)
