__author__ = 'Ciancetta Thomas, Francesco Maria Giacomi'
__version__ = '01.02 2020-12-14'

import codecs
import datetime
import json
import mysql.connector
import os
import sys
import time
import wmi
import yaml

import urllib.request as urllib2


def main():
    """ Reads the list of endpoints and writes information on output files """
    try:  # Try opening log file, else create it
        file_log = open('..\\log\\log.log', 'a')
    except:
        print('Log file not found, creating new one...\n')
        file_log = open('..\\log\\log.log', 'a+')
        logMessage(file_log)
        file_log.write('Error: Missing log file, created new."\n')

    # Functions to write log file
    logMessage(file_log)
    file_log.write('Inizio esecuzione: ')
    dataEsecuzione(file_log)

    config = []
    try:  # Try looking for config file parameters(output path, mac separator, sync), else use default settings
        file_yaml = open('config.yaml', 'r')
        dictionary = yaml.safe_load(file_yaml)
        for key, value in dictionary.items():
            config.append(value)
        
    except:
        print('Output file parameters not found, using default...\n')
        config = ["..\\flussi\\osversion.csv", "..\\flussi\\netinfo.csv", "..\\flussi\\usb.csv", "..\\flussi\\eventviewer.csv", "..\\flussi\\product.csv", "..\\flussi\\uptime.csv", "..\\flussi\\updatepending.csv", "..\\flussi\\logicaldisk.csv", ";", "no", "sync_path", "192.168.1.202", "admin", "admin", "ciaotest"]
        logMessage(file_log)
        file_log.write('Error: Missing output file parameters, used default."\n')

    #Output files
    output_osversion = open(config[0], 'w')
    output_netinfo = open(config[1], 'w')
    output_usb = open(config[2], 'w')
    output_eventviewer = open(config[3], 'w')
    output_product = open(config[4], 'w')
    output_uptime = open(config[5], 'w')
    output_updatepending = open(config[6], 'w')
    output_logicaldisk = open(config[7], 'w')

    try:  # Main program for writing info in output files
        with open('..\\flussi\\computers.csv') as input:

            for line in input:
                output_osversion.write(line.strip('\n'))
                output_osversion.write(';')
                output_netinfo.write(line.strip('\n'))
                output_netinfo.write(';')
                output_uptime.write(line.strip('\n'))
                output_uptime.write(';')

                pc = str(line).strip('"')[:-2]

                if ping(pc) == False:  # Executes a ping to the endpoint to see if it's reachable
                    output_osversion.write('"Il seguente endpoint non è raggiungibile"\n')
                    output_netinfo.write('"Il seguente endpoint non è raggiungibile"\n')
                    output_eventviewer.write(f'"{pc}";"Il seguente endpoint non è raggiungibile"\n')
                    output_product.write(f'"{pc}";"Il seguente endpoint non è raggiungibile"\n')
                    output_uptime.write('"Il seguente endpoint non è raggiungibile"\n')
                    output_logicaldisk.write(f'"{pc}";"Il seguente endpoint non è raggiungibile"\n')

                    logMessage(file_log)
                    file_log.write(pc)
                    file_log.write(' non è raggiungibile"\n')
                    continue

                # Series of function to write everything in files and trace
                try:  # Try OS
                    writeOS(pc, output_osversion)
                    logMessage(file_log)
                    file_log.write(pc)
                    file_log.write('";"WriteOS: OK";"')
                except:
                    logMessage(file_log)
                    file_log.write(pc)
                    file_log.write('";"WriteOS: Error";"')

                try:  # Try NIC
                    writeNIC(pc, output_netinfo, config[8], config)
                    file_log.write('MACVendor: OK";"')
                    file_log.write('WriteNIC: OK";"')
                except:
                    file_log.write('MACVendor: Error";"')
                    file_log.write('WriteNIC: Error";"')

                try:  # Try Event
                    if config[9] == 'yes':
                        try:
                            writeEvent(pc, output_eventviewer)
                            file_log.write('WriteEvent: OK";"')
                        except:
                            file_log.write('WriteEvent: Error";"')
                    else:
                        file_log.write('WriteEvent: NO";"')
                except:
                    file_log.write('WriteEvent: Error";"')

                try:  # Try Product
                    writeProduct(pc, output_product)
                    file_log.write('WriteProduct: OK";"')
                except:
                    file_log.write('WriteProduct: Error";"')

                try:  # Try Uptime
                    output_uptime.write(f'"Uptime: {str(get_uptime(pc))}";')
                    output_uptime.write(f'Ticks: "{str(round(time.time()))}"\n')
                    file_log.write('WriteUptime: OK";"')
                except:
                    file_log.write('WriteUptime: Error";"')

                try:  # Try LogicalDisk
                    writeDisk(pc, output_logicaldisk)
                    file_log.write('WriteLogicalDisk: OK"\n')
                except:
                    file_log.write('WriteLogicalDisk: Error"\n')

        try:  # Try Updatepending
            writeUpdate(output_updatepending)
            logMessage(file_log)
            file_log.write('WriteUpdate: OK";"')
        except:
            logMessage(file_log)
            file_log.write('WriteUpdate: Error";"')

        try:  # Try USB
            writeUSB(output_usb)
            file_log.write('WriteUSB: OK";"')
        except:
            file_log.write('WriteUSB: Error";"')

        try:  # Try Sync
            if config[10] != 'sync_path':
                os.system('xcopy ..\\flussi ' + config[10] + ' /q /i /s /e /y /k')
            else:
                file_log.write('Sync: No"\n')
        except:
            file_log.write('Sync: Error"\n')

        # Functions to write log file
        logMessage(file_log)
        file_log.write('Termine Esecuzione: ')
        dataEsecuzione(file_log)

    except:
        print('Error: Something went Horribly wrong, ending program...')
        logMessage(file_log)
        file_log.write('Error: Something went wrong"\n')

        # Functions to write log file
        logMessage(file_log)
        file_log.write('Termine Esecuzione: ')
        dataEsecuzione(file_log)
        sys.exit(1)
    sys.exit(0)


