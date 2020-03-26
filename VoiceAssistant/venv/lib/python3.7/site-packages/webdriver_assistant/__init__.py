#!/usr/bin/env python
# coding: utf-8

import os
import re
import time
import platform
from typing import Optional

from selenium.webdriver import Chrome, ChromeOptions, DesiredCapabilities

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from contextlib import contextmanager

system_is_linux = platform.system() == 'Linux'


class BrowserTimeout(Exception):
    pass


def start_display_on_linux():
    """
    Ubuntu の場合、仮想フレームバッファを起動する
    生で使わずに、下に書いてあるコンテクストマネージャを使うこと
    """
    if not system_is_linux:
        return
    try:
        from pyvirtualdisplay import Display
    except ImportError:
        return

    display = Display(visible=0, size=(1280, 800))
    display.start()
    return display


@contextmanager
def virtual_display_on_linux():
    """
    仮想ディスプレイを起動じ、自動的にクローズするコンテクストマネージャ
    デコレータとしても使える
    使う時は () 必要なので書き忘れないこと
    """
    display = start_display_on_linux()
    yield display
    if display:
        display.stop()


default_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/67.0.3396.99 Safari/537.36'


def start_chrome_driver(
        *, headless: Optional[bool] = None,
        user_agent: Optional[bool] = None,
        insecure: bool = False) -> WebDriver:
    options = ChromeOptions()

    def _is_headless_mode():
        if headless is None:
            import sys
            if 'test' in sys.argv:
                return True
        return headless or system_is_linux

    if _is_headless_mode():
        # ヘッドレスモードを有効にする
        options.add_argument('--headless')
    options.add_argument('--lang=ja')

    if system_is_linux:
        options.add_argument('--no-sandbox')
        options.add_argument('--no-zygote')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

    options.add_argument('--ignore-certificate-errors')  # 多分意味ない
    if user_agent is None:
        user_agent = default_user_agent
    options.add_argument(
        '--user-agent=' + user_agent)

    capabilities = DesiredCapabilities.CHROME
    if insecure:
        capabilities['acceptSslCerts'] = True  # 多分意味ない
        capabilities['acceptInsecureCerts'] = True  # 効く

    driver = Chrome(options=options, desired_capabilities=capabilities)
    return driver


def preview(driver: WebDriver, filename_prefix: str = None) -> None:
    """
    画像とHTMLでプレビュー
    """
    import subprocess
    import tempfile

    tmpdir = tempfile.gettempdir()
    filename_prefix = filename_prefix or 'webdriver-assistant-preview'
    png_path = os.path.join(tmpdir, '{}.png'.format(filename_prefix))
    html_path = os.path.join(tmpdir, '{}.html'.format(filename_prefix))

    driver.save_screenshot(png_path)

    subprocess.Popen(['open', png_path])
    with open(html_path, 'w') as fp:
        fp.write(driver.page_source)
    subprocess.Popen(['open', html_path])


def wait_visible(driver: WebDriver, css_selector: str,
                 timeout: int = 3000) -> None:
    """
    エレメントが表示されるまで待つ
    """
    for i in range(int(timeout / 100)):
        e = driver.find_element_by_css_selector(css_selector)
        if e.is_displayed():
            return
        time.sleep(0.1)
    raise BrowserTimeout(css_selector)


def find_element_or_none(
        driver: WebDriver, css_selector: str
) -> Optional[WebElement]:
    """
    エレメントを取得、もしくは None
    """
    try:
        return driver.find_element_by_css_selector(css_selector)
    except WebDriverException:
        return None


def build_requests_session(driver: WebDriver):
    import requests
    from requests.cookies import create_cookie

    s = requests.session()
    s.headers['User-Agent'] = default_user_agent
    for cookie in driver.get_cookies():
        c = create_cookie(**{
            'name': cookie['name'],
            'value': cookie['value'],
            'domain': cookie['domain'],
            'path': cookie['path'],
            'expires': cookie['expiry'],
            'secure': cookie['secure'],
            'rest': {'HttpOnly': cookie['httpOnly'], },
        })
        s.cookies.set_cookie(c)

    return s


