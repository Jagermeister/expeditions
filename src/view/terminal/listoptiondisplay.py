""" Terminal display of a select element """

from termcolor import colored

class ListOptionsDisplay():
    """ Display, selection, and action delegation for a list of options """

    def __init__(self, options=None, on_selected=None):
        self.options = options if options else []
        self.on_selected = on_selected
        self.index_selected = 0

    def handle_events(self):
        """ Issue and process user events """
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
        """ Visual display of state """
        for i, option in enumerate(self.options):
            selected = i == self.index_selected
            foreground, background = "yellow", "blue"
            print((f"{'>' if selected else ' '}   ") + colored(
                f"{i+1}. {option}",
                background if selected else foreground,
                'on_' + (foreground if selected else background)))
