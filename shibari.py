import functools


class Rig:
    """A store of functions inside nested dicts.

    Each dict acts as a scope. Functions inside a scope will only run once
    until that scope is cleared.

    Takes an arbitrary number of arguments as the list of scopes to create.

    Attributes:
        rigs (dict): A nested dict which stores bound functions in a scope.

    """

    def __init__(self, *names):
        self.rigs = {}

        for n in names:
            self.rigs[n] = {}

    def bind(self, scope: str, name=None):
        """Bind a function to a named scope.

        Arguments:
            scope: The name to which the wrapped function is bound.
        """
        if not self.rigs.get(scope):
            self.rigs[scope] = {}

        def decorator(function):
            @functools.wraps(function)
            def wrapper(instance=None, *args, **kwargs):
                scoped_funcs = self.rigs[scope]
                func_name = name or function.__name__

                bound_func = scoped_funcs.get(func_name)
                if not bound_func:
                    if instance:
                        scoped_funcs[func_name] = function(
                            instance, *args, **kwargs,
                        )
                    else:
                        scoped_funcs[func_name] = function(*args, **kwargs)

                return scoped_funcs[func_name]

            return wrapper
        return decorator

    def free(self, name: str):
        """Free all functions in a scope.

        Arguments:
            name: The scope to free.
        """
        def decorator(function):
            @functools.wraps(function)
            def wrapper(instance=None, *args, **kwargs):
                try:
                    if instance:
                        f = function(instance, *args, **kwargs)
                    else:
                        f = function(*args, **kwargs)
                    return f
                finally:
                    self.rigs[name] = {}

            return wrapper
        return decorator
