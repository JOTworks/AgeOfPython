import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pickle
import os
from pprint import pprint
from typing import Dict

class ParameterStorage:
    def __init__(self, options: Dict[int, str], range, parameter_description = None):
        self.description = parameter_description
        self.range = range
        self.options = options

class CommandStorage:
    def __init__(self,args , command_description = None, ):
        self.args = args
        self.description = command_description
        

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

def good_soup(url_list, class_to_wait:str = None, wait_time:int = 1):
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
    soups = good_soup(["https://airef.github.io/commands/commands-details.html#"+name for name in command_names],wait_time=.2)
    command_dict = {}
    if len(command_names) != len(soups):
        raise ValueError("Number of command names and soups do not match")
    for name, soup in zip(command_names, soups):
        command_description = get_description_text(soup)
        command_params = [c.text for c in soup.find_all(attrs={'class' : 'param'}, recursive=True)]
        command_dict[name] = CommandStorage(command_params, command_description)
        save_to_file(command_dict, 'command_dict.pkl')

def save_parameter_names():
    soup = good_soup("https://airef.github.io/parameters/parameters-index.html")
    data_table = soup.find("table", attrs={"id": "index-table"}).find_all("tr")
    parameter_names = [data.find_all("td")[0].get_text(strip=True) for data in data_table[1:]]
    save_to_file(parameter_names, 'parameter_names.pkl')

def find_description_column(data_table):
    header_row = data_table.find('tr').find_all('th')
    for index, cell in enumerate(header_row):
        if cell.get_text(strip=True) == "Description":
            return index
    return None # Return -1 if "Description" is not found

def find_id_column(data_table):
    header_row = data_table.find('tr').find_all('th')
    for index, cell in enumerate(header_row):
        if cell.get_text(strip=True) == "DE ID":
            return index
    for index, cell in enumerate(header_row):
        if cell.get_text(strip=True) == "ID":
            return index
    return None  # Return -1 if "Description" is not found

def find_data_table(name,soup):
    # Find all tables on the page
    tables = soup.find_all('table')
    
    # Iterate over the tables in reverse order
    for table in reversed(tables):
        header_row = table.find('tr').find_all('th')  # Assuming the header is in <th> tags
        for cell in header_row:
            if cell.get_text(strip=True) == "Description":
                return table
    return None  # Return None if no such table is found
        
def find_info_table(name,soup):
    # Find all h3 tags
    h3_tags = soup.find_all('h3')
    for h3 in h3_tags:
        # Check if the h3 tag contains the text "Info"
        if h3.get_text(strip=True) == "Info":
            # Find the next table after this h3 tag
            next_table = h3.find_next('table')
            if next_table:
                return next_table
    return None  # Return None if no such table is found

def get_description_text(soup):
    description_h3 = soup.find('h3', string="Description")
    info_h3 = soup.find('h3', string="Info")
    
    if not description_h3 or not info_h3:
        return ""
    
    # Find all <p> tags between the two <h3> tags
    p_tags = []
    for tag in description_h3.find_all_next():
        if tag == info_h3:
            break
        if tag.name == 'p':
            p_tags.append(tag.get_text(strip=True))
    
    return ' '.join(p_tags)

def save_parameter_options(test = None): #WIP
    '''
    compareOp - spaces 
    ActionId, Formation, OrderId - has -1
    buildingID, EventType - only has 1 entry
    alot have result of
    ['Version Introduced', 'Related Parameters', 'Used In These Commands']
    because there is not a param list. they should be blank? or accecp a number perhapse?
    '''
    parameter_names = open_file('parameter_names.pkl')
    if test:
        parameter_names = parameter_names[:test]
    soups = good_soup(["https://airef.github.io/parameters/parameters-details.html#"+name for name in parameter_names],wait_time=1)
    parameter_dict = {}
    if len(parameter_names) != len(soups):
        raise ValueError("Number of parameter names and soups do not match")
    for name, soup in zip(parameter_names, soups):
        
        data_table = find_data_table(name,soup)
        info_table = find_info_table(name,soup)

        parameter_storage = ParameterStorage(None,None,get_description_text(soup))

        if data_table:
            description_column_index = find_description_column(data_table)
            id_column_index = find_id_column(data_table)
            if name == "compareOp":
                description_column_index -= 2

            parameter_options = [data.find_all("td")[description_column_index-1].get_text(strip=True) for data in data_table.find_all('tr')[1:]]
            option_ids = [data.find_all("td")[id_column_index].get_text(strip=True) for data in data_table.find_all('tr')[1:]]
            parameter_storage.options = dict(zip(parameter_options, option_ids))
        if info_table:
            info_title = info_table.find_all('tr')[0].find_all('td')[0].get_text(strip=True)
            info_value = info_table.find_all('tr')[0].find_all('td')[1].get_text(strip=True)
            parameter_storage.range = f'{info_title}: {info_value}'
        
        parameter_dict[name] = parameter_storage
            
        
    save_to_file(parameter_dict, 'parameter_dict.pkl')


