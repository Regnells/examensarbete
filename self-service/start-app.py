import os

# Start app by typing "py start-app.py" in the terminal
os.system('cmd /k' "py -m waitress --port=5000 app:app")