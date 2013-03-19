#!/usr/bin/python

import os
import lib.vamtam as vamtam

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

print 'Setting up apache vhost.'
domain = vamtam.option("Enter domain")
home = vamtam.option("Enter home directory", True, ('/home/vamtam/public/%s' % domain))
if vamtam.confirm("Creating vhost configuration for %s at %s" % (domain, home), True):
  os.system("mkdir -p ~/public/%s/{public,log,backup}" % domain)
  os.system("sudo chown -R www-data:www-data ~/public/%s/public" % domain)
  os.system("sudo chmod -R 775 ~/public/%s/public" % domain)

  mydict = {
    'domain': domain,
    'home': home
  }

  myFile = open('/tmp/%s' % domain, 'w')
  myFile.write(vhost_template % mydict)
  myFile.close()

  os.system("sudo mv /tmp/%s /etc/apache2/sites-available/")
  os.system("sudo a2ensite %s" % domain)

  print ''

  print render('Created vhost %(RED)s%(BOLD)s'+domain+'%(NORMAL)s in '+home)

  if(vamtam.confirm("Restart apache?", True)):
    os.system("sudo service apache2 restart")
  else:
    print "Please restart apache manually"

else:
  print "abort"
  exit(0)