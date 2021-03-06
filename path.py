import os
import globals
import json
from utils import read_file, write_file, colorprint
from typing import Dict

# This is being declared globally in order to prevent the data file being read from disk every single time it is required
pathdict: Dict = {"please_dont_use_this_as_a_segment_it_is_required_by_zconfer": ""}

def init_pathdict():
    global pathdict
    if pathdict.get('please_dont_use_this_as_a_segment_it_is_required_by_zconfer', 'already_init') != 'already_init':
        pathdict = json.loads(read_file(globals.jsondata.path))

def dump_pathdict():
    global pathdict
    write_file(globals.jsondata.path, json.dumps(pathdict))


def check_segment_exists(seg):
    global pathdict
    init_pathdict()

    if seg.upper() not in pathdict:
        print(colorprint("Segment {} was not found in PATH".format(seg), "red"))
        return False

    return True


def generate():
    global pathdict
    init_pathdict()

    pathstring = "export PATH=$PATH:"
    for seg in pathdict:
        if pathdict[seg]['enabled']:
            pathstring = pathstring + pathdict[seg]['value'] + ":"

    write_file(globals.modules.path, pathstring[:-1])

def set_segment(seg, value):
    global pathdict
    init_pathdict()

    seg = seg.upper()
    pathdict.setdefault(seg, {'value': "", 'enabled': True})
    pathdict[seg]['value'] = value

    dump_pathdict()
    generate()

    print(colorprint(f"Successfully set segment {seg} to '{value}'", "green"))

def get_segment(seg):
    global pathdict
    init_pathdict()

    seg = seg.upper()

    if not check_segment_exists(seg):
        return
    
    print(pathdict[seg]['value'])

def remove_segment(seg):
    global pathdict
    init_pathdict()

    seg = seg.upper()

    if not check_segment_exists(seg):
        return

    del pathdict[seg]

    dump_pathdict()
    generate()

    print(colorprint(f"Successfully removed segment {seg}", "green"))

def enable_segment(seg):
    global pathdict
    init_pathdict()

    seg = seg.upper()

    if not check_segment_exists(seg):
        return

    pathdict[seg]['enabled'] = True

    dump_pathdict()
    generate()

    print(colorprint(f"Successfully enabled segment {seg}", "green"))
    
def disable_segment(seg):
    global pathdict
    init_pathdict()

    seg = seg.upper()

    if not check_segment_exists(seg):
        return

    pathdict[seg]['enabled'] = False
    dump_pathdict()
    generate()

    print(colorprint(f"Successfully disabled segment {seg}", "green"))

def view():
    global pathdict
    init_pathdict()

    if len(pathdict) == 0:
        print(colorprint("No ZConf-created segments in PATH", "red"))
        return

    print(colorprint("{:20}{:60}{:15}".format("Segment", "Value", "Enabled"), "bold"))
    for seg in pathdict:
        print("{:20}{:60}{:15}".format(seg, pathdict.get(seg)['value'], ("YES" if pathdict[seg]['enabled'] else "NO")))
    print()