def writeNIC(pc, file_output, mac_sep, config):
    """ Writes information about Network Interface Card"""
    i = 1
    val = []
    array_load_key = []
    array_load_value = []
    for scheda in wmi.WMI(pc).Win32_NetworkAdapterConfiguration(
            IPEnabled=True):  # Repeats the function for the number of NIC
        file_output.write(f'"Scheda numero: {str(i)}";')

        for j in range(len(scheda.IPAddress)):  # Writes both Ipv4 and Ipv6 address
            file_output.write(f'"IP: {scheda.IPAddress[j]}";')
            array_load_key.append('IPV4')
            array_load_key.append('IPV6')
            array_load_value.append(scheda.IPAddress[j])

        file_output.write(
            '"MACAddress: ";"')  # Writes the MAC address in the various standards and then the seller of the NIC
        MAC = scheda.MACAddress
        array_load_key.append('MACAddress')
        array_load_value.append(MAC)
        if '-' in str(MAC):
            MACAddressSep(MAC, file_output, '-')
        elif ':' in str(MAC):
            MACAddressSep(MAC, file_output, ':')
        else:
            MACAddressSep(MAC, file_output, ' ')
        try:
            MACAddressSep(MAC, file_output, mac_sep)
        except:
            print('Missing MAC Separator parameter...')
        file_output.write(f'{MAC}";')
        MACAddressVendor(MAC, file_output)  # Writes the NIC seller

        file_output.write(f'"DHCP: {str(scheda.DHCPEnabled)}";')

        val.append((MAC, scheda.DHCPEnabled))

        i += 1
    databaseUpload(config[11], config[12], config[13], config[14], val)
    file_output.write(f'"Ticks: {str(round(time.time()))}"\n')


def MACAddressSep(MAC, file_output, sep):
    """ Writes the standardized MACAddress in the output file """
    file_output.write(str(MAC).replace(sep, ':'))
    file_output.write('";"')
    file_output.write(str(MAC).replace(sep, ' '))
    file_output.write('";"')
    file_output.write(str(MAC).replace(sep, ';'))
    file_output.write('";"')
    file_output.write(str(MAC).replace(sep, ''))
    file_output.write('";"')


def writeOS(pc, file_output):
    """ Writes information about the Operating System """
    for so in wmi.WMI(pc).Win32_OperatingSystem():
        file_output.write(f'"{so.Caption}";')
        file_output.write(f'"Version: {so.version}";')
        file_output.write(f'"Build: {so.BuildNumber}";')
        file_output.write(f'"Language: {so.OSLanguage}"')
    file_output.write('\n')


