from typing import Any


class Model():
    def __init__(self, name,icd,pname):
        ## private varibale or property in Python
        self.__name = name
        self.__icd = icd
        self.__pname = pname

    def get_name(self):
        return self.__name

    def get_icd(self):
        return self.__icd

    def get_pname(self):
        return self.__pname



