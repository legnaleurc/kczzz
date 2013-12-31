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


class Library(object):

    def __init__(self):
        self._browser_alert = "browser_alert.png"
        self._browser_alert_button_cancel = "browser_alert_button_cancel.png"
        self._flash_alert = "flash_alert.png"
        self._flash_alert_button_yes = "flash_alert_button_yes.png"

        self._long_trip_menu_mission = {
            2: "long_trip_menu_mission_2.png",
            3: "long_trip_menu_mission_3.png",
            5: "long_trip_menu_mission_5.png",
            6: "long_trip_menu_mission_6.png",
            9: "long_trip_menu_mission_9.png",
            17: "long_trip_menu_mission_17.png",
            20: "long_trip_menu_mission_20.png",
        }
        self._long_trip_menu_stage = {
            2: "long_trip_menu_stage_2.png",
            3: "long_trip_menu_stage_3.png",
        }

        self._select_menu_team = {
            2: "select_menu_second_team.png",
            3: "select_menu_third_team.png",
            4: "select_menu_forth_team.png",
        }

    @property
    def browserAlert(self):
        return self._browser_alert

    @property
    def browserAlertButtonCancel(self):
        return self._browser_alert_button_cancel

    @property
    def flashAlert(self):
        return self._flash_alert

    @property
    def flashAlertButtonYes(self):
        return self._flash_alert_button_yes

    @property
    def outButton(self):
        return "out_button.png"

    @property
    def systemScreenError(self):
        return "system_screen_error.png"

    @property
    def systemButtonStart(self):
        return "system_button_start.png"

    @property
    def mainMenuButtonGo(self):
        return "main_menu_button_go.png"

    @property
    def mainMenuButtonRepair(self):
        return "main_menu_button_repair.png"

    @property
    def mainMenuButtonReload(self):
        return "main_menu_button_reload.png"

    @property
    def mainMenuLabelLongTripDone(self):
        return "main_menu_label_long_trip_done.png"

    @property
    def submenuButtonBack(self):
        return "submenu_button_back.png"

    @property
    def longTripScreenSucceed(self):
        return "long_trip_screen_succeed.png"

    @property
    def longTripScreenFailed(self):
        return "long_trip_screen_failed.png"

    @property
    def longTripScreenButtonNext(self):
        return "long_trip_screen_button_next.png"

    @property
    def goMenuButtonLongTrip(self):
        return "go_menu_button_long_trip.png"

    @property
    def longTripMenuButtonOk(self):
        return "long_trip_menu_button_ok.png"

    @property
    def longTripMenuButtonConfirm(self):
        return "long_trip_menu_button_confirm.png"

    def longTripMenuMission(self, id_):
        return self._long_trip_menu_mission[id_]

    def longTripMenuStage(self, id_):
        return self._long_trip_menu_stage[id_]

    def longTripMenu(self, id_):
        stage = None
        if id_ >= 9 and id_ <= 16:
            stage = 2
        elif id_ >= 17 and id_ <= 20:
            stage = 3
        mission = self.longTripMenuMission(id_)
        if stage:
            stage = self.longTripMenuStage(stage)
        return stage, mission

    @property
    def selectMenuLabel(self):
        return "select_menu_label.png"

    def selectMenuTeam(self, id_):
        return self._select_menu_team[id_]

    @property
    def selectMenuButtonReload(self):
        return "select_menu_button_reload.png"

    @property
    def dockMenuLabel(self):
        return "dock_menu_label.png"

    @property
    def dockButtonEmptySlot(self):
        return "dock_button_empty_slot.png"

    @property
    def dockTableHeader(self):
        return "dock_table_header.png"

    @property
    def dockTableLabelRepairing(self):
        return "dock_table_label_repairing.png"

    @property
    def dockSubmenuStartRepair(self):
        return "dock_submenu_start_repair.png"

    @property
    def dockScreenConfirmRepairYes(self):
        return "dock_screen_confirm_repair_yes.png"
