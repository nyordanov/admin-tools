#!/usr/bin/python3

import os
import lib.vamtam as vamtam
from glob import glob
from colorama import Fore, Back, Style

vhost_template = '''
# domain: %(domain)s
# public: %(home)s

<VirtualHost *:80>
  # Admin email, Server Name (domain name), and any aliases
  ServerAdmin webmaster@%(domain)s
  ServerName  %(domain)s
  ServerAlias %(domain)s

  # Index file and Document Root (where the public files are located)
  DirectoryIndex index.html index.php
  DocumentRoot %(home)s/public

  # Log file locations
  LogLevel warn
  ErrorLog  %(home)s/log/error.log
  CustomLog %(home)s/log/access.log combined
</VirtualHost>
'''.strip()

print("Setting up apache vhost.")
domain = vamtam.option("Enter domain")
home = vamtam.option("Enter home directory", True, os.path.expanduser('~/public/%s' % domain))
if vamtam.confirm("Creating vhost configuration for %s at %s" % (domain, home), True):
  vamtam.mkdir_p("%s/public" % home)
  vamtam.mkdir_p("%s/backup" % home)
  vamtam.mkdir_p("%s/log" % home)
  os.system("mkdir -p %s/{public,backup,log}" % home)
  os.system("sudo chown -R www-data:www-data ~/public/%s/public" % domain)

  mydict = {
    'domain': domain,
    'home': home
  }

  vhost = open(('/tmp/%s' % domain), 'w')
  vhost.write(vhost_template % mydict)
  vhost.close()

  os.system("sudo mv /tmp/%s /etc/apache2/sites-available/" % domain)
  os.system("sudo a2ensite %s" % domain)

  print('')

  print('Created vhost '+Fore.RED+domain+Style.RESET_ALL+' in '+home)

  if(vamtam.confirm("Restart apache?", True)):
    os.system("sudo service apache2 restart")
  else:
    print("Please restart apache manually")

else:
  print("abort")
  exit(0)