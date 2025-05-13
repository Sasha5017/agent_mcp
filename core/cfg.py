import os
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, 'env')

load_dotenv(env_path)

class CFG:
    BASE_DIR = os.getenv("BASE_DIR")


