import os
if os.name == 'nt':
    from ctypes import c_ulong, windll

def color_update(self, color, bgcolor=15 if os.name == 'nt' else 0):
    """cross platform background and foreground color output"""
    if os.name == 'nt':
        print("", end="", flush=True)
        if self.std_output_hdl is None:
            standard_output_handle = c_ulong(0xfffffff5)
            windll.Kernel32.GetStdHandle.restype = c_ulong
            self.std_output_hdl = windll.Kernel32.GetStdHandle(standard_output_handle)
        windll.Kernel32.SetConsoleTextAttribute(self.std_output_hdl, bgcolor | color)
    else:
        print("\033[" + str(bgcolor) + ";" + str(color) + "m", end="")