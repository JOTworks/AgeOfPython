from math import ceil, floor

from colorama import Fore, Back, Style


def print_completion_bar(percentage, bar_length=50):
    """
    Prints a static completion bar with the given percentage filled.

    :param percentage: The percentage to fill the bar (0 to 100).
    :param bar_length: The total length of the bar in characters.
    """
    print(percentage)
    filled_length = int(bar_length * (percentage))
    empty_length = bar_length - filled_length
    bar = "\u2588" * filled_length + "-" * empty_length  # \u2588 is a solid block
    print(f"[{bar}] {percentage*100:.2f}%")

def print_stats(defrule_num, free_memory_count, used_memory_count):
    print_bordered("code stats")
    print(f"{defrule_num}/10,000 DefRules Used")
    print_completion_bar(defrule_num/10000)
    print(f"{used_memory_count}/{used_memory_count+free_memory_count} Memory Used")
    print_completion_bar(used_memory_count/(used_memory_count+free_memory_count))

def display_scanner(myScanner):
    print_bordered("Scanner Results")
    max_value_len = 18
    token_list = []
    last_file_line = ""
    for tok in myScanner.tokens:
        print(tok)
    for tok in myScanner.tokens:
        val = str(tok.print_value())
        if len(val) > max_value_len:
            val = val[: max_value_len - 2] + "~" + str(len(val))
        row = [str(tok.tokenType).split(".")[1], val]
        if str(tok.file) + str(tok.line) != last_file_line:
            last_file_line = str(tok.file) + str(tok.line)
            row.append(Fore.WHITE + str(tok.file))
            row.append(str(tok.line) + Fore.WHITE)
        else:
            row.append(Fore.LIGHTBLACK_EX + str(tok.file))
            row.append(str(tok.line) + Fore.WHITE)
        token_list.append(row)
    print_column(token_list, 3)

def print_dim(string):
    print(Style.DIM + string + Style.NORMAL)

def print_bright(string):
    print(Style.BRIGHT + string + Style.NORMAL)


def print_bordered(string):
    bordered_string = ["", "", ""]
    min_width = 20
    border_length = max(min_width, len(string) + 2)
    right_side_padding = max(0, floor((border_length - len(string)) / 2))
    left_side_padding = right_side_padding + (border_length - len(string)) % 2
    # left side
    bordered_string[0] += "\u2554"
    bordered_string[1] += "\u2551"
    bordered_string[2] += "\u255a"
    # middle
    bordered_string[1] += " " * (left_side_padding)
    for i in range(border_length):
        bordered_string[0] += "\u2550"
        bordered_string[1] += string[i] if i < len(string) else ""
        bordered_string[2] += "\u2550"
    bordered_string[1] += " " * (right_side_padding)
    # right side
    bordered_string[0] += "\u2557\n"
    bordered_string[1] += "\u2551\n"
    bordered_string[2] += "\u255d"
    return print_bright("".join(bordered_string))


def print_column(rows, num_columns):
    columned_rows = []
    length_column = ceil(len(rows) / num_columns)
    extra_rows_needed = len(rows) % num_columns
    if extra_rows_needed > 0:
        for i in range(num_columns - extra_rows_needed):
            rows.append(["-", "-", "\x1b[37m-", "-\x1b[37m"])
    col_line = ["  \u2502"]
    for i in range(length_column):
        single_row = []
        for j in range(num_columns):
            single_row += col_line
            try:
                single_row += rows[i + (j * length_column)]
            except Exception as e:
                print(f"EXECPTION:{e}")
        columned_rows.append(single_row)
    widths = [max(map(len, col)) for col in zip(*columned_rows)]
    for row in columned_rows:
        print("  ".join((val.ljust(width) for val, width in zip(row, widths))))


def read_file_as_string(file_path):
    if file_path == "TEST": #todo: bad magic string
        return None
    if file_path == "NOFILE": #todo: bad magic string
        return None
    with open(file_path, "r") as file:
        file_contents = file.read()
    return file_contents
