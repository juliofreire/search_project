# Import packages
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from io_files import save_dict_in_file

# Some setups to search
# url = 'https://www.olx.com.br'
#################### CONGIS #######################
url = 'https://www.olx.com.br/imoveis/'
price_min = 150000
price_max = 300000
state = "Rio Grande do Norte"
city = "Natal"
type_of_property = "house" # options: house, apartament or both
ADD_LINK = True

first_setup = {"category-selector": "Venda", # or "Aluguel" #
         "location-selector": state, # Estado
        }

prices = {"specific_price": True, # False to not specific a range price
          "price_min": str(price_min),
          "price_max": str(price_max),
        }
####################################################

firefox_options = webdriver.FirefoxOptions()
firefox_options.set_preference('intl.accept_languages', 'pt')
firefox = webdriver.Firefox(options=firefox_options)
firefox.maximize_window()

# Accessing the url and doing some stuffs
firefox.get(url)

# time.sleep(5)

xpath = '//*[@id="adopt-accept-all-button"]'
cookies_button = WebDriverWait(firefox, 10).until(
    EC.element_to_be_clickable((By.XPATH, xpath))
)
cookies_button.click()


for key, value in first_setup.items():
    dropdown = firefox.find_element(By.ID, key)
    select = Select(dropdown)
    select.select_by_visible_text(value)

if prices["specific_price"]:
    min_price_input = firefox.find_element(By.ID, "price_min")
    min_price_input.clear()
    min_price_input.send_keys(prices["price_min"])

    max_price_input = firefox.find_element(By.ID, "price_max")
    max_price_input.clear()
    max_price_input.send_keys(prices["price_max"])


xpath = '/html/body/div[1]/main/section[1]/div[3]/div/div/a/span'
search_button = WebDriverWait(firefox, 10).until(
    EC.element_to_be_clickable((By.XPATH, xpath))
)
search_button.click()

# time.sleep(5)
WebDriverWait(firefox, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)

def checkboxes(type_of_property):
    match type_of_property:
        case "house":
            xpath_house = '/html/body/div[1]/div[1]/main/div[2]/div/div/div/div/div/div[2]/fieldset/fieldset[1]/ul/li[2]/label/label/input'
            checkbox_house = WebDriverWait(firefox, 15).until(
                EC.element_to_be_clickable((By.XPATH, xpath_house))
            )
            if not checkbox_house.is_selected():
                firefox.execute_script("arguments[0].scrollIntoView(true)", checkbox_house)
                checkbox_house.click()
        case "apartament":
            xpath_apartament = '/html/body/div[1]/div[1]/main/div[2]/div/div/div/div/div/div[2]/fieldset/fieldset[1]/ul/li[1]/label/label/input'
            checkbox_apartament = WebDriverWait(firefox, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_apartament))
            )
            if not checkbox_apartament.is_selected():
                firefox.execute_script("arguments[0].scrollIntoView(true)", checkbox_apartament)
                checkbox_apartament.click()
        case "both":
            xpath_house = '/html/body/div[1]/div[1]/main/div[2]/div/div/div/div/div/div[2]/fieldset/fieldset[1]/ul/li[2]/label/label/input'
            checkbox_house = WebDriverWait(firefox, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_house))
            )
            if not checkbox_house.is_selected():
                firefox.execute_script("arguments[0].scrollIntoView(true)", checkbox_house)
                checkbox_house.click()

            xpath_apartament = '/html/body/div[1]/div[1]/main/div[2]/div/div/div/div/div/div[2]/fieldset/fieldset[1]/ul/li[1]/label/label/input'
            checkbox_apartament = WebDriverWait(firefox, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_apartament))
            )
            if not checkbox_apartament.is_selected():
                firefox.execute_script("arguments[0].scrollIntoView(true)", checkbox_apartament)
                checkbox_apartament.click()


time.sleep(3)
checkboxes(type_of_property)

time.sleep(2)
firefox.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")


time.sleep(2)
xpath = '//*[@id="location-autocomplete-desktop-input"]'
# xpath = '//*[@id="location-autocomplete-desktop-input"]'

city_input = WebDriverWait(firefox, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)

# city_input = WebDriverWait(firefox, 10).until(
#     firefox.find_element(By.XPATH, xpath)
# )

time.sleep(2)
city_input.clear()
city_input.send_keys(city)

