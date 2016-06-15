# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Addition IT Solutions Pvt. Ltd. (<http://www.aitspl.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from ftplib import FTP
import logging
import subprocess
import os
import tempfile

from openerp.osv import osv
import openerp.service.db as DB
import openerp.tools.config as CONFIG
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)

p = subprocess.Popen(["locate", "/etc/*-server.conf"], stdout=subprocess.PIPE)
output, err = p.communicate()
filepath = output.split('\n')[0]

# Setup Configuration
fp = open(filepath,'r')
for line in fp.readlines():
    if line.find('=') > 0:
        key, val = line.split('=')
        if key.startswith('db_'):
            CONFIG[key.rstrip()] = val.strip(' \n')

class addsol_res_users(osv.osv):
    _inherit = 'res.users'

    def run_autobackup_database(self, cr, uid, context=None):
        _logger.info("Auto Backup Starts...")
        user = self.browse(cr, SUPERUSER_ID, uid, context)
        host = '127.0.0.1'
        port = '8021'
        foldername = ''
        ftp_url = (user.company_id.document_ftp_url).replace('ftp://','')
        ftp_user = user.company_id.document_ftp_user
        ftp_passwd = user.company_id.document_ftp_passwd
        for url in ftp_url.split('/'):
            if url.find(':') > 0:
                host, port = url.split(':')[0], url.split(':')[1]
            else:
                foldername += '/'+ url
        db_list = DB.exp_list()
        for db in db_list:
            backup_db = DB.exp_dump(db)
            values = {
                      'host': str(host),
                      'port': str(port),
                      'timeout': 10.0,
                      'foldername': foldername,
                      'backup_db': backup_db,
                      'ftp_user': ftp_user,
                      'ftp_passwd': ftp_passwd,
                      'db_name': db,
            }
            self.get_ftp(cr, uid, values, context)
        _logger.info("Auto Backup Completed...")

    def get_ftp(self, cr, uid, values, context=None):
        ftp = FTP()
        host = values.get('host','127.0.0.1')
        port = values.get('port','8021')
        timeout = values.get('timeout',10.0)
        try:
            ftp.connect(host, port, timeout)
        except:
            _logger.info('FTP %s:%s Connection Refused!'%(host,port))
        user = values.get('ftp_user')
        passwd = values.get('ftp_passwd')
        foldername = values.get('foldername')
        backup_db = values.get('backup_db')
        try:
            ftp.login(user, passwd)
        except:
            _logger.info('Authentication Failed! User: %s'%(user,))
        db = values.get('db_name')
        data_file = tempfile.NamedTemporaryFile(delete=False)
        data_file.write(backup_db.decode('base64'))
        data_file.close()
        filename = db +'_'+time.strftime('%Y-%m-%d')+'.dump'
        #fw = open(filename,'w')
        #fw.write(backup_db.decode('base64'))
        #fw.close()
        ftp.cwd(foldername)
        ftp.storbinary('STOR ' + filename, open(data_file.name,'rb'))
        #ftp.storbinary('STOR ' + filename, open(filename,'rb'))
        ftp.close()
        os.unlink(data_file.name)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: