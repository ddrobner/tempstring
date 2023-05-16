class GlobalManager:
    def __init__(self):
        self.params = dict()

    def getParam(self, param) -> dict:
        return self.params[param]

    def setParam(self, param: dict) -> None:
        self.params.update(param)

    def listParams(self) -> str:
        return str(self.params)