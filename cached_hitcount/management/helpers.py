# -*- coding: utf-8 -*-
import string
import getpass

def to_bool(val, default=False, yes_choices=None, no_choices=None):
    if not isinstance(val, basestring):
        return bool(val)

    yes_choices = yes_choices or ('y', 'yes', '1', 'on', 'true', 't')
    no_choices = no_choices or ('n', 'no', '0', 'off', 'false', 'f')

    if val.lower() in yes_choices:
        return True
    elif val.lower() in no_choices:
        return False
    return default


def prompt(name, default=None):
    """
    Grab user input from command line.

    :param name: prompt text
    :param default: default value if no input provided.
    """

    prompt = name + (' [%s]' % default if default else '')
    prompt += ' ' if name.endswith('?') else ': '
    while True:
        rv = raw_input(prompt)
        if rv:
            return rv
        if default is not None:
            return default


def prompt_pass(name, default=None):
    """
    Grabs hidden (password) input from command line.

    :param name: prompt text
    :param default: default value if no input provided.
    """

    prompt = name + (default and ' [%s]' % default or '')
    prompt += name.endswith('?') and ' ' or ': '
    while True:
        rv = getpass.getpass(prompt)
        if rv:
            return rv
        if default is not None:
            return default


def prompt_bool(name, default=False, yes_choices= ('y', 'yes', '1', 'on', 'true', 't'), no_choices=('n', 'no', '0', 'off', 'false', 'f')):
    """
    Grabs user input from command line and converts to boolean
    value.

    :param name: prompt text
    :param default: default value if no input provided.
    :param yes_choices: default 'y', 'yes', '1', 'on', 'true', 't'
    :param no_choices: default 'n', 'no', '0', 'off', 'false', 'f'
    """

    while True:
        rv = prompt(name + '?', yes_choices[0] if default else no_choices[0])
        if not rv:
            return default
        rv = to_bool(rv, default=None, yes_choices=yes_choices, no_choices=no_choices)
        if rv is not None:
            return rv


def prompt_choices(name, choices, default=None, resolve=string.lower,
                   no_choice=('none',)):
    """
    Grabs user input from command line from set of provided choices.

    :param name: prompt text
    :param choices: list or tuple of available choices. Choices may be
                    single strings or (key, value) tuples.
    :param default: default value if no input provided.
    :param no_choice: acceptable list of strings for "null choice"
    """

    _choices = []
    options = []

    for choice in choices:
        if isinstance(choice, basestring):
            options.append(choice)
        else:
            options.append("[%s] %s" % (choice[0], choice[1]))
            choice = choice[0]
        _choices.append(choice)

    while True:
        rv = prompt(name + '? - %s' % '\n'.join(options), default)
        if not rv:
            return default
        rv = resolve(rv)
        if rv in no_choice:
            return None
        if rv in _choices:
            return rv
