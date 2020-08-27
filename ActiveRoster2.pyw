from collections import defaultdict
import tkinter as tk
import os

events = defaultdict(lambda: 0)
members = defaultdict(lambda: defaultdict(lambda: 0))
active_members = 0


def read_csv(directory, file):
    counted = list()
    events[directory] += 1
    with open(f"{directory}/{file}", "r", encoding="utf-16-le") as csv:
        line = csv.readline()
        for line in csv:
            cells = str(line).split("\t")[0:2]
            if cells[0] != '\x00' and cells[0] not in counted and "Joined" in cells[1]:
                members[cells[0]][directory] += 1


def read_directory(path):
    for file in os.listdir(path):
        read_csv(path, file)


def analyze_csvs():
    events.clear()
    members.clear()
    for directory in next(os.walk('.'))[1]:
        if directory[0] == ".":
            continue
        read_directory(directory)


def member_str(name):
    string = f"{white_to_len(name, 30)}"
    for key in events.keys():
        string = string + \
            f"    {key}: {white_to_len(str(get_ratio(name, key)), 6)}%"
    return string


def get_ratio(name, group):
    return round(100 / events[group] * members[name][group], 1)


def is_active(name, group):
    if get_ratio(name, group) >= 75:
        return True
    return False


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


def rgb_to_tk(rgb):
    """
    Converts rgb values to tkinter color codes.
    :param rgb: Tuple of 3 ints.
    :return: tk color code string
    """
    return "#%02x%02x%02x" % rgb


class Window(tk.Tk):
    def __init__(self):
        # Window initialization
        super().__init__()
        self.title("ActiveRoster2")
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Event Info
        self.event_labels = dict()
        self.event_frame = tk.Frame(self.frame)
        self.event_frame.grid(row=0, column=2, sticky=tk.N)
        tk.Label(self.event_frame, text="Events", font='Helvetica 12 bold').grid(
            row=0, column=0, columnspan=2, sticky=tk.N)
        eventRow = 1
        for event_type in events.keys():
            tk.Label(self.event_frame, text=f"{event_type}:", anchor=tk.E).grid(
                row=eventRow, column=0)
            self.event_labels[event_type] = tk.Label(
                self.event_frame, text=str(events[event_type]), anchor=tk.W)
            self.event_labels[event_type].grid(
                row=eventRow, column=1, sticky=tk.N)
            eventRow += 1

        # Member Info
        self.member_labels = dict()
        self.member_frame = tk.Frame(self.frame)
        self.member_frame.grid(row=0, column=1, sticky=tk.N)
        tk.Label(self.member_frame, text="Members", font='Helvetica 12 bold').grid(
            row=0, column=0, columnspan=2, sticky=tk.N)
        tk.Label(self.member_frame, text="Total Active Members:",
                 anchor=tk.E).grid(row=1, column=0, sticky=tk.N)
        self.total_active = tk.Label(
            self.member_frame, text=str(active_members), anchor=tk.W)
        self.total_active.grid(row=1, column=1, sticky=tk.N)
        for event_type in events.keys():
            tk.Label(self.member_frame, text=f"Active in {event_type}:", anchor=tk.E).grid(
                row=eventRow, column=0)
            self.member_labels[event_type] = tk.Label(
                self.member_frame, text="##", anchor=tk.W)
            self.member_labels[event_type].grid(
                row=eventRow, column=1, sticky=tk.N)
            eventRow += 1

        # Main components
        tk.Button(self.frame, text="Recalculate", width=15,
                  command=self.recalculate, bg=rgb_to_tk((252, 197, 68))).grid(row=0, column=0, sticky=tk.W + tk.S + tk.E)

        self.listbox = tk.Listbox(
            self.frame, width=120, height=30, font="TkFixedFont")
        self.listbox.grid(row=1, column=0, sticky=tk.W +
                          tk.E + tk.N + tk.S, columnspan=3)
        listscroll = tk.Scrollbar(self.frame)
        listscroll.grid(row=1, column=4, sticky=tk.N + tk.S)
        self.listbox.config(yscrollcommand=listscroll.set)
        listscroll.config(command=self.listbox.yview)
        self.recalculate()

    def recalculate(self):
        analyze_csvs()
        self.listbox.delete(0, tk.END)
        active_members = 0
        group_members = defaultdict(lambda: 0)
        index = 0
        for member in sorted(members.keys()):
            active_groups = 0
            self.listbox.insert(tk.END, member_str(member))
            for event_type in events.keys():
                activity = is_active(member, event_type)
                if activity:
                    group_members[event_type] += 1
                    active_groups += 1
            if active_groups >= 2:
                self.listbox.itemconfig(index, bg=rgb_to_tk((102, 255, 102)))
                active_members += 1
            else:
                self.listbox.itemconfig(index, bg=rgb_to_tk((255, 102, 102)))
            index += 1
        self.total_active.config(text=str(active_members))

        for label in self.event_labels.keys():
            self.event_labels[label].config(text=str(events[label]))
            self.member_labels[label].config(text=str(group_members[label]))

    def close_window(self):
        self.destroy()


if __name__ == "__main__":
    analyze_csvs()
    Window().mainloop()
