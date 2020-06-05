import time

class Timer:
    timers = dict()

    def __init__(self, name):
        self.name = name
        self._start_time = time.time()
        self.timers.setdefault(name, 0)

    def reset(self, name=None):
        self._start_time = time.time()
        self.timers.setdefault(name, self._start_time)

    def read(self):
        elapsed_time = time.time() - self._start_time
        if self.name:
            self.timers[self.name] += elapsed_time
        return elapsed_time