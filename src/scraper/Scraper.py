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
from itertools import chain
import inspect
import logging
logger = logging.getLogger(__name__)


class ObjectStorage:
    def __init__(
        self, id, name, ai_name, line, obj_class, cmd_id, category, age, dead_id
    ):
        self.id = id
        self.name = name
        self.ai_name = ai_name
        self.line = line
        self.obj_class = obj_class.split(" (")[0]
        self.obj_class_id = obj_class.split("(")[1].replace(")", "")
        self.cmd_id = cmd_id
        self.category = category
        self.age = age
        self.dead_id = dead_id


class TechnologyStorage:
    def __init__(self, id, name, ai_name, building, age, civ):
        self.id = id
        self.name = name
        self.ai_name = ai_name
        self.building = building
        self.age = age
        self.civ = civ


class ParameterStorage:
    def __init__(self, options, range, parameter_description=None):
        self.description = parameter_description
        self.range = range
        self.options = options


class CommandStorage:
    def __init__(self, args, command_description, type, version, category, complexity):
        self.args = args
        self.description = command_description
        self.type = type
        self.version = version
        self.category = category
        self.complexity = complexity


class StrategicNumberStorage:
    def __init__(
        self,
        name,
        id,
        description,
        default,
        min,
        max,
        min_req,
        max_req,
        category,
        effective,
        network,
        defined,
        active,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.default = default
        self.min = min
        self.max = max
        self.min_req = min_req
        self.max_req = max_req
        self.category = category
        self.effective = effective  # indicates whether the strategic number has an impact on AI behavior.
        self.network = network  # indicates whether the strategic number is sent along the network to clients to prevent out of sync issues.
        self.defined = defined  # indicates whether the name of the strategic number is predefined in the AI engine and doesn't require a defconst to be used.
        self.active = active  # indicates that the strategic number cannot be used like an extra goal because it's value impacts the game


def save_to_file(data, file_name):
    if not file_name.endswith(".pkl"):
        file_name += ".pkl"
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, "wb") as file:
        pickle.dump(data, file)


def open_file(file_name):
    if not file_name.endswith(".pkl"):
        file_name += ".pkl"
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, "rb") as file:
        return pickle.load(file)


def good_soup(url_list, class_to_wait: str = None, wait_time: int = 1):
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


# object codes ----------------------------------------
def save_object_codes():
    soup = good_soup("https://airef.github.io/tables/objects.html")
    data_tables = soup.find_all("table", attrs={"class": "objects-table"})
    object_dict = {}

    for row in chain(*[table.find_all("tr")[1:] for table in data_tables]):
        cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
        (
            id,
            name,
            ai_name,
            line,
            obj_class,
            cmd_id,
            category,
            age,
            dead_id,
            proj_id,
            chem_proj_id,
            version,
            notes,
        ) = cells
        if "DE" in id:
            id = id.split("DE: ")[-1]
        ai_name = ai_name.replace("-", "_")
        line = line.replace("-", "_")
        obj_class = obj_class.replace("-", "_")
        object_dict[ai_name] = ObjectStorage(
            id, name, ai_name, line, obj_class, cmd_id, category, age, dead_id
        )
    save_to_file(object_dict, "object_dict.pkl")


# technologies codes ----------------------------------------
def save_tech_codes():
    soup = good_soup("https://airef.github.io/tables/techs.html")
    data_tables = soup.find_all("table", attrs={"class": "techs-table"})
    tech_dict = {}
    for row in chain(*[table.find_all("tr")[1:] for table in data_tables]):
        cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
        id, name, ai_name, building, age, civ, version, note = cells
        ai_name = ai_name.replace("-", "_")
        tech_dict[ai_name] = TechnologyStorage(id, name, ai_name, building, age, civ)
    save_to_file(tech_dict, "tech_dict.pkl")


# strategic numbers ----------------------------------------
def save_strategic_number_names():
    soup = good_soup("https://airef.github.io/strategic-numbers/sn-index.html")
    data_table = soup.find("table", attrs={"id": "index-table"}).find_all("tr")
    sn_touples = [
        (
            data.find_all("td")[0].get_text(strip=True),
            data.find_all("td")[1].get_text(strip=True),
        )
        for data in data_table[1:]
    ]
    save_to_file(
        sn_touples, "sn_touples_id_name.pkl"
    )  # needs to keep - becuase result is used in url later


