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


import heapq
import threading


class EventLoop(object):

    def __init__(self, stopper=None):
        if not stopper:
            stopper = _stopper
        self._el = _EventLoop(stopper)

    def daemon(self, sec, priority=0L):
        def a(cb):
            def b():
                self._el.post(sec, cb, priority)
            return b

        return a

    def every(self, sec, cb, priority=0L):
        self._el.post(sec, cb, priority)


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
        self.post(0.5, self._check, 100L)

    def post(self, sec, cb, priority):
        task = _Task(self, sec, cb, priority)
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

    _counter = 0L
    _counterLock = threading.Lock()

    @staticmethod
    def _getID():
        _Task._counterLock.acquire()
        _Task._counter = _Task._counter + 1
        tmp = _Task._counter
        _Task._counterLock.release()

    def __init__(self, el, sec, cb, priority):
        self._el = el
        self._sec = sec
        self._cb = cb
        self._timer = threading.Timer(self._sec, self)
        self._id = 0L
        self._priority = priority

        self._el.add(self._timer)

    def __call__(self):
        self._el.remove(self._timer)

        if self._el.stop:
            return

        # tell the worker to execute job
        self._id = _Task._getID()
        self._el.worker.enqueue(self)

    def __lt__(self, rhs):
        if self._priority > rhs._priority:
            return True
        if self._priority < rhs._priority:
            return False
        return self._id < rhs._id

    def __eq__(self, rhs):
        return self._priority == rhs._priority and self._id == rhs._id

    def __ne__(self, rhs):
        return not self == rhs

    def __gt__(self, rhs):
        return self >= rhs and self != rhs

    def __ge__(self, rhs):
        return not self < rhs

    def __le__(self, rhs):
        return not self > rhs

    def start(self):
        self._timer.start()

    @property
    def tag(self):
        return id(self._cb)

    def action(self):
        try:
            self._cb()
        except Exception, e:
            print e
        except:
            pass

        self._el.post(self._sec, self._cb, self._priority)


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
                    task = heapq.heappop(self._queue)
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
        if task.tag not in (t.tag for t in self._queue):
            heapq.heappush(self._queue, task)
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
