from configparser import ConfigParser

# load data
config_file = 'config/config.ini'
config_object = ConfigParser(comment_prefixes=('#', ';'), allow_no_value=True)
config_object.read(config_file)

# objects
model_cfg = config_object['MODEL']
insights_cfg = config_object['INSIGHTS']
