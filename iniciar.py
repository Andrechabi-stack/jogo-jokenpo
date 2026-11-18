import os
import subprocess
import sys
import time

pasta = os.path.dirname(os.path.abspath(__file__))

servidor = subprocess.Popen([sys.executable, "servidor.py"], cwd=pasta)
time.sleep(2)

try:
    subprocess.run([sys.executable, "jogo.py"], cwd=pasta)
finally:
    servidor.terminate()