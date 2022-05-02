# voltage_measure_python
Measuring a voltage input with python (and RaspberryPi4), plotting voltage measure data actively with pyqtgraph in a GUI.


As I'm new to Python and spent a lot of time figuring out how to create a GUI and a program in general for a voltage measuring app for my thesis in mechanical engineering I now want to present my solution for anyone, that might have similar struggles:

I created the raw GUI in Qt Designer and converted it to Python code with PySide2. You can call the Designer by typing "designer" in your python console. You can watch the console instructions how to translate the generated .ui-file for the GUI to a .py-file in the file "console_converter_instruction.py" in this GitHub project.

It is important to set the reference to the module you wrote your widget (the live plot in this case) in Qt Designer. In the designer I added "Widget" to the GUI from the "Containers" section. Right click the widget, add reference/place holder and type in the class name of your widget class (here: "VoltagePlot"), as well as the header-file (include file) which is yourt self written module/file "real_time_plot_arduino_widget.py" in this case. (you can find a screenhot in German language for how I connected the referenced code snippet to the widget in the designer.

The file "real_time_plot_arduino_widget.py" is changed to make a widget from a MainWindow code for the live data plot. The widget can then be embedded in the main GUI "Jenike_Scherzelle_GUI.py". The structure of the main GUI is saved in the Qt Designer generated file "Jenike_Scherzelle_GUI.py" and called by the main code "main_Messprogramm.py". Please see the changes that have to be made to change the live plot MainWindow to an embeddable widget in another GUI in the code.

I hope that if you struggled with the same problem, this project might save you some time.

Like I said I'm still pretty new to Python, so if you find some interesting better solutions to set this up, I'd be very glad if you leave a comment or something, as I'm very interested what improvements are possible here :)

In this GUI there are no actions connected to the buttons yet, but I think that one is more trivial than the actual live data plot and embedding it into a GUI.
