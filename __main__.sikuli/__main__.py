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


import ticks
import ui
import util


class Action(object):

    def __init__(self, daemon=True):
        self._logger = util.Logger()
        self._imgs = ui.Library()
        self._el = ticks.EventLoop() if daemon else None


    def exec_(self):
        if self._el:
            self._el.exec_()


    def every(self, sec, cb, priority=0L):
        if self._el:
            self._el.every(sec, cb, priority)


    def refresh(self):
        a = find(self._imgs.outButton)
        a = a.left(200)
        click(a)
        type(Key.F5)
        a = wait(self._imgs.systemButtonStart, 30)
        wait(5)
        click(a)
        wait(self._imgs.mainMenuButtonGo, 30)


    def reloadTeam(self, teamID):
        m = exists(self._imgs.mainMenuButtonReload)
        if not m:
            return
        click(m)
        wait(self._imgs.selectMenuLabel)
        m = find(self._imgs.selectMenuTeam(teamID))
        click(m)
        offset = {
            2: 55,
            3: 85,
            4: 115,
        }
        click(m.getTarget().left(offset[teamID]))
        m = exists(self._imgs.selectMenuButtonReload)
        if m:
            # this team has not been reloaded
            click(m)
            wait(3)
        m = find(self._imgs.submenuButtonBack)
        click(m)
        hover(m.getTarget().left(100))


    def startLongTrip(self, teamID, missionID):
        m = wait(self._imgs.mainMenuButtonGo, 20)
        click(m)
        m = wait(self._imgs.goMenuButtonLongTrip, 20)
        click(m)
        wait(2)
        stage, mission = self._imgs.longTripMenu(missionID)
        if stage:
            click(stage)
        click(mission)
        click(self._imgs.longTripMenuButtonOk)
        wait(2)
        click(self._imgs.selectMenuTeam(teamID))
        click(self._imgs.longTripMenuButtonConfirm)
        m = find(self._imgs.submenuButtonBack)
        click(m)
        hover(m.getTarget().left(100))


    def farm(self, teamID, missionID):
        self._logger.info('team %d begin mission %d' % (teamID, missionID))
        self.reloadTeam(teamID)
        self.startLongTrip(teamID, missionID)
        self._logger.info('team %d end mission %d' % (teamID, missionID))


    def dismissDMMError(self):
        if exists(self._imgs.browserAlert):
            self._logger.warn(u'found DMM error')

            click(self._imgs.browserAlertButtonCancel)


    def dismissKanColleError(self):
        a = exists(self._imgs.systemScreenError)
        b = exists(self._imgs.flashAlert)
        if a:
            a = False
        elif b:
            a = False
            click(self._imgs.flashAlertButtonYes)
        else:
            try:
                a = wait(self._imgs.mainMenuButtonGo, 30)
                a = True
            except:
                a = False

        if not a:
            self._logger.warn(u'found KanColle error')

            refresh()


    def checkLongTrip(self):
        a = exists(self._imgs.mainMenuLabelLongTripDone)
        b = exists(self._imgs.longTripScreenSucceed)
        c = exists(self._imgs.longTripScreenFailed)
        d = exists(self._imgs.longTripScreenButtonNext)
        a = a or b or c or d

        if a:
            self._logger.info(u'a long trip has been done')

            click(a)
            a = wait(self._imgs.longTripScreenSucceed, 20)
            click(a)
            wait(3)
            click(a)
            wait(self._imgs.mainMenuButtonGo, 30)


    def preventSleep(self):
        a = Env.getMouseLocation()
        hover(a.above(100))
        hover(a)


    def failMonitor(self):
        # go to main menu
        a = find(self._imgs.submenuButtonBack)
        click(a)
        # move cursor out to prevent help text popup
        a = a.getTarget().left(100)
        hover(a)
        # ensure it is in main menu, i.e. initial state
        wait(self._imgs.mainMenuButtonGo, 20)


    def repair(self):
        a = exists(self._imgs.mainMenuButtonRepair)
        if not a:
            return
        click(a)
        wait(self._imgs.dockMenuLabel, 20)

        # loop every empty slot in the dock
        while True:
            try:
                # click an empty slot
                a = wait(self._imgs.dockButtonEmptySlot, 20)
                click(a)

                # locate girl table
                a = wait(self._imgs.dockTableHeader, 20)
                # height / 2 of table header
                thGap = 10
                # height / 2 of table row
                trGap = 15
                # move to the first row
                a = a.getTarget().below(thGap + trGap)

                # find the first non-repairing girl by seeking repairing icon
                # creates search area
                r = Region(a.getX() - 1, a.getY() - trGap + 2, 1, trGap * 2 + 4).right()
                while True:
                    # search repairing icon in this area
                    a = r.exists(self._imgs.dockTableLabelRepairing)
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
                a = wait(self._imgs.dockSubmenuStartRepair, 20)
                click(a)
                # confirm
                a = wait(self._imgs.dockScreenConfirmRepairYes, 20)
                click(a)

                # sometimes empty slot will not update immediately
                # so wait here to avoid clicking an invalid slot
                wait(5)
            except:
                self._logger.warn(u'an error occured, stop searching')
                break
        # go to main menu
        a = find(self._imgs.submenuButtonBack)
        click(a)
        # move cursor out to prevent help text popup
        a = a.getTarget().left(100)
        hover(a)
        # ensure it is in main menu, i.e. initial state
        wait(self._imgs.mainMenuButtonGo, 20)


a = Action()

a.every(30, a.dismissDMMError, 5L)
a.every(30, a.dismissKanColleError, 4L)
a.every(30, a.checkLongTrip, 3L)
a.every(30, a.failMonitor)
a.every(30, a.preventSleep)

a.every(60, a.repair)

#a.every(21 * 60, lambda: a.farm(teamID=2, missionID=3))
#a.every(121 * 60, lambda: a.farm(teamID=4, missionID=20))
a.every(41 * 60, lambda: a.farm(teamID=4, missionID=17))
a.every(91 * 60, lambda: a.farm(teamID=3, missionID=5))
#a.every(41 * 60, lambda: a.farm(teamID=4, missionID=6))
a.every(241 * 60, lambda: a.farm(teamID=2, missionID=9))
#a.every(31 * 60, lambda: a.farm(teamID=4, missionID=2))

a.exec_()