def fill_inputs(driver: WebDriver, data: dict) -> None:
    for key, value in data.items():
        e = find_element_or_none(driver, key)
        if not e:
            continue
        e.send_keys(value)


def send_return(driver: WebDriver, css_selector: str) -> None:
    e = find_element_or_none(driver, css_selector)
    if not e:
        return
    e.send_keys(Keys.RETURN)


def parse_url_query(url, flatten=True, *kwargs):
    """
    Get parsed url queries
    """
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(url)
    qs = parse_qs(parsed_url.query, *kwargs)
    if not flatten:
        return qs
    return {
        k: v if len(v) >= 2 else v[0]
        for k, v in qs.items()
    }


def val(driver: WebDriver, css_selector, text=None, wait=True, end=None,
        enter=False):
    """
    テキストを入力もしくは取得
    """
    if wait:
        wait_visible(driver, css_selector)
    if text is None:
        return driver.find_element_by_css_selector(css_selector) \
            .get_attribute('value')
    element = driver.find_element_by_css_selector(css_selector)
    element.clear()
    if enter:
        end = Keys.ENTER
    t = element.get_attribute('type')
    if t == 'file':
        element.send_keys(text)
    else:
        element.send_keys(text, end if end is not None else Keys.TAB)


def find_elements_by_css_selector_and_text_match(
        driver: WebDriver, css_selector: str, re_text: str):
    """
    css_selector で絞り込んだ後、re_text にテキストマッチするものをさらに探して
    返す
    """
    re_compiled = re.compile(re_text)
    elements = driver.find_elements_by_css_selector(css_selector)
    for element in elements:
        if re_compiled.search(element.text):
            yield element


def find_element_by_css_selector_and_text_match(
        driver: WebDriver, css_selector: str, re_text: str):
    for e in find_elements_by_css_selector_and_text_match(
            driver, css_selector, re_text):
        return e


def find_elements_by_css_selector_matched(
        driver: WebDriver, css_selector: str, match_method: callable):
    """
    css_selector で絞り込んだ後、match_method でマッチしたものを返す
    """
    elements = driver.find_elements_by_css_selector(css_selector)
    for element in elements:
        if match_method(element):
            yield element


def find_element_by_css_selector_matched(
        driver: WebDriver, css_selector: str, match_method: callable):
    for e in find_elements_by_css_selector_matched(
            driver, css_selector, match_method):
        return e


def vlookup_text_match(driver: WebDriver, tr_css_selector, re_text,
                       td_position, td_css_selector='td'):
    """
    :param tr_css_selector: tr タグを絞り込むための CSS セレクタ
    :param re_text: tr タグのテキストを検索するための正規表現文字列
    :param td_position: td のいくつめを返すか。0スタート
    :param td_css_selector: td のセレクタ。td タグ以外を検索する場合など変更
    """
    tr = find_element_by_css_selector_and_text_match(
        driver, tr_css_selector, re_text)
    tds = tr.find_elements_by_css_selector(td_css_selector)
    return tds[td_position]


def vlookup_text_matched(driver: WebDriver, tr_css_selector, match_method,
                         td_position, td_css_selector='td'):
    """
    :param tr_css_selector: tr タグを絞り込むための CSS セレクタ
    :param match_method: tr タグのテキストを検索するためのメソッド
    :param td_position: td のいくつめを返すか。0スタート
    :param td_css_selector: td のセレクタ。td タグ以外を検索する場合など変更
    """
    tr = find_elements_by_css_selector_matched(
        driver, tr_css_selector, match_method)
    tds = tr.find_elements_by_css_selector(td_css_selector)
    return tds[td_position]
