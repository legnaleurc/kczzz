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

import ticks
import ui


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


logger = Logger()

el = ticks.EventLoop()
imgs = ui.Library()


@el.daemon(30, 5L)
def dismissDMMError():
    logger.info(u'checking DMM error')

    if exists(imgs.browserAlert):
        logger.info(u'found DMM error')

        click(imgs.browserAlertButtonCancel)

    logger.info(u'done DMM error checking')


def refresh():
    type(Key.F5)
    a = wait(imgs.systemButtonStart, 30)
    wait(5)
    click(a)
    wait(imgs.mainMenuButtonGo, 30)


@el.daemon(30, 4L)
def dismissKanColleError():
    logger.info(u'checking KanColle error')

    a = exists(imgs.systemScreenError)
    b = exists(imgs.flashAlert)
    if a:
        a = False
    elif b:
        a = False
        click(imgs.flashAlertButtonYes)
    else:
        try:
            a = wait(imgs.mainMenuButtonGo, 30)
            a = True
        except:
            a = False

    if not a:
        logger.info(u'found KanColle error')

        refresh()

    logger.info(u'done KanColle error checking')


@el.daemon(30, 3L)
def checkLongTrip():
    logger.info(u'checking long trip')

    a = exists(imgs.mainMenuLabelLongTripDone)
    b = exists(imgs.longTripScreenSucceed)
    c = exists(imgs.longTripScreenFailed)
    d = exists(imgs.longTripScreenButtonNext)
    a = a or b or c or d

    if a:
        logger.info(u'a long trip has been done')

        click(a)
        a = wait(imgs.longTripScreenSucceed, 20)
        click(a)
        wait(3)
        click(a)
        wait(imgs.mainMenuButtonGo, 30)

    logger.info(u'done long trip checking')


@el.daemon(30)
def preventSleep():
    logger.info(u'start prevent sleep')

    a = Env.getMouseLocation()
    hover(a.above(100))
    hover(a)

    logger.info(u'prevent sleep done')


@el.daemon(30)
def failMonitor():
    logger.info(u'start fail monitor')

    # go to main menu
    a = find(imgs.submenuButtonBack)
    click(a)
    # move cursor out to prevent help text popup
    a = a.getTarget().left(100)
    hover(a)
    # ensure it is in main menu, i.e. initial state
    wait(imgs.mainMenuButtonGo, 20)

    logger.info(u'fail monitor done')


@el.daemon(60)
def repair():
    logger.info(u'start repair checking')

    a = exists(imgs.mainMenuButtonRepair)
    if not a:
        logger.info(u'done repair checking')
        return
    click(a)
    wait(imgs.dockMenuLabel, 20)

    # loop every empty slot in the dock
    while True:
        try:
            # click an empty slot
            a = wait(imgs.dockButtonEmptySlot, 20)
            click(a)

            # locate girl table
            a = wait(imgs.dockTableHeader, 20)
            # height / 2 of table header
            thGap = 10
            # height / 2 of table row
            trGap = 15
            # move to the first row
            a = a.getTarget().below(thGap + trGap)

            # find the first non-repairing girl by seeking repairing icon
            # creates search area
            r = Region(a.getX() - 1, a.getY() - trGap + 1, 1, trGap * 2 + 2).right()
            while True:
                # search repairing icon in this area
                a = r.exists(imgs.dockTableLabelRepairing)
                if a:
                    # move to next row
                    r = r.offset(Location(0, trGap * 2))
                else:
                    break
            # get click location
            a = r.getTopLeft().below(trGap)

            # click target girl
            click(a)
            # start repair
            a = wait(imgs.dockSubmenuStartRepair, 20)
            click(a)
            # confirm
            a = wait(imgs.dockScreenConfirmRepairYes, 20)
            click(a)

            # sometimes empty slot will not update immediately
            # so wait here to avoid clicking an invalid slot
            wait(5)
        except:
            logger.warn(u'an error occured, stop searching')
            break
    # go to main menu
    a = find(imgs.submenuButtonBack)
    click(a)
    # move cursor out to prevent help text popup
    a = a.getTarget().left(100)
    hover(a)
    # ensure it is in main menu, i.e. initial state
    wait(imgs.mainMenuButtonGo, 20)

    logger.info(u'done repair checking')


@el.daemon(21 * 60)
def farmSteel():
    m = exists(imgs.mainMenuButtonReload)
    if not m:
        return
    click(m)
    wait(imgs.selectMenuLabel)
    m = find(imgs.selectMenuSecondTeam)
    click(m)
    click(m.getTarget().left(55))
    m = exists(imgs.selectMenuButtonReload)
    if m:
        # this team has not been reloaded
        click(m)
        wait(3)
    m = find(imgs.submenuButtonBack)
    click(m)
    hover(m.getTarget().left(100))

    m = wait(imgs.mainMenuButtonGo, 20)
    click(m)
    m = wait(imgs.goMenuButtonLongTrip, 20)
    click(m)
    click(imgs.longTripMenuMission3)
    click(imgs.longTripMenuButtonOk)
    click(imgs.selectMenuSecondTeam)
    click(imgs.longTripMenuButtonConfirm)
    m = find(imgs.submenuButtonBack)
    click(m)
    hover(m.getTarget().left(100))


dismissDMMError()
dismissKanColleError()
checkLongTrip()
failMonitor()
preventSleep()
repair()
farmSteel()