def to_bool(string):
    if "yes" == string.lower():
        return True
    elif "no" in string.lower():
        return False
    else:
        return False


def save_strategic_number_info(test=None):
    sn_touples = open_file("sn_touples_id_name.pkl")
    if test:
        sn_touples = sn_touples[:test]
    soups = good_soup(
        [
            "https://airef.github.io/strategic-numbers/sn-details.html#" + name
            for id, name in sn_touples
        ],
        wait_time=0.2,
    )
    strategic_number_dict = {}
    for touple, soup in zip(sn_touples, soups):
        id, name = touple
        name = name.replace("-", "_")
        description = get_description_text(soup)
        info_table = find_info_table(name, soup)
        info_default = (
            info_table.find_all("tr")[0].find_all("td")[1].get_text(strip=True)
        )
        info_range_req = (
            info_table.find_all("tr")[1].find_all("td")[1].get_text(strip=True)
        )
        info_min_req, info_max_req = map(int, info_range_req.split(" to "))
        info_range = info_table.find_all("tr")[2].find_all("td")[1].get_text(strip=True)
        info_min, info_max = map(int, info_range.split(" to "))
        info_category = (
            info_table.find_all("tr")[3].find_all("td")[1].get_text(strip=True)
        )
        info_effective = to_bool(
            info_table.find_all("tr")[4].find_all("td")[1].get_text(strip=True)
        )
        info_network = to_bool(
            info_table.find_all("tr")[5].find_all("td")[1].get_text(strip=True)
        )
        info_defined = to_bool(
            info_table.find_all("tr")[6].find_all("td")[1].get_text(strip=True)
        )
        info_active = to_bool(
            info_table.find_all("tr")[7].find_all("td")[1].get_text(strip=True)
        )
        strategic_number_dict[name] = StrategicNumberStorage(
            name,
            id,
            description,
            info_default,
            info_min,
            info_max,
            info_min_req,
            info_max_req,
            info_category,
            info_effective,
            info_network,
            info_defined,
            info_active,
        )
    save_to_file(strategic_number_dict, "strategic_number_dict.pkl")


# commands ----------------------------------------
def save_command_names():
    soup = good_soup(
        "https://airef.github.io/commands/commands-index.html",
        class_to_wait="command-name",
    )
    command_names = [
        c.text for c in soup.find_all(attrs={"class": "command-name"}, recursive=True)
    ]
    save_to_file(
        command_names, "command_names.pkl"
    )  # needs to keep - becuase result is used in url later


def save_command_parameters(test=None):
    command_names = open_file("command_names.pkl")
    if test:
        command_names = command_names[:test]
    soups = good_soup(
        [
            "https://airef.github.io/commands/commands-details.html#" + name
            for name in command_names
        ],
        wait_time=0.2,
    )
    command_dict = {}
    if len(command_names) != len(soups):
        raise ValueError("Number of command names and soups do not match")
    for name, soup in zip(command_names, soups):
        command_description = get_description_text(soup)
        command_params = [
            c.text for c in soup.find_all(attrs={"class": "param"}, recursive=True)
        ]
        info_table = find_info_table(name, soup)
        info_title = info_table.find_all("tr")[0].find_all("td")[0].get_text(strip=True)
        info_value = info_table.find_all("tr")[0].find_all("td")[1].get_text(strip=True)

        info_version = (
            info_table.find_all("tr")[1].find_all("td")[1].get_text(strip=True)
        )
        info_category = (
            info_table.find_all("tr")[2].find_all("td")[1].get_text(strip=True)
        )
        info_complexity = (
            info_table.find_all("tr")[3].find_all("td")[1].get_text(strip=True)
        )
        info_value = info_table.find_all("tr")[0].find_all("td")[1].get_text(strip=True)

        if info_title != "Command Type":
            raise Exception(f"{name}: exspected {info_title} to be Command Type")
        if info_value.split(".")[0] not in ["Action", "Fact", "Both"]:
            raise Exception(
                f"{name}: exspected {info_value} to start with Action, Fact, or Both"
            )
        command_dict[name] = CommandStorage(
            command_params,
            command_description,
            info_value.split(".")[0],
            info_version,
            info_category,
            info_complexity,
        )
        save_to_file(command_dict, "command_dict.pkl")


