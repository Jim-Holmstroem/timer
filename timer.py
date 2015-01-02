#!/usr/bin/env python
from __future__ import print_function, division

from functools import partial
from itertools import product

from collections import Iterable

import os

import argparse

import gtk


def window(component):
    window = gtk.Window()
    window.connect("destroy", gtk.mainquit)
    window.add(component)
    window.show_all()
    gtk.main()


def component(Component):
    """
    {
        label = gtk.Label('label')
        label.set_size_request(640, 480)
        label.set_justify(gtk.JUSTIFY_FILL)
    } =>
    {
        Label = component(gtk.Label)
        label = Label(
            'label',
            size_request=(640, 480),
            justify=gtk.JUSTIFY_FILL
        )
    }
    """
    def new_style_component(*args, **kwargs):
        component = Component(*args)

        def set_property(name, values):
            getattr(
                component,
                "set_{name}".format(name=name)
            )(
                *(values if isinstance(values, Iterable) else (values, ))
            )

        map(
            partial(apply, set_property),
            kwargs.iteritems()
        )

        return component

    return new_style_component


def attributes(**kwargs):
    """
    Label(
        'text',
        attributes=attributes(
            Scale=3,
            Stretch=pango.STRETCH_EXPANDED
        )
    )

    Note
    ----
    At it's current state it always force the attributes on the entire
    component.
    See. start_index, end_index
    """
    pango = __import__('pango')
    attr_list = pango.AttrList()

    def attribute(name, values):
        return getattr(
            pango,
            "Attr{name}".format(name=name)
        )(
            *(values if isinstance(values, Iterable) else (values, )),
            **{'start_index': 0, 'end_index': -1}
        )

    attributes = map(
        partial(apply, attribute),
        kwargs.iteritems()
    )
    map(
        attr_list.insert,
        attributes
    )

    return attr_list


Label = component(gtk.Label)


def player(filename, chunk_size=1024):
    """
    Note
    ----
    Somthing makes the player stop before it reaches the end of the sample.
    But it is more or less the official first example of pyaudio..
    """
    pyaudio = __import__('pyaudio')
    wave = __import__('wave')

    def _player():
        wf = wave.open(filename, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(
                wf.getsampwidth()
            ),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        data = wf.readframes(chunk_size)

        while data != '':
            stream.write(data)
            data = wf.readframes(chunk_size)

        stream.stop_stream()
        stream.close()

        p.terminate()

    return _player


def main(minutes):
    assert(minutes >= 1)

    def done(
        alarm_player=player(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'sounds',
                'truck_horn.wav',
            )
        )
    ):
        alarm_player()

    # renderer = partial(apply, "{}:{}".format)
    renderer = str

    closure = {
        'counts': product(
            reversed(range(minutes)),
            reversed(range(60))
        )
    }  # HACK non-local
    start_time = (minutes, 0)
    time_left = Label(
        renderer(start_time),
        attributes=attributes(
            Scale=16
        )
    )

    def timer_tick():
        try:
            time_left.set_text(renderer(closure['counts'].next()))
        except StopIteration:
            done()

        return True

    ms = 1
    s = 1000 * ms

    gtk.timeout_add(s, timer_tick)

    window(component=time_left)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start timer with m minutes')
    parser.add_argument('minutes', type=int)
    args = parser.parse_args()
    main(
        minutes=args.minutes
    )
