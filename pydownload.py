#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ftplib import FTP # ftputil is good for this, but ftplib comes with the py install

class Ftp:

    def __init__(self, hostname, username, password, port = 21):

        print '\nConnecting to %s on port %d' % (hostname, port)

        ftp = FTP()

        try:
            ftp.connect(hostname, port)
        except:
            raise Exception('\n\nThe hostname %s:%d could not be found/connected to\n' % (hostname, port))

        try:
            ftp.login(user=username, passwd=password)
            self.start = ftp.pwd()
            
            print 'Login Successful: %s\n' % username
        except: #ftplib.error_perm
            raise Exception('\n\nUnable to login using the credentials provided: \nHost: %s\nUser: %s\nPass: %s\n\n' % (hostname, username, password))

        self.ftp = ftp
        self.hostname = hostname

    def end(self):
        try:
          self.ftp.quit()
        except:
            pass
        print '\n\nConnection to %s has been closed\n' % self.hostname

    def ls(self):
        return self.ftp.nlst()

    def get(self, file):
        return self.ftp.retrbinary('RETR ' + file, open('%s/%s' % (self.hostname, file), 'wb').write)

    def cwd(self, file):
        return self.ftp.cwd(file)

    def pwd(self):
        return self.ftp.pwd()

    def download(self):
        print 'Downloading Files:'
        self._dl()
        print '\nAll Files Downloaded'
        self.end()

    def _dl(self, changedir='/'):

        if changedir is not '/':
            self.cwd(changedir)
        current = self.pwd()
        folders = []
        files = self.ls()

        for file in files:
            try:
                self.cwd(file)
                if current is not '/':
                    path = '%s%s/%s' % (host, current, file)
                else:
                    path = '%s%s%s' % (host, current, file)
                if not os.path.exists(path):
                    os.makedirs(path)
                    if path != '%s/.' % host:
                        folders.append(path)

                self.cwd(current)
            except:
                if current is not '/':
                    self.get('%s/%s' % (current, file))
                else:
                    self.get('%s' % file)
                print '    %s' % file
        try:
            for fold in folders:
                print '  /%s' % fold
                self._dl(fold.replace(host, ''))
        except:
            pass