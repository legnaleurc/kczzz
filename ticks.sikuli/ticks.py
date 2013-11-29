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
        # keep timer objects to cleanup
        self._timers = []
        # prevent race condition
        self._timerLock = threading.Lock()
        # check if about to close
        self._stopper = stopper
        # true if about to close
        self._stop = False
        # prevent race condition
        self._stopLock = threading.Lock()
        # the worker that do real jobs
        # it will only run one job at a time
        self._worker = _Worker(self)

        self._worker.start()

        # check terminate condition every 0.5 sec
        self.post(0.5, self._check)

    def post(self, sec, cb):
        task = _Task(self, sec, cb)
        task.start()

    def add(self, timer):
        self._timerLock.acquire()
        self._timers.append(timer)
        self._timerLock.release()

    def remove(self, timer):
        self._timerLock.acquire()
        self._timers.remove(timer)
        self._timerLock.release()

    @property
    def stop(self):
        self._stopLock.acquire()
        tmp = self._stop
        self._stopLock.release()
        return tmp

    @property
    def worker(self):
        return self._worker

    def _check(self):
        if self._stopper():
            self._stopLock.acquire()
            self._stop = True
            self._stopLock.release()

            self._timerLock.acquire()
            for timer in self._timers:
                timer.cancel()
            self._timerLock.release()


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

        # tell the worker to execute job
        self._el.worker.enqueue(self)

    def start(self):
        self._timer.start()

    @property
    def id_(self):
        return id(self._cb)

    def action(self):
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
            # sleep until task arrive
            self._condition.acquire()
            self._condition.wait()
            self._condition.release()

            while True:
                self._queueLock.acquire()
                if len(self._queue) > 0:
                    task = self._queue[0]
                    del self._queue[0]
                else:
                    task = None
                # actions may take a long time
                # release the lock here to avoid
                # queue blocking
                self._queueLock.release()

                if not task:
                    break
                task.action()

    def enqueue(self, task):
        if self._el.stop:
            return

        self._queueLock.acquire()
        # must ensure there is no same job in the queue
        if task.id_ not in (t.id_ for t in self._queue):
            self._queue.append(task)
        self._queueLock.release()

        # notify worker to consume
        self._condition.acquire()
        self._condition.notifyAll()
        self._condition.release()


def _stopper():
    import os
    if os.path.exists(_MARK):
        os.remove(_MARK)
        return True
    return False
