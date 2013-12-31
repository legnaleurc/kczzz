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


import logging


class Logger(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._fh = logging.FileHandler(u'/tmp/kczzz.log')
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self._fh.setFormatter(fmt)
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(self._fh)

    def debug(self, msg):
        self._logger.debug(msg)
        self._flush()

    def info(self, msg):
        self._logger.info(msg)
        self._flush()

    def warn(self, msg):
        self._logger.warn(msg)
        self._flush()

    def error(self, msg):
        self._logger.error(msg)
        self._flush()

    def _flush(self):
        self._fh.flush()
