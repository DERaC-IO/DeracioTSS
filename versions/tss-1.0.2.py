"""
DeracioTSS -- Tornado Startup Script
Copyright (c) 2023 DERaC, LLC.

BTC: 3GSGPvNeSv1j9LobjzZWiCL2Vd29rpmyXE
ETH: 0x8928534c8beca7875059edce7afae202836a0d4c
"""
# -*- coding: utf-8 -*-
import os, argparse, re, json, random, time, hashlib, subprocess, questionary

class DeracioTSS:
    def __init__(self):
        # Opening banner
        self.title = 'Tornado Startup Script'
        self.copy = 'Copyright (c) 2023 DERaC, LLC.'
        self.version = '1.0.2'
        self.license = 'MIT License'
        self.banner = """
_____________________________________________________________________
    _____                                    ______     __       __  
    /    )                           ,         /      /    )   /    )
---/----/----__---)__----__----__--------__---/-------\--------\-----
  /    /   /___) /   ) /   ) /   ' /   /   ) /         \        \    
_/____/___(___ _/_____(___(_(___ _/___(___/_/______(____/___(____/___                                                                  
"""
        # Arg parser
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-q", "--quickstart", help="quick start with default params", action="store_true")
        self.parser.add_argument("-o", "--overwrite", help="overwrite all directories/folders", action="store_true")
        self.parser.add_argument("-a", "--all", help="generate all files", action="store_true")
        self.parser.add_argument("-n", "--name", help="application name (default = app)")
        self.parser.add_argument("-d", "--domain", help="port number (default = localhost)")
        self.parser.add_argument("-p", "--port", help="port number (default = 8000)")
        # Parameters
        self.name = 'app'
        self.template = 'templates'
        self.static = 'static'
        self.domain = 'localhost'
        self.port = '8000'
        self.encoding = 'utf-8'
        self.python_path = subprocess.run("which python3", shell=True, stdout=subprocess.PIPE, encoding=self.encoding)
        self.script_header = f'#!{self.python_path}\n'
        self.script_header += f'# -*- coding: {self.encoding} -*-\n'
        # Handler
        self.handler = 'MainHandler'
        self.settings = 'settings'
        self.path = '/'
        self.view = 'view'
        self.model = 'model'
        # Server script
        self.server_name = "server.sh"
        self.shell = "bash"
        self.mode = '0755'
        # Daemon script
        self.daemon_name = "tornadod.service"
        self.description = 'Tornado Web Service'
        self.cwd = os.getcwd()
        self.user = subprocess.run("whoami", shell=True, stdout=subprocess.PIPE, encoding=self.encoding).stdout.strip()
        self.group = subprocess.run("id -g -n", shell=True, stdout=subprocess.PIPE, encoding=self.encoding).stdout.strip()
        # Donations
        self.btcaddr = '3GSGPvNeSv1j9LobjzZWiCL2Vd29rpmyXE'
        self.ethaddr = '0x8928534c8beca7875059edce7afae202836a0d4c'
        self.donation = 'Donations are welcome!'
        # Misc messages
        self.bye = 'bye...'
        # Colors
        self.BLACK     = '\033[30m'
        self.RED       = '\033[31m'
        self.GREEN     = '\033[32m'
        self.YELLOW    = '\033[33m'
        self.BLUE      = '\033[34m'
        self.PURPLE    = '\033[35m'
        self.CYAN      = '\033[36m'
        self.WHITE     = '\033[37m'
        # Decors
        self.END       = '\033[0m'
        self.BOLD      = '\033[1m'
        self.UNDERLINE = '\033[4m'
        self.INVISIBLE = '\033[08m'
        self.REVERCE   = '\033[07m'

    def start(self):
        print(self.banner)
        print(f'{self.title} v{self.version}')
        print(self.copy)
        print(f'{self.license}\n')
        self.args = self.parser.parse_args()
        if self.args.name:
            self.name = self.args.name
        if self.args.domain:
            self.domain = self.args.domain
        if self.args.port:
            self.port = self.args.port
        if self.args.quickstart:
            print(self.BOLD + self.YELLOW + "NOTICE: quickstarter turned on\n" + self.END + self.END)

    def exit(self):
        print(self.BOLD + f'\n{self.donation}\n' + self.END)
        print(f'BTC: {self.btcaddr}')
        print(f'ETH: {self.ethaddr}\n')
        print(f'{self.bye}\n')

    def error(self, err):
        print(self.BOLD + self.RED + err + self.END + self.END)
        exit()

    def createProject(self):
        if not self.args.quickstart:
            self.name = questionary.text(f'Project name', default = self.name).ask()
        if self.name == '':
            print(self.RED + '\nProject name cannot be blank...\n' + self.END)
            exit()
        self.name = re.sub('\s', '_', self.name)
        print(self.BOLD + f'\nStart creating new project [{self.name}]...\n' + self.END)
        self.generatingApp()
        self.generateHandler()
        self.generateSettings()
        self.generatingTemplate()
        self.generateStatic()
        self.generateServerScript()
        self.generateDaemonScript()


    def generatingApp(self):
        self.app_name = f'{self.name}.py'
        if not self.args.quickstart:
            self.template = questionary.text(f'Template folder name', default = self.template).ask()
            self.static = questionary.text(f'Static file folder name', default = self.static).ask()
            self.port = questionary.text(f'Which port will you use?', default = self.port).ask()
            self.app_name = questionary.text(f'App file name', default = self.app_name).ask()
            self.python_path = questionary.path(f'Path to python3', default = self.python_path.stdout.strip()).ask()
    
        exist = os.path.isfile(self.app_name)
        overwrite = self.args.overwrite
        if exist and not overwrite:
            overwrite = questionary.confirm(f'Overwrite existing {self.app_name}?', default=False).ask()
        if not exist or overwrite:
            script = self.script_header
            script += f'from {self.handler}.{self.view} import {self.handler}\n\n'
            script += """
import tornado.ioloop, tornado.web
import os, re, json, threading

# Define fundamental parameters for the service
# These params are in settings.py generated from files in settings.d

from settings import config

__template__ = config.get("template")
__static__ = config.get("static")
__port__ = config.get("port")

# Definition for the web service
# Routing, debug (autoload) setting, template/static folders, etc...
application = tornado.web.Application(
    [
        ("/", MainHandler),
    ],
    debug=True,
    template_path=os.path.join(os.getcwd(), __template__),
    static_path=os.path.join(os.getcwd(), __static__),
)

# Startup script for the server (read by server.sh)
if __name__ == "__main__":
    application.listen(__port__)
    tornado.ioloop.IOLoop.instance().start()
"""
            try:
                with open(self.app_name, 'w') as f:
                    f.write(script)
                    f.close()
                print(self.GREEN + f'Folder {self.app_name} is generated successfully!' + self.END)
            except Exception as e:
                self.error(e)
        else:
            print(self.YELLOW + f'{self.app_name} already exists...' + self.END)

    def generateHandler(self):
        print('\nGenerating handler...')
        path = '/'
        # ask if MainHandler exists first
        if os.path.isdir(self.handler):
            if not self.args.quickstart:
                self.path = questionary.text('URI (path) for the handler', default = self.path).ask()
            if self.path == '/':
                self.handler = re.sub('handler$', '', self.handler.capitalize()) + 'Handler'
            else:
                divs = path.split('/')
                h = ''
                for div in divs:
                    if div.strip() != '':
                        h += div.capitalize()
                self.handler = re.sub('handler$', '', h) + 'Handler'
            if not self.args.quickstart:
                self.handler = questionary.text('Handler name', default = self.handler).ask()
        # ask if self.handler exists that may not be MainHandler
        exist = os.path.isdir(self.handler)
        if not exist:
            try:
                os.mkdir(self.handler)
                print(self.GREEN + f'\nFolder {self.handler} is created successfully!' + self.END)
            except Exception as e:
                self.error(e)
        else:
            if not self.args.overwrite:
                create = questionary.confirm(f'Overwrite existing {self.handler}?').ask()
            else:
                create = False
        if not exist or create:
            try:
                if not os.path.isdir('settings.d'):
                    os.mkdir('settings.d')
                handlers = 'settings.d/handlers.json'
                entries = dict()
                if os.path.isfile(handlers):
                    with open(handlers) as f:
                        entries = f.read()
                        if entries:
                            entries = json.loads(entries)
                        f.close()
                entries[path] = self.handler
                with open(handlers, "w") as f:
                    f.write(json.dumps(entries))
                    f.close()
            except Exception as e:
                self.error(e)
                
            # Generating handler class file
            script = self.script_header
            script += '\n'
            script += 'import tornado.ioloop, tornado.web\n\n'
            script += f'class {self.handler}(tornado.web.RequestHandler):\n'
            script += '\tdef initialize(self):\n'
            script += '\t\tself.params = {"title": "' + self.title + '"}\n'
            script += '\n'
            script += '\tdef get(self):\n'
            script += '\t\tself.render("index.html", params = self.params)\n'
            script += '\n'
            script += '\tdef post(self):\n'
            script += '\t\tself.render("index.html", params = self.params)\n'
            try:
                with open(f'{self.handler}/{self.view}.py', 'w') as f:
                    f.write(script)
                    f.close()
                print(self.GREEN + f'\nFile {self.handler}/{self.view}.py is generated successfully!' + self.END)
            except Exception as e:
                self.error(e)

    def generateSettings(self):
        print('\nCreating settings files...')
        settingsd = f'{self.settings}.d'
        if not os.path.isdir(settingsd):
            os.mkdir(settingsd)
        exist = os.path.isfile(f'{self.settings}.py')
        overwrite = False
        if exist and not self.args.overwrite:
            overwrite = questionary.confirm(f'Overwrite existing {self.settings}.py?', default=False).ask()
        if not exist or overwrite:
            dat = str(random.randint(0, 999999)) + str(time.time()) + self.name
            config = {
                'appId': hashlib.sha256(dat.encode()).hexdigest(),
                'template': self.template,
                'static': self.static,
                'port': int(self.port),
            }
            with open(f'{settingsd}/config.json', 'w') as f:
                f.write(json.dumps(config))
                f.close()

            files = os.listdir(settingsd)
            script = self.script_header
            script += f"# Settings generated from JSON files (identified by .json) in {settingsd} folder\n\n"
            for file in files:
                name = file.split('.')
                if name[1] == 'json':
                    script += f'# {file}\n'
                    script += name[0] + " = {\n"
                    with open(f"{settingsd}/{file}") as f:
                        entry = f.read()
                        if entry:
                            entry = json.loads(entry)
                            for key, value in entry.items():
                                if type(value) is str:
                                    script += '\t"{}": "{}",\n'.format(key, value)
                                else:
                                    script += '\t"{}": {},\n'.format(key, value)
                        f.close()
                    script += "}\n\n"
            try:
                with open(f'{self.settings}.py', 'w') as f:
                    f.write(script)
                    f.close()
                print(self.GREEN + f'\nFile {self.settings}.py is created successfully!' + self.END)
            except Exception as e:
                self.error(e)

    def generatingTemplate(self):
        print('\nCreating template folder...\n')
        if not os.path.isdir(self.template):
            try:
                os.mkdir(self.template)
                print(self.GREEN + f'Folder {self.template} is created successfully!' + self.END)
            except Exception as e:
                self.error(e)
        else:
            print(self.YELLOW + f'Folder {self.template} already exists...' + self.END)

        print()
            
        exist = os.path.isfile(f'{self.template}/index.html')
        overwrite = self.args.overwrite
        if exist and not overwrite:
            overwrite = questionary.confirm(f'Overwrite existing {self.template}/index.html?', default=False).ask()
        if not exist or overwrite:
            script ="""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset="utf-8">
    <title>{{ params.get('title') }}</title>
    <!-- UIkit CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.16.24/dist/css/uikit.min.css" />
    <!-- UIkit JS -->
    <script async src="https://cdn.jsdelivr.net/npm/uikit@3.16.24/dist/js/uikit.min.js" defer></script>
    <script async src="https://cdn.jsdelivr.net/npm/uikit@3.16.24/dist/js/uikit-icons.min.js" defer></script>
</head>
<body>
{% block body %}
<div class="uk-margin-top uk-text-center">
    <img src="https://raw.githubusercontent.com/DERaC-IO/DeracioTSS/2a43aac2a5138902f83d24b38a367b7366aa8548/misc/deractss_logo.png">
    <div class="uk-h1">Congratulations!</div>
    <div class="uk-text-success">Tornado is now working!</div>
    <div class="uk-h2">Donations</div>
    <center>
    <p class="uk-width-1-3@m">
        DeracioTSS is open source under MIT license, but we appreciate donations if you have felt any utility from our code!
    </p>
    <table class="uk-table uk-width-1-3@m uk-text-center uk-margin-top">
        <tr><td>BTC</td><td>ETH</td></tr>
        <tr>
            <td>
                <img src="https://raw.githubusercontent.com/DERaC-IO/DeracioTSS/2a43aac2a5138902f83d24b38a367b7366aa8548/misc/btc_bitflyer_qr.png">
            </td>
            <td>
                <img src="https://raw.githubusercontent.com/DERaC-IO/DeracioTSS/2a43aac2a5138902f83d24b38a367b7366aa8548/misc/eth_bitflyer_qr.png">
            </td>
        </tr>
    </table>
    </center>
    <div class="uk-text-primary">For BTC: 3GSGPvNeSv1j9LobjzZWiCL2Vd29rpmyXE</div>
    <div class="uk-text-primary">For ETH: 0x8928534c8beca7875059edce7afae202836a0d4c</div>
</div>
{% end %}
</body>
</html>
"""
            try:
                with open(f'{self.template}/index.html', 'w') as f:
                    f.write(script)
                    f.close()
                print(self.GREEN + f'{self.template}/index.html is generated successfully!' + self.END)
            except Exception as e:
                self.error(e)
        else:
            print(self.YELLOW + f'{self.template}/index.html already exists...' + self.END)

    def generateStatic(self):
        print('\nCreating static file folder...\n')
        if not os.path.isdir(self.static):
            try:
                os.mkdir(self.static)
                print(self.GREEN + f'Folder {self.static} is created successfully!' + self.END)
            except Exception as e:
                self.error(e)
        else:
            print(self.YELLOW + f'Folder {self.static} already exists...' + self.END)

    def generateServerScript(self):
        print('\nGenerating server scripts...')
        generate = self.args.all
        if not generate:
            generate = questionary.confirm('Do you wish to generate server startup script?').ask()
        if generate:
            if not self.args.quickstart:
                self.shell = questionary.select(
                    'Which shell do you use?',
                    choices = ['bash','zsh','csh','tcsh','sh'],
                    default = self.shell
                ).ask()
                self.server_name = questionary.text(f'Script name', default=self.server_name).ask()
                self.mode = questionary.text('File permission mode', default = self.mode).ask()
            shell_path = subprocess.run(f"which {self.shell}", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
            if not self.args.quickstart:
                shell_path = questionary.path(f'Path to {self.shell}', default=shell_path.stdout.strip()).ask()
            exist = os.path.isfile(self.server_name)
            overwrite = self.args.overwrite
            if exist and not overwrite:
                overwrite = questionary.confirm(f'Overwrite existing {self.server_name}?', default=False).ask()
            if not exist or overwrite:
                script = f'#!{shell_path}\n'
                script += """
# Define the app name
APP_NAME="Deracio Tornado/Python"

# Full path to the app directory
HOME_DIR=`pwd`

# Full path to the server program
# Tornado launches webserver of itself => path to python
"""                 
                script += f'SERVER="{self.python_path}"\n'
                script += """
# App file name that includes 'application' to 'listen'
### For example:
### application = tornado.web.Application(...)
### application.listen(...)
"""
                script += f'APP="{ self.app_name }"\n'
                script += """
# Startup script
echo "Starting $APP_NAME"
$SERVER $HOME_DIR/$APP
"""
                try:
                    with open(self.server_name, 'w') as f:
                        f.write(script)
                        f.close()
                    print(self.GREEN + f'\n{ self.server_name } is generated successfully!' + self.END)
                    if subprocess.call(["chmod", self.mode, self.server_name]) == 0:
                        print(self.GREEN + f'Permission is set {self.mode} for { self.server_name }\n' + self.END)        
                except Exception as e:
                    self.error(e)
            else:
                print(self.YELLOW + f'\n{ self.server_name } already exists...\n' + self.END)

    def generateDaemonScript(self):
        generate = self.args.all
        if not generate:
            generate = questionary.confirm('Do you wish to generate system daemon script?').ask()
        if generate:
            if not self.args.quickstart:
                self.daemon_name = questionary.text('System daemon file name', default = self.daemon_name).ask()
                self.description = questionary.text('Brief system description', default = 'Tornado Web Service').ask()
                self.cwd = questionary.path('Working directory', default = os.getcwd()).ask()
                self.user = questionary.text('User name to execute', default = self.user).ask()
                self.group = questionary.text('Group name to execute', default = self.group).ask()
                self.mode = questionary.text('File permission mode', default = self.mode).ask()

            exist = os.path.isfile(self.daemon_name)
            overwrite = self.args.overwrite
            if exist and not overwrite:
                    overwrite = questionary.confirm(f'Overwrite existing {self.daemon_name}?', default=False).ask()
            if not exist or overwrite:
                script = """
[Unit]
# Clarify to descrive this service
"""
                script += f'Description={self.description}\n'
                script += """
[Service]
# Full path to your project
"""
                script += f'WorkingDirectory={self.cwd}\n'
                script += '# Full path to your server startup script\n'
                script += f'ExecStart="{self.cwd}/{self.server_name}"'
                script += """
Restart=always
RestartSec=3s
Type=simple

# User and group names to launch the service
# Avoid root or equivalent user/group
"""
                script += f'User={self.user}\n'
                script += f'Group={self.group}\n'
                script += """
[Install]
WantedBy=multi-user.target
"""
                try:
                    with open(self.daemon_name, 'w') as f:
                        f.write(script)
                        f.close()
                    print(self.GREEN + f'\n{ self.daemon_name } is generated successfully!' + self.END)
                    if subprocess.call(["chmod", self.mode, self.daemon_name]) == 0:
                        print(self.GREEN + f'Permission is set {self.mode} for { self.daemon_name }' + self.END)
                except Exception as e:
                    self.error(e)
                finally:
                    print(self.BOLD + f'\nFollow the procedure below to daemonize { self.daemon_name }\n' + self.END)
                    print(f'1. sudo mv { self.daemon_name } /etc/systemd/system/')
                    print(f'2. sudo systemctl daemon-reload')
                    print(f'3. sudo systemctl enable { self.daemon_name } --now')

    def completed(self):
        print(self.GREEN + self.BOLD + '\nCongratulations!\n' + self.END + self.END)
        print('Tornado is ready to work with you now!')
        print('Don\'t forget to "pip install tornado"')

def __main__():
    tss = DeracioTSS()
    tss.start()
    if questionary.confirm('Starting a new project?').ask():
        tss.createProject()
        tss.completed()
    tss.exit()

if __name__=='__main__':
    __main__()
