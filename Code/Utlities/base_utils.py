import yaml

import functools
import logging

import time


def get_config_val(config_type:str,*args) -> str:
    """
    Retrieve a configuration value from a YAML configuration file based on the provided configuration type and keys.

    Input:
    - config_type (str): The type of configuration to retrieve.
    - *args (str): Variable length argument list of keys to navigate through the configuration.

    Output:
    - str: The value corresponding to the specified configuration type and keys.

    Raises:
    - KeyError: If the provided configuration type is not found in the configuration file.
    - AttributeError: If unable to resolve the configuration value from the list of keys provided.

    """
    with open("config_paths.yaml","r") as conf_pths:
        config_map = yaml.load(conf_pths,loader=yaml.FullLoader)

        if config_type not in config_map.keys():
            raise KeyError(f"{config_type} : Config Type not Correct")

    with open(config_map[config_type],'r') as conf_file:
        config_val = yaml.load(conf_file,loader=yaml.FullLoader)
        for key_val in args:
            config_val = conf_file[key_val]

    if isinstance(config_val,dict):
        raise AttributeError("Unable to resolve confog value from list of keys provided")

    return config_val



def log_function(func):
    """
    Decorator function to log the inputs, outputs, and exceptions of a function.

    Input:
    - func (callable): The function to be decorated.

    Output:
    - callable: The decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log function inputs
        logging.info(f"'{func.__name__}'|{time.time}|Start||")

        try:
            # Execute the function
            result = func(*args, **kwargs)

            # Log function output
            logging.info(f"'{func.__name__}'|{time.time}|Sucess||")
            return result

        except Exception as e:
            # Log exceptions
            logging.error(f"'{func.__name__}'|{time.time}|Error|ErrorMessage{str(e)}|Args:{args} , Kwargs:{kwargs}")

    return wrapper



