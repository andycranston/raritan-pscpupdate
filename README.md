# raritan-pscpupdate

A helper script for performing multiple Raritan PDU firmware upgrades via the PSCP.EXE Windows command.

## ATTENTION! UNDER DEVEOPMENT - NOT READY FOR GENERAL USE!

This script is still under deveopment. Do not use (or use at your own risk).

## Prerequisites

You will need:

+ Windows 10 desktop
+ Python 3
+ The PSCP.EXE command in your PATH

You can get PSCP.EXE from:

[https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html](Download PuTTY: latest release {0.nn})


## Quick start

The `pscpupdate.py` Python helper script makes upgrading multiple Raritan PDUs easier by generating
a Windows batch file called `fwupdate.bat` to run the PSCP.EXE command for each PDU listed in
the `hostlist.txt` file.

Say the `hostlist.txt` file contains:

```
px2study
px3rack
10.1.1.41
10.1.1.42
10.1.1.43
```

and you run:

```
python pscpupdate.py --firmware pdu-px2-030600-46486.bin --pw adminpassword
```

the `pscpupdate.py` will create a Windows batch file called `fwupdate.bat` with the following content:

```
@ECHO OFF
ECHO "Rartitan PDU firmware batch file"
ECHO "To cancel type Control^C"
ECHO "To begin updates"
PAUSE
@ECHO ON
pscp -P 22 -pw adminpassword pdu-px2-030600-46486.bin admin@px2study:/fwupdate
pscp -P 22 -pw adminpassword pdu-px2-030600-46486.bin admin@px3rack:/fwupdate
pscp -P 22 -pw adminpassword pdu-px2-030600-46486.bin admin@10.1.1.41:/fwupdate
pscp -P 22 -pw adminpassword pdu-px2-030600-46486.bin admin@10.1.1.42:/fwupdate
pscp -P 22 -pw adminpassword pdu-px2-030600-46486.bin admin@10.1.1.43:/fwupdate
```

The Windows batch file can then be run by typing:

```
fwupdate
```

The following message will be displayed:

```
"Rartitan PDU firmware batch file"
"To cancel type Control^C"
"To begin updates"
Press any key to continue . . .
```

This is the last chance to stop the batch file by typing Control^C.

If you are happy to proceed then press any key and the copying will begin.

Once firmware file has been copied to each PDU wait a number of
minutes for all the updates to complete and then login to each PDU to
check the upgrade worked.

## Warnings

The password is specified in clear text on the command line (given as the argument to the
`--pw` command line argument) and it is stored in clear text in the `fwupdate.bat` file.

For this reason clear the command prompt screen after running the `pscpupdate.py` Python
program and delete from disk the `fwupdate.bat` file after it has been run successfully.

--------------------------------
End of README.md

