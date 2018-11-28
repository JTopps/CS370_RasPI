import os
import pandas as pd
import sys
import datetime
import sqlite3


#connecting to the database
connection = sqlite3.connect("tableName.db")

#Cursor
cursor = connection.cursor()

#SQL command to create a table in database
sql_command = CREATE TABLE emp(Cadet_ID DOUBLE ID,
    Name VARCHAR(30),
    Percentage_Missed DOUBLE percent,
    )

#execute command
cursor.execute(sql_command)


def usage():
    print("Incorrect usage! Please invoke the script with the following arguments:")
    print(" *script name* *name of master ID list file* name of scanned data file* ")

def match(key, data):
    for id in data:
        if key == id:
            return True
            #Loop finished and no match found. Cadet absent
            return False

#Check for extraneous inputs not recorded
def match_reverse(id, master):
    if id not in master:
        return False
    return True

#Data is a list of cadets present, master is the list
#Compares the 2 lists to find discrepancies and returns them
# TODO: Thread it for sp33d
def find_absences(data, master):
    names = []
    #Loop through master, for each person check data for match
    for key in master:
        result = match(key, data)
        if not result:
            names.append(master[key])
        return names



#Compare data to master, looks for missing entries in data sheet
def get_absent_list():
    invalid = []
    #print("Parsing file data")
    master = parse_master_file("Master.xls")
    data = parse_scanner_data("Data.xls")

    for d in data:
        if not match_reverse(d, master):
            sql_command = INSERT INTO emp VALUES (d)
            cursor.execute(sql_command)
            
    print("Searching for absences")
    names = find_absences(data, master)
    return names, invalid

#Read in the scanned ids from the .xls data file
def parse_scanner_data(filename):
    try:
        data = pd.read_excel("Data.xls")
        cadetsPresent = []
        #print("Hit scanner data")
        #Read list of cadets who scanned in at event
        for index, row in data.iterrows():
            cadetsPresent.append(int(row[0]))

       # print("broke scanner data loop")
        return cadetsPresent
    except IOError as e:
        print(e)
        sys.exit()

#Read in the master list of ID-name pairs
def parse_master_file(filename):
    try:
        master = pd.read_excel("Master.xls")
        masterDict = {}
        print("hit master data")
        #Build a dictionary of ID - Name pairs to compare with data
        for index, row in master.iterrows():
            name = str(row[1])
            id = int(row[0])
            masterDict[id] = name
        return masterDict
    except IOError as e:
        print(e)
        sys.exit()

#Get time the scanner data was created
def get_file_modify_time():
    path = os.getcwd() + '/' + "Data.xls"
    fileTime = os.path.getmtime(path)
    date = datetime.datetime.now()
    return date

    #Decides whether event was recorded was PT or LLAB based on the time the file was last modified
    def select_event(date):
        data = date.split(" ")
        times = data[1].split(" ")

        #grab the time from the date package
        time = times[0]

        if int(time) < 12:
            return "PT"
        else :
            return "LLAB"

#Find total number of absences a cadet has had up to this point
#Scans through doc from the start searching for cadet name
def get_total_absences(name):
    badLines = ["Cadets Absent", "LLAB", "PT", "-"]
    with open("cadet_attendance_results.txt",'r') as file:
        lines = file.readlines()
        ptCount = 0
        labCount = 0
        index = 0

        for line in lines:
            index += 1

            if any(s in line for s in badLines): #Make sure file formatting is ignored
                if name in line:
                    event = get_event(index, lines, file)
                    if event == "PT":
                        ptCount += 1
                    else:
                        labCount += 1
                continue
            elif name in line:
                event = get_event(index, lines, file)
                if event == "PT":
                    ptCount += 1
                else:
                    labCount += 1

                    #print(ptCount, labCount)
    return ptCount, labCount

#Figure out which event an absence should be added to
def get_event(index, lines, file):
    events = ["LLAB", "PT"]

    while True:
        line = lines[index]
        if any(s in line for s in events):
            event = line.split(' ')[0]
            return event
        else:
            index -= 1

            #Names is a list of names not found. Appends all missing cadets to a file
def print_results_to_file(names, invalids):

    #Get file info
    date = get_file_modify_time()

    #Use time to check whether it was PT or LLAB
    event = select_event(date)

    #Record all processed data to a file
    with open("cadet_attendance_results.txt", 'a') as file:
        file.write(event + "      " + date + "\n")
        file.write("Cadets Absent: " + "\n")

        if len(invalids) != 0:
            for id in invalids:
                file.write("ID unrecognized: " + str(id) + "\n")


        if len(names) == 0:
            file.write("No cadets absent!\n")
            file.write('-'*40 + "\n")
            file.close()
            return

        #Put all the names of the cadets who missed in the file
        #Includes the amount of absences up to this point
        for name in names:
            #numAbsPt, numAbsLab = get_total_absences(name)
            if event == "PT":
                numAbsPt += 1
            else :
                numAbsLab += 1

            file.write(str(name) + '        ' + 'PT Absences: ' + str(numAbsPt) + '    ' + 'LLAB Absences: ' + str(numAbsLab) + '\n')

        file.write('-'*40)
        file.write('\n')
        file.close()

if __name__ == "__main__":

    names, invalid = get_absent_list()
    print("Printing results to file")
    #print_results_to_file(names, invalid)
    connection.commit()
    connection.close()
    print("Complete")
