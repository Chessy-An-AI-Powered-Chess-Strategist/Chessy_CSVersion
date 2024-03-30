"""
Set up the package settings
"""

# ToDo: Create this for security and better comunication between the modules
from .settings import gui_settings
from .game import main
from .graphicsUserInterface import GraphicsUserInterface


__all__ = ["gui_settings", "main", "GraphicsUserInterface"]