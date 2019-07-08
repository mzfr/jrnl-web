import os

import slugify
import yaml
from jrnl import Journal, exporters, util

import gfm


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

def ls():
    """List all the jorunals that are available
    """
    return CONFIG['journals'].keys()


def load(journal_name):
    if journal_name not in CONFIG['journals']:
        return None
    return CONFIG['journals'][journal_name]
    # config = load_config(CONFIG)
    # return Journal.open_journal(journal_name, config, legacy=True)


def search_entry(journal, timestamp):
    for entry in journal.entries:
        if timestamp == entry.date.timestamp():
            return entry
    return None


# TODO: Better name & organization of this module!
def entries(journal, count=None):
    """Send back dictionary"""
    # Return all entries
    if not count:
        entries = reversed(journal.entries)
    else:
        entries = list(reversed(journal.entries))[:count]

    rv = []
    for entry in entries:
        e = exporters.to_json(entry)
        e['markdown'] = e['body']
        e['html'] = gfm.markdown(e['body'])
        e['slug'] = slugify.slugify(e['title'])
        del e['body']
        rv.append(e)

    return rv


def tags(journal):
    return [{"name": tag.name, "count": tag.count} for tag in journal.tags]
