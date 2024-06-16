import subprocess
import sys
import os

def run_streamlit():
    # Set the working directory to the location of launcher.py
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, "-m", "streamlit", "run", "quanbot.py"])

if __name__ == "__main__":
    run_streamlit()