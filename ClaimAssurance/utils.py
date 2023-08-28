from configparser import ConfigParser

def get_connection_params(config_file_path, section):
    parser = ConfigParser()
    parser.read(config_file_path)
    if parser.has_section(section):
        db_con_params = {}
        
        key_val_tuple = parser.items(section)
        
        for key,val in key_val_tuple:
            db_con_params[key] = val
            
        return db_con_params