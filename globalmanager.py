class GlobalManager:
    """A class which handles the state of global variable. This should be used as little as possible and generally only for constants
       This was done to avoid passing things like date ranges through 3 layers of encapsulation
    """
    def __init__(self):
        self.params = dict()

    def getParam(self, param: str) -> any:
        """Gets a global parameter

        Args:
            param (str): The ID of the parameter

        Returns:
            any: The global variable 
        """
        return self.params[param]

    def setParam(self, param: dict) -> None:
        """Sets a global parameter

        Args:
            param (dict): A dictionary with the parameter names and values to set 
        """
        self.params.update(param)

    def listParams(self) -> dict:
        """Gets all parameters

        Returns:
            dict: A dictionary containing the global parameters
        """
        return self.params