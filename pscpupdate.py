#
# @(!--#) @(#) fwviasnmp.py, sversion 0.1.0, fversion 008, 06-january-2021
#
# get the firmware revision of a Raritan PDU via SNMP v2c
#

#
# Help from:
# ---------
#
#    https://help.raritan.com/px2-2000/v3.5.0/en/#35085.htm
#    https://help.raritan.com/px3-5000/v3.6.1/en/#35085.htm
#

##############################################################################

#
# imports
#

import sys
import os
import argparse
import random
import socket
import select

##############################################################################

#
# globals
#

##############################################################################

def pscpupdate(hostlist, batchfile, username, firmware, pw):
    global   progname

    if not os.path.isfile(firmware):
        print('{}: unable to access firmware file "{}"'.format(progname, firmware), file=sys.stderr)
        return 1
            
    try:
        hostf = open(hostlist, 'r', encoding='utf-8')
    except IOError:
        printf('{}: unable to open hostlist file "{}" for reading'.format(progname, hostlist), file=sys.stderr)
        return 1
    
    try:
        batchf = open(batchfile, 'w', encoding='utf-8')
    except IOError:
        printf('{}: unable to open batch file "{}" for writing'.format(progname, batchfile), file=sys.stderr)
        return 1
    
    print('@ECHO OFF', file=batchf)
    print('ECHO "Rartitan PDU firmware batch file"', file=batchf)
    print('ECHO "To cancel type Control^C"', file=batchf)
    print('ECHO "To begin updates"', file=batchf)
    print('PAUSE', file=batchf)
    print('@ECHO ON', file=batchf)
    
        
    linenum = 0
    
    for rawline in hostf:
        linenum += 1
        
        line = rawline.strip()
        
        if len(line) == 0:
            continue
        
        if line[0] == '#':
            continue
        
        words = line.split()
        
        if len(words) == 0:
            continue

        outputline = 'pscp -P 22 -pw {} {} {}@{}:/fwupdate'.format(pw, firmware, username, words[0])

        print(outputline)
        
        print(outputline, file=batchf)
        
        batchf.flush()

    batchf.close()
            
    hostf.close()
    
    return 0    

##############################################################################

def main():
    global progname
    global DEBUG
    
    parser = argparse.ArgumentParser()
        
    parser.add_argument('--hostlist',
                        help='file containing list of PDU hostnames/IP addresses',
                        default='hostlist.txt')
                        
    parser.add_argument('--batchfile',
                        help='name of batch file to create',
                        default='fwupdate.bat')
                        
    parser.add_argument('--username',
                        help='username to access PDU',
                        default='admin')
                        
    parser.add_argument('--firmware',
                        help='name of firmware file',
                        required=True)
                        
    parser.add_argument('--pw',
                        help='password',
                        required=True)
                        
    args = parser.parse_args()
    
    retcode = pscpupdate(args.hostlist, args.batchfile, args.username, args.firmware, args.pw)
    
    return retcode

##############################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file





