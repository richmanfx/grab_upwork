# -*- coding: utf-8 -*-
from os import system
import functions
import grab_upwork_cfg
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver

VERSION = '1.0.0'
__author__ = 'Aleksandr Jashhuk, Zoer, R5AM, www.r5am.ru'


def main():
    functions.clear_console()  # Очистить консоль
    print 'Start at ' + functions.current_time()

    # Получить ВЕБ-драйвер
    driver = functions.get_webdriver(grab_upwork_cfg)

    # Открыть главную страницу сайта
    full_server_name = 'http://' + grab_upwork_cfg.site_name
    driver.get(full_server_name)

    # Пока не найдём элемент или N секунд (N сек - для всех, до отмены, глобально)
    driver.implicitly_wait(grab_upwork_cfg.implicitly_wait_timeout)

    # Доступен ли сервер
    result = functions.site_available(driver, 'Upwork')
    print result
    if not result:
        print 'Website ' + grab_upwork_cfg.site_name + ' or page is unavailable.'
        driver.close()
        exit(1)

    driver.close()          # Закрыть браузер


if __name__ == '__main__':
    main()
