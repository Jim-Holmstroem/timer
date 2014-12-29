#!/usr/bin/python
from __future__ import print_function, division

import argparse
import os

import gtk

def window(component):
    window = gtk.Window()
    window.connect("destroy", gtk.mainquit)
    window.add(component)
    window.show_all()
    gtk.main()


def main(time):
    content = gtk.Label(time)
    window(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start timer')
    parser.add_argument('time')
    args = parser.parse_args()
    main(
        time=args.time
    )
