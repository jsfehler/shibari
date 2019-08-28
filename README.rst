shibari
=======

.. image:: https://img.shields.io/github/license/jsfehler/shibari.svg
    :alt: GitHub
    :target: https://github.com/jsfehler/shibari/blob/master/LICENSE

.. image:: https://travis-ci.org/jsfehler/stere.svg?branch=master
    :target: https://travis-ci.org/jsfehler/stere

Bind functions to only run once inside a desired scope.

Documentation
-------------

The Rig class exposes two methods: `bind` and `free`. Bind takes one argument: A name for a scope to bind the function.

Functions wrapped with `bind` will be called only once until the scope it is inside is freed.

Functions wrapped with `free` will free all the bound functions in a specific scope after the function's execution.

Example:

.. code-block:: python

    import shibari


    rig = shibari.Rig('ebi')


    @rig.bind('ebi')
    def timestamp():
        return str(time.time())


    @rig.free('ebi')
    def finish():
        pass


    >>> t = timestamp()
    >>> t2 = timestamp()
    >>> assert t == t2

    >>> finish()

    >>> t3 = timestamp()
    >>> t4 == timestamp()
    >>> assert t != t3
    >>> assert t3 == t4

Functions that take arguments can be bound, but will always return the same result until they are freed.

Example:

.. code-block:: python

    import shibari


    rig = shibari.Rig('ebi')


    @rig.bind('ebi')
    def timestamp(a, b):
        return f'{a}_{str(time.time())}_{b}'


    >>> t = timestamp('goodbye', 'world')
    >>> t2 = timestamp('hello', 'space')
    >>> assert t == t2
