"""
DeracioTSS -- Tornado Startup Script
Copyright (c) 2023 DERaC, LLC.

PayPal: https://paypal.me/deracjp
BTC: 3GSGPvNeSv1j9LobjzZWiCL2Vd29rpmyXE
ETH: 0x8928534c8beca7875059edce7afae202836a0d4c
"""
# -*- coding: utf-8 -*-
import os, argparse, re, json, random, time, hashlib, subprocess, questionary, threading
from questionary import Choice, Separator

class DeracioTSS:
    def __init__(self):
        # Opening banner
        self.title = 'Tornado Startup Script'
        self.copy = 'Copyright (c) 2023 DERaC, LLC.'
        self.version = '1.1.0'
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
        # Main Menu
        self.newproject = 'New Project'
        self.projecthealth = 'Health Check'
        self.newhandler = 'New Handler'
        self.listhandlers = 'List Handlers'
        self.deletehandler = 'Delete Handler'
        self.managerouting = 'Rouitng'
        self.showsettings = 'Show Settings'
        self.configuresettings = 'Configure'
        self.serverstatus = 'Stop/Start Server'
        self.quit = 'Quit'
        self.mainmenu = [
            Separator("--- Project ---"),
            self.projecthealth,
            self.newproject,
            Separator("--- Handler ---"),
            self.listhandlers,
            self.managerouting,
            self.newhandler,
            self.deletehandler,
            Separator("--- Setting ---"),
            self.showsettings,
            self.configuresettings,
            Separator("---------------"),
            self.serverstatus,
            self.quit,
        ]
        # Parameters
        self.name = 'app'
        self.appId = False
        self.template = 'templates'
        self.static = 'static'
        self.protocol = 'http'
        self.domain = 'localhost'
        self.port = '8000'
        self.encoding = 'utf-8'
        self.devel = True
        self.imports = [
            {'name':'os', 'as': None, 'from': None},
            {'name':'re', 'as': None, 'from': None},
            {'name':'json', 'as': None, 'from': None},
            {'name':'threading', 'as': None, 'from': None},
        ]
        self.python_path = subprocess.run("which python3", shell=True, stdout=subprocess.PIPE, encoding=self.encoding).stdout.strip()
        self.script_header = f'#!{self.python_path}\n'
        self.script_header += f'# -*- coding: {self.encoding} -*-\n'
        # Handler
        self.handler = 'MainHandler'
        self.settings = 'settings'
        self.settingd = f'{self.settings}.d'
        self.paramconf = f'{self.settingd}/config.json'
        self.handlerconf = f'{self.settingd}/handlers.json'
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
        self.goback = 'Go back'
        self.changerouting = 'Routing'
        self.changehandler = 'Handler'
        self.delete = 'Delete'
        self.addnewuri = 'Add New URI'
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
        self.REVERSE   = '\033[07m'

    def start(self, banner = True):
        if banner:
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
            print(self.BOLD + self.YELLOW + "NOTICE: quickstarter turned on\n" + self.END)
        if self.args.quickstart:
            return self.createProject()
        if self.statServer() > 0:
            print(self.BOLD + self.GREEN + f"Server is active at {self.protocol}://{self.domain}:{self.port}\n" + self.END)
        else:
            print(self.BOLD + self.RED + "Server is dead...\n" + self.END)

        return questionary.select('TSS Menu', self.mainmenu, use_shortcuts = True).ask()

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
        self.generatingApp(self.args.overwrite)
        self.generateHandler(self.args.overwrite)
        self.generateSettings(self.args.overwrite)
        self.generatingTemplate(self.args.overwrite)
        self.generateStatic()
        self.generateServerScript(self.args.overwrite)
        self.generateDaemonScript(self.args.overwrite)


    def generatingApp(self, overwrite = False):
        self.app_name = f'{self.name}.py'
        if not self.args.quickstart:
            self.template = questionary.text(f'Template folder name', default = self.template).ask()
            self.static = questionary.text(f'Static file folder name', default = self.static).ask()
            self.port = questionary.text(f'Which port will you use?', default = self.port).ask()
            self.app_name = questionary.text(f'App file name', default = self.app_name).ask()
            self.python_path = questionary.path(f'Path to python3', default = self.python_path).ask()
    
        exist = os.path.isfile(self.app_name)
        if exist and not overwrite:
            overwrite = questionary.confirm(f'Overwrite existing {self.app_name}?', default=False).ask()
        if not exist or overwrite:
            script = self.script_header
            script += """
import tornado.ioloop, tornado.web, os

# Define fundamental parameters for the service
# These params are in settings.py generated from files in settings.d

for cnf in os.listdir('settings.d'):
    name = cnf.split('.')
    if name[1] == 'json':
        exec(f"from settings import {name[0]}")

# Handlers and routes are read from settings.handlers
# Use of routing manager is recommended

routes = ""
for route, handler in handlers.items():
    exec(f"from {handler}.view import {handler}")
    routes += f'(r"{route}", {handler}),'

cwd = os.getcwd()

# Definition for the web service
# Routing, debug (autoload) setting, template/static folders, etc...

application = tornado.web.Application(
    eval(f"[{routes}]"),
    debug = config.get("devel", False),
    template_path = os.path.join(cwd, config.get("template")),
    static_path = os.path.join(cwd, config.get("static")),
)

# Startup script for the server (read by server.sh)
if __name__ == "__main__":
    application.listen(config.get("port"))
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

    def generateHandler(self, overwrite = False):
        print('\nGenerating handler...')
        path = '/'
        # ask if MainHandler exists first
        if os.path.isdir(self.handler):
            if not self.args.quickstart:
                path = questionary.text('URI (path) for the handler', default = self.path).ask()
            if path == '/':
                self.handler = re.sub('handler$', '', self.handler.capitalize()) + 'Handler'
            else:
                divs = path.split('/')
                h = ''
                for div in divs:
                    if div.strip() != '':
                        h += div.capitalize()
                self.handler = re.sub('handler$', '', h) + 'Handler'
            if not self.args.quickstart:
                self.handler = questionary.text('Handler', default = self.handler).ask()
        # ask if self.handler exists that may not be MainHandler
        exist = os.path.isdir(self.handler)
        if not exist:
            try:
                os.mkdir(self.handler)
                print(self.GREEN + f'\nFolder {self.handler} is created successfully!' + self.END)
            except Exception as e:
                self.error(e)
        else:
            if not overwrite:
                overwrite = questionary.confirm(f'Overwrite existing {self.handler}?').ask()
        if not exist or overwrite:
            try:
                if not os.path.isdir(self.settingd):
                    os.mkdir(self.settingd)
                handlers = f'{self.settingd}/handlers.json'
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
            script += '\tdef head(self):\n'
            script += '\t\treturn\n'
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

    def generateSettings(self, overwrite = False):
        print('\nCreating settings files...')
        settingsd = f'{self.settings}.d'
        if not os.path.isdir(settingsd):
            os.mkdir(settingsd)
        exist = os.path.isfile(f'{self.settings}.py')
        if exist and not overwrite:
            overwrite = questionary.confirm(f'Overwrite existing {self.settings}.py?', default=False).ask()
        if not exist or overwrite:
            config = {
                'template': self.template,
                'static': self.static,
                'port': int(self.port),
                'devel': self.devel,
            }
            if not self.appId:
                if os.path.isfile(self.paramconf):
                    with open(self.paramconf) as f:
                        params = f.read()
                        f.close()
                        if params.strip() != '':
                            config = json.loads(params)
                            self.appId = params.get('appId')
            if not self.appId:
                dat = str(random.randint(0, 999999)) + str(time.time()) + self.name
                self.appId = hashlib.sha256(dat.encode()).hexdigest()
            config['appId'] = self.appId
            with open(self.paramconf, 'w') as f:
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

    def generatingTemplate(self, overwrite = False):
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

    def generateServerScript(self, overwrite = False):
        print('\nGenerating server scripts...')
        generate = self.args.all
        if not generate:
            generate = questionary.confirm('Do you wish to generate server startup script?').ask()
        if generate:
            if not self.args.quickstart:
                self.shell = questionary.select(
                    'Which shell do you use?',
                    choices = ['bash','zsh','csh','tcsh','sh'],
                    default = self.shell,
                    use_shortcuts = True
                ).ask()
                self.server_name = questionary.text(f'Script name', default=self.server_name).ask()
                self.mode = questionary.text('File permission mode', default = self.mode).ask()
            shell_path = subprocess.run(f"which {self.shell}", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.strip()
            if not self.args.quickstart:
                shell_path = questionary.path(f'Path to {self.shell}', default=shell_path).ask()
            exist = os.path.isfile(self.server_name)
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

    def generateDaemonScript(self, overwrite = False):
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

    def manageSettings(self):
        retval, message = self.loadSettings()
        if not retval:
            return print(message)
        retval.append(self.quit)
        param = questionary.select("Choose a parameter to edit", retval, use_shortcuts = True).ask()
        if param != self.quit:
            if param == 'template' or param == 'static':
                old_folder = eval(f'self.{param}')
                new_folder = questionary.text(f'New folder name for {param}', default = old_folder).ask()
                if questionary.confirm(f'Change {param} = "{old_folder}" -> "{new_folder}"').ask():
                    subprocess.run(f"mv {old_folder} {new_folder}", shell = True)
                    exec(f'self.params["{param}"] = self.{param} = "{new_folder}"')
                else:
                    return print(self.YELLOW + self.BOLD + '\nCancelled' + self.END)
            elif param == 'appId':
                if questionary.confirm('Change appID').ask():
                    dat = str(random.randint(0, 999999)) + str(time.time()) + self.name
                    self.params[param] = self.appId = hashlib.sha256(dat.encode()).hexdigest()
                else:
                    return print(self.YELLOW + self.BOLD + '\nCancelled' + self.END)
            elif param == 'port':
                old_port = str(self.port)
                new_port = questionary.text('Port', default = old_port).ask()
                if questionary.confirm(f'Change {param} = {old_port} -> {new_port}').ask():
                    self.params[param] = self.port = int(new_port)
                else:
                    return print(self.YELLOW + self.BOLD + '\nCancelled' + self.END)
            elif param == 'devel':
                old_devel = self.devel
                new_devel = questionary.confirm('Development', default = old_devel).ask()
                if questionary.confirm(f'Change {param} = {old_devel} -> {new_devel}').ask():
                    self.params[param] = self.devel = new_devel
                else:
                    return print(self.YELLOW + self.BOLD + '\nCancelled' + self.END)
            try:
                with open(self.paramconf, "w") as f:
                    f.write(json.dumps(self.params))
                    f.close()
                    print(self.GREEN + f'\n{param} is updated successfully!' + self.END)
            except Exception as e:
                return self.error(e)
            finally:
                self.generateSettings(overwrite = True)
                print(self.GREEN + f'\n{self.settings} is updated successfully!' + self.END)
                self.manageServer()
        elif param == self.quit:
            self.exit()

    def manageHandlers(self):
        status, message = self.loadHandlers()
        if not status:
            return print(message)
        routes = list(self.handlers.keys())
        routes.append(self.quit)
        confs = ""
        for key, value in self.handlers.items():
            confs += f"Choice(\"('{key}', {value})\",'{key}'),"
        confs = eval(f"[{confs}]")
        confs.append(self.quit)
        route = questionary.select("Choose a route/handler to edit", confs, use_shortcuts = True).ask()
        if route == self.quit:
            return self.exit()
        handler = self.handlers.get(route)
        form = f"('{route}', {self.handlers.get(route)})"
        action = questionary.select(
            form,
            [
                self.changerouting,
                self.changehandler,
                self.delete,
                self.quit
            ],
            use_shortcuts = True
        ).ask()
        if action != self.quit:
            if action == self.changerouting:
                routes.insert(0, self.addnewuri)
                route = questionary.select("Routes", routes, use_shortcuts = True).ask()
                if route == self.addnewuri:
                    route = questionary.text(f'New URI for {handler}', default = "/").ask()
                if route.strip() == '':
                    route = "/"
                if route in self.handlers:
                    if not questionary.confirm(f'Overwrite settings for "{route}"?', default = False).ask():
                        return print(self.RED + f'\nOverwriting "{route}" is cancelled' + self.END)
                if route in routes:
                    del self.handlers[route]
                self.handlers[route] = handler
            elif action == self.changehandler:
                handlerdirs = os.listdir('.')
                availables = list()
                for entry in handlerdirs:
                    if re.search('Handler$', entry) and os.path.isdir(entry):
                        if os.path.isfile(f"{entry}/view.py"):
                            availables.append(entry)
                self.handlers[route] = questionary.select(f'Handler for "{route}"', availables, default = handler, use_shortcuts = True).ask()
            elif action == self.delete:
                if questionary.confirm('Delete "{route}"?').ask():
                    del self.handlers[route]
            try:
                with open(self.handlerconf, "w") as f:
                    f.write(json.dumps(self.handlers))
                    f.close()
                    print(self.GREEN + f'\n("{route}", {handler}) is updated successfully!' + self.END)
            except Exception as e:
                return self.error(e)
            finally:
                self.generateSettings(overwrite = True)
                print(self.GREEN + f'\n{self.settings} is updated successfully!' + self.END)
                self.manageServer()
        elif action == self.quit:
            self.exit()

    def loadSettings(self):
        status = False
        self.params = dict()
        if os.path.isfile(self.paramconf):
            with open(self.paramconf) as f:
                params = f.read()
                f.close()
                if params:
                    params = json.loads(params)
                    message = self.BOLD + '\nList of Parameters\n\n' + self.END
                    for key, value in params.items():
                        if key == 'port' or key == 'devel':
                            exec(f'self.params["{key}"] = self.{key} = {value}')
                        else:
                            exec(f'self.params["{key}"] = self.{key} = "{value}"')
                        if key != 'appId':
                            message += f"{key} = {value}\n"
                        else:
                            message += f"{key} = " + "*"*12 + "\n"
                    message += '\n' + self.CYAN + str(len(params)) + ' parameter(s) found' + self.END
                    status = list(params.keys())
                else:
                    message = self.RED + '\nParameter is empty...' + self.END
        else:
            message = self.RED + '\nParameter does not exist...' + self.END
        return status, message
    
    def displayAppId(self):
        if not self.appId:
            status, message = self.loadSettings()
        else:
            status = True
        if not status:
            return print(message)
        return print(f"\n{self.BLUE}{self.BOLD}{self.appId}{self.END}\n")

    def loadHandlers(self):
        self.classifyHandlers()
        if os.path.isfile(self.handlerconf):
            with open(self.handlerconf) as f:
                self.handlers = f.read()
                f.close()
            if self.handlers:
                self.handlers = json.loads(self.handlers)
                message = '\n'
                linked = f'{self.BOLD}Linked Handlers{self.END}\n\n'
                unlinked = f'{self.BOLD}Unlinked Handlers{self.END}\n\n'
                if len(self.handlers) == 0:
                    message += linked + "None\n"
                else:
                    for key, value in self.handlers.items():
                        linked += f"('{key}', {value})\n"
                    message += f"{linked}\n"
                if len(self.all_handlers) == 0:
                    message += unlinked + "None\n"
                else:
                    for value in self.all_handlers:
                        unlinked += f"{value}\n"
                    message += f"{unlinked}\n"
                message += '\n' + self.CYAN + str(len(self.handlers)) + ' linked handler(s) and '
                message += str(len(self.all_handlers)) + ' handler(s) are found' + self.END
                status = True
            else:
                message = self.RED + '\nHandler is empty...' + self.END
                status = False
        else:
            message = self.RED + '\nHandler does not exist...' + self.END
            status = False
        return status, message

    def deleteHandler(self):
        self.classifyHandlers()
        options = self.all_handlers
        options.append(self.quit)
        delete = questionary.select('Unlinked handlers to delete', options).ask()
        if delete != self.quit:
            if questionary.confirm(f'Delete {delete}', default = False).ask():
                subprocess.run(f"rm -Rf {delete}", shell = True)
                return print(self.GREEN + f'{delete} is deleted successfully!' + self.END)
        return print(self.YELLOW + '\nCancelled' + self.END)

    def classifyHandlers(self):
        entries = os.listdir('.')
        self.all_handlers = list()
        for entry in entries:
            if re.search('Handler$', entry):
                self.all_handlers.append(entry)
        if os.path.isfile(self.handlerconf):
            with open(self.handlerconf) as f:
                self.handlers = f.read()
                f.close()
            if self.handlers:
                self.handlers = json.loads(self.handlers)
                for _, value in self.handlers.items():
                    self.all_handlers.remove(value)

    def health(self):
        print(f"\n{self.BOLD}Health Status of {self.CYAN}[{self.name}]{self.END}\n")
        host = f"{self.protocol}://{self.domain}:{self.port}"
        status, message = self.loadHandlers()
        fail = list()
        if status:
            for key, value in self.handlers.items():
                curl = subprocess.run("curl " + host + key + " -o /dev/null -w '%{http_code}\n' -s", shell=True, stdout=subprocess.PIPE, encoding=self.encoding)
                form = f"('{key}', {value})"
                if re.search("^0", curl.stdout.strip()):
                    print(self.RED + self.BOLD + "The server seems dead...\n" + self.END)
                    return self.startServerAsDaemon()
                elif re.search("^2", curl.stdout.strip()):
                    print(f"{form}: " + self.GREEN + self.BOLD + "OK" + self.END)
                elif re.search("^3", curl.stdout.strip()):
                    print(f"{form}: " + self.YELLOW + self.BOLD + "Redirect: " + self.END)
                else:
                    print(f"{form}: " + self.RED + self.BOLD + curl.stdout.strip() + self.END)
                    fail.append(form)
            n = len(fail)
            print(self.BOLD + '\nHealth check completed for ' + self.CYAN + str(len(self.handlers)) + self.END + self.BOLD + ' route(s)\n' + self.END)
            if n > 0:
                print('The project has ' + self.BOLD + self.RED + str(n) + self.END + ' problem(s)...\n')
            else:
                print(self.GREEN + 'The system is healthy!\n' + self.END)
        else:
            print(message)
        stay = True
        while stay:
            stay = not questionary.confirm(self.goback).ask()
        return fail

    def startServer(self):
        if self.do_start == self.server_name:
            proc = subprocess.run(f"sh {self.server_name}", shell=True, stdout=subprocess.PIPE, encoding=self.encoding)
        elif self.do_start == self.daemon_name:
            proc = subprocess.run(f"sudo systemctl start {self.daemon_name}", shell=True, stdout=subprocess.PIPE, encoding=self.encoding)
        return proc

    def stopServer(self):
        for pid in self.pid:
            subprocess.run(f"kill {pid}", shell=True)
        return self.statServer()

    def startServerAsDaemon(self):
        self.do_start = questionary.select('Start server?',
            [
                Choice(f'Script ({self.server_name})', self.server_name),
                Choice(f'Daemon ({self.daemon_name})', self.daemon_name),
                self.quit,
            ]
        ).ask()
        if self.do_start == self.quit:
            return
        server = threading.Thread(target=self.startServer, daemon=True)
        server.start()
        stat = 0
        i = 0
        error = False
        while stat == 0:
            time.sleep(.1)
            stat = self.statServer()
            i = i + 1
            if i > 10:
                j = i*.1
                error = 'Timeout (' + str(j) + ')'
                stat = 0
        return error

    def statServer(self):
        self.loadSettings()
        proc = subprocess.run(f"lsof -i:{self.port}", shell=True, stdout=subprocess.PIPE, encoding=self.encoding)
        status = proc.stdout.strip().split("\n")
        if len(status) > 1:
            header = re.sub('\s{1,}','\t',status[0].lower()).split('\t')
            pid_idx = header.index('pid')
            pid = list()
            for i in range(1,len(status) ):
                entry = re.sub('\s{1,}','\t',status[i]).split('\t')
                pid.append(entry[pid_idx])
                i = i + i
            self.pid = list(set(pid))
            return len(self.pid)
        return 0

    def manageServer(self):
        if self.statServer() > 0:
            print(self.GREEN  + self.BOLD + "\nServer is active\n" + self.END)
            action = questionary.select(f'PID = {self.pid}', ['Restart', 'Stop', self.quit]).ask()
            if action != self.quit:
                self.stopServer()
                if action == 'Restart':
                    self.startServerAsDaemon()
        else:
            print(self.RED + self.BOLD + "\nServer is dead\n" + self.END)
            if questionary.confirm('Start service').ask():
                self.startServerAsDaemon()

    def completed(self):
        print(self.GREEN + self.BOLD + '\nCongratulations!\n' + self.END + self.END)
        print('Tornado is ready to work with you now!')
        print('Don\'t forget to "pip install tornado"')

def __main__(banner = True):
    tss = DeracioTSS()
    start = tss.start(banner)
    if start == tss.newproject:
        tss.createProject()
        tss.completed()
    elif start == tss.projecthealth:
        tss.health()
        print()
        return __main__(banner = False)
    elif start == tss.newhandler:
        tss.generateHandler()
        tss.manageServer()
        print()
        return __main__(banner = False)
    elif start == tss.deletehandler:
        tss.deleteHandler()
        print()
        return __main__(banner = False)
    elif start == tss.managerouting:
        tss.manageHandlers()
        print()
        return __main__(banner = False)
    elif start == tss.listhandlers:
        _, message = tss.loadHandlers()
        print(message + '\n')
        stay = True
        while stay:
            stay = not questionary.confirm(tss.goback).ask()
        return __main__(banner = False)
    elif start == tss.showsettings:
        _, message = tss.loadSettings()
        print(message + '\n')
        if questionary.confirm('Display appId', default = False).ask():
            tss.displayAppId()
        stay = True
        while stay:
            stay = not questionary.confirm(tss.goback).ask()
        return __main__(banner = False)
    elif start == tss.configuresettings:
        tss.manageSettings()
    elif start == tss.serverstatus:
        tss.manageServer()
        return __main__(banner = False)
    tss.exit()

if __name__=='__main__':
    __main__()
