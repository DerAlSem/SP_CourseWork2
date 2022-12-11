import logging
# настраиваем логирование
logging.basicConfig(level=logging.INFO)
# инициализируем логгер для запросов апи
logger_api = logging.getLogger('api')
# создаем обработчик
file_handler_api = logging.FileHandler('log/api.log')
console_handler_api = logging.StreamHandler()
# устанавливаем формат лога
formatter_api = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler_api.setFormatter(formatter_api)
# добавляем обработчик к логгеру
logger_api.addHandler(file_handler_api)
logger_api.addHandler(console_handler_api)