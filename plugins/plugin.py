import abc


class PLUGIN(metaclass=abc.ABCMeta):
    def __init__(self):
        pass
    
    @abc.abstractclassmethod
    def compare_images(self,imageA,imageB):
        pass

