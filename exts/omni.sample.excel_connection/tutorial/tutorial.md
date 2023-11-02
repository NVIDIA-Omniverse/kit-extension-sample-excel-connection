
<div style="text-align: center;">
    <img src="Images/logo.png" alt="extension search path" width="200"/>
</div>

# Write an Extension that Connects Excel and Omniverse

Follow along with this tutorial to write your own extension that can transfer data back and forth between Microsoft Excel and NVIDIA Omniverse. This tutorial not only demonstrates how to connect Excel and Omniverse specifically, but also serves as a template you can use to connect to other COM applications such as other Microsoft Office Applications as well as CATIA V5. It can also serve as a starting point to connect to applications that have Python, .NET or other libraries available.

## Learning Objectives

- Use COM libraries from an Omniverse extension
- Listen for and respond to changes in Excel
- Update an Omniverse Scene
- Listen for and respond to changes in Omniverse
- Update an Excel spreadsheet

## prerequisites

- [Set up your environment](https://github.com/NVIDIA-Omniverse/ExtensionEnvironmentTutorial/blob/master/Tutorial.md#4-create-a-git-repository)
- Omniverse Kit 105.1.1 or higher

## Step 1: Code Starting Point

To get started, build a new extension from the extension template and open the `extension.py` file as demonstrated in [this video](https://www.youtube.com/watch?v=eGxV_PGNpOg).

From there, code in `extension.py` can be replaced with the code below which shows where to add snippets at each step: 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1

# Step 3.1

# Step 3.2

# Step 3.3

# Step 5.1

    # Step 6.5

    # Step 5.2

        # Step 6.2

        # Step 6.3

        # Step 6.4

class OmniSampleExcel_connectionExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[omni.sample.excel_connection] omni sample excel_connection startup")

        self._window = ui.Window("Excel Connection", width=600, height=200)

        # Step 2.1

    # Step 2.2

        # Step 4

        # Step 6.6
        
        # Step 7.1
        
        # Step 7.2

    # Step 2.2

        # Step 9

    # Step 7.3

        # Step 8.1
        
        # Step 8.2

    def on_shutdown(self):
        # Step 9
        pass
```
</details>

So far, the extension only contains comments that show where to add code at each step as well as the minimum code needed to launch an extension with a window. The `OmniSampleExcel_connectionExtension` class encapsulates the extension itself. The `on_startup` function runs when the extension is loaded. Currently, this function simply creates an empty window with `Excel Connection` as its title. 

This serves as a roadmap for the rest of the tutorial. At each step we will add code to the marked location. After each major step, such as `Step 2` you can build and launch the extension to see your progress. After each minor step, such as `Step 5.1`, the code may be missing necessary elements to run. 

## Step 2: Define The User Interface

Next we will build the user interface for the extension. 

### Step 2.1: Add the UI Elements to `on_startup`

The first step is to add the following code below the assignment of `self._window` in the `on_startup` function:

```Python
with self._window.frame:
    with ui.VStack():

        self._sheet_path = ui.SimpleStringModel(r"C:\Warehouse_BOM.xlsx")
        with ui.HStack(style={"margin": 5}, height=40):
            ui.Label("Spreadsheet Path:", width=50)
            ui.StringField(self._sheet_path, width=500)

        with ui.HStack(style={"margin": 5}, height=40):
            ui.Spacer()
            ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
            ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
            ui.Spacer()
```

Here is where most of the user interface is built. You will see that there is a vertical stack which contains two horizontal stacks. This creates two rows in the user interface, and each row has two columns. The first row has a string field where the user can enter a path to the Excel spreadsheet they would like to connect to Omniverse. The second row has buttons that can connect or disconnect the given spreadsheet.

### Step 2.2: Add the Button Clicked Functions

Each `ui.Button` has a `clicked_fn` argument passed into its constructor. This is the function that will run when the button is clicked. For now, let's simply define the functions and have them do nothing, so that our UI is complete and the extension will build. This can be done with the following code block:

```Python
def on_Connect_Click(self):
    # Step 4
    pass        

def on_Disconnect_Click(self):
    # Step 9
    pass
```

And so, with just a few lines of code the user interface for the Excel connector is complete. Next we will add the dependencies required to call the Excel API from within the extension. 

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1

# Step 3.1

# Step 3.2

# Step 3.3

# Step 5.1

    # Step 6.5

    # Step 5.2

        # Step 6.2

        # Step 6.3

        # Step 6.4

class OmniSampleExcel_connectionExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[omni.sample.excel_connection] omni sample excel_connection startup")

        self._window = ui.Window("Excel Connection", width=600, height=200)

        # Step 2.1
        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-excel-connection\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    # Step 2.2
    def on_Connect_Click(self):
        # Step 4

        # Step 6.6
        
        # Step 7.1
        
        # Step 7.2
        pass

    # Step 2.2
    def on_Disconnect_Click(self):
        # Step 9
        pass

    # Step 7.3

        # Step 8.1
        
        # Step 8.2

    def on_shutdown(self):
        # Step 9
        pass
```
</details>

## Step 3: Add the `Win32Com` Dependencies

Many applications have automation API libraries. These libraries come in a wide variety of languages and formats; this sample is helpful for any libraries that can be accessed from Python. If the libraries are Python libraries, which is common, this is very straightforward. .NET libraries are also very common. While not quite as simple to import as Python libraries, .NET libraries can be brought in by using the `Python.NET library`. COM libraries are a bit trickier to use, which is one reason they were chosen for this tutorial. Hopefully demonstrating how to use COM libraries will serve as a head start for those who want to use Python, .NET, COM or other technologies.

### Step 3.1: How to Import Pip Packages

If there is one code snippet to learn from this sample, this is it:
    
```Python
import omni.kit.pipapi
omni.kit.pipapi.install("pywin32")
```

This code snippet installs pip packages that are not distributed with Omniverse, opening up a wide range of possibilities. In this case it installs `pywin32`, a library that allows us to work with COM .dlls that are registered on the user's local machine.

> **_Note_**: First-time pip installation of `pywin32` sometimes fails from within the Omniverse environment. If this happens copy the attempted pip command from the console logs and run it in a command prompt.

### Step 3.2: Configure the `pywin32` Environment

The next step is less common when installing a package and probably will not be necessary unless you are working with COM APIs. In order to use the `win32com.client` library which is required to access COM APIs, a few environment variables must be set within the Omniverse environment. If you were to use `pywin32` in a local Python environment, you would first install the package and then run an installer that sets these environment variables. We cannot do this within the Omnviverse environment, so instead we essentially install the library into the environment by hand. In the case that you are working with COM libraries and thus `pywin32`, you can use the exact snippet included below:

```Python
# you also need to set the following environment variables to install pywin32
import os
import sys
import carb
from pathlib import Path
import Pythonwin.pywin

dlls_path = Path(Pythonwin.pywin.__file__).parent.parent.parent / "pywin32_system32"
com = Path(Pythonwin.pywin.__file__).parent.parent.parent / "win32"
lib = Path(Pythonwin.pywin.__file__).parent.parent.parent / "win32" / "lib"
pywin = Path(Pythonwin.pywin.__file__).parent.parent.parent / "Pythonwin"
carb.log_info(dlls_path)
sys.path.insert(0, str(com))
sys.path.insert(0, str(lib))
sys.path.insert(0, str(pywin))
carb.log_info(sys.path)
os.environ["PATH"] = f"{dlls_path};{os.environ['PATH']}"
carb.log_info(os.environ["PATH"])
# End of pywin32 installation.
```

### Step 3.3: Import `win32com.client`

Now that `pywin32` is completely installed, the next step is to import `win32com.client` which will give access to COM APIs. It is imported as follows:

```Python
# win32com.client lets you work with com libraries
import win32com.client
```

With that, all libraries needed to work with COM APIs have been installed. In the next step we will use this library to access the Excel application.

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1

# Step 3.1
# In order to work with com you will need to import pywin32
import omni.kit.pipapi
omni.kit.pipapi.install("pywin32")

# Step 3.2
# you also need to set the following environment variables to install pywin32
import os
import sys
import carb
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

# Step 3.3
# win32com.client lets you work with com libraries
import win32com.client

# Step 5.1

    # Step 6.5

    # Step 5.2

        # Step 6.2

        # Step 6.3

        # Step 6.4

class OmniSampleExcel_connectionExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[omni.sample.excel_connection] omni sample excel_connection startup")

        self._window = ui.Window("Excel Connection", width=600, height=200)

        # Step 2.1
        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-excel-connection\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    # Step 2.2
    def on_Connect_Click(self):
        # Step 4

        # Step 6.6
        
        # Step 7.1
        
        # Step 7.2
        pass

    # Step 2.2
    def on_Disconnect_Click(self):
        # Step 9
        pass

    # Step 7.3

        # Step 8.1
        
        # Step 8.2

    def on_shutdown(self):
        # Step 9
        pass
```
</details>


## Step 4: Connect to the Excel Application

The sample connects to Excel in the `on_Connect_Click` function using the following snippet:

```Python
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
```

If you have spent time automating Excel with VBA or .NET, this code might be familiar to you. That is because this snippet is calling the same functions from the same libraries! First it launches the Excel application; then it makes sure it is visible. Next, this snippet opens the workbook specified in the user interface. In the next step where a variable is assigned the value of the first worksheet in the worksheets collection, there is an `if` `else` statement with code that might be new to you. This statement checks if the worksheets property is where we would expect it to be; if not it looks for it under the `_dispobj_` property. There appears to be a bug in `win32com` that sometimes includes this extra layer in the class hierarchy and so the worksheets property can be found at either of these two paths.

Now that the extension can open the Excel spreadsheet, the next section will explain how to subscribe to changes from Excel.

> **_NOTE:_** COM libraries do not typically have Python documentation. In order to learn how to automate these applications, it is recommended you use their VBA documentation and adapt it to Python. The Excel VBA documentation can be found [here](https://learn.microsoft.com/en-us/office/vba/api/overview/excel). It can also be helpful to prototype functionality in the VBA environment and then adapte it to Python. The VBA Object browser is another tool that can help you identify API elements which can be accessed from an application's COM libraries.

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1

# Step 3.1
# In order to work with com you will need to import pywin32
import omni.kit.pipapi
omni.kit.pipapi.install("pywin32")

# Step 3.2
# you also need to set the following environment variables to install pywin32
import os
import sys
import carb
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

# Step 3.3
# win32com.client lets you work with com libraries
import win32com.client

# Step 5.1

    # Step 6.5

    # Step 5.2

        # Step 6.2

        # Step 6.3

        # Step 6.4

class OmniSampleExcel_connectionExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[omni.sample.excel_connection] omni sample excel_connection startup")

        self._window = ui.Window("Excel Connection", width=600, height=200)

        # Step 2.1
        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-excel-connection\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    # Step 2.2
    def on_Connect_Click(self):
        # Step 4
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

        # Step 6.6
        
        # Step 7.1
        
        # Step 7.2

    # Step 2.2
    def on_Disconnect_Click(self):
        # Step 9
        pass

    # Step 7.3

        # Step 8.1
        
        # Step 8.2

    def on_shutdown(self):
        # Step 9
        pass
```
</details>

## Step 5: Prepare to Subscribe to Changes from Excel

If you have done Excel automation with VBA, you have probably used the `Worksheet_Change` function to perform actions whenever a user edits a worksheet. We do the same thing in this sample in four steps. First, identify the class and event name you would like to subscribe to. In the case of Excel we can use the VBA object browser to do this. For this sample, we want to listen for changes to a worksheet. We find the `Worksheet` class and if you look there is a `Change` event as shown in the image below:

<center>
    <figure>
        <img src="Images/VBA_Object_Browser.png"
            alt="The worksheet changed event in the VBA object browser"
            style="width:400px">
        <figcaption>You can identify available events through the VBA object browser</figcaption>
    </figure>
</center>

### Step 5.1: Create The Event Subscription Class

We will make a class with the same name as the class we want to subscribe to plus the `Events` appended to it, in this case `WorksheetEvents`:

```Python
class WorksheetEvents:
```

### Step 5.2: Create The Event Subscription Function

Next we will add a function with the same name as the event in the VBA object browser, prepended with `On`. In this case that event is `OnChange`. The function will be an instance function, so it will have `self` as an argument, as well as a pointer to any arguments expected from the COM library as demonstrated here:

```Python
def OnChange(self, *args):
```

Put together, this is what the class looks like so far:

```Python
class WorksheetEvents:

    def OnChange(self, *args):
        pass
```

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1

# Step 3.1
# In order to work with com you will need to import pywin32
import omni.kit.pipapi
omni.kit.pipapi.install("pywin32")

# Step 3.2
# you also need to set the following environment variables to install pywin32
import os
import sys
import carb
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

# Step 3.3
# win32com.client lets you work with com libraries
import win32com.client

# Step 5.1
# This class mirrors the events in the com dll you would like to subscribe to
class WorksheetEvents:

    # Step 6.5

    # Step 5.2
    def OnChange(self, *args):

        # Step 6.2

        # Step 6.3

        # Step 6.4

class OmniSampleExcel_connectionExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[omni.sample.excel_connection] omni sample excel_connection startup")

        self._window = ui.Window("Excel Connection", width=600, height=200)

        # Step 2.1
        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-excel-connection\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    # Step 2.2
    def on_Connect_Click(self):
        # Step 4
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

        # Step 6.6
        
        # Step 7.1
        
        # Step 7.2

    # Step 2.2
    def on_Disconnect_Click(self):
        # Step 9
        pass

    # Step 7.3

        # Step 8.1
        
        # Step 8.2

    def on_shutdown(self):
        # Step 9
        pass
```
</details>

## Step 6: Respond to Changes from Excel

### Step 6.1

First, in this section we will be working with the Omniverse scene and we will use regular expressions to compare string. So, we will need to import the following libraries:

```Python
import omni.usd
import re
```

with those libraries imported, we will now perform the following steps in the OnChange function created in the last section: 

1. Check if the change happened in a cell that should be tracked
2. Get the prim
3. Move the prim

### Step 6.2: Check Change Address

The first step is to check whether the address of the changed cell is one we are tracking. This is done with the following snippet:

```Python
# check if changed cell is one we are tracking
try:
    address_pattern = r'\$[DE]\$[3456]'
    address = str(args[0].Address)
    if not re.match(address_pattern, address):
        return
except Exception as e:
    carb.log_error('Could not detect cell changes' + e)
```

In this snippet we create a regular expression that will match addresses of import and then check whether the changed address matches that pattern. If it does not match we do not continue any further. 

### Step 6.3: Get Prim

The second step is to find the prim path that has been effected by the change. This has been made easy in this sample by storing the prim's path in the spreadhseet to be retrieved later as follows:

```Python
# get prim path from Excel
prim_path_cell_address = r"C" + address[3]
prim_path = WorksheetEvents._excel_worksheet.Range(prim_path_cell_address).Value

stage = omni.usd.get_context().get_stage()
prim = stage.GetPrimAtPath(prim_path)

if not prim.IsValid():
    carb.log_error("Can't find prim at path")
    return
```

The row is taken from the event argment and appended to the column containing the prim path. Then, the value of that cell is read and that string is used within the Omniverse stage to retrieve the prim. It is important to check whether the prim is valid before continuing, because it is very easy to make a mistake when working with prim paths.

### Step 6.4: Move Prim

Finally, we will move the prim to its new location with this snippet:

```Python
# move prim to new coordinates        
new_value = WorksheetEvents._excel_worksheet.Range(address).Value

translate = prim.GetAttribute("xformOp:translate").Get()
if (address[1] == "D"):
    translate[0] = new_value
else:
    translate[1] = new_value

prim.GetAttribute("xformOp:translate").Set(translate)
```

First, read the new position from Excel, second read the current position from Omniverse, then assign the new value from Excel to the Omniverse Translation vector and finally, write the new translation vector back to Omniverse.

### Step 6.5

It should be noted that a class variable has been added to the `WorksheetEvents` class:

```Python
_excel_worksheet = None
```

### Step 6.6

This variable has been added so that the connected Excel spreadsheet can be accessed from within the event function. This variable is set in the `on_Connect_Click` function immediately before subscribing to the worksheet's `OnChanged` event:

```Python
WorksheetEvents._excel_worksheet = self._excel_worksheet
self._excel_events = win32com.client.WithEvents(self._excel_worksheet, WorksheetEvents)
```

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!HACK!!!!!!!!!!!!!!!!!!!!!!
### Combined two sections here, they need to be made into one

We then subscribe to that event in the `on_Connect_Click` function with the help of the `win32com.client` library:

```Python
self._excel_events = win32com.client.WithEvents(self._excel_worksheet, WorksheetEvents)
```

Now that we have subscribed to changes from the Excel spreadsheet, in the next section we will take action upon those changes.

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

This is a great point to pause and check your work. You should be able to launch the extension and if you change the position of a prim in Excel, the prim should move in Omniverse. In the next section we will subscribe to Omniverse changes so that we can get data flowing back in the other direction. 

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1
import omni.usd
import re

# Step 3.1
# In order to work with com you will need to import pywin32
import omni.kit.pipapi
omni.kit.pipapi.install("pywin32")

# Step 3.2
# you also need to set the following environment variables to install pywin32
import os
import sys
import carb
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

# Step 3.3
# win32com.client lets you work with com libraries
import win32com.client

# Step 5.1
# This class mirrors the events in the com dll you would like to subscribe to
class WorksheetEvents:

    # Step 6.5
    _excel_worksheet = None

    # Step 5.2
    def OnChange(self, *args):

        # Step 6.2
        # check if changed cell is one we are tracking
        try:
            address_pattern = r'\$[DE]\$[3456]'
            address = str(args[0].Address)
            if not re.match(address_pattern, address):
                return
        except Exception as e:
            carb.log_error('Could not detect cell changes' + e)

        # Step 6.3
        # get prim path from excel
        prim_path_cell_address = r"C" + address[3]
        prim_path = WorksheetEvents._excel_worksheet.Range(prim_path_cell_address).Value
        
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath(prim_path)

        if not prim.IsValid():
            carb.log_error("Can't find prim at path")
            return

        # Step 6.4
        # move prim to new coordinates        
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

        # Step 2.1
        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-excel-connection\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    # Step 2.2
    def on_Connect_Click(self):
        # Step 4
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

        # Step 6.6
        WorksheetEvents._excel_worksheet = self._excel_worksheet
        self._excel_events = win32com.client.WithEvents(self._excel_worksheet, WorksheetEvents)
        
        # Step 7.1
        
        # Step 7.2

    # Step 2.2
    def on_Disconnect_Click(self):
        # Step 9
        pass

    # Step 7.3

        # Step 8.1
        
        # Step 8.2

    def on_shutdown(self):
        # Step 9
        pass
```
</details>


## Step 7: Subscribe to Changes from Omniverse

### Step 7.1 
Working with Omniverse in Python is more straightforward than working with COM APIs in Python because Omniverse was designed to work with Python. In Omniverse we can deliberately subscribe to changes in a specific prim attribute as shown below:

```Python
self._stage = omni.usd.get_context().get_stage()

watcher = omni.usd.get_watcher()

self.prim_1 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C3').Value)        
if self.prim_1.IsValid():
    translate_attr = self.prim_1.GetAttribute("xformOp:translate")
    self.watcher1 = watcher.subscribe_to_change_info_path(
        translate_attr.GetPath(), 
        self._translate_changed
        )
```
        
In this snippet, the first prim listed in the Excel spreadsheet is retrieved. If the prim is valid, its translate attribute is assigned to a variable and then a watcher is set that listens for any changes to that attribute. This is then done for the other three pallets in the Excel spreadsheet:

### Step 7.2

```Python
self.prim_2 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C4').Value)
if self.prim_2.IsValid():
    translate_attr = self.prim_2.GetAttribute("xformOp:translate")
    self.watcher2 = watcher.subscribe_to_change_info_path(
        translate_attr.GetPath(), 
        self._translate_changed
        )

self.prim_3 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C5').Value)        
if self.prim_3.IsValid():
    translate_attr = self.prim_3.GetAttribute("xformOp:translate")
    self.watcher3 = watcher.subscribe_to_change_info_path(
        translate_attr.GetPath(), 
        self._translate_changed
        )

self.prim_4 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C6').Value)
if self.prim_4.IsValid():
    translate_attr = self.prim_4.GetAttribute("xformOp:translate")
    self.watcher4 = watcher.subscribe_to_change_info_path(
        translate_attr.GetPath(), 
        self._translate_changed
        )
```

### Step 7.3

Don't forget to create the `_translate_changed` function that is called when one of these prims is changed:

```Python
def _translate_changed(self, *args):
    pass
```

With the subscription made, the final step in the tutorial is to respond to changes that come from Omniverse and update Excel.

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1
import omni.usd
import re

# Step 3.1
# In order to work with com you will need to import pywin32
import omni.kit.pipapi
omni.kit.pipapi.install("pywin32")

# Step 3.2
# you also need to set the following environment variables to install pywin32
import os
import sys
import carb
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

# Step 3.3
# win32com.client lets you work with com libraries
import win32com.client

# Step 5.1
# This class mirrors the events in the com dll you would like to subscribe to
class WorksheetEvents:

    # Step 6.5
    _excel_worksheet = None

    # Step 5.2
    def OnChange(self, *args):

        # Step 6.2
        # check if changed cell is one we are tracking
        try:
            address_pattern = r'\$[DE]\$[3456]'
            address = str(args[0].Address)
            if not re.match(address_pattern, address):
                return
        except Exception as e:
            carb.log_error('Could not detect cell changes' + e)

        # Step 6.3
        # get prim path from excel
        prim_path_cell_address = r"C" + address[3]
        prim_path = WorksheetEvents._excel_worksheet.Range(prim_path_cell_address).Value
        
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath(prim_path)

        if not prim.IsValid():
            carb.log_error("Can't find prim at path")
            return

        # Step 6.4
        # move prim to new coordinates        
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

        # Step 2.1
        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-excel-connection\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    # Step 2.2
    def on_Connect_Click(self):
        # Step 4
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

        # Step 6.6
        WorksheetEvents._excel_worksheet = self._excel_worksheet
        self._excel_events = win32com.client.WithEvents(self._excel_worksheet, WorksheetEvents)
        
        # Step 7.1
        # Link to Scene
        self._stage = omni.usd.get_context().get_stage()
        
        watcher = omni.usd.get_watcher()

        self.prim_1 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C3').Value)        
        if self.prim_1.IsValid():
            translate_attr = self.prim_1.GetAttribute("xformOp:translate")
            self.watcher1 = watcher.subscribe_to_change_info_path(translate_attr.GetPath(), self._translate_changed)
        
        # Step 7.2
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

    # Step 2.2
    def on_Disconnect_Click(self):
        # Step 9
        pass

    # Step 7.3
    def _translate_changed(self, *args):
        # Step 8.1
        
        # Step 8.2
        pass

    def on_shutdown(self):
        # Step 9
        pass
```
</details>

## Step 8: Respond to Changes from Omniverse

Responding to changes from Omniverse is very similar to responding to changes from Excel, but has important differences:

1. Check if the translation value has changed
2. Update the values in Excel

### Step 8.1

It is critical with any bi-directional connection such as this that at some point you check whether values have actually changed. If you do not do this, the connector will enter an infinite loop. So, with that in mind here is the snippet that does this when the Omniverse scene is changed:

```Python
# Check if the translation in Excel is different
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
    carb.log_info("prim not found in Excel worksheet")
    return

x_address = "D" + str(row)
excel_x = self._excel_worksheet.Range(x_address).Value

y_address = "E" + str(row)
excel_y = self._excel_worksheet.Range(y_address).Value

# No change in value
if excel_x == translate[0] and excel_y == translate[1]:
    return
```

This code snippet first gets the translate value as well as the prim path from the attribute path passed into the event. Next, Excel is searched to find the row that matches the prim path. Once the correct row is found, the X and Y values are read from Excel. Finally, these values are compared with the current Omniverse values and if they are the same, the event handler returns.

### Step 8.2

If either of the values is different, the code continues with the following snippet:

```Python
    # If so change it.
    self._excel_worksheet.Range(x_address).Value = translate[0]
    self._excel_worksheet.Range(y_address).Value = translate[1]
```

This uses Excel's COM API to change the cell values of interest.

Saving the file at this point should launch the extension and let you see your progress. To view the full code up until this point, click to expand the item below. 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1
import omni.usd
import re

# Step 3.1
# In order to work with com you will need to import pywin32
import omni.kit.pipapi
omni.kit.pipapi.install("pywin32")

# Step 3.2
# you also need to set the following environment variables to install pywin32
import os
import sys
import carb
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

# Step 3.3
# win32com.client lets you work with com libraries
import win32com.client

# Step 5.1
# This class mirrors the events in the com dll you would like to subscribe to
class WorksheetEvents:

    # Step 6.5
    _excel_worksheet = None

    # Step 5.2
    def OnChange(self, *args):

        # Step 6.2
        # check if changed cell is one we are tracking
        try:
            address_pattern = r'\$[DE]\$[3456]'
            address = str(args[0].Address)
            if not re.match(address_pattern, address):
                return
        except Exception as e:
            carb.log_error('Could not detect cell changes' + e)

        # Step 6.3
        # get prim path from excel
        prim_path_cell_address = r"C" + address[3]
        prim_path = WorksheetEvents._excel_worksheet.Range(prim_path_cell_address).Value
        
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath(prim_path)

        if not prim.IsValid():
            carb.log_error("Can't find prim at path")
            return

        # Step 6.4
        # move prim to new coordinates        
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

        # Step 2.1
        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-excel-connection\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    # Step 2.2
    def on_Connect_Click(self):
        # Step 4
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

        # Step 6.6
        WorksheetEvents._excel_worksheet = self._excel_worksheet
        self._excel_events = win32com.client.WithEvents(self._excel_worksheet, WorksheetEvents)
        
        # Step 7.1
        # Link to Scene
        self._stage = omni.usd.get_context().get_stage()
        
        watcher = omni.usd.get_watcher()

        self.prim_1 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C3').Value)        
        if self.prim_1.IsValid():
            translate_attr = self.prim_1.GetAttribute("xformOp:translate")
            self.watcher1 = watcher.subscribe_to_change_info_path(translate_attr.GetPath(), self._translate_changed)
        
        # Step 7.2
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

    # Step 2.2
    def on_Disconnect_Click(self):
        # Step 9
        pass

    # Step 7.3
    def _translate_changed(self, *args):
        # Step 8.1
        # Check if the translation in excel is different
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

        # Step 8.2
        # If so change it.
        self._excel_worksheet.Range(x_address).Value = translate[0]
        self._excel_worksheet.Range(y_address).Value = translate[1]

    def on_shutdown(self):
        # Step 9
        pass
```
</details>

## Step 9: Disconnect from Excel

Finally, the extension must gracefully disconnect from excel, both when the users clicks the `disconnect` button and when the extension shuts down. To do this, add the following snippet to both the `on_Disconnect_Click` function and the on_shutdown function:

```Python
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
```

Saving the file at this point should launch the extension and let you use the completed extension. To view the full sample, click to expand the item below. 

<details>
    <summary>Click to Reveal Code</summary>
    
```Python
import omni.ext
import omni.ui as ui

# Step 6.1
import omni.usd
import re

# Step 3.1
# In order to work with com you will need to import pywin32
import omni.kit.pipapi
omni.kit.pipapi.install("pywin32")

# Step 3.2
# you also need to set the following environment variables to install pywin32
import os
import sys
import carb
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

# Step 3.3
# win32com.client lets you work with com libraries
import win32com.client

# Step 5.1
# This class mirrors the events in the com dll you would like to subscribe to
class WorksheetEvents:

    # Step 6.5
    _excel_worksheet = None

    # Step 5.2
    def OnChange(self, *args):

        # Step 6.2
        # check if changed cell is one we are tracking
        try:
            address_pattern = r'\$[DE]\$[3456]'
            address = str(args[0].Address)
            if not re.match(address_pattern, address):
                return
        except Exception as e:
            carb.log_error('Could not detect cell changes' + e)

        # Step 6.3
        # get prim path from excel
        prim_path_cell_address = r"C" + address[3]
        prim_path = WorksheetEvents._excel_worksheet.Range(prim_path_cell_address).Value
        
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath(prim_path)

        if not prim.IsValid():
            carb.log_error("Can't find prim at path")
            return

        # Step 6.4
        # move prim to new coordinates        
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

        # Step 2.1
        with self._window.frame:
            with ui.VStack():

                self._sheet_path = ui.SimpleStringModel(r"C:\projects\kit-extension-sample-excel-connection\Assets\Warehouse_BOM.xlsx")
                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Label("Spreadsheet Path:", width=50)
                    ui.StringField(self._sheet_path, width=500)

                with ui.HStack(style={"margin": 5}, height=40):
                    ui.Spacer()
                    ui.Button("Connect", clicked_fn=self.on_Connect_Click, width=300)
                    ui.Button("Disconnect", clicked_fn=self.on_Disconnect_Click, width=300)
                    ui.Spacer()

    # Step 2.2
    def on_Connect_Click(self):
        # Step 4
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

        # Step 6.6
        WorksheetEvents._excel_worksheet = self._excel_worksheet
        self._excel_events = win32com.client.WithEvents(self._excel_worksheet, WorksheetEvents)
        
        # Step 7.1
        # Link to Scene
        self._stage = omni.usd.get_context().get_stage()
        
        watcher = omni.usd.get_watcher()

        self.prim_1 = self._stage.GetPrimAtPath(self._excel_worksheet.Range('C3').Value)        
        if self.prim_1.IsValid():
            translate_attr = self.prim_1.GetAttribute("xformOp:translate")
            self.watcher1 = watcher.subscribe_to_change_info_path(translate_attr.GetPath(), self._translate_changed)
        
        # Step 7.2
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

    # Step 2.2
    def on_Disconnect_Click(self):
        # Step 9
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

    # Step 7.3
    def _translate_changed(self, *args):
        # Step 8.1
        # Check if the translation in excel is different
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

        # Step 8.2
        # If so change it.
        self._excel_worksheet.Range(x_address).Value = translate[0]
        self._excel_worksheet.Range(y_address).Value = translate[1]

    def on_shutdown(self):
        # Step 9
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
```
</details>

## Conclusion

This sample and tutorial demonstrates how to connect an Excel spreadsheet to NVIDIA Omniverse through a Python extension. It has done this through COM libraries, but the general approach can be applied to many apps and technologies.
