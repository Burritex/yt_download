from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DESTINY_DIR_VIDEO = os.getenv("DESTINY_DIR_VIDEO")
    DESTINY_DIR_MUSIC = os.getenv("DESTINY_DIR_MUSIC")
