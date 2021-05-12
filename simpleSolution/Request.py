from Global import *


class Request():
    def __init__(self, l=0, iu=False):
        self.layer = l
        self.is_Up = iu

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Request):
            return self.layer == o.layer and self.is_Up == o.is_Up
        else:
            raise Exception("Invalid input!")
