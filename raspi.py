import threading


class RaspberryThread(threading.Thread):
    def __init__(self, function):
        self.paused = True
        self.state = threading.Condition()
        self.function = function
        super(RaspberryThread, self).__init__()
        self._stop = threading.Event()

    def start(self):
        super(RaspberryThread, self).start()

    def run(self):
        # self.resume() #unpause self
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # block until notifed
            while not self.paused:
                # Call function
                self.function()

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True

    def stop(self):
        #log.debug('{0} stopped'.format(self.name))
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
