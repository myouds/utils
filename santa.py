#!/usr/bin/env python

import random
import argparse

class Santa:
    def __init__(self, name, santees):
        self.name = name
        self.possible_santees = { s for s in santees if s != name }
        if not self.possible_santees:
            raise ValueError("Santa %s has no possible santees" % name)

    def remove_santee(self, name):
        try:
            self.possible_santees.remove(name)
        except KeyError:
            return False
        return True

    def select_santee(self):
        return random.choice(list(self.possible_santees))

    def __lt__(self, other):
        return len(self.possible_santees) < len(other.possible_santees)

class ExcludeAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        #
        # First, split the value into its parts - it should be "<sender>:<recpt>"
        #
        try:
            sender, recpt = value.split(':')
        except ValueError as e:
            raise ValueError('Invalid exclude argument')
        #
        # Get the existing set
        #
        cur = getattr(namespace, self.dest)
        
        #
        # Initialise this sender's set if necessary
        #
        if sender not in cur:
            cur[sender] = set()
        #
        # Add the recipient
        #
        cur[sender].add(recpt)
        #
        # Now update the attribute
        #
        setattr(namespace, self.dest, cur)

#
# Command line args
#
parser = argparse.ArgumentParser()
parser.add_argument('names', nargs='*')
parser.add_argument('--exclude', '-e', action=ExcludeAction, default=dict())
args = parser.parse_args()

#
# Create the Santa objects
#
santas = list()
for sender in args.names:
    recpts = [ n for n in args.names if n not in args.exclude.get(sender, []) ]
    try:
        santas.append(Santa(sender, recpts))
    except ValueError as e:
        print(e)
        exit(1)

while len(santas):
    #
    # Sort list so that we always take the element with the smallest
    # number of options. This is to avoid any elements running out
    # of options.
    #
    santas.sort()
    #
    # Now calculate this santa/santee combination
    #
    sender = santas[0].name
    recpt = santas[0].select_santee()
    print("%s --> %s" % (sender, recpt))
    #
    # Remove this element from list
    #
    santas.remove(santas[0])
    
    for s in santas:
        #
        # Nobody else give to this recipient
        #
        s.remove_santee(recpt)
        #
        # The recipient should not send to this sender if it can be avoided
        #
        if s.name == recpt and len(s.possible_santees) > 1:
            s.remove_santee(sender)

exit(0)
