# voltage_measure_python
Measuring a voltage input with python and RaspberryPi4, plotting voltage measure data actively with pyqtgraph in a GUI. Please note: you have to get analog data by an arduino or something similar or at least simulate some data for plotting to make the code running. I used a Raspberry Pi 4 with a MCP3008 analog to digital converter to directly recieve data from an analog voltage input on the raspberry pi.

As I'm new to Python and spent a lot of time figuring out how to create a GUI and a program in general for a voltage measuring app for my thesis in mechanical engineering I now want to present my solution for anyone, that might have similar struggles:

I created the different GUIs in Qt Designer and converted it to Python code with PySide2. You can call the Designer by typing "designer" in your python console. You can watch the console instructions how to translate the generated .ui-file for the GUI to a .py-file in the file "console_converter_instruction.py" in this GitHub project.

It is important to set the reference to the module you wrote your widget (the live plot in this case) in Qt Designer. In the designer I added "Widget" to the GUI from the "Containers" section. Right click the widget, add reference/place holder and type in the class name of your widget class (here: "VoltagePlot"), as well as the header-file (include file) which is yourt self written module/file "real_time_plot_arduino_widget.py" in this case. (you can find a screenhot in German language and some previous different named files in the repository files for how I connected the referenced code snippet to the widget in the designer).

The file "real_time_plot_widget.py" is changed to make a widget from a MainWindow code for the live data plot (there is a link for the original code I used in that section). The widget can then be embedded in the main GUI "Jenike_Scherzelle_GUI.py". The structure of the main GUI is saved in the Qt Designer generated file "Jenike_Scherzelle_GUI_main.py" and called by the main code "main_Messprogramm.py". Please see the changes that have to be made to change the live plot MainWindow to an embeddable widget while comparing the linked original code and the changed widget code in this project.

I hope that if you struggled with the same problem, this project might save you some time.

Like I said I'm still pretty new to Python, so if you find some interesting better solutions to set this up, I'd be very glad if you leave a comment or so, as I'm very interested what improvements are possible here :)

To make the GUI running fluently while executing all the different tasks at once, I had to make use of PyQt's "QThread" classes. Thanks to those, the GUI can run everything at the same time without freezing to wait for every single task to end and step to the next one. Using multiple threads is indispensable here.

Any other details are hopefully mostly easy to understand by the comments in the codes.

Used modules/apps for writing/executing the app:

pyqt5==5.12.3
spyder==5.1.5
pqtgraph
numpy
pyserial (imported with serial)
matplotlib
+ self created GUIs as well as the self created live plot widget
datetime
xlsxwriter