# Parameters ----------------------------------------
def save_parameter_names():
    soup = good_soup("https://airef.github.io/parameters/parameters-index.html")
    data_table = soup.find("table", attrs={"id": "index-table"}).find_all("tr")
    parameter_names = [
        data.find_all("td")[0].get_text(strip=True) for data in data_table[1:]
    ]
    save_to_file(
        parameter_names, "parameter_names.pkl"
    )  # needs to keep - becuase result is used in url later


def save_parameter_options(test=None):
    """
    compareOp - spaces
    ActionId, Formation, OrderId - has -1
    buildingID, EventType - only has 1 entry
    alot have result of
    ['Version Introduced', 'Related Parameters', 'Used In These Commands']
    because there is not a param list. they should be blank? or accecp a number perhapse?
    """
    parameter_names = open_file("parameter_names.pkl")
    if test:
        parameter_names = parameter_names[:test]
    soups = good_soup(
        [
            "https://airef.github.io/parameters/parameters-details.html#" + name
            for name in parameter_names
        ],
        wait_time=1,
    )
    parameter_dict = {}
    if len(parameter_names) != len(soups):
        raise ValueError("Number of parameter names and soups do not match")
    for name, soup in zip(parameter_names, soups):
        data_table = find_data_table(name, soup)
        info_table = find_info_table(name, soup)

        parameter_storage = ParameterStorage(None, None, get_description_text(soup))

        if data_table:
            description_column_index = find_description_column(data_table)
            id_column_index = find_id_column(data_table)
            if name == "compareOp":
                description_column_index -= 2

            parameter_options = [
                data.find_all("td")[description_column_index - 1].get_text(strip=True)
                for data in data_table.find_all("tr")[1:]
            ]
            option_ids = [
                data.find_all("td")[id_column_index].get_text(strip=True)
                for data in data_table.find_all("tr")[1:]
            ]
            parameter_storage.options = dict(zip(parameter_options, option_ids))
        if info_table:
            info_title = (
                info_table.find_all("tr")[0].find_all("td")[0].get_text(strip=True)
            )
            info_value = (
                info_table.find_all("tr")[0].find_all("td")[1].get_text(strip=True)
            )
            parameter_storage.range = f"{info_title}: {info_value}"

        parameter_dict[name] = parameter_storage

    save_to_file(parameter_dict, "parameter_dict.pkl")


def find_description_column(data_table):
    header_row = data_table.find("tr").find_all("th")
    for index, cell in enumerate(header_row):
        if cell.get_text(strip=True) == "Description":
            return index
    return None  # Return -1 if "Description" is not found


def find_id_column(data_table):
    header_row = data_table.find("tr").find_all("th")
    for index, cell in enumerate(header_row):
        if cell.get_text(strip=True) == "DE ID":
            return index
    for index, cell in enumerate(header_row):
        if cell.get_text(strip=True) == "ID":
            return index
    return None  # Return -1 if "Description" is not found


def find_data_table(name, soup):
    # Find all tables on the page
    tables = soup.find_all("table")

    # Iterate over the tables in reverse order
    for table in reversed(tables):
        header_row = table.find("tr").find_all(
            "th"
        )  # Assuming the header is in <th> tags
        for cell in header_row:
            if cell.get_text(strip=True) == "Description":
                return table
    return None  # Return None if no such table is found


def find_info_table(name, soup):
    # Find all h3 tags
    h3_tags = soup.find_all("h3")
    for h3 in h3_tags:
        # Check if the h3 tag contains the text "Info"
        if h3.get_text(strip=True) == "Info":
            # Find the next table after this h3 tag
            next_table = h3.find_next("table")
            if next_table:
                return next_table
    return None  # Return None if no such table is found


def get_description_text(soup):
    description_h3 = soup.find("h3", string="Description")
    info_h3 = soup.find("h3", string="Info")

    if not description_h3 or not info_h3:
        return ""

    # Find all <p> tags between the two <h3> tags
    p_tags = []
    for tag in description_h3.find_all_next():
        if tag == info_h3:
            break
        if tag.name == "p":
            p_tags.append(tag.get_text(strip=True))

    return " ".join(p_tags)


