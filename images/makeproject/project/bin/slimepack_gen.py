#!/usr/bin/env python
from Boinc import database, boinc_project_path, boinc_db, sched_messages
import re, os


threshold = 1000
def _writeLog(self, mode, *args):
    """
    A private helper function for writeing to the log
    """
    self.log.printf(mode, *args)
        
def logCritical(self, *messageArgs):
    """
    A helper function for logging critical messages
    """
    self._writeLog(sched_messages.CRITICAL, *messageArgs)

def logNormal(self, *messageArgs):
    """
    A helper function for logging normal messages
    """
    self._writeLog(sched_messages.NORMAL, *messageArgs)

def logDebug(self, *messageArgs):
    """
    A helper function for logging debug messages
    """
    self._writeLog(sched_messages.DEBUG, *messageArgs)

def GenerateWork(unassigned):
    path = boinc_project_path.project_path("slimepack_data")
    input_path = path + "/slimepack_workgen_last"
    input_str = ''
    cmdProto = 'create_work --appname slimepack --wu_template templates/seeds_in --result_template ../templates/slimepack_out --command_line "-s $(('
    
    try:
        with open(input_path) as input_file:
        input_str = input_file.read()
    except OSError as e:
        logCritical("Unable to open input file: %s. Assuming no work has been generated for this Project!\n", e.filename)
        input_str = "0"
    for i in range(threshold - unassigned):
        num = i + int(input_str)
        wu_name = 'slimepack_' + num
        cmd = cmdProto + num * 33554432 + ')) -e $(((' + num + 1 * 33554432 + '))" --wu_name ' + wu_name
        try:
            os.system(cmd)
        except OSError as e:
            logCritical("Unable to generate work! Error: %s \n", e.strerror)
    amount = threshold - unassigned
    input_str = amount + int(input_str)
    try:
        with open(input_path, "w") as input_file:
            input_file.write(input_str)
    except OSError as e:
        logCritical("Unable to write last workunit number information to file! Error: %s\n", e.strerror)

def do_pass(result):
    appid = result.appid
    unassigned = database.Results.count(appid=appid, hostid=None)
    if(unassigned < threshold):
        GenerateWork()
def CheckWork():
    database.connect()
    app=database.Apps.find1(name='slimepack')
    database.close()

    while(1):
        database.connect()
        do_pass(app)
        database.close()
        time.sleep(120)
