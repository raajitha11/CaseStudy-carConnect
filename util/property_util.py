import configparser

class PropertyUtil:
    @staticmethod
    def getPropertyString(property_file):
        config = configparser.ConfigParser()
        config.read(property_file)
        connection_string = {
            'user': config['DATABASE']['user'],
            'host': config['DATABASE']['host'],
            'port': config['DATABASE'].getint('port'),
            'passwd': config['DATABASE']['passwd'],
            'database': config['DATABASE']['database']
        }
        return connection_string