def make_parameter_class_lines(parameter_name, parameter_storage: ParameterStorage):
    lines = []
    parameter_options_dict = parameter_storage.options

    if isinstance(
        parameter_options_dict, str
    ):  # TODO: this is janky but wnated to show what needs to be in or goal id instead of enum
        return [f"class {parameter_name}:", "    pass #" + parameter_options_dict]
    lines.append(f"class {parameter_name}(Enum):")

    if not parameter_options_dict:
        lines.append("    pass #empty options_dict")
        return lines
    for option, id in parameter_options_dict.items():
        option = option.replace("-", "_")
        option = option.replace(" ", "_")
        option = option.replace(",", "_")
        option = option.replace("__", "_")
        if parameter_name in ["ObjectData", "ClassId"]:
            option = option.replace("*", "") #todo: ClassID is missing the ones with *, figure out why
        if parameter_name in ["AttrId"]:
            option = option.replace(".", "")
        if not option:
            option = parameter_storage.name
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

def make_function_param_list(command_name, command_storage: CommandStorage, p_dict):
    line = '    "'+command_name+'":('
    for arg in command_storage.args:
        if arg in ["Point1", "Point2"]:
            arg = "Point"
        line += '"' + arg + '",'
    line += '),'
    return [line]

def make_function_def_lines(command_name, command_storage: CommandStorage, p_dict):
    lines = []
    args = command_storage.args
    def_line = f"def {command_name.replace('-', '_')}("
    help_text = ['    """', command_storage.description]
    arg_duplicate_counter = {arg: 0 for arg in set(args)}
    for arg in args:
        if arg == "typeOp":
            continue
        elif arg in ["Point1", "Point2"]:
            def_line += f"{arg}:Point,"
            help_text.append(f":param {arg}: is a point object")
        elif arg in p_dict:
            arg_count = (
                str(arg_duplicate_counter[arg])
                if arg_duplicate_counter[arg] > 0
                else ""
            )
            arg_duplicate_counter[arg] += 1
            parameter_storage = p_dict[arg]
            def_line += f"{arg}{arg_count}: {get_arg_type(arg, p_dict)},"
            help_text.append(f":param {arg}{arg_count}: {parameter_storage.range}")
            help_text.append(f"{parameter_storage.description}")
        else:
            def_line += f"{arg},"
            help_text.append(f":param {arg}: NOT_DEFINED")
    def_line += "):"
    lines.append(def_line)
    help_text.append('"""')
    lines += help_text
    lines.append("    pass")
    return lines


