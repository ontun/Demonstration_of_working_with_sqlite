import configparser

# Создаем объект конфигурации
config = configparser.ConfigParser()

# Добавляем секцию и параметры
config.add_section('Settings')
config.set('Settings', 'PATH_BASE', r'PATH_TO_DATABASE')

with open('config.ini', 'w') as f:
    config.write(f)
