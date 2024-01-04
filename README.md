![DeracioTSS](/misc/deractss_logo.png)

Latest Version: 1.1.1 (September 5, 2023)

![GitHub](https://img.shields.io/github/license/DERaC-IO/DeracioTSS)
![GitHub top language](https://img.shields.io/github/languages/top/DERaC-IO/DeracioTSS)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/DERaC-IO/DeracioTSS)

# Instructions
DeracioTSS is a Tornado/Python startup script. This script is primarily written for developers and affiliates of DERaC, but it is also open to the public under the [MIT License](/LICENSE). The change log is available at [CHANGELOG](/CHANGELOG.md) with some detailed discussions in [Issues](https://github.com/DERaC-IO/DeracioTSS/issues).

###### Requirements

- Linux or compatibles, e.g., WSL

### Functions

- Quick Startup/Daemonization
- Routing/Handler Management (1.1.0+)
- Settings Configurations (1.1.0+)
- Server Watcher (1.1.0+)

###### Main Menu of the CLI App

```
   --- Project ---
 » 1) Health Check
   2) New Project
   --- Handler ---
   3) List Handlers
   4) Rouitng
   5) New Handler
   6) Delete Handler
   --- Setting ---
   7) Show Settings
   8) Configure
   ---------------
   9) Stop/Start Server
   0) Quit
```

##### Caveat Emptor

Scripts are coded with intensive care, but please notice issues that bugs and security holes may be found in the future. We are not responsible for any troubles caused by the usage of DeracioTSS. If you found any issues that may affect t the community, please let us know.

## Getting Started

### Startup Script

##### Installation

###### Installation with pip

```
pip install torms
```

###### Install manually

Download or copy'n paste `torms.py` to your server directory that the Tornado project is to be placed. For example, `wget` will work like this.

```
wget https://raw.githubusercontent.com/DERaC-IO/DeracioTSS/main/torms.py
```

If you love `cURL` or `requests`, it's OK. The script requires the `questionary` package, so install it with `pip` in your virtual environment.

```
pip install questionary
```

Now you are ready to start the script with `python` or `python3`.

```
python -m torms
```

```_____________________________________________________________________
    _____                                    ______     __       __  
    /    )                           ,         /      /    )   /    )
---/----/----__---)__----__----__--------__---/-------\--------\-----
  /    /   /___) /   ) /   ) /   ' /   /   ) /         \        \    
_/____/___(___ _/_____(___(_(___ _/___(___/_/______(____/___(____/___                                                                  

Tornado Startup Script v1.1.0
Copyright (c) 2023 DERaC, LLC.
MIT License

Server is active at http://localhost:8000
```

You will see the startup logo of the program if successfully installed. Please answer questions to generate the following files. By default, folders and files are generated as shown below.

- python app file (default = `app.py`)
- template index (`index.html`)
- server startup script (default = `server.sh`)
- system daemon script (default = `tornadod.service`)

###### Directory Structure
```
<PROJECT_ROOT>
    │
    ├─ app.py
    │
    ├─ server.sh
    │
    ├─ tornadod.service
    │
    ├─ settings.py (added in 1.0.1+)
    │
    ├─ settings.d  (added in 1.0.1+)
    │    │
    │    ├─ config.json
    │    │
    │    └─ handler.json  (added in 1.0.2+)
    │
    ├─ templates
    │    │
    │    └─ index.html
    │ 
    └─ static
```

#### CLI Options (v1.0.2+)

CLI command has options whose descriptions are available with `-h` or (`--help`) option:

```
usage: tss.py [-h] [-q] [-o] [-a] [-n NAME] [-d DOMAIN] [-p PORT]

options:
  -h, --help            show this help message and exit
  -q, --quickstart      quick start with default params
  -o, --overwrite       overwrite all directories/folders
  -a, --all             generate all files
  -n NAME, --name NAME  application name (default = app)
  -d DOMAIN, --domain DOMAIN
                        port number (default = localhost)
  -p PORT, --port PORT  port number (default = 8000)
```

##### Quick-Start

The fastest option is the following that enables you to launch the Tornado server in seconds!

```
python tss.py -q -o -a
```

After installation, do `sh server.sh` on the command line.

### GitHub Cloning

```
git clone https://github.com/DERaC-IO/DeracioTSS.git
```

`git clone` will give you the copy of the entire directory of the package. If you do git-clone, paths are not detected and some other parameters are also not configured automatically, so you are requested to edit files and scripts manually that include these parameters. List of parameters are listed as follows.

###### app.py (v1.0.0)

- path to `python`
- template folder name (`__template__`)
- static file folder name (`__static__`)
- port (`__port__`)

###### app.py (v1.0.1+)

- path to `python`

###### settings.py and settings.d/config.json (v1.0.1+)

- path to `templates`
- path to `static`
- port number

###### server.sh

- `APP_NAME` (descritive app name)
- `SERVER` (path to `python`)
- `APP` (python app file)

###### tornadod.service

- `Description` (clarify service)
- `WorkingDirectory` (path to server script)
- `ExecStart` (command starting server script)
- `User` (launching user name)
- `Group` (launching group name)

### Daemonization

If installation is successful, you are already set to go. Move the service file (`tornadod.service` is default) to the system daemon directory (i.e., `/etc/systemd/system/`) in order for `systemctl` command can recognize the script. Before starting the daemon, don't forget reloading registered systems by `systemctl daemon-reload`. After that you can eventually start the daemonized Tornado application.

```
sudo mv tornadod.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start tornadod
```
If you want the Tornado application to start automatically, enable the daemon as follows (`--now` option simultaneously start the daemon after enabling it).

```
sudo systemctl enable tornadod --now
```

Now you are able to access the served website via the port you have designated, congrats!

![DeracioTSS](/misc/snapshot.png)

##### Reverse Proxy

You may want to open your Tornado web server directly to the public. In that case, set you port 80/443 (or the likes depending on your infra settings) to run the server. However, someone may feel not good to do so like me as WAF may not be applied easily or etc. In that case, you may want to use reverse proxy or CGI/FCGI techniques. Usually DERaC considers performing speed and uses reverse proxy.

## Future Roadmap

DeracioTSS tries to enhance development experiences with Tornado. The eventual goal is to build a full-stack package manager for Tornado application that is friendly even for newbie developers. The package is primarily designed for our affiliates and staffs while it is open to our communities. Following functions are going to be implemented to realize the ultimate goal (the latest version is `1.1`). Please watch [CHANGELOG](/CHANGELOG.md) for updates.

| Function | Style | Version | Status |
|:---|:---:|:---:|:---:|
|project setup script|CLI|`1.0`|Ready|
|handler (app) setup script|CLI|`1.1`|Ready|
|settings managing script|CLI|`1.2` &rarr; `1.1`|Ready|
|integrations with alembic/sqlalchemy|CLI|`1.3` &rarr; `1.2`|Working|
|routing manager|GUI/CLI|`2.0`|Working|
|handler class manager|GUI/CLI|`2.1`|Working|
|system monitor|GUI|`3.0`|-|
|wrapping web app|GUI|`3.1`|-|

##### Contributions

As an open source package, any kinds of contributions are open and welcome!

##### Donations

This package is open source, but we appreciate donations if you have felt any utility from our code and/or future development plan. Your donations via [PayPal](https://paypal.me/deracjp) or cryptos help further enhancements/developments, thanks!

| Crypto | Address |
|:---:|:---:|
| BTC | ![BTC](/misc/btc_bitflyer_qr.png)<br>3GSGPvNeSv1j9LobjzZWiCL2Vd29rpmyXE |
| ETH | ![ETH](/misc/eth_bitflyer_qr.png)<br>0x8928534c8beca7875059edce7afae202836a0d4c |

## About DERaC

Decentralized Economy Research & Consulting (DERaC) was founded by Tetsuya (Tedd) Saito, Ph.D. in December 2022 based on his specilties -- network security, mathematical/data science, economics, and 25+ years of experience in web development. DERaC provides services on network security, web development, statistical analysis, mathematical modeling, economic consulting, and web development with several affiliated specialists of each field.

Occasional job opportunities are posted on our website at https://derac.io (en) or https://derac.jp (ja), but applications from talented specialists/developers that are capable of Python, R, statistics, economics/econometrics, applied mathematics, machine learning, and ethical hackers are always welcome.
