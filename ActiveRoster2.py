from collections import defaultdict
import tkinter as tk
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


def member_str(name):
    string = f"{white_to_len(name, 60)}|"
    for key in members[name].keys():
        ratio = 100 / events[key] * members[name][key]
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


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ActiveRoster2 : HPRC")
        tk.Button(self, text="Recalculate", width=15,
                  command=run_analysis).pack()
        self.listbox = tk.Listbox(self, width=200, font="TkFixedFont")
        self.listbox.pack()
        for member in members.keys():
            self.listbox.insert(tk.END, member_str(member))
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        self.destroy()


if __name__ == "__main__":
    run_analysis()
    Window().mainloop()
    for member in members.keys():
        print(member_str(member))