# Generate files ----------------------------------------
class UniqueParamGenerator:
    unique_names = [
        "typeOp",
        "mathOp",
        "compareOp",
        "UnitId",
        "BuildingId",
        "ClassId",
        "TechId",
        "SnId",
        "TypeId",  # object id
        "ObjectId",  # object id
        "ItemId",  # object id or Tech id
        "OnMainland",
        "Perimeter",
    ]
    goal_id_names = [
        "GoalId",
        "VictoryType",  # goal id to store VictoryCondition
        "VictoryTime",  # goal id
        "VictoryPlayer",  # goal id
        "ThreatTime",  # goal id
        "ThreatTarget",  # goal id
        "ThreatSource",  # goal id
        "ThreatPlayer",  # goal id
        "EscrowGoalId",
        "OptionGoalId",
        "OutputGoalId",
    ]
    int_names = [
        "Value",  # -32768 to 32767 or -2,147,483,648 to 2,147,483,647
        "TimerId",  # 1-50
        "EventId",  # 0-255
        "SignalId",  # 0-255 th same as eventId right now as signals are the only event type
        "GroupId",  # 0-19
        "Id",  # objects indevidual id on the map
        "Index",  # 0 to 239 for the search-local list. 0 to 39 for the search-remote list.
        "MinGarrison",  # -1 to 32767, -1 sets no limit
        "MaxGarrison",  # -1 to 32767, -1 sets no limit
        "MaxDistance",  # -1 to 32767, -1 sets no limit
        "MinDistance",  # -1 to 32767, -1 sets no limit
        "Percent",  # 0-100
        "RuleDelta",
        "RuleId",
        "SharedGoalId",  # 1-256 seperate goals
        "TauntId",  # 1 to 255 theoreticaly i could make this an enum with all the taunts in it.
    ]
    banned_names = [
        "RuleId",
        "RuleDelta",
        "SharedGoalId",
    ]
    class_names = [
        "Point",
        "String",
    ]
    clear_names = [
        "LocalIndex",
        "LocalList",
        "RemoteIndex",
        "RemoteList",
    ]
    dont_understand = [
        "ColorId",  # player color and buffer related
        "Defconst",  # string related'
        "FactParameter",  # dependent on FactId value, all possibilities can be found at https://airef.github.io/parameters/parameters-details.html#FactId
        "Flag",  # bitwize minipulation of goals. greate for optimization im sure
        "LanguageId",  # dealing with language files
        "Option",  # changes based on command its in, but usualy int options? could be enumerated per command
    ]

    def __init__(self):
        self.names = (
            self.unique_names
            + self.goal_id_names
            + self.int_names
            + self.dont_understand
            + self.clear_names
            + self.class_names
        )
        self.object_dict = open_file("object_dict.pkl")
        self.tech_dict = open_file("tech_dict.pkl")
        self.strategic_number_dict = open_file("strategic_number_dict.pkl")
        self.parameter_dict = open_file("parameter_dict.pkl")

    def get_Perimeter(self):
        return {
            "Inner": 1,
            "Outer": 2,
        }

    def get_OnMainland(self):
        return {
            "On": 0,
            "Off": 1,
            "Ignore": -1,
        }

    def get_compareOp(self):
        return {
            "not-equal": 18,
            "less-or-equal": 19,
            "greater-than": 20,
            "greater-or-equal": 21,
            "equal": 22,
            "not-equal": 23,
        }

    def get_mathOp(self):
        return {
            "eql": 0,
            "add": 1,
            "sub": 2,
            "mul": 3,
            "div_fl": 9,
            "div_rd": 4,
            "mod": 7,
            "min": 5,
            "max": 6,
            "neg": 8,
            "per": 11,
            "per_of": 10,
        }

    def get_typeOp(self):
        return {
            "constant": 0,
            "goal": 2,
            "strategic_number": 1,
        }

    def get_ObjectId(self):
        return dict(
            [
                (object_storage.ai_name, object_storage.id)
                if object_storage.ai_name
                else (object_storage.name.replace(" ", "_"), object_storage.id)
                for object_storage in self.object_dict.values()
            ]
        )

    def get_TypeId(self):
        return self.get_ObjectId()

    def get_ItemId(self):
        return self.get_ObjectId() | self.get_TechId()

    def get_TechId(self):
        return dict(
            [
                (tech.ai_name, tech.id)
                if tech.ai_name
                else (tech.name.replace(" ", "_"), tech.id)
                for tech in self.tech_dict.values()
            ]
        )

    def get_SnId(self):
        return dict([(sn.name, sn.id) for sn in self.strategic_number_dict.values()])

    def get_ClassId(self):
        return dict(
            [
                (object_storage.obj_class, object_storage.obj_class_id)
                for object_storage in self.object_dict.values()
            ]
        )

    def get_BuildingId(self):
        building_id_dict = {}
        for object_storage in self.object_dict.values():
            if object_storage.category == "Buildings":
                building_id_dict[object_storage.ai_name] = object_storage.id
        return building_id_dict

    def get_UnitId(self):
        unit_id_dict = {}
        for object_storage in self.object_dict.values():
            if object_storage.category != "Buildings":
                if object_storage.ai_name:
                    unit_id_dict[object_storage.ai_name] = object_storage.id
                else:
                    unit_id_dict[object_storage.name.replace(" ", "_")] = (
                        object_storage.id
                    )
        return unit_id_dict

    def create_options_dict(self, name):
        if name in self.class_names:
            return name
        if name in self.banned_names:
            return "USER SHOULD NEVER USE THIS!"
        if name in self.int_names:
            return "int"
        if name in self.goal_id_names:
            return "var"
        if name in self.dont_understand:
            return "unImplemented"
        if name in self.clear_names:
            return {
                "keep": 0,
                "clear": 1,
            }
        if name in self.unique_names:
            method = getattr(self, "get_" + name)
            return method()

        raise Exception(f"Name {name} not found in UniqueParamGenerator")

