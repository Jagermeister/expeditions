from .terminal import terminalview

def factory_create():
    """return like view.viewinterface"""
    return terminalview.TerminalView()