"""
   File Name: theme_manager.py
Contributors: Jayden Ferreira
Date Created: March 15, 2026
 Description: this file contains the function and logic necessary for managing themes
              and retrieving their styling.
"""

def apply_theme(window, theme):
    # Top controls
    window.btnInfo.setStyleSheet(theme.STYLE_INFO_BTN)
    window.btnDisclaimer.setStyleSheet(theme.STYLE_DISC_PARAM_BTN)
    window.btnParameter.setStyleSheet(theme.STYLE_DISC_PARAM_BTN)
    window.btnSources.setStyleSheet(theme.STYLE_SOURCE_BTN)
    window.btnTheme.setStyleSheet(theme.STYLE_THEME_CIRCLE_BTN)

    # Info / text boxes
    window.disclaimerBox.setStyleSheet(theme.STYLE_DISC_PARAM_BOXES)
    window.parameterBox.setStyleSheet(theme.STYLE_DISC_PARAM_BOXES)

    # Overlays
    window.btnOlDropdown.setStyleSheet(theme.STYLE_OL_DROPDOWN_BTN)
    window.btnClearOverlays.setStyleSheet(theme.STYLE_CLEAR_BTN)
    window.overlayList.setStyleSheet(theme.STYLE_OVERLAY_LIST)
    window.overlayLabel.setStyleSheet(theme.STYLE_CONFIG_LABELS)

    # Simulation buttons
    window.btnStart.setStyleSheet(theme.STYLE_RUN_PAUSE_BTN)
    window.btnReset.setStyleSheet(theme.STYLE_RESET_BTN)

    # Main panes / misc
    window.infoBubb.setStyleSheet(theme.STYLE_STATUS_BUBBLE)
    window.leftPane.setStyleSheet(theme.STYLE_PANES)
    window.rightPaneWidget.setStyleSheet(theme.STYLE_PANES)
    window.windowSplit.setStyleSheet(theme.STYLE_SPLITTER)

    # Radio groups
    for container in getattr(window, "themeRadioContainers", []):
        container.setStyleSheet(theme.STYLE_RADIO_BOXES)

    for label in getattr(window, "themeRadioLabels", []):
        label.setStyleSheet(
            theme.STYLE_CONFIG_LABELS +
            "border: none; background-color: transparent;"
        )

    for radio_button in getattr(window, "themeRadioButtons", []):
        radio_button.setStyleSheet(theme.STYLE_RADIO_BTN)

    # Scrubber
    if hasattr(window, "scrubber"):
        window.scrubber.applyTheme(theme)