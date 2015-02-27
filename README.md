YAUL -- Yet Another Utility Library
===================================

YAUL is a loose collection of often-reimplemented tools published in
order to promote code reuse. Its components function independently and
are intended to be as lightweight as possible.

The documentation sections below provide some details on each
component's usage and some sample code. More comprehensive examples
can be found in the (demos/)[./demos/] directory.

yaul.cache
----------

This component provides a basic cache mechanism implemented via an
`@cache` decorator. If Python 3's `functools.lru_cache` is available,
`@cache` just serves as a wrapper. If not (e.g. Python 2), a simple
implementaion of a cache using a dict is put in place.

    >>> from yaul.cache import cache
    >>> @cache(maxsize=32)
    ... def foo():
    ...     print('running foo()')
    ...     return 'bar'
    ... 
    >>> foo()
    running foo()
    'bar'
    >>> foo()
    'bar'

yaul.daemon
-----------

This component provides a method to easily turn a script or program
into a background daemon controlled by an init script.

This is done via the `yaul.daemon.Daemon` class, which can be subclassed by a
user's class. Override the `run()` method to define what counts as
"running" the daemon. To run properly, a `Daemon` also requires its
`pidfile` attribute to be set, indicating a file location that can be
used to track the running process. A Daemon object can be run as an
init script by calling `yaul.daemon.run_as_service`.

A brief example:

    from yaul.daemon import Daemon, run_as_service
    class TimeWriterDaemon(Daemon):
        def run(self):
	    import time
	    while True:
	        time.sleep(1)
		with open("/tmp/time.txt", "w") as f:
		    f.write(str(time.time()))

    d = TimeWriterDaemon("/tmp/timedaemon.pid")
    run_as_service(d)

If the following code were in a file named `timedaemon.py`, then the
process could be controlled by the following commands:

    $ python timedaemon.py start
    $ python timedaemon.py restart
    $ python timedaemon.py stop

`yaul.daemon.Daemon` does not currently support the `status` command.

