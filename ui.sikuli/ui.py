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
        self._out_button = "out_button.png"
        self._system_screen_error = "system_screen_error.png"
        self._system_button_start = "system_button_start.png"
        
        self._main_menu_button_go = "main_menu_button_go.png"
        self._main_menu_button_repair = "main_menu_button_repair.png"
        self._main_menu_button_reload = "main_menu_button_reload.png"
        self._main_menu_label_long_trip_done = "main_menu_label_long_trip_done.png"
        self._submenu_button_back = "submenu_button_back.png"
        self._long_trip_screen_succeed = "long_trip_screen_succeed.png"
        self._long_trip_screen_failed = "long_trip_screen_failed.png"
        self._long_trip_screen_button_next = "long_trip_screen_button_next.png"
        self._go_menu_button_long_trip = "go_menu_button_long_trip.png"
        self._long_trip_menu_button_ok = "long_trip_menu_button_ok.png"
        self._long_trip_menu_button_confirm = "long_trip_menu_button_confirm.png"
        self._long_trip_menu_mission_2 = "long_trip_menu_mission_2.png"
        self._long_trip_menu_mission_3 = "long_trip_menu_mission_3.png"
        self._long_trip_menu_mission_5 = "long_trip_menu_mission_5.png"
        self._long_trip_menu_mission_6 = "long_trip_menu_mission_6.png"
        self._long_trip_menu_mission_9 = "long_trip_menu_mission_9.png"
        self._long_trip_menu_mission_17 = "long_trip_menu_mission_17.png"
        self._long_trip_menu_mission_20 = "long_trip_menu_mission_20.png"
        self._long_trip_menu_stage_2 = "long_trip_menu_stage_2.png"
        self._long_trip_menu_stage_3 = "long_trip_menu_stage.png"
        self._select_menu_label = "select_menu_label.png"
        self._select_menu_second_team = "select_menu_second_team.png"
        self._select_menu_third_team = "select_menu_third_team.png"
        self._select_menu_forth_team = "select_menu_forth_team.png"
        self._select_menu_button_reload = "select_menu_button_reload.png"
        self._dock_menu_label = "dock_menu_label.png"
        self._dock_button_empty_slot = "dock_button_empty_slot.png"
        self._dock_table_header = "dock_table_header.png"
        self._dock_table_label_repairing = "dock_table_label_repairing.png"
        self._dock_submenu_start_repair = "dock_submenu_start_repair.png"
        self._dock_screen_confirm_repair_yes = "dock_screen_confirm_repair_yes.png"

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
        return self._out_button

    @property
    def systemScreenError(self):
        return self._system_screen_error
    
    @property
    def systemButtonStart(self):
        return self._system_button_start
    
    @property
    def mainMenuButtonGo(self):
        return self._main_menu_button_go
    
    @property
    def mainMenuButtonRepair(self):
        return self._main_menu_button_repair

    @property
    def mainMenuButtonReload(self):
        return self._main_menu_button_reload
    
    @property
    def mainMenuLabelLongTripDone(self):
        return self._main_menu_label_long_trip_done
    
    @property
    def submenuButtonBack(self):
        return self._submenu_button_back
    
    @property
    def longTripScreenSucceed(self):
        return self._long_trip_screen_succeed
    
    @property
    def longTripScreenFailed(self):
        return self._long_trip_screen_failed
    
    @property
    def longTripScreenButtonNext(self):
        return self._long_trip_screen_button_next

    @property
    def goMenuButtonLongTrip(self):
        return self._go_menu_button_long_trip

    @property
    def longTripMenuButtonOk(self):
        return self._long_trip_menu_button_ok

    @property
    def longTripMenuButtonConfirm(self):
        return self._long_trip_menu_button_confirm

    @property
    def longTripMenuMission2(self):
        return self._long_trip_menu_mission_2

    @property
    def longTripMenuMission3(self):
        return self._long_trip_menu_mission_3

    @property
    def longTripMenuMission5(self):
        return self._long_trip_menu_mission_5

    @property
    def longTripMenuMission6(self):
        return self._long_trip_menu_mission_6

    @property
    def longTripMenuMission9(self):
        return self._long_trip_menu_mission_9

    @property
    def longTripMenuMission17(self):
        return self._long_trip_menu_mission_17

    @property
    def longTripMenuMission20(self):
        return self._long_trip_menu_mission_20

    @property
    def longTripMenuStage2(self):
        return self._long_trip_menu_stage_2

    @property
    def longTripMenuStage3(self):
        return self._long_trip_menu_stage_3

    @property
    def selectMenuLabel(self):
        return self._select_menu_label

    @property
    def selectMenuSecondTeam(self):
        return self._select_menu_second_team

    @property
    def selectMenuThirdTeam(self):
        return self._select_menu_third_team

    @property
    def selectMenuForthTeam(self):
        return self._select_menu_forth_team

    @property
    def selectMenuButtonReload(self):
        return self._select_menu_button_reload
    
    @property
    def dockMenuLabel(self):
        return self._dock_menu_label
    
    @property
    def dockButtonEmptySlot(self):
        return self._dock_button_empty_slot
    
    @property
    def dockTableHeader(self):
        return self._dock_table_header
    
    @property
    def dockTableLabelRepairing(self):
        return self._dock_table_label_repairing
    
    @property
    def dockSubmenuStartRepair(self):
        return self._dock_submenu_start_repair
    
    @property
    def dockScreenConfirmRepairYes(self):
        return self._dock_screen_confirm_repair_yes
