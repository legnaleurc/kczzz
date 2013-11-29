"""
Copyright (c) 2013 Wei-Cheng Pan <legnaleurc@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


import threading


class EventLoop(object):

    def __init__(self, stopper=None):
        if not stopper:
            stopper = _stopper
        self._el = _EventLoop(stopper)

    def every(self, sec, cb=None):
        if cb:
            self._el.post(sec, cb)
            return

        def a(cb):
            def b():
                self._el.post(sec, cb)
            return b

        return a


_MARK = u'/tmp/stop'


class _EventLoop(object):

    def __init__(self, stopper):
        self._timers = []
        self._stop = False
        self._worker = _Worker(self)
        self._stopper = stopper

        self._worker.start()

        self.post(0.5, self._check)

    def post(self, sec, cb):
        task = _Task(self, sec, cb)
        task._timer.start()

    def add(self, timer):
        self._timers.append(timer)

    def remove(self, timer):
        self._timers.remove(timer)

    @property
    def stop(self):
        return self._stop

    @property
    def worker(self):
        return self._worker

    def _check(self):
        if self._stopper():
            self._stop = True
            for timer in self._timers:
                timer.cancel()


class _Task(object):

    def __init__(self, el, sec, cb):
        self._el = el
        self._sec = sec
        self._cb = cb
        self._timer = threading.Timer(self._sec, self)
        self._el.add(self._timer)

    def __call__(self):
        self._el.remove(self._timer)

        if self._el.stop:
            return

        self._el.worker.enqueue(self._action, id(self._cb))

    def _action(self):
        try:
            self._cb()
        except Exception, e:
            print e
        except:
            pass

        self._el.post(self._sec, self._cb)


class _Worker(threading.Thread):

    def __init__(self, el):
        threading.Thread.__init__(self)

        self._el = el
        self._queue = []
        self._condition = threading.Condition()
        self._queueLock = threading.Lock()

    def run(self):
        while not self._el.stop:
            self._condition.acquire()
            self._condition.wait()
            self._condition.release()

            while True:
                self._queueLock.acquire()
                if len(self._queue) > 0:
                    action, id_ = self._queue[0]
                    del self._queue[0]
                else:
                    action, id_ = None, None
                self._queueLock.release()

                if not action:
                    break
                action()

    def enqueue(self, action, id_):
        self._queueLock.acquire()
        if id_ not in (x[1] for x in self._queue):
            self._queue.append((action, id_))
        self._queueLock.release()

        self._condition.acquire()
        self._condition.notifyAll()
        self._condition.release()


def _stopper():
    import os
    if os.path.exists(_MARK):
        os.remove(_MARK)
        return True
    return False
