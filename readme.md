# README

This project has dependencies

* python 3.9.0
* PySide6
* openpyxl
* numpy
* matplotlib
* requests
* brain-isotopic-distribution
* scipy

You must have Python installed before downloading and using this software, Python could be install from [https://www.python.org/downloads/release/python-390/](https://www.python.org/downloads/release/python-390/)
## Run from binary distribution
Download the zipped binary distributions corresponding to the OS Platform that the users are using from the [https://github.com/RaoboXu/Lipidwizard/releases/](https://github.com/RaoboXu/Lipidwizard/releases/)

Unzip the downloaded package

Launch the softeware
* For Windows users, double click the LipidWizard.exe
* For Ubuntu Users, double click the LipidWizard
* For Apple OSX Users, you must open the Terminal and change the current directory to the unzipped folder. Then, run the following command to launch the software.
  ```bash
  ./LipidWizard
  ```

## Run from Source Code
After python was installed, douwnload the sourcecode
Call the the following commands to configure and run the software from the source code.
Run the following commands to download all the dependecies
For linux and osx users:
```bash
pip install -r requirements.txt
```
For Windows users:
```bash
python -m pip install -r requirements.txt
```
Run the following commands to launch the software
For OSX users and Linux users:
```bash
python3 gui.py
```
For Windows users:
```bash
python gui.py
```

See the file "User Manual for Lipid Wizard.pdf" for the using guidance.