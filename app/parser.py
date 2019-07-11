# TODO: The title length should be fixed like maybe 10 chars or so(would not be good still let's see)
import re
import string
from slugify import slugify

ALPHA = string.ascii_letters
TIME = r'(2[0-3]|[01]?[0-9]):([0-5]?[0-9])'
DATE = r"\d{4}-\d{2}-\d{2}"


def journal(filepath):
    """Convert a jrnl file into dictionary.

    The formatted data would be:
        {
            "starred": True/False
            "Date": date of the entry
            "Title": Title of the entry
            "Body": Body of the entry (if any)

        }
    """
    with open(filepath, 'r') as f:
        read = f.read().splitlines()

    read = list(filter(None, read))
    records = sanitize(read)
    entries = list()

    for record in records:
        e = dict()
        e['date'] = re.search(DATE, record).group()
        e['time'] = re.search(TIME, record).group()
        if "*" in record:
            e['starred'] = True
        else:
            e['starred'] = False

        e['title'], e['body'] = body_title(record)
        #https://stackoverflow.com/questions/427102/what-is-a-slug-in-django
        e['slug'] = slugify(e['title'])
        entries.append(e)
    return entries


def body_title(entry: str):
    """Choose what is body and what is title.

    Arguments:
        entry {str} -- entry to decide on
    """
    entry = entry[17:]
    if "\n" in entry:
        split = entry.split("\n")
    else:
        split = entry.split()

    if split:
        title = split[0]
        split.pop(0)
        body = " ".join(split)
    else:
        title, body = "",""
    return title, str(body)


def sanitize(records: list):
    """Join all the separated records to their headers

    when the jrnl file is read, it separates string on "\n"
    which can cause problem when parsing them as journal entries.
    This function will fix that problem.

    EX:
        Input: ["2019-09-04 7:00 what is this", "this is something."]
        Output: ["2019-09-04 7:00 what is this \nthis is something."]

    Arguments:
        records {list} -- List having all the journal entries
    """

    def helper():
        """Help in sanitization
        """
        for ind, r in enumerate(records):
            if ind == 0:
                continue
            else:
                if re.match(DATE, r[:10]):
                    continue
                else:
                    records[ind-1] = records[ind-1] + " \n " + r
                    records.pop(ind)

        return records

    data = helper()

    while True:
        if any(d.startswith(tuple(ALPHA)) for d in data):
            data = helper()
        else:
            break

    return data
