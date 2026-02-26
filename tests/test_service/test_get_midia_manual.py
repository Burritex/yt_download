import pytest

from src.service import Get_Midia


url = 'https://www.youtube.com/watch?v=JQBz83cdu50'

def test_get_video():
    Get_Midia(0, url)

def test_get_music():
    Get_Midia(1, url)
