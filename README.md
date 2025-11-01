
<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/luismco/pycket-tracer/refs/heads/main/images/logo.svg" alt="Pycket Tracer" width="200">
  <br>
  Pycket Tracer
  <br>
</h1>

<h4 align="center">Python Module (25H) • Final Project</h4>
<br><br>

Final project for a Python Module (25H) within a Networking and Cyber Sercurity course
The repository has 2 Python files:
* [Pycket Tracer Tools](https://github.com/luismco/pycket-tracer/blob/main/pycket-tracer.py)
  - Full Netwoking Tools
  - English
* [Project](https://github.com/luismco/pycket-tracer/blob/main/project.py)
  - Basic Networking Tools
  - User Accounts and Administration (Required for the project)
  - Portuguese

The project file is not intended for general use.<br>
<br>
If you intend to test the networking tools, please use [Pycket Tracer Tools](https://github.com/luismco/pycket-tracer/blob/main/pycket-tracer.py) since it can be used without any user account and it has a more complete tool set available.

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#modules">Modules</a>
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/luismco/pycket-tracer/refs/heads/main/images/screenshot.png" alt="screenshot">
<p/>

## Key Features

* IP Conversion
  - Decimal to Binary
  - Binary to Decimal
* Subnet Mask/CIDR Calculator
  - Based on number of hosts needed
* IP Classification
  - Private vs Public
  - IP Classes
* Subnetting
  - Based on number of needed networks
* VLSM
  - Based on number of hosts needed per network

## How To Use

To clone and run this application, you'll just need [Python](https://www.python.org/downloads/) installed on your computer. From your command line:

<b>Example for Linux</b>
```bash
# Clone this repository
git clone https://github.com/luismco/pycket-tracer

# Go into the repository
cd pycket-tracer

# Run the app
python3 ./pycket-tracer.py
```

## Modules

This software uses the following python modules

- ipaddress
- random
- textwrap
- hashlib
- getpass
- string


