"""
Imports that we need at runtime, but might not be present.

When importing one of these modules, always do it in the function where you
need the module.  Some tests will need to remove the module.  If you import
it at the top level of your module, then the test won't be able to simulate
the module being unimportable.

The import will always succeed, but the value will be None if the module is
unavailable.

Bad::

    # MyModule.py
    import unsure

    def use_unsure():
        unsure.something()

Also bad::

    # MyModule.py
    from scriv.extras import unsure

    def use_unsure():
        unsure.something()

Good::

    # MyModule.py

    def use_unsure():
        from scriv.extras import unsure
        if unsure is None:
            raise Exception("Module unsure isn't available!")

        unsure.something()

"""

import contextlib

# This file's purpose is to provide modules to be imported from here.
# pylint: disable=unused-import

# TOML support is an install-time extra option.
try:
    import toml
except ImportError:  # pragma: no cover
    toml = None  # type: ignore


@contextlib.contextmanager
def without(modname):
    """
    Hide a module for testing.

    Use this in a test function to make an optional module unavailable during
    the test::

        with scriv.extras.without('toml'):
            use_toml_somehow()

    Arguments:
        modname (str): the name of a module importable from `scriv.optional`.

    """
    real_module = globals()[modname]
    try:
        globals()[modname] = None
        yield
    finally:
        globals()[modname] = real_module
