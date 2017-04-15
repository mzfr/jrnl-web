from jrnl import (
    Journal,
    plugins,
    util,
)

import gfm

import slugify

main_config = util.load_config('jrnl-config.yaml')


def ls():
    return main_config['journals'].keys()


def load(journal_name):
    if journal_name not in main_config['journals']:
        return None
    config = util.scope_config(main_config, journal_name)
    return Journal.open_journal(journal_name, config, legacy=True)


def search_entry(journal, timestamp):
    for entry in journal.entries:
        if timestamp == entry.date.timestamp():
            return entry
    return None


# TODO: Better name & organization of this module!
def entries(journal, count=None):
    exporter = plugins.get_exporter('json')

    # Return all entries
    if not count:
        entries = reversed(journal.entries)
    else:
        entries = list(reversed(journal.entries))[:count]

    rv = []
    for entry in entries:
        e = exporter.entry_to_dict(entry)
        e['markdown'] = e['body']
        e['html'] = gfm.markdown(e['body'])
        e['slug'] = slugify.slugify(e['title'])
        del e['body']
        rv.append(e)

    return rv


def tags(journal):
    return [{"name": tag.name, "count": tag.count} for tag in journal.tags]
