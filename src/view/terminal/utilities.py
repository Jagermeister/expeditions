""" Collection of common algorithms for terminal views """

import os

def display_clear():
    """Utility for cross platform terminal clear"""
    os.system('cls' if os.name == 'nt' else 'clear')
