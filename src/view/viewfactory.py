""" Entrypoint for creating concrete view implementations """

from src.view.terminal.terminalview import TerminalView

def factory_create():
    """return like view.viewinterface"""
    return TerminalView()
