import time
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def find_rnk(rnk: str, id: str, years: str) -> None:
    """ Поиск нужного идентификатора по РНК

    Данная функция принимает три аргумента -  РНК, идентификатор и год этапа контракта.
    При помощи selenium функция открывает нужную страницу, переходит на нужную вкладку. Открывает
    выпадающий список с различными идентификаторами. Далее с помощью bs4 в исходном коде страницы
    осуществляется поиск нужного идентификатора. Если на странице его нет - переход на следующую.

    
    """ 
    rnk = int(rnk)
    url = f'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber={rnk}'
    arrow = True
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
    chrome_options.headless = True # also works
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    time.sleep(2)
    # закрыть всплывающее окно
    driver.find_element(By.XPATH, "//div[@id='sslCertificateChecker-right']").find_element(
        By.XPATH, 
        "//span[@class='btn-close closePopUp']"
    ).click()
    wait.until(EC.visibility_of_element_located((
        By.XPATH, 
        "//div[@class='tabsNav d-flex align-items-end']"
    )))
    # открыть вкладку "Исполнение (расторжение) контракта"
    driver.find_element(By.XPATH, "//div[@class='tabsNav d-flex align-items-end']").find_element(
        By.XPATH,
        "//a[contains(@href, 'process-info')]"
    ).click()
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='contractExecution']")))
    # раскрыть список документов в соответствии с годом
    driver.find_element(
        By.XPATH, 
        f"""//td[.//div[contains(text(), '{years}')]]
        //preceding-sibling::td//span[contains(@class, 'general-chevron-handler')]""").click()
    while arrow:
        try:
            time.sleep(1)
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//table[@class='blockInfo__table tableBlock grayBorderBottom']"))
            )
            # найти блок с идентификатором 
            _e = BeautifulSoup(driver.page_source, "html.parser").find(
                'table', {"class": "blockInfo__table tableBlock grayBorderBottom"})
            # поиск в блоке заданного идентификатора (id)
            l = [x for x in 
                 _e.find_all("td", {"class": "tableBlock__col tableBlock__col_first"}) 
                 if id in x.text]
            if l:
                arrow = False
                for td in l:
                    span = td.find('span', class_="section__title")
                    idf = []
                    if span:
                        id_text = span.text.strip()
                        id_num = id_text.split(':')[-1].strip()
                        idf.append(id_num)
                    print(f'Элемент {''.join(idf)} найден')
            else:
                try:
                    # нажать на стрелку для перехода на другую страницу
                    t = driver.find_element(
                        By.XPATH, 
                        """//div[@class='d-flex justify-content-between']"""
                    ).find_element(
                        By.XPATH, 
                        "//a[@class='paginator-button paginator-button-next cursorPointer general-pagination-page-select-handler']"
                    )
                    t.click()
                except Exception: 
                    break
        except Exception as e: # NoSuchElementException:
            # print(driver.page_source)
            pass
    if not l: 
        print(f'Элемент {id} не найден')
    

def cli() -> None:
    args: list = []
    if len(sys.argv) < 3:
        args.append(input("Введите rnk: "))
        args.append(input("Введите id: "))
        args.append(input("Введите год: "))
    else:
        args = sys.argv[1:]
    find_rnk(*args)


if __name__ == "__main__":
    cli()