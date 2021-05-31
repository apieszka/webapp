import sys
sys.path.insert(0, '/unit5/unit5/unit5_webapp.py')
import importlib

scriptpath = "unit5/unit5/unit5_webapp.py"
sys.path.append(os.path.abspath(scriptpath))
import unit5_webapp

from unit5_webapp import app as application
if __name__ == "__main__":
    app.run()