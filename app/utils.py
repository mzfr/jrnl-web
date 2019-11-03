import os

# import slugify
import yaml
# from jrnl import Journal, util



def load_config(filename):
    """Load config file

    Arguments:
        filename {str} -- Name of the configuration file.
    """
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            try:
                journal = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
        return journal

    else:
        print("[!] The config doesn't exists")

CONFIG = load_config('jrnl-config.yaml')

def load(journal_name):
    if journal_name not in CONFIG['journals']:
        return None
    return CONFIG['journals'][journal_name]