xpath = '/html/body/div[1]/div[1]/main/div[2]/div/main/div[3]/div[2]/form/div/div/ul/div/li[1]'

first_input = WebDriverWait(firefox, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)

first_input.click()

time.sleep(1)

#div das sections
#/html/body/div[1]/div[1]/main/div[2]/div/main/div[7]
def find_house_div():
    div_houses = firefox.find_element(By.XPATH, '/html/body/div[1]/div[1]/main/div[2]/div/main/div[7]')
    return div_houses


def find_house_info(ul_section):
    # time.sleep(5)
    house_info=[]
    WebDriverWait(firefox, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'li'))
    )
    for ul_index, ul in enumerate(ul_section, start=1):
        # print(f"Ul {ul_index} from section {index}")
        # if ul_index==1:
            # print("ok")
        li_elements = ul.find_elements(By.TAG_NAME, "li")
        if ul_index==2:
            for li in li_elements:
                WebDriverWait(firefox, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'span'))
                )
                spans_element = li.find_elements(By.TAG_NAME, "span")
                for span in spans_element:
                    house_info.append(span.get_attribute("aria-label"))
        if ul_index==3:
            tag_property = "Direto com o proprietario"
            house_info.append(tag_property)
    return house_info

def find_house_price(house_section):
    WebDriverWait(firefox, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h3"))
    )
    house_price = house_section.find_element(By.TAG_NAME, "h3")
    # print(house_price.text)

    return house_price.text


def find_house_location(house_section):
    WebDriverWait(firefox, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'p'))
    )
    house_location = house_section.find_element(By.XPATH, ".//div[2]/div[2]/div/div/div[1]/p")
    return house_location.text

def find_house_link(house_section):
    WebDriverWait(firefox, 10).until(
        EC.presence_of_element_located((By.XPATH, './/a'))
    )
    house_href = house_section.find_element(By.XPATH, ".//a")
    house_link = house_href.get_attribute("href")
    return house_link


def crawl_house_info(index=0, dict_houses_info=None):
    # time.sleep(3)
    if index== 0 or dict_houses_info is None:
        dict_houses_info = {}
    div_houses = find_house_div()
    WebDriverWait(div_houses, 10).until(
        EC.presence_of_element_located((By.XPATH, './/section'))
    )
    house_sections = div_houses.find_elements(By.XPATH, './/section')

    for _, section in enumerate(house_sections, start=1):
        # print(f"Section {section_index}")

        ul_section = section.find_elements(By.TAG_NAME, "ul")

        house_info = find_house_info(ul_section)
        house_price = find_house_price(section)
        house_location = find_house_location(section)
        house_link = find_house_link(section)

        if ADD_LINK == False:
            dict_houses_info[index]={"house_info": house_info, "house_price": house_price, \
                                 "house_location": house_location}
        else:
            dict_houses_info[index]={"house_info": house_info, "house_price": house_price, \
                                 "house_location": house_location, "house_link": house_link}
            
        # print("-" * 30)
        index+=1
    return index, dict_houses_info


def crawl_pages(index=0, dict_houses=None, limitter=100):

    next_page_up = True
    pages = 0
    while next_page_up == True and pages < limitter:
        try:
            index, dict_houses = crawl_house_info(index, dict_houses)

            buttons = WebDriverWait(firefox, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="listing-pagination"]//button'))
                # EC.element_to_be_clickable((By.XPATH, '//*[@id="listing-pagination"]//a[contains(text(), "Próxima página")]'))
            )
            next_page_button = buttons[-2]
            if next_page_button.get_attribute("aria-disabled") == "true":
                print("O programa vai finalizar porque não tem mais páginas")
                next_page_up = False
            print(next_page_button.text)
            # print(next_page_button)
            # next_page_button = firefox.find_element(By.XPATH, '//*[@id="listing-pagination"]//a[contains(text(), "Próxima página")]')
            # firefox.execute_script("arguments[0].click();", next_page_button)
            firefox.execute_script("arguments[0].scrollIntoView(true)", next_page_button)
            WebDriverWait(firefox, 10).until(
                EC.element_to_be_clickable(next_page_button)
            )
            time.sleep(3)
            next_page_button.click()
            time.sleep(2)
            pages+=1
        except NoSuchElementException:
            next_page_up == False

    return index, dict_houses

index = 0
dict_houses = {}
i, d = crawl_pages(index, dict_houses, 5)
print(d)

firefox.quit()

save_dict_in_file(d, "houses_dict")

