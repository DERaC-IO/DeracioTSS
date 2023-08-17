![DeracioTSS](/misc/deractss_logo.png)

# Instructions
DeracioTSS is a Tornado/Python startup script. This script is primarily written for developers and affiliates of DERaC, but it is also open to the public under the [MIT Licence](/LICENSE).

##### Caveat Emptor

Scripts are coded with intensive care, but please notice issues that bugs and security holes may be found in the future. We are not responsible for any troubles caused by the usage of DeracioTSS. If you found any issues that may affect t the community, please let us know.

## Getting Started

### Startup Script

##### Installation

Download or copy'n paste `tss.py` to your server directory that the Tornado project is to be placed. For example, `wget` will work like this.

```
wget https://raw.githubusercontent.com/DERaC-IO/DeracioTSS/f6691d177de800434593cb336f102c1181c73439/tss.py
```

If you love `cURL` or `requests`, it's OK. The script requires `questionary` and `subprocess` packages, so install the two with `pip` in your virtual environment.

```
pip install questionary subprocess
```

Now you are ready to start the script with `python` or `python3`.

```
python tss.py
```

```_____________________________________________________________________
    _____                                    ______     __       __  
    /    )                           ,         /      /    )   /    )
---/----/----__---)__----__----__--------__---/-------\--------\-----
  /    /   /___) /   ) /   ) /   ' /   /   ) /         \        \    
_/____/___(___ _/_____(___(_(___ _/___(___/_/______(____/___(____/___                                                                  

Tornado Startup Script v1.0.0
Copyright (c) 2023 DERaC, LLC.
MIT License

? Starting a new project?
```

You will see the startup logo of the program if successfully installed. Please answer questions to generate the following files. By default, folders and files are generated as shown below.

- python app file (default = `app.py`)
- template index (`index.html`)
- server startup script (default = `server.sh`)
- system daemon script (default = `tornadod.service`)

###### Directory Structure
```
<PROJECR_ROOT>
    │
    ├─ app.py
    │
    ├─ server.sh
    │
    ├─ tornadod.service
    │
    ├─ templates
    │    │
    │    └─ index.html
    │ 
    └─ static
```

### GitHub Cloning

```
git clone https://github.com/DERaC-IO/DeracioTSS.git
```

`git clone` will give you the copy of the entire directory of the package. If you do git-clone, paths are not detected and some other parameters are also not configured automatically, so you are requested to edit files and scripts manually that include these parameters. List of parameters are listed as follows.

###### app.py

- path to `python`
- template folder name (`__template__`)
- static file folder name (`__static__`)
- port (`__port__`)

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

###### Reverse Proxy

You may want to open your Tornado web server directly to the public. In that case, set you port 80/443 (or the likes depending on your infra settings) to run the server. However, someone may feel not good to do so like me as WAF may not be applied easily or etc. In that case, you may want to use reverse proxy or CGI/FCGI techniques. Usually DERaC considers performing speed and uses reverse proxy.

## About DERaC

Decentralized Economy Research & Consulting (DERaC) was founded by Tetsuya (Tedd) Saito, Ph.D. in December 2022 based on his specilties -- network security, mathematical/data science, economics, and 25+ years of experience in web development. DERaC provides services on network security, web development, statistical analysis, mathematical modeling, economic consulting, and web development with several affiliated specialists of each field.

Occasional job opportunities are posted on our website at https://derac.io (en) or https://derac.jp (ja), but applications from talented specialists/developers that are capable of Python, R, statistics, economics/econometrics, applied mathematics, machine learning, and ethical hackers are always welcome.

##### Donations

This package is open source, but we appreciate donations if you have felt any utility from our code.

| Crypto | Address |
|:---:|:---:|
| BTC | ![BTC](/misc/btc_bitflyer_qr.png)<br>3GSGPvNeSv1j9LobjzZWiCL2Vd29rpmyXE |
| ETH | ![ETH](/misc/eth_bitflyer_qr.png)<br>0x8928534c8beca7875059edce7afae202836a0d4c |

