# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException

import functions
import grab_upwork_cfg
import pswd

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
    if not result:
        print 'Website ' + grab_upwork_cfg.site_name + ' or page is unavailable.'
        driver.close()
        exit(1)

    # Логинимся
    print 'Login...'
    if upwork_logging(driver):
        print 'Successful login.'
    else:
        print 'Unsuccessful login'
        driver.close()
        exit(1)

    functions.input_symbol()

    # Разлогиниться
    print 'Logout...'
    if upwork_logout(driver):
        print 'Successful logout.'
    else:
        print 'Unsuccessful logout'
        driver.close()
        exit(1)

    functions.input_symbol()

    driver.close()  # Закрыть браузер


def upwork_logging(driver):
    # Идём логиниться
    driver.find_element_by_xpath('//a[@href="/login"]').click()

    # Поле для имени пользователя
    username_field = driver.find_element_by_xpath('//input[@id="login_username"]')
    username_field.send_keys(pswd.user_name)

    # Поле для пароля
    password_field = driver.find_element_by_xpath('//input[@id="login_password"]')
    password_field.send_keys(pswd.user_password)

    # Кнопка "Log In"
    driver.find_element_by_xpath('//button[@type="submit" and contains(text(),"Log In")]').click()

    # Проверка удачного логирования
    login_result = True
    try:
        driver.find_element_by_xpath('//a[@title="Alex Jashhuk"]/span[text()="Alex Jashhuk"]')
    except NoSuchElementException:
        login_result = False

    return login_result


def upwork_logout(driver):
    driver.find_element_by_xpath('//a[@class="dropdown-toggle" and @title="Alex Jashhuk"]').click()
    driver.find_element_by_xpath('//a[@data-ng-click="logout()"]').click()

    # Проверка удачного разлогирования
    logout_result = True
    try:
        driver.find_element_by_xpath('//h1[text()="Log in and get to work"]')
    except NoSuchElementException:
        logout_result = False

    return logout_result


if __name__ == '__main__':
    main()
