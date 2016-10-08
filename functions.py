# -*- coding: utf-8 -*-
from os import system, path
from sys import platform
from pytz import timezone
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# Очистка консоли в Windows и Linux
def clear_console():
    """ Console clearing in windows and linux. """
    if platform == 'win32':
        system('cls')
    else:
        system('clear')
    print("")


# Возвращает WebDriver соответствующий браузеру, указанному в INI-файле
def get_webdriver(config_file):
    """ Returns WebDriver the appropriate browser that you specified in the config-file. """
    driver = webdriver

    if config_file.browser.lower() == 'phantomjs':
        driver = webdriver.PhantomJS(executable_path='webdrivers' + path.sep + 'phantomjs')
    elif config_file.browser.lower() == 'chrome':
        driver = webdriver.Chrome(executable_path='webdrivers' + path.sep + 'chromedriver.exe')
    elif config_file.browser.lower() == 'firefox':      # FF v47.0.1, not older
        binary = FirefoxBinary('C:' + path.sep + 'Program Files' + path.sep + 'Mozilla Firefox' +
                               path.sep + 'firefox.exe')
        driver = webdriver.Firefox(firefox_binary=binary)
    else:
        print('In config file ' + config_file + ' the browser not specified.')
        exit(1)
    print("Use '" + config_file.browser.capitalize() + "' browser.")

    driver2 = set_browser_size(driver, config_file)  # Размеры окна браузера

    return driver2


# Установка размера окна браузера
def set_browser_size(driver, config_file):
    """ Sets the size of the browser window. """
    try:
        width = config_file.browser_size[0]
        height = config_file.browser_size[1]
    except KeyError:
        print('The size of the browser window is not specified in the config-file, will be maximum size.')
        driver.maximize_window()
    else:
        driver.set_window_size(width, height)

    return driver


# Проверяет доступность сайта и, если недоступен, выходит из программы.
# Параметры: driver - экземпляр WebDriver-а, part_string - часть title страницы
# Возвращает: boolean
def site_available(driver, part_string):
    """ Checks the availability of the website and, if unavailable, out of the program. """
    site_title = driver.title
    try:
        site_title.index(part_string)
    except ValueError:
        status = False
    else:
        status = True
    return status


# Обработка символа в консоли
# Считывает символ с консоли, при 'q', 'Q' - выход из приложения,
#  при 'n', 'N' - ничего не делаем и идём дальше, при других символах - снова считываем
def input_symbol():
    """
    Processing symbol in the console:
                                     'q', 'Q' - quit application;
                                     'n', 'N' - do nothing and continue;
                                     with other characters - again read
    """
    print("Input 'q' and 'Enter' to exit or input 'n' 'Enter' to continue: ")
    status = ''
    input_string = ''

    while input_string != 'q' and input_string != 'Q' and input_string != 'n' and input_string != 'N':

        input_string = raw_input()

        if input_string == 'q' or input_string == 'Q':
            status = 'exit'
            print(u'Quit.')
        elif input_string == 'n' or input_string == 'N':
            print(u'Continue.')
            status = 'next'
        else:
            print('Bad input: ' + input_string)

    return status


def console_input():
    """ Check the result of the character input and, if necessary, exit the application. """
    if input_symbol() == 'exit':
        print('Bye-bye!')
        exit(2)


# Возврат форматированных текущих даты и времени с временнОй зоной
def current_time():
    """ Return a formatted current date and time with time zone. """
    return timezone('Europe/Moscow').fromutc(datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S %Z")
