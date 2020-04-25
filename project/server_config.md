## Initial server setup
https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04

## After setting up ssh key...
https://www.digitalocean.com/community/questions/error-permission-denied-publickey-when-i-try-to-ssh?answer=44730

## Create user
```
adduser username
```

## Give sudo privileges
```
usermod -aG sudo username
```

## Set up firewall (have to do this from root)
```
ufw allow OpenSSH
ufw enable
```

# Next steps
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

## Important--log in as user, not root!

## Update list of available packages
```
sudo apt update
```

## Upgrade packages
```
sudo apt upgrade
```

## Install required packages for project
```
sudo apt install python3-pip python3-dev libpq-dev nginx curl
```

## Upgrade pip
```
sudo -H pip3 install --upgrade pip
```

## Install venv
```
sudo -H pip install virtualenv
```

## Create venv called 'env'
```
virtualenv env
```

## Activate it
```
source env/bin/activate
```

## Install Django and Gunicorn
```
pip install django gunicorn
```

## Clone repo
```
git clone https://github.com/heds1/ScoreStuff.git
cd ScoreStuff
```

## Install dependencies
```
pip install -r requirements.txt
```

## Add IP address and domain of site to settings
(also add localhost to check dev server)
```
nano ~/ScoreStuff/project/project/settings_production.py

ALLOWED_HOSTS = [
    '.scorestuff.nz',
    '128.199.238.34',
    'localhost'
]
```

## Create exception in firewall for port 8000
```
sudo ufw allow 8000
```

## Add Django secret key to env var
SCORESTUFF_SECRET_KEY='...'
export SCORESTUFF_SECRET_KEY

## Check dev server (no static files at this point)
```
~/ScoreStuff/project/manage.py runserver 0.0.0.0:8000
```
Go to 128.199.238.34:8000. Check it works, then ctrl-C to stop dev server.

## Test Gunicorn can serve project
```
gunicorn --chdir ~/ScoreStuff/project --bind 0.0.0.0:8000 project.wsgi
```
All good.

## Stop Gunicorn and deactivate venv.
```
Ctrl+C
deactivate
```

## Make and open systemd socket file
```
sudo nano /etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

## Make systemd service file
Note that SCORESTUFF_SECRET_KEY was defined and exported into environment earlier
```
sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Environment="SCORESTUFF_SECRET_KEY=SCORESTUFF_SECRET_KEY"
User=hedley
Group=www-data
WorkingDirectory=/home/hedley/ScoreStuff/project
ExecStart=/home/hedley/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          project.wsgi:application

[Install]
WantedBy=multi-user.target
```

## Start and enable the socket
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

## Check status
sudo systemctl status gunicorn.socket

## Check for existence of gunicorn.sock file within the /run directory. Should output /run/gunicorn.sock: socket
file /run/gunicorn.sock

# testing socket activation
# at the mo, we've only started the gunicorn.socket unit, so the
# gunicorn.service will not be active yet since the socket has not received any
# connections. check this: should say inactive (dead)
sudo systemctl status gunicorn

## Test socket activation mechanism; should return the html output from the app
curl --unix-socket /run/gunicorn.sock localhost

## Create and open a new server block
```
sudo nano /etc/nginx/sites-available/ScoreStuff

server {
    listen 80;
    server_name 128.199.238.34 .scorestuff.nz;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/hedley/ScoreStuff/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

## Enable the file by linking it to the sites-enabled directory
sudo ln -s /etc/nginx/sites-available/ScoreStuff /etc/nginx/sites-enabled

## Test config for syntax errors
sudo nginx -t

## Restart nginx when you change config file
sudo systemctl restart nginx

## Open up firewall to normal traffic on port 80. also remove port 8000 since we no longer need access to dev server.
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'




gunicorn --chdir ~/ScoreStuff/project --bind 0.0.0.0:8000 project.wsgi