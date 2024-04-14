import configparser
import os


class ReadProperties:
    def read_properties(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), './config/app_configuration.cfg'))

        properties_map = dict()
        properties_map['container_name'] = config['container']['name']
        properties_map['db_port'] = config['database']['port']
        properties_map['db_username'] = config['database']['username']
        properties_map['db_password'] = config['database']['password']
        properties_map['db_name'] = config['database']['name']

        return properties_map


read_props = ReadProperties()