def generate_aoe2scriptEnums():
    #todo: add all the PlayerNumber Options from the description
    #todo: sort out snId and SN enums
    #todo: forage_
    p_dict = open_file("parameter_dict.pkl")
    lines = [
        "# --- Removed parameters --- #",
        "# all of the parameter types from the website with their IDs.",
        "# mathops and comparison ops are handdled by the intepreter.",
        "#",
        "from enum import Enum",
    ]
    unique_param_generator = UniqueParamGenerator()
    for parameter_name, parameter_storage in p_dict.items():
        assert isinstance(parameter_storage, ParameterStorage)
        if parameter_name in unique_param_generator.names:
            parameter_storage.options = unique_param_generator.create_options_dict(
                parameter_name
            )
        lines += make_parameter_class_lines(parameter_name, parameter_storage)

    #add stategic numbers
    sn_dict = open_file("strategic_number_dict.pkl")
    options = dict(zip([sn[3:] if sn[:3] == "sn_" else sn for sn in sn_dict.keys()], [i for i in range(len(sn_dict.keys()))]))
    lines += make_parameter_class_lines("SN", ParameterStorage(options, "", ""))

    # add command enums
    try:
        import aoe2scriptFunctions
        command_names = [
            name
            for name, obj in inspect.getmembers(aoe2scriptFunctions, inspect.isfunction)
        ]
        options = dict(zip(command_names, [i for i in range(len(command_names))]))
        lines += make_parameter_class_lines("AOE2FUNC", ParameterStorage(options, "", ""))
        
        class_names = [
            name for name, obj in inspect.getmembers(aoe2scriptFunctions, inspect.isclass)
        ]
        options = dict(zip(class_names, [i for i in range(len(class_names))]))
        lines += make_parameter_class_lines("AOE2OBJ", ParameterStorage(options, "", ""))
    except ModuleNotFoundError as e:
        if e.name == "aoe2scriptEnums":
            logger.info("aoe2scriptEnums not found, (expsected first run)")
        else:
            raise e

    lines += ['class State():']
    lines += ['    pass #added manually']
        
    output_path = os.path.join(os.path.dirname(__file__), "aoe2scriptEnums.py")
    with open(output_path, "w") as file:
        file.write("\n".join(lines))
    logger.info("aoe2scriptEnums.py generated")

def delete_aoe2script_files():
    try:
        os.remove(os.path.join(os.path.dirname(__file__), "aoe2scriptEnums.py"))
        logger.info("aoe2scriptEnums.py removed")
    except FileNotFoundError:
        logger.info("aoe2scriptEnums.py not found")
    try:
        os.remove(os.path.join(os.path.dirname(__file__), "aoe2scriptFunctions.py"))
        logger.info("aoe2scriptFunctions.py removed")
    except FileNotFoundError:
        logger.info("aoe2scriptEnums.py not found")

def generate_aoe2scriptFunctions():
    c_dict = open_file("command_dict.pkl")
    p_dict = open_file("parameter_dict.pkl")
    lines = []
    lines += ['try:']
    lines += ['    from scraper.aoe2scriptEnums import *']
    lines += ['except:']
    lines += ['    from aoe2scriptEnums import *']
    function_list_line = ['function_list = {']
    for command_name, command_storage in c_dict.items():
        function_list_line += make_function_param_list(command_name, command_storage, p_dict)
        lines += make_function_def_lines(command_name, command_storage, p_dict)
    function_list_line += ['}']
    lines += function_list_line
    output_path = os.path.join(os.path.dirname(__file__), "aoe2scriptFunctions.py")
    with open(output_path, "w") as file:
        full_lines = "\n".join(lines)
        full_lines = full_lines.replace('\\','|')
        file.write(full_lines)
    logger.info("aoe2scriptFunctions.py generated")

def main(scrap_wesite = False, generate_files = True):
    if scrap_wesite:
        save_object_codes()
        save_tech_codes()
        save_strategic_number_names()
        save_strategic_number_info()
        save_command_names()
        save_parameter_names() 
        save_command_parameters()
        save_parameter_options()
    if generate_files:
        delete_aoe2script_files()
        generate_aoe2scriptFunctions() 
        generate_aoe2scriptEnums()
        generate_aoe2scriptEnums() #second time for the ModuleNotFoundError skip
    

if __name__ == "__main__":
    main(scrap_wesite = False, generate_files = True)