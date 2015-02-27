YAUL -- Yet Another Utility Library
===================================

YAUL is a loose collection of often-reimplemented tools published in
order to promote code reuse. Its components function independently and
are intended to be as lightweight as possible.

The documentation sections below provide some details on each
component's usage and some sample code. More comprehensive examples
can be found in the [demos/](./demos/) directory.

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

yaul.parallel
-------------

`yaul.parallel` provides a common parallel processing "pool"
functionality for multiple (and disparate) parallelism methods in
Python. It supports these parallelism methods:

- **serial** (`yaul.parallel.SERIAL`) - not true parallelism, but
    useful for testing code in a  sane(r) environment.
- **threaded** (`yaul.parallel.THREADED`) - parallel processing
    achieved through Python threads, using the
    `multiprocessing.pool.ThreadPool` builtin.
- **multiproessed** (`yaul.parallel.MULTIPROCESSED`) - parappel
    processing achieved through the Python `multiprocessing.Pool`
    builtin.

### Constructing a GenericPool

The core object of `yaul.parallel` is `GenericPool`, which serves as a
common interface to access the different parallelism methods. It can
be constructed as follows:

    >>> from yaul.parallel import GenericPool
    >>> pool = GenericPool(parallel_type, num_threads)

Both arguments are optional. Their descriptions:

- `parallel_type` - One of the pre-defined parallelism types described
  above; if not given, `yaul.parallel._DEFAULT` will be used instead
  (default: serial).
- `num_threads` - The number of parallel "threads" (or processes) the
  pool should support; by default, it will make a best guess based on
  `multiprocessing.cpu_count()`.

### Using a GenericPool

The pool can be used via its `map_reduce` method. The method is
invoked as follows:

    >>> pool.map_reduce(mapfunc, collection, reducer, blocking)

Its arguments:

- `mapfunc` (required) - must be a function that takes a single input
  argument, and returns a single value.
- `collection` (required) - an iterable (list, set, etc) collection of
  inputs to be passed to the mapping function one by one.
- `reducer` (optional) - a function taking an iterable as input and
  returning a (possibly smaller) iterable of "reduced" results;
  default: a pass-through function that leaves mapping results unchanged.
- `blocking` (optional) - a True/False toggle on whether the
  `map_reduce` call returns an iterator to serve results as they
  become ready, or waits for all results to be ready and serves a list
  instead.

`map_reduce()` returns results in the same order that their respective
inputes were read in.

A full (interactive) example of the usage of `GenericPool` can be found in a
separate [demo file](./demos/word_count.py), which counts the number
of words in a file by splitting counting words in the file's lines
over the multithreaded pool. 