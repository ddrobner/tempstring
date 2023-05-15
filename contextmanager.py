class ContextManager:
    def __init__(self):
        self.params = dict()

    def getParam(self) -> dict:
        return self.params

    def setParam(self, param: dict) -> None:
        self.params.update(param)

    def listParams(self) -> str:
        return str(self.params)