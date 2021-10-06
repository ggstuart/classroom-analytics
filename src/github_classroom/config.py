from configparser import ConfigParser

from .organisation import Organisation
from .assignment import Assignment

def config_from_filename(filename):
    conf = ConfigParser()
    conf.read(filename)
    return conf

def org_from_config(filename):
    conf = config_from_filename(filename)
    username = conf.get('github', 'username')
    token = conf.get('github', 'token')
    org_name = conf.get('github', 'organisation')
    return Organisation(org_name, username, token)

def assignments_from_config(filename):
    conf = config_from_filename(filename)
    username = conf.get('github', 'username')
    token = conf.get('github', 'token')
    org_name = conf.get('github', 'organisation')
    assignment = conf.get('classroom', 'assignment')
    org = Organisation(org_name, username, token)
    return org.assignments(assignment)

def assignment_from_config(filename):
    conf = config_from_filename(filename)
    username = conf.get('github', 'username')
    token = conf.get('github', 'token')
    org_name = conf.get('github', 'organisation')
    roster_filename = conf.get('classroom', 'roster_filename')
    prefix = conf.get('classroom', 'assignment_prefix')
    org = Organisation(org_name, username, token)
    return Assignment(org, roster_filename, prefix)
