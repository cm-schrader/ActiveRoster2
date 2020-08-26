from collections import defaultdict
import os

events = defaultdict(lambda: 0)
members = defaultdict(lambda: defaultdict(lambda: 0))


def read_csv(directory, file):
    counted = list()
    events[directory] += 1
    with open(f"{directory}/{file}", "r") as csv:
        line = csv.readline()
        for line in csv:
            cells = str(line).split("\t")[0:2]
            if cells[0] != '\x00' and cells[0] not in counted and cells[1] == '\x00J\x00o\x00i\x00n\x00e\x00d\x00':
                members[cells[0]][directory] += 1


def read_directory(path):
    for file in os.listdir(path):
        read_csv(path, file)


def run_analysis():
    for directory in next(os.walk('.'))[1]:
        if directory[0] == ".":
            continue
        read_directory(directory)


def member_str(name, member):
    string = f"{white_to_len(name, 40)}|"
    for key in member.keys():
        ratio = 100 / events[key] * member[key]
        string = string + f"\t{key}: {white_to_len(str(round(ratio, 1)), 6)}%"
    return string


def white_to_len(string, length):
    """
    Fills white space into a string to get to an appropriate length.  If the string is too long, it cuts it off.
    :param string: String to format.
    :param length: The desired length.
    :return: The final string.
    """
    if len(string) < length:
        string = string + (length - len(string)) * " "
    else:
        string = string[0: length - 3] + "..."
    return string


if __name__ == "__main__":
    run_analysis()
    for member in members.keys():
        print(member_str(member, members[member]))
