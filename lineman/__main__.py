"""
Lineman

Usage: lineman.py [-h] (<file> <config>) [-o <output.json>]

Options:
  -h --help                                     show this message and exit
  -o <output.json> --output=<output.json>       optional output file for results

"""
import csv
import json
import pdb

from docopt import docopt
import yaml
import dateutil.parser as date_parser

import cappy

_file = '<file>'
_config = '<config>'
_output = '--output'

# config magic strings
_cv = 'cappy_version'
_es = 'event_assignment_strategy'
_ao = 'arm_order'
_cm = 'check_mappings'
_tk = 'token'
_ru = 'redcap_url'
_si = 'subject_id'

# config mapping magic strings
_k = 'key'
_m = 'match_against'

def main(args):
    """
    Uses a config and a records json file to generate redcap api sendable data
    """
    with open(args[_config], 'r') as config_file:
        global config
        config = yaml.load(config_file.read())

    with open(args[_file], 'r') as json_infile:
        records = json.loads(json_infile.read())

    api = cappy.API(config[_tk], config[_ru], config[_cv])

    records = get_valid_records(api, records, config[_cm])
    records = fix_events(api, records)

    if args.get(_output):
        with open(args[_output], 'w') as outfile:
            outfile.write(json.dumps(records))
    else:
        print(json.dumps(records))

def get_valid_records(api, records, mappings):
    """
    Returns records that have a subjecto to latch onto in redcap. For instance if there
    was a subject present in the input that does not have a corresponding redcap entry
    it will not be in this list
    """
    redcap_records = get_redcap_records(api)
    is_valid = get_validator(redcap_records, mappings)
    return [record for record in records if is_valid(record)]

def get_redcap_records(api):
    """
    Grab records from the api
    """
    res = api.export_records()
    return json.loads(res.content)

def get_validator(check_against_records, mappings):
    """
    Returns a validator function that will check to see if a record has a corresponding
    subject in redcap
    """
    def validate(record):
        nonlocal check_against_records
        nonlocal mappings
        valid = False
        for check_record in check_against_records:
            for map in mappings:
                records_have_data = record.get(map[_k]) and check_record.get(map[_m])
                records_match = record.get(map[_k]) == check_record.get(map[_m])
                if records_have_data and records_match:
                    valid = True
                    record[map[_k]] = check_record[map[_k]]
        return valid
    return validate

def fix_events(api, records):
    """
    Fixs the redcap_event_name field in the records based on the event names that are in the
    target project
    """
    redcap_records = get_redcap_records(api)

    if (config[_es] == 'chronological'):
        events = get_events(api)
        subjects = init_subjects(records)
        rename_events_in_subjects(subjects, events)
        return records

def get_events(api):
    """
    Get the events from the target redcap and filter ones that are not listed in the arm_order
    field in the config
    """
    res = api.export_events()
    redcap_events = json.loads(res.content)
    events = [event for event in redcap_events if int(event.get('arm_num')) in config[_ao]]
    events.sort(key=lambda e : int(e.get('day_offset')))
    return events

def init_subjects(records):
    """
    Builds out a dictionary that has subject ids as keys and lists of records. Also sorts
    those events.
    """
    subjects = {}
    for record in records:
        value = subjects.get(record[config[_si]])
        if type(value) == type(None):
            value = subjects[record[config[_si]]] = []
        value.append(record)
    for key in subjects:
        subjects[key].sort(key=lambda r : r.get('redcap_event_name'))
    return subjects

def rename_events_in_subjects(subjects, events):
    """
    Goes through all subject events and renames the datetime to the event name in the corresponding
    index of the events list. Uses zip so if one runs out before the other, its fine
    """
    for key in subjects:
        zipped = list(zip(subjects[key], events))
        for index, record in enumerate(zipped):
            subjects[key][index]['redcap_event_name'] = events[index]['unique_event_name']

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
    exit()
