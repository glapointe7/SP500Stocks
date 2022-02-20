import importlib.util
import subprocess
import sys

def installPackageIfNotInstalled(library_name):
    spec = importlib.util.find_spec(library_name)
    if spec is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
