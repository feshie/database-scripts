"""
    Basic database configuration reading tools
"""


from configobj import ConfigObj

class FeshieDb:
    """
        A class containing the connection information required to access the
        database
    """
    def __init__(self, config_file):
        """
            Read the config file and extract the required information
        """
        try:
            config = ConfigObj(config_file)
            self.database = config["database"]
            self.server = config["server"]
            self.user = config["user"]
            self.password = config["pass"]
        except KeyError:
            raise ConfigError("Invalid config File")    

class ConfigError(Exception):
    """
        An error for when something has gone wrong reading the config
    """
    pass
