"""
DeracioTSS -- Tornado Startup Script
Copyright (c) 2023 DERaC, LLC.

** Donations **
BTC: 3GSGPvNeSv1j9LobjzZWiCL2Vd29rpmyXE
ETH: 0x8928534c8beca7875059edce7afae202836a0d4c
"""
#! python3
# -*- coding: utf-8 -*-
import os, sys, re, subprocess, questionary

def main():
    banner = """
_____________________________________________________________________
    _____                                    ______     __       __  
    /    )                           ,         /      /    )   /    )
---/----/----__---)__----__----__--------__---/-------\--------\-----
  /    /   /___) /   ) /   ) /   ' /   /   ) /         \        \    
_/____/___(___ _/_____(___(_(___ _/___(___/_/______(____/___(____/___                                                                  
"""
    print(banner)
    print('Tornado Startup Script v1.0.0')
    print('Copyright (c) 2023 DERaC, LLC.')
    print('MIT License\n')
    if questionary.confirm('Starting a new project?').ask():
        name = questionary.text(f'Let me know the project name').ask()
        if name == '':
            print('\nProject name cannot be blank...\n')
            exit()
        name = re.sub('\s', '_', name)
        if questionary.confirm(f'Create {name}?').ask():
            template = 'templates'
            static = 'static'
            app_name = f'{name}.py'
            if not questionary.confirm(f'Use default template folder name ({template})?').ask():
                template = questionary.text(f'Template folder name').ask()
            if not questionary.confirm(f'Use default static file folder name ({static})?').ask():
                static = questionary.text(f'Static file folder name').ask()
            port = questionary.text(f'Which port will you use?', default='8000').ask()
            if not questionary.confirm(f'Use default app file name ({app_name})?').ask():
                app_name = questionary.text(f'App file name').ask()
            python_path = subprocess.run("which python3", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
            python_path = questionary.path(f'Path to python3', default=python_path.stdout.strip()).ask()
            
            print('\nStart creating files...')

            exist = os.path.isfile(app_name)
            if exist:
                overwrite = questionary.confirm(f'Overwrite existing {app_name}?', default=False).ask()
            if not exist or overwrite:
                script = f'#!{python_path}\n'
                script += """
# -*- coding: utf-8 -*-
import tornado.ioloop, tornado.web
import os, re, json, threading

# Define fundamental parameters for the service
# These params can be alternatively in, i.e., settings.py
"""
                script += f'__template__ = "{template}"\n'
                script += f'__static__ = "{static}"\n'
                script += f'__port__ = {port}\n\n'

                script += """
# Classes are separately stored in external files
# Follow the structure rule of each project
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        params = {
            'title': 'Deracio Tornado/Python Setupper'
        }
        self.render("index.html", params = params)

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
                    with open(app_name, 'w') as f:
                        f.write(script)
                        f.close()
                    print(f'Folder {app_name} is generated successfully!')
                except Exception as e:
                    print(e)
                    exit()
            else:
                print(f'{app_name} already exists...')

            print('\nCreating template folder...')

            if not os.path.isdir(template):
                try:
                    os.mkdir(template)
                    print(f'Folder {template} is created successfully!')
                except Exception as e:
                    print(e)
                    exit()
            else:
                print(f'Folder {template} already exists...')

            print()
            
            exist = os.path.isfile(f'{template}/index.html')
            if exist:
                overwrite = questionary.confirm(f'Overwrite existing {template}/index.html?', default=False).ask()
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
    <div class="uk-text-muted">Tornado is now working!</div>
</div>
{% end %}
</body>
</html>
"""
                try:
                    with open(f'{template}/index.html', 'w') as f:
                        f.write(script)
                        f.close()
                    print(f'{template}/index.html is generated successfully!')
                except Exception as e:
                    print(e)
                    exit()
            else:
                print(f'{template}/index.html already exists...')

            print('\nCreating static file folder...')

            if not os.path.isdir(static):
                try:
                    os.mkdir(static)
                    print(f'Folder {static} is created successfully!')
                except Exception as e:
                    print(e)
                    exit()
            else:
                print(f'Folder {static} already exists...')

            print()

            if questionary.confirm('Do you wish to generate server startup script?').ask():
                shell = questionary.select(
                    'Which shell do you use?',
                    choices = ['bash','zsh','csh','tcsh','sh'],
                    default = 'bash'
                ).ask()
                shell_path = subprocess.run(f"which {shell}", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
                shell_path = questionary.path(f'Path to {shell}', default=shell_path.stdout.strip()).ask()
                server_name = questionary.text(f'Script name', default="server.sh").ask()
                mode = questionary.text('File permission mode', default='0755').ask()
                exist = os.path.isfile(server_name)
                if exist:
                    overwrite = questionary.confirm(f'Overwrite existing {server_name}?', default=False).ask()
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
                    script += f'SERVER="{python_path}"\n'
                    script += """
# App file name that includes 'application' to 'listen'
### For example:
### application = tornado.web.Application(...)
### application.listen(...)
"""
                    script += f'APP="{ app_name }"\n'
                    script += """
# Startup script
echo "Starting $APP_NAME"
$SERVER $HOME_DIR/$APP
"""
                    try:
                        with open(server_name, 'w') as f:
                            f.write(script)
                            f.close()
                        print(f'\n{ server_name } is generated successfully!')
                        if subprocess.call(["chmod", mode, server_name]) == 0:
                            print(f'Permission is set {mode} for { server_name }\n')
                        
                    except Exception as e:
                        print(e)
                        exit()
                else:
                    print(f'{ server_name } already exists...\n')

                if questionary.confirm('Do you wish to generate system daemon script?').ask():
                    daemon_name = questionary.text('System daemon file name', default='tornadod.service').ask()
                    description = questionary.text('Brief system description', default='Tornado Web Service').ask()
                    cwd = questionary.path('Working directory', default=os.getcwd()).ask()
                    user = questionary.text('User name to execute', default='nobody').ask()
                    group = questionary.text('Group name to execute', default='nobody').ask()
                    mode = questionary.text('File permission mode', default='0755').ask()

                    exist = os.path.isfile(daemon_name)
                    if exist:
                        overwrite = questionary.confirm(f'Overwrite existing {daemon_name}?', default=False).ask()
                    if not exist or overwrite:
                        script = """
[Unit]
# Clarify to descrive this service
"""
                        script += f'Description={description}\n'
                        script += """
[Service]
# Full path to your project
"""
                        script += f'WorkingDirectory={cwd}\n'
                        script += '# Full path to your server startup script\n'
                        script += f'ExecStart="{cwd}/{server_name}"'
                        script += """
Restart=always
RestartSec=3s
Type=simple

# User and group names to launch the service
# Avoid root or equivalent user/group
"""
                        script += f'User={user}\n'
                        script += f'Group={group}\n'
                        script += """
[Install]
WantedBy=multi-user.target
"""
                        try:
                            with open(daemon_name, 'w') as f:
                                f.write(script)
                                f.close()
                            print(f'{ daemon_name } is generated successfully!')
                            mode = '0755'
                            if subprocess.call(["chmod", mode, daemon_name]) == 0:
                                print(f'Permission is set {mode} for { daemon_name }')
                        except Exception as e:
                            print(e)
                            exit()
                        finally:
                            print(f'\nFollow the procedure below to daemonize { daemon_name }')
                            print(f'1. sudo mv { daemon_name } /etc/systemd/system/')
                            print(f'2. sudo systemctl daemon-reload')
                            print(f'3. sudo systemctl enable { daemon_name } --now')
        print('\nCongratulations!')
        print('Tornado is ready to work with you now!')
        print('Don\'t forget to "pip install tornado"')
    print('\nDonations are welcome!\n')
    print('BTC: 3GSGPvNeSv1j9LobjzZWiCL2Vd29rpmyXE\n')
    print('ETH: 0x8928534c8beca7875059edce7afae202836a0d4c\n')
    print('bye...\n')

if __name__=='__main__':
    main()
