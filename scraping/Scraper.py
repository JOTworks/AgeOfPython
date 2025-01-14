import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pickle
import os
from pprint import pprint

def save_to_file(data, file_name):
    if not file_name.endswith('.pkl'):
        file_name += '.pkl'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def open_file(file_name):
    if not file_name.endswith('.pkl'):
        file_name += '.pkl'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def good_soup(url_list, class_to_wait:str = None, wait_time:int = 0):
    driver = webdriver.Chrome()
    soup = []
    if isinstance(url_list, str):
        url_list = [url_list]
    for url in url_list:
        try:
            driver.get(url)
            if class_to_wait:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_to_wait))
                )
            if wait_time > 0:
                time.sleep(wait_time)
        finally:
            html = driver.page_source
            soup.append(BeautifulSoup(html, "html.parser"))
    driver.quit()
    if len(soup) == 1:
        return soup[0]
    return soup

def save_command_names():
    soup = good_soup("https://airef.github.io/commands/commands-index.html", class_to_wait = "command-name")
    command_names = [c.text for c in soup.find_all(attrs={'class' : 'command-name'}, recursive=True)]
    save_to_file(command_names, 'command_names.pkl')

def save_command_parameters(): 
    command_names = open_file('command_names.pkl')
    soups = good_soup(["https://airef.github.io/commands/commands-details.html#"+name for name in command_names])
    command_dict = {}
    if len(command_names) != len(soups):
        raise ValueError("Number of command names and soups do not match")
    for name, soup in zip(command_names, soups):
        command_params = [c.text for c in soup.find_all(attrs={'class' : 'param'}, recursive=True)]
        command_dict[name] = command_params 
        save_to_file(command_dict, 'command_dict.pkl')

def save_parameter_names():
    soup = good_soup("https://airef.github.io/parameters/parameters-index.html")
    list_data = soup.find("table", attrs={"id": "index-table"}).find_all("tr")
    parameter_names = [data.find_all("td")[0].get_text(strip=True) for data in list_data[1:]]
    save_to_file(parameter_names, 'parameter_names.pkl')

def find_description_column(list_data):
    header_row = list_data[0].find_all("th")  # Assuming the header is in <th> tags
    for index, cell in enumerate(header_row):
        if cell.get_text(strip=True) == "Description":
            return index
    return -1  # Return -1 if "Description" is not found

def save_parameter_options(): #WIP
    '''
    compareOp - spaces 
    ActionId, Formation, OrderId - has -1
    buildingID, EventType - only has 1 entry
    alot have result of
    ['Version Introduced', 'Related Parameters', 'Used In These Commands']
    because there is not a param list. they should be blank? or accecp a number perhapse?
    '''
    parameter_names = open_file('parameter_names.pkl')
    soups = good_soup(["https://airef.github.io/parameters/parameters-details.html#"+name for name in parameter_names],wait_time=5)
    parameter_dict = {}
    if len(parameter_names) != len(soups):
        raise ValueError("Number of parameter names and soups do not match")
    for name, soup in zip(parameter_names, soups):
        #need to get the list data, and figure out what the names of each thing is
        try:
            list_data = soup.find_all("table",recursive=True)[-1].find_all("tr")
        except IndexError:
            raise Exception(f"Could not find table in soup for {name}")
        description_column_index = find_description_column(list_data)
        if description_column_index == -1:
            parameter_dict[name] = []
        else:
            if name == "compareOp":
                description_column_index -= 2
            parameter_options = [data.find_all("td")[description_column_index-1].get_text(strip=True) for data in list_data[1:]]
            parameter_dict[name] = parameter_options 
    save_to_file(parameter_dict, 'parameter_dict.pkl')

save_command_names()
save_parameter_names()
save_command_parameters()
#save_parameter_options()

#parameter_dict = open_file('parameter_dict.pkl')
#for p in parameter_dict:
#    pprint(p)
#    pprint(parameter_dict[p])
#    input("Press Enter to continue...")
#pprint(len(parameter_dict))