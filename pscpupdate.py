#
# @(!--#) @(#) pscpupdate.py, sversion 0.1.0, fversion 002, 11-january-2021
#
# generate a fwupdate.bat Windows batch file to upgrade
# the firmware on multiple Raitan PDUs via the PSCP.EXE command
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

def expandips(ip):
    octets = ip.split('.')
    
    if len(octets) != 4:
        return [ip]
    
    lastoctet = octets[3]
    
    if lastoctet.find('-') == -1:
        return [ip]

    startend = lastoctet.split('-')
    
    if len(startend) != 2:
        return [ip]
    
    try:
        start = int(startend[0])
        end = int(startend[1])
    except ValueError:
        return [ip]

    iplist = []
        
    while start <= end:
        iplist.append("{}.{}.{}.{}".format(octets[0], octets[1], octets[2], start))
        start += 1

    return iplist

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

        hostnames = expandips(words[0])
        
        for hostname in hostnames:
            outputline = 'pscp -P 22 -pw {} {} {}@{}:/fwupdate'.format(pw, firmware, username, hostname)
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





