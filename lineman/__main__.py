docstr = """
Lineman

Usage: lineman.py [-hv] (<file> <config>) [-o <output.json>] [-l <log.json>]

Options:
  -h --help                                     show this message and exit
  -v --version                                  show version.
  -o <output.json> --output=<output.json>       optional output file for results
  -l <log.json> --log=<log.json>                optional log output for infomation related to the run

"""

import csv
import json
import pdb

from docopt import docopt
import yaml
import dateutil.parser as date_parser

import cappy

from lineman.version import __version__

_file = '<file>'
_config = '<config>'
_output = '--output'
_log = '--log'

# config magic strings
_cv = 'cappy_version'
_tv = 'template_version'
_es = 'event_assignment_strategy'
_ao = 'arm_order'
_cm = 'check_mappings'
_tk = 'token'
_ru = 'redcap_url'
_si = 'subject_id'
_ro = 'requests_options'

# config mapping magic strings
_k = 'key'
_m = 'match_against'

def main(args):
    """
    Uses a config and a records json file to generate redcap api sendable data
    """
    set_config(args[_config])

    with open(args[_file], 'r') as json_infile:
        records = json.loads(json_infile.read())

    global report
    report = {
        'records': {
            'num_inputed': 0,
            'num_redcap': 0,
            'num_valid': 0,
            'num_invalid': 0,
            'validated': [],
            'not_validated': [],
            'mappings_done': {},
        },
        'subject_event_dict': {}
    }

    api = cappy.API(config[_tk], config[_ru], config[_cv], config.get(_ro))

    records = get_valid_records(api, records, config[_cm])
    records = fix_events(api, records)

    final_report = make_hawk_prey(report)

    if args.get(_log):
        with open(args[_log], 'w') as logfile:
            logfile.write(json.dumps(final_report, indent=4, sort_keys=True))

    if args.get(_output):
        with open(args[_output], 'w') as outfile:
            outfile.write(json.dumps(records))
    else:
        print(json.dumps(final_report))

def set_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        global config
        config = yaml.load(config_file.read())
    return config

def get_valid_records(api, records, mappings):
    """
    Returns records that have a subjecto to latch onto in redcap. For instance if there
    was a subject present in the input that does not have a corresponding redcap entry
    it will not be in this list
    """
    redcap_records = get_redcap_records(api)
    report['records']['num_inputed'] = len(records)
    report['records']['num_redcap'] = len(redcap_records)
    is_valid = get_validator(redcap_records, mappings)
    validated = [record for record in records if is_valid(record)]
    report['records']['num_valid'] = len(validated)
    report['records']['num_invalid'] = len(records) - len(validated)
    return validated

def make_hawk_prey(report_dict):
    """
    Returns a dictionary containing the source with version, and
    the log's output so hawk_eye can read it
    """

    final_report = {'source': "lineman_%s" % config[_tv], 'output': {}}
    for key,value in report_dict.items():
        final_report['output'][key] = value

    return final_report


def get_redcap_records(api):
    """
    Grab records from the api
    """
    res = api.export_records(fields=['dm_subjid', 'dm_usubjid'], events=['1_arm_1'])
    return json.loads(str(res.content, 'utf-8'))

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
                    log_mappings_done(map, record, check_record)
                    record[map[_k]] = check_record[map[_k]]
        log_validated(valid, record)
        report['records']['validated'] = sorted(list(set(report['records']['validated'])))
        report['records']['not_validated'] = sorted(list(set(report['records']['not_validated'])))
        return valid
    return validate

def log_mappings_done(map, record, check_record):
    mapping_zone = report['records']['mappings_done'].get(record[config[_si]])
    if not type(mapping_zone) == type([]):
        report['records']['mappings_done'][record[config[_si]]] = []
    report['records']['mappings_done'][record[config[_si]]].append({
        'key': map[_k],
        'match_against': map[_m],
        'mapped_from': record[map[_k]],
        'mapped_to': check_record[map[_k]],
    })

def log_validated(valid, record):
    if valid:
        report['records']['validated'].append(record[config[_si]])
    else:
        report['records']['not_validated'].append(record[config[_si]])

def fix_events(api, records):
    """
    Fixs the redcap_event_name field in the records based on the event names that are in the
    target project
    """

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
    redcap_events = json.loads(str(res.content, 'utf-8'))
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
    index of the events list. Uses zip so if subject information runs out before the events
    get used up it's fine.

    However we need to make sure we dont' go over the maximum amount of events. We pop of any
    trailing subject events in that case otherwise we get a strange error from redcap about
    it not being able to parse what we gave it.
    """
    for key in subjects:
        zipped = list(zip(subjects[key], events))
        max_events = len(events)
        for index, record in enumerate(zipped):
            log_subject_events(subjects, key, index, events)
            subjects[key][index]['redcap_event_name'] = events[index]['unique_event_name']
        while len(subjects[key]) > max_events:
            subjects[key].pop()


def log_subject_events(subjects, subjkey, index, events):
    pairings = report['subject_event_dict'].get(subjkey)
    if not type(pairings) == type([]):
        report['subject_event_dict'][subjkey] = []
    report['subject_event_dict'][subjkey].append({
        'date': subjects[subjkey][index]['redcap_event_name'],
        'event_name': events[index]['unique_event_name']
    })

def cli_run():
    args = docopt(docstr, version='Lineman %s' % __version__)
    main(args)

if __name__ == '__main__':
    cli_run()
    exit()