def make_parameter_class_lines(parameter_name,parameter_storage: ParameterStorage):
    lines = []
    lines.append(f"class {parameter_name}(enum):")
    if parameter_name in ['typeOp','mathOp','compareOp']:
        lines.append('    pass')
        return lines
    parameter_options_dict = parameter_storage.options
    if not parameter_options_dict:
        lines.append('    pass #empty options_dict')
        return lines
    for option, id in parameter_options_dict.items():
        option = option.replace('-','_')
        option = option.replace(' ','_')
        if parameter_name in ['ObjectData','ClassId']:
            option = option.replace('*','')
        if parameter_name in ['AttrId']:
            option = option.replace('.','')
        lines.append(f"    {option} = {id}")
    return lines

def get_arg_type(arg, p_dict):
    if arg == "String":
        return "str"
    if not p_dict[arg].options:
        return "int"
    if len(p_dict[arg].options) == 0:
        return "int"
    else:
        return arg

def make_function_def_lines(command_name,command_storage: CommandStorage, p_dict):
    lines = []
    args = command_storage.args
    def_line = f"def {command_name.replace('-','_')}("
    help_text = ['    """',command_storage.description]
    arg_duplicate_counter = {arg:0 for arg in set(args)}
    for arg in args:
        if arg == 'typeOp':
            continue
        elif arg in ['Point1','Point2']:
            def_line += f'{arg}:Point,'
            help_text.append(f':param {arg}: is a point object')
        elif arg in p_dict:
            arg_count = str(arg_duplicate_counter[arg]) if arg_duplicate_counter[arg] > 0 else ''
            arg_duplicate_counter[arg] += 1
            parameter_storage = p_dict[arg]
            def_line += f'{arg}{arg_count}: {get_arg_type(arg, p_dict)},'
            help_text.append(f':param {arg}{arg_count}: {parameter_storage.range}')
            help_text.append(f'{parameter_storage.description}')
        else:
            def_line += f'{arg},'
            help_text.append(f':param {arg}: NOT_DEFINED')
    def_line += "):"
    lines.append(def_line)
    help_text.append('"""')
    lines += help_text
    lines.append('    pass')
    return lines

def make_import_lines():
    return [
        '# --- Removed parameters --- #',
        '# all of the parameter types from the website with their IDs.',
        '# mathops and comparison ops are handdled by the intepreter.',
        '#',
        "import enum",
    ]

def generate_aoe2scriptEnums():
    p_dict = open_file('parameter_dict.pkl')
    lines = []
    lines += make_import_lines()
    for parameter_name, parameter_storage in p_dict.items():
        lines += make_parameter_class_lines(parameter_name, parameter_storage)
    
    output_path = os.path.join(os.path.dirname(__file__), 'aoe2scriptEnums.py')
    with open(output_path, 'w') as file:
        file.write('\n'.join(lines))

def generate_aoe2scriptFunctions():
    c_dict = open_file('command_dict.pkl')
    p_dict = open_file('parameter_dict.pkl')
    lines = ["from aoe2scriptEnums import *"]
    for command_name, command_storage in c_dict.items():
        lines += make_function_def_lines(command_name,command_storage, p_dict)

    output_path = os.path.join(os.path.dirname(__file__), 'aoe2scriptFunctions.py')
    with open(output_path, 'w') as file:
        file.write('\n'.join(lines))

"""
#TODO:
 -- pull the object https://airef.github.io/tables/objects.html
 and populate unitID buildingID and and sort out any other categories
"""
#save_command_names()
#save_parameter_names()
#save_command_parameters()
#save_parameter_options()
generate_aoe2scriptEnums()
generate_aoe2scriptFunctions()
