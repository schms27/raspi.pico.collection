cd ui
pyuic5 -o .\resources_rc.py .\resources.qrc
pyuic5 -o .\main_config_window.py .\main_config_window.ui --from-imports
pyuic5 -o .\_button_function_dialog.py .\_button_function_dialog.ui --from-imports