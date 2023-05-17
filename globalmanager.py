class GlobalManager:
    """A class which handles the state of global variable. This should be used as little as possible and generally only for constants
       This was done to avoid passing things like date ranges through 3 layers of encapsulation
    """
    def __init__(self):
        self.params = dict()

    def getParam(self, param) -> dict:
        return self.params[param]

    def setParam(self, param: dict) -> None:
        self.params.update(param)

    def listParams(self) -> str:
        return str(self.params)