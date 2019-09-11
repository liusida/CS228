import numpy as np
import pickle
from Reader import READER


Reader = READER()
gestureData = Reader.Read()
print(gestureData)