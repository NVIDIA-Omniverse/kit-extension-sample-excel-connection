# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import omni.ext
import omni.ui as ui
import omni.usd
import carb
import usd
from pxr import Tf
from pxr import Usd, Sdf, UsdShade

import re

# In order to work with com you will need to import pywin32
import omni.kit.pipapi

omni.kit.pipapi.install("pywin32")

# you also need to set the following environment variables to install pywin32
import os
import sys
from pathlib import Path
import pythonwin.pywin

dlls_path = Path(pythonwin.pywin.__file__).parent.parent.parent / "pywin32_system32"
com = Path(pythonwin.pywin.__file__).parent.parent.parent / "win32"
lib = Path(pythonwin.pywin.__file__).parent.parent.parent / "win32" / "lib"
pywin = Path(pythonwin.pywin.__file__).parent.parent.parent / "pythonwin"
carb.log_info(dlls_path)
sys.path.insert(0, str(com))
sys.path.insert(0, str(lib))
sys.path.insert(0, str(pywin))
carb.log_info(sys.path)
os.environ["PATH"] = f"{dlls_path};{os.environ['PATH']}"
carb.log_info(os.environ["PATH"])
# End of pywin32 installation.

# win32com.client lets you work with com libraries
import win32com.client

# This class mirrors the events in the com dll you would like to subscribe to
class WorksheetEvents:

    _excel_worksheet = None

    def OnChange(self, *args):
        #1. check if changed cell is one we are tracking
        try:
            address_pattern = r'\$[DE]\$[3456]'
            address = str(args[0].Address)
            if not re.match(address_pattern, address):
                return
        except Exception as e:
            carb.log_error('Could not detect cell changes' + e)

        # 2. get prim path from excel
        prim_path_cell_address = r"C" + address[3]
        prim_path = WorksheetEvents._excel_worksheet.Range(prim_path_cell_address).Value
        
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath(prim_path)

        if not prim.IsValid():
            carb.log_error("Can't find prim at path")
            return

        # 3. move prim to new coordinates        
        new_value = WorksheetEvents._excel_worksheet.Range(address).Value

        translate = prim.GetAttribute("xformOp:translate").Get()
        if (address[1] == "D"):
            translate[0] = new_value
        else:
            translate[1] = new_value
        
        prim.GetAttribute("xformOp:translate").Set(translate)

class OmniSampleExcel_connectionExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[omni.sample.excel_connection] omni sample excel_connection startup")

        self._window = ui.Window("Excel Connection", width=600, height=200)

        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-msexcel\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    def on_Connect_Click(self):

        # Link to Excel
        self._excel_app = win32com.client.DispatchEx("excel.application")
        self._excel_app.Visible = True

        # Open workbook
        self._excel_workbook = self._excel_app.Workbooks.Open(self._sheet_path.as_string)
        
        try:
            if hasattr(self._excel_workbook, 'Worksheets'):
                self._excel_worksheet = self._excel_workbook.Worksheets(1)
            else:
                self._excel_worksheet = self._excel_workbook._dispobj_.Worksheets(1)
        except:
            carb.log_info("Could not find Worksheets attribute")
            return

        WorksheetEvents._excel_worksheet = self._excel_worksheet
        self._excel_events = win32com.client.WithEvents(self._excel_worksheet, WorksheetEvents)
        
        # Link to Scene
        self._stage = omni.usd.get_context().get_stage()
        
        watcher = omni.usd.get_watcher()

        self.prim_1 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C3').Value)        
        if self.prim_1.IsValid():
            translate_attr = self.prim_1.GetAttribute("xformOp:translate")
            self.watcher1 = watcher.subscribe_to_change_info_path(translate_attr.GetPath(), self._translate_changed)
        
        self.prim_2 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C4').Value)
        if self.prim_2.IsValid():
            translate_attr = self.prim_2.GetAttribute("xformOp:translate")
            self.watcher2 = watcher.subscribe_to_change_info_path(translate_attr.GetPath(), self._translate_changed)

        self.prim_3 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C5').Value)        
        if self.prim_3.IsValid():
            translate_attr = self.prim_3.GetAttribute("xformOp:translate")
            self.watcher3 = watcher.subscribe_to_change_info_path(translate_attr.GetPath(), self._translate_changed)
        
        self.prim_4 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C6').Value)
        if self.prim_4.IsValid():
            translate_attr = self.prim_4.GetAttribute("xformOp:translate")
            self.watcher4 = watcher.subscribe_to_change_info_path(translate_attr.GetPath(), self._translate_changed)

    def on_Disconnect_Click(self):
        # Share in livestream
        self._excel_events = None
        self._excel_worksheet = None

        if hasattr(self, '_excel_workbook'):
            if self._excel_workbook is not None:
                self._excel_workbook.Close(False)
                self._excel_workbook = None

        if hasattr(self, '_excel_app'):
            if self._excel_app is not None:
                self._excel_app.Application.Quit()
                self._excel_app = None

    def _translate_changed(self, *args):
        # 1. Check if the translation in excel is different
        translate_attribute = self._stage.GetAttributeAtPath(args[0])
        translate = translate_attribute.Get()
        prim_path = translate_attribute.GetPrimPath()

        next_address = ""
        row = 3
        found = False
        for row in range(3, 7):
            next_address = "C" + str(row)
            next_path = self._excel_worksheet.Range(next_address).Value
            if next_path == prim_path:
                found = True
                break
        
        if not found:
            carb.log_info("prim not found in excel worksheet")
            return

        x_address = "D" + str(row)
        excel_x = self._excel_worksheet.Range(x_address).Value

        y_address = "E" + str(row)
        excel_y = self._excel_worksheet.Range(y_address).Value

        # No change in value
        if excel_x == translate[0] and excel_y == translate[1]:
            return

        # 2. If so change it.
        self._excel_worksheet.Range(x_address).Value = translate[0]
        self._excel_worksheet.Range(y_address).Value = translate[1]

    def on_shutdown(self):

        # Share in livestream
        self._excel_events = None
        self._excel_worksheet = None

        if hasattr(self, '_excel_workbook'):
            if self._excel_workbook is not None:
                self._excel_workbook.Close(False)
                self._excel_workbook = None

        if hasattr(self, '_excel_app'):
            if self._excel_app is not None:
                self._excel_app.Application.Quit()
                self._excel_app = None

        print("[omni.sample.excel_connection] omni sample excel_connection startup")
