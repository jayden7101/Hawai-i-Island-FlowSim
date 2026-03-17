"""
   File Name: themes.py
Contributors: Jayden Ferreira
Date Created: March 15, 2026
 Description: this file tracks the existing themes and gets the styling for them.
"""

import light_style_sheet as light_theme
import dark_style_sheet as dark_theme

THEMES = {
    "light" : light_theme,
    "dark"  : dark_theme,
}

# getter function for themes
def get_theme(theme_name: str):
    return THEMES[theme_name]

# toggle between moon and sun icon for the mode switch button
def get_theme_button_icon(theme_name: str) -> str:
    if theme_name == "light":
        return "\u263E"    # crescent moon icon
    else:
        return "\u263C"    # sun icon