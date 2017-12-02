# monkey patch mongo cursor to have len
from pymongo.cursor import Cursor

Cursor.__len__ = Cursor.count