def writeUSB(file_output):
    """ Writes information about the USB port """
    with open('usb_devices') as porte:
        for linee in porte:
            linee.strip(' ')
            if 'Mass Storage' in linee:
                file_output.write(linee)


def ping(pc):
    """ Executes a ping and returns if the endpoint is reachable """
    comando = 'ping -n 1 ' + pc
    pc_ping = os.popen(comando).read()
    if 'Impossib' in pc_ping:
        return False


def dataEsecuzione(file_output):
    """ Reads the execution date and writes it in the specified output file """
    file_output.write('Execution date, Format ISO 8601 YYYY-mm-dd HH-MM-SS: ')
    file_output.write(str(datetime.datetime.now()))
    file_output.write(f' Ticks: {str(int(time.time()))}"\n')


def logMessage(file_output):
    """ Writes time and ticks in the log file """
    file_output.write(f'"{str(datetime.datetime.now())}')
    file_output.write(f' {str(round(time.time()))}";"')


def MACAddressVendor(MAC, file_output):
    """ Writes in the output file the seller of the Network Interface Card """
    URL = "http://macvendors.co/api/"
    richiesta = urllib2.Request(URL + MAC, headers={'User-Agent': "API Browser"})
    risposta = urllib2.urlopen(richiesta)
    codifica = codecs.getreader("utf-8")
    obj = json.load(codifica(risposta))
    file_output.write('"Vendor: ')
    if 'error' in str(obj):  # If it doesn't find the vendor writes that there was an error
        file_output.write('Error finding MACVendor')
    else:
        file_output.write(str(obj).strip('{}'))
    file_output.write('";')


def writeEvent(pc, file_output):
    """ Gets info from event viewer """
    for event in wmi.WMI(pc).Win32_NTLogEvent(Logfile='System'):
        file_output.write(f'"{pc}";')
        file_output.write(f'"{event.SourceName}";')
        file_output.write(f'"{event.Logfile}";')
        file_output.write(f'"{event.Type}"\n')


def writeProduct(pc, file_output):
    """ Gets the information about the software installed on the computer """
    for products in wmi.WMI(pc).Win32_Product():
        try:
            file_output.write(f'"{pc}";')
            file_output.write(f'"{str(products.Caption)}";')
            file_output.write(f'"InstallDate: {str(products.InstallDate)}";')
            file_output.write(f'"InstallSource: {str(products.InstallSource)}";')
            file_output.write(f'"Version: {str(products.Version)}";')
            file_output.write(f'"Ticks: {str(round(time.time()))}"\n')
        except None as e:
            pass


def get_uptime(computer):
    """ Returns the uptime hours of the endpoint """
    c = wmi.WMI(computer=computer, find_classes=False)
    secs_up = int([uptime.SystemUpTime for uptime in c.Win32_PerfFormattedData_PerfOS_System()][0])
    return secs_up / 3600


def writeUpdate(file_output):
    """ Writes in the output file the list of pending updates """
    with open('updatepending.txt') as upt_pnd:
        for lines in upt_pnd:
            file_output.write('"localhost";"')
            file_output.write(lines.strip('\n'))
            file_output.write(f'";"{str(round(time.time()))}"\n')


def writeDisk(pc, file_output):
    """  Gets the information about the logical disk on the specified pc """
    for disk in wmi.WMI(pc).Win32_LogicalDisk():
        file_output.write(f'"{pc}";')
        file_output.write(f'"{disk.Caption}";')
        file_output.write(f'"Type: {str(disk.DriveType)}";')
        file_output.write(f'"File System: {disk.FileSystem}";')
        file_output.write(f'"Byte totali: {str(disk.Size)}";')
        file_output.write(f'"Byte liberi: {str(disk.FreeSpace)}";')
        file_output.write(f'"Serial: {disk.VolumeSerialnumber}";')
        file_output.write(f'"Ticks: {str(round(time.time()))}"\n')

def databaseUpload(dbhost, dbusername, dbpassword, dbdatabase, val):
    """ Uploads data on database """
    try:
        mydb = mysql.connector.connect(
        host=dbhost,
        user=dbusername,
        password=dbpassword,
        database=dbdatabase
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO network_card2 VALUES (%s, %s)"

        mycursor.executemany(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "was inserted.")
    except:
        print("Error inserting data into database.")


if __name__ == '__main__':
    main()
