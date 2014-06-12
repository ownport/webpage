#!/usr/bin/env python
#
#   bottle dev server
#
import os
import sys
import time
import bottle
import logging
import argparse    

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = data_path = os.path.join(CURRENT_DIR, 'data')

# monkey patching for BaseHTTPRequestHandler.log_message
def log_message(obj, format, *args):
    logging.info("%s %s" % (obj.address_string(), format % args))


@bottle.route('/')
@bottle.route('/<filename:path>')
def index(filename=None):

    if not filename:
        filename = 'index.html'

    elif filename == 'timeout':
        time.sleep(3)
        filename = 'index.html'
    
    elif filename.startswith('attachment'):
        if filename == 'attachment-unquoted':
            bottle.response.headers['content-disposition'] = 'attachment; filename=text-file-unquoted.txt'
            filename = 'text-file.txt'
        else:
            bottle.response.headers['content-disposition'] = 'attachment; filename="text-file.txt"'
            filename = 'text-file.txt'

        bottle.response.content_type = 'text/plain'
        return open(os.path.join(DATA_PATH, filename)).read()      

    elif filename.endswith('.xml.gz'):
        return bottle.static_file(filename, root=DATA_PATH, 
                                mimetype='application/octet-stream')        

    elif filename.endswith('.gz'):
        return bottle.static_file(filename, root=DATA_PATH, 
                                mimetype='application/gzip')        

    elif filename == 'index-western-encoding.html':
        bottle.response.content_type = 'text/html; charset=iso-8859-1'
        return u'This will be sent with ISO-8859-1 encoding.'

    return bottle.static_file(filename, root=DATA_PATH)


parser = argparse.ArgumentParser(description='dev-serv.py') 
parser.add_argument('--logfile', type=str, help='log file')
parser.add_argument('--datapath', type=str, help='path to data files')
args = parser.parse_args()

if args.datapath:
    DATA_PATH = args.datapath

if args.logfile:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=args.logfile,
                        filemode='w')

    from BaseHTTPServer import BaseHTTPRequestHandler
    BaseHTTPRequestHandler.log_message = log_message
    
bottle.run(host='localhost', port=8888, debug=True)
