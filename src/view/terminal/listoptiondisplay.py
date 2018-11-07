from termcolor import colored

class ListOptionsDisplay():

    def __init__(self, options=[], on_selected=None):
        self.options = options
        self.on_selected = on_selected
        self.index_selected = 0

    def handle_events(self):
        answer = input("\n\rType item number or use [P]rev/[N]ext\n\r").upper()
        options_count = len(self.options)
        if answer.isdigit():
            self.index_selected = max(min(options_count, int(answer))-1, 0)
        elif answer == "P" and self.index_selected > 0:
            self.index_selected -= 1
        elif answer == "N" and self.index_selected < options_count - 1:
            self.index_selected += 1
        elif not answer:
            self.on_selected(self.options[self.index_selected])

    def display(self):
        for i, o in enumerate(self.options):
            selected = i == self.index_selected
            f, b = "yellow", "blue"
            print((">   " if selected else "    ") + colored("{}. {}".format(
                i+1, o), b if selected else f, 'on_' + (f if selected else b)))