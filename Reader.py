import numpy as np
import pickle


class READER:
    def __init__(self):
        pass
    def Read(self):
        pickle_in = open("userData/gesture2.p","rb")
        gestureData = pickle.load(pickle_in)
        pickle_in.close()
        return gestureData
