# -*- coding: utf-8 -*-
""" Грабинг с Upwork.com заявок по ключевым словам. """
from sys import argv

from selenium.common.exceptions import NoSuchElementException
import logging
from os import path


import functions
import grab_upwork_cfg
import pswd

VERSION = '1.0.0'
__author__ = 'Aleksandr Jashhuk, Zoer, R5AM, www.r5am.ru'


def order_find(find_string):
    """ Поиск заявок по строке с ключевыми словами """
    logging.info('Find string in jobs: ' + find_string.replace('\n', ''))


def main():
    """ Main function """

    # Логирование
    message_level = logging.CRITICAL    # Уровень логирования по умолчанию
    if grab_upwork_cfg.logging_level == 'DEBUG':
        message_level = logging.DEBUG
    elif grab_upwork_cfg.logging_level == 'INFO':
        message_level = logging.INFO
    elif grab_upwork_cfg.logging_level == 'WARNING':
        message_level = logging.WARNING
    elif grab_upwork_cfg.logging_level == 'ERROR':
        message_level = logging.ERROR

    logger = logging.getLogger()
    logger.setLevel(message_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y‌​-%m-%d_%H-%M-%S')

    # логирование в файл
    log_path = 'logs'
    if not path.exists(log_path):
        print 'ERROR: Path "' + log_path + '" not found.'
        exit(1)

    date_time_log_file = functions.current_time().replace(' ', '_').replace(':', '-')
    log_file_name = date_time_log_file + '.log'
    file_handler = logging.FileHandler(log_path + path.sep + log_file_name)
    file_handler.setLevel(message_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # логирование в консоль
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(message_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.info('Logging level is ' + grab_upwork_cfg.logging_level)

    functions.clear_console()  # Очистить консоль
    logger.info('Start at ' + functions.current_time())

    # Поиск заказа по фразе
    if len(argv) != 2:
        logger.error('One parameter is required - the search string.')
        input()
        exit(1)
    else:
        order_find(argv[1])

    # functions.console_input(logger)

    # Получить ВЕБ-драйвер
    driver = functions.get_webdriver(grab_upwork_cfg, logger)

    # Открыть главную страницу сайта
    full_server_name = 'http://' + grab_upwork_cfg.site_name
    driver.get(full_server_name)

    # Пока не найдём элемент или N секунд (N сек - для всех, до отмены, глобально)
    driver.implicitly_wait(grab_upwork_cfg.implicitly_wait_timeout)

    # Доступен ли сервер
    result = functions.site_available(driver, 'Upwork')
    if not result:
        logger.info('Website ' + grab_upwork_cfg.site_name + ' or page is unavailable.')
        driver.close()
        logger.info('Quit at ' + functions.current_time())
        exit(1)

    # Логинимся
    logger.info('Login...')
    if upwork_logging(driver):
        logger.info('Successful login.')
    else:
        logger.error('Unsuccessful login.')
        driver.close()
        logger.info('Quit at ' + functions.current_time())
        exit(1)

    # Поиск заказа по фразе
    # order_find()

    functions.console_input(logger)

    # Разлогиниться
    logger.info('Logout...')
    if upwork_logout(driver, logger):
        logger.info('Successful logout.')
    else:
        logger.error('Unsuccessful logout')
        driver.close()
        logger.error('Quit at ' + functions.current_time())
        exit(1)

    # functions.console_input(logger)

    driver.close()  # Закрыть браузер
    logger.info('Quit at ' + functions.current_time())


def upwork_logging(driver):
    """ Авторизация """

    # Удаляем куки
    # driver.delete_all_cookies()

    # Выводим все куки доступные для текущего URL
    # for cookie in driver.get_cookies():
    #     print "%s -> %s" % (cookie['name'], cookie['value'])

    # Идём логиниться
    driver.find_element_by_xpath('//a[@href="/login"]').click()

    # Поле для имени пользователя
    username_field = driver.find_element_by_xpath('//input[@id="login_username"]')
    username_field.send_keys(pswd.user_name)

    # Поле для пароля
    password_field = driver.find_element_by_xpath('//input[@id="login_password"]')
    password_field.send_keys(pswd.user_password)

    # Кнопка "Log In"
    driver.find_element_by_xpath(
        '//button[@type="submit" and contains(text(),"Log In")]'
    ).click()

    # Проверка удачного логирования
    login_result = True
    try:
        driver.find_element_by_xpath(
            '//a[@title="Alex Jashhuk"]/span[text()="Alex Jashhuk"]'
        )
    except NoSuchElementException:
        login_result = False

    return login_result


def upwork_logout(driver, logger):
    """ Логаут - разлогирование """
    logout_result = True

    try:
        driver.find_element_by_xpath(
            '//a[@class="dropdown-toggle" and @title="Alex Jashhuk"]'
        ).click()
        driver.find_element_by_xpath(
            '//a[@data-ng-click="logout()"]'
        ).click()
    except NoSuchElementException:
        logger.error('Not logged in!')
        logout_result = False

    # Проверка удачного разлогирования
    try:
        driver.find_element_by_xpath('//h1[text()="Log in and get to work"]')
    except NoSuchElementException:
        logout_result = False

    return logout_result


if __name__ == '__main__':
    main()
