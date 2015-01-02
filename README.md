timer
=====

requirements
------------

* gtk
* pyaudio

Installation
------------

    sudo ln -s `pwd`/timer.py /usr/bin/timer
    # then it's possible to
    timer 1
    timer 15
    # great with dmenu

Note
----
This is a quick and dirty application where to goal was to have as little logic
as possible. The first implementation is 6 lines + boiler plate code for audio
playback, window creation, argument parsing and non-local variable in callback.
