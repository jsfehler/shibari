import functools


class Rig:
    def __init__(self, *names):
        self.rigs = {}
        
        for n in names:
            self.rigs[n] = {}

    def free(self, name):
        def decorator(function):
            @functools.wraps(function)
            def wrapper(instance, **kwargs):
                try:
                    function()
                    self.rigs[name] = {}
                except Exception as e:
                    self.rigs[name] = {}
                    raise e

            return wrapper
        return decorator


    def bind(self, rig):
        if not self.rigs.get(rig):
            self.rigs[rig] = {}

        def decorator(function):    
            @functools.wraps(function)
            def wrapper(instance=None, *args, **kwargs):
                rig_ref = self.rigs[rig]
                
                r = rig_ref.get(function.__name__)

                if not r:
                    if instance:
                        rig_ref[function.__name__] = function(instance, *args, **kwargs)
                    else:
                        rig_ref[function.__name__] = function(*args, **kwargs)

                return rig_ref[function.__name__]

            return wrapper
        return decorator
