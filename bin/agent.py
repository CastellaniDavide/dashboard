__author__ = 'Ciancetta Thomas'
__version__ = '01.01 2022-01-01'

import datetime
import mysql.connector
import os
import requests
import sys
import time
import wmi
import yaml


class Dashboard:
    def __init__(self):
        self.setup()
        self.run()

    
    def setup(self):
        try:  # Try opening log file, else create it
            self.file_log = open('..\\log\\log.log', 'a')
        except:
            print('Log file not found, creating new one...\n')
            self.file_log = open('..\\log\\log.log', 'a+')
            self.logMessage()
            self.file_log.write('Error: Missing log file, created new."\n')

        # Functions to write log file
        self.logMessage()
        self.file_log.write('Inizio esecuzione: ')
        self.dataEsecuzione()

        try:  # Try looking for config file parameters(output path), else use default settings
            file_yaml = open('config.yaml', 'r')
            self.config = yaml.safe_load(file_yaml)
            file_yaml.close()
            
        except:
            print('Missing configuration parameters, please add config file.\n')
            self.logMessage()
            self.file_log.write('Error: Missing configuration parameters, please add config file."\n')
            sys.exit(1)

        # Output files
        self.output_osversion = open(self.config['output-osversion'], 'w')
        self.output_netinfo = open(self.config['output-netinfo'], 'w')
        self.output_product = open(self.config['output-product'], 'w')
        self.output_uptime = open(self.config['output-uptime'], 'w')
        self.output_logicaldisk = open(self.config['output-logicaldisk'], 'w')
        self.db_values = []
        self.db_load_key = []
        self.db_load_value = []


    def run(self):
        """ Reads the list of endpoints and writes information on output files """
        try:  # Main program for writing info in output files
            with open('..\\flussi\\computers.csv') as input:

                for line in input:
                    self.output_osversion.write(line.strip('\n'))
                    self.output_osversion.write(';')
                    self.output_netinfo.write(line.strip('\n'))
                    self.output_netinfo.write(';')
                    self.output_uptime.write(line.strip('\n'))
                    self.output_uptime.write(';')

                    pc = str(line).strip('"')[:-2]

                    self.db_values.append(pc)
                    self.db_load_key.append('Nome macchina')
                    self.db_load_value.append(pc)

                    if self.ping(pc) == False:  # Executes a ping to the endpoint to see if it's reachable
                        self.output_osversion.write('"Il seguente endpoint non è raggiungibile"\n')
                        self.output_netinfo.write('"Il seguente endpoint non è raggiungibile"\n')
                        self.output_product.write(f'"{pc}";"Il seguente endpoint non è raggiungibile"\n')
                        self.output_uptime.write('"Il seguente endpoint non è raggiungibile"\n')
                        self.output_logicaldisk.write(f'"{pc}";"Il seguente endpoint non è raggiungibile"\n')

                        self.logMessage()
                        self.file_log.write(pc)
                        self.file_log.write(' non è raggiungibile"\n')
                        continue

                    # Series of function to write everything in files and trace
                    try:  # Try OS
                        self.writeOS(pc)
                        self.logMessage()
                        self.file_log.write(pc)
                        self.file_log.write('";"WriteOS: OK";"')
                    except:
                        self.logMessage()
                        self.file_log.write(pc)
                        self.file_log.write('";"WriteOS: Error";"')

                    try:  # Try NIC
                        self.writeNIC(pc)
                        self.file_log.write('WriteNIC: OK";"')
                    except:
                        self.file_log.write('WriteNIC: Error";"')

                    try:  # Try Product
                        self.writeProduct(pc)
                        self.file_log.write('WriteProduct: OK";"')
                    except:
                        self.file_log.write('WriteProduct: Error";"')

                    try:  # Try Uptime
                        self.output_uptime.write(f'"Uptime: {str(self.getUptime(pc))}";')
                        self.output_uptime.write(f'Ticks: "{str(round(time.time()))}"\n')
                        self.db_values.append(self.getUptime(pc))
                        self.db_load_key.append('Uptime')
                        self.db_load_value.append(self.getUptime(pc))
                        self.file_log.write('WriteUptime: OK";"')
                    except:
                        self.file_log.write('WriteUptime: Error";"')

                    try:  # Try LogicalDisk
                        self.writeDisk(pc)
                        self.file_log.write('WriteLogicalDisk: OK";"')
                    except:
                        self.file_log.write('WriteLogicalDisk: Error";""')
                    
                    try:  # Try Database Upload
                        #self.databaseUpload()
                        self.file_log.write('DatabaseUpload: OK";"')
                    except:
                        self.file_log.write('DatabaseUpload: Error";"')

                    try:  # Try Harper Upload
                        if self.config['token'] != "":
                            #self.harperUpload(self.buildPayload())
                            self.file_log.write('HarperUpload: OK"\n')
                    except:
                        self.file_log.write('HarperUpload: Error"\n')
                        

            # Functions to write log file
            self.logMessage()
            self.file_log.write('Termine Esecuzione: ')
            self.dataEsecuzione()

        except:
            print('Error: Something went Horribly wrong, ending program...')
            self.logMessage()
            self.file_log.write('Error: Something went wrong"\n')

            # Functions to write log file
            self.logMessage()
            self.file_log.write('Termine Esecuzione: ')
            self.dataEsecuzione()
            sys.exit(1)
        sys.exit(0)


    def writeNIC(self, pc):
        """ Writes information about Network Interface Card"""
        i = 1
        for scheda in wmi.WMI(pc).Win32_NetworkAdapterConfiguration(
                IPEnabled=True):  # Repeats the function for the number of NIC
            self.output_netinfo.write(f'"Scheda numero: {str(i)}";')

            for j in range(len(scheda.IPAddress)):  # Writes both Ipv4 and Ipv6 address
                self.output_netinfo.write(f'"IP: {scheda.IPAddress[j]}";')

            self.output_netinfo.write('"MACAddress: ";"')  # Writes the MAC address and then the seller of the NIC
            MAC = scheda.MACAddress
            
            if '-' in str(MAC):
                self.output_netinfo.write(str(MAC).replace('-', ' '))
                self.output_netinfo.write('";"')
            elif ':' in str(MAC):
                self.output_netinfo.write(str(MAC).replace(':', ' '))
                self.output_netinfo.write('";"')
            elif ';' in str(MAC):
                self.output_netinfo.write(str(MAC).replace(';', ' '))
                self.output_netinfo.write('";"')
            else:
                self.output_netinfo.write(str(MAC))
                self.output_netinfo.write('";"')

            self.output_netinfo.write(f'"DHCP: {str(scheda.DHCPEnabled)}";')

            if i == 1:
                self.db_values.append(MAC)
                self.db_load_key.append('MAC')
                self.db_load_value.append(MAC)
                self.db_values.append(scheda.DHCPEnabled)
                self.db_load_key.append('DHCP')
                self.db_load_value.append(scheda.DHCPEnabled)

            i += 1
        self.output_netinfo.write(f'"Ticks: {str(round(time.time()))}"\n')


    def writeOS(self, pc):
        """ Writes information about the Operating System """
        for so in wmi.WMI(pc).Win32_OperatingSystem():
            self.output_osversion.write(f'"{so.Caption}";')
            self.output_osversion.write(f'"Version: {so.version}";')
            self.output_osversion.write(f'"Build: {so.BuildNumber}";')
            self.output_osversion.write(f'"Language: {so.OSLanguage}"')
        self.db_values.append(so.Caption)
        self.db_load_key.append('Sistema operativo')
        self.db_load_value.append(so.Caption)
        self.db_values.append(so.version)
        self.db_load_key.append('Versione sistema operativo')
        self.db_load_value.append(so.version)
        self.output_osversion.write('\n')


    def ping(self, pc):
        """ Executes a ping and returns if the endpoint is reachable """
        comando = 'ping -n 1 ' + pc
        pc_ping = os.popen(comando).read()
        if 'Impossib' in pc_ping:
            return False


    def dataEsecuzione(self):
        """ Reads the execution date and writes it in the specified output file """
        self.file_log.write('Execution date, Format ISO 8601 YYYY-mm-dd HH-MM-SS: ')
        self.file_log.write(str(datetime.datetime.now()))
        self.file_log.write(f' Ticks: {str(int(time.time()))}"\n')


    def logMessage(self):
        """ Writes time and ticks in the log file """
        self.file_log.write(f'"{str(datetime.datetime.now())}')
        self.file_log.write(f' {str(round(time.time()))}";"')


    def writeProduct(self, pc):
        """ Gets the information about the software installed on the computer """
        for products in wmi.WMI(pc).Win32_Product():
            try:
                self.output_product.write(f'"{pc}";')
                self.output_product.write(f'"{str(products.Caption)}";')
                self.output_product.write(f'"InstallDate: {str(products.InstallDate)}";')
                self.output_product.write(f'"InstallSource: {str(products.InstallSource)}";')
                self.output_product.write(f'"Version: {str(products.Version)}";')
                self.output_product.write(f'"Ticks: {str(round(time.time()))}"\n')
            except None as e:
                pass


    def getUptime(self, pc):
        """ Returns the uptime hours of the endpoint """
        c = wmi.WMI(computer=pc, find_classes=False)
        secs_up = int([uptime.SystemUpTime for uptime in c.Win32_PerfFormattedData_PerfOS_System()][0])
        return secs_up / 3600


    def writeDisk(self, pc):
        """  Gets the information about the logical disk on the specified pc """
        for disk in wmi.WMI(pc).Win32_LogicalDisk():
            self.output_logicaldisk.write(f'"{pc}";')
            self.output_logicaldisk.write(f'"{disk.Caption}";')
            self.output_logicaldisk.write(f'"Type: {str(disk.DriveType)}";')
            self.output_logicaldisk.write(f'"File System: {disk.FileSystem}";')
            self.output_logicaldisk.write(f'"Byte totali: {str(disk.Size)}";')
            self.output_logicaldisk.write(f'"Byte liberi: {str(disk.FreeSpace)}";')
            self.output_logicaldisk.write(f'"Serial: {disk.VolumeSerialnumber}";')
            self.output_logicaldisk.write(f'"Ticks: {str(round(time.time()))}"\n')

    def databaseUpload(self):
        """ Uploads data on database """
        mydb = mysql.connector.connect(
        host=self.config['db-host'],
        user=self.config['db-username'],
        password=self.config['db-password'],
        database=self.config['db-dbname']
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO macchine VALUES (%s, %s, %s, %s, %s, %s)"

        mycursor.executemany(sql, tuple(self.db_values))

        mydb.commit()

        print(mycursor.rowcount, "was inserted.")


    def harperUpload(self, payload):
        """ Uploads data on harper database """
        url = 'https://cloud-1-itimarconivr.harperdbcloud.com'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.config['token']
        }
        response = requests.request('POST', url, headers = headers, data = payload)
        print(response.text.encode('utf8'))

    def buildPayload(self):
        """ Builds the payload for the harper upload """
        payload = '{\n\t\"operation\":\"sql\",\n\t\"sql\": \"INSERT INTO dev.agent ('
        for key in self.db_load_key:
            payload += f'{key}, '
        payload += f'Timestamp) VALUES('
        for values in self.db_load_value:
            payload += f'{values}, '
        payload += f'{str(round(time.time()))})\"\n'
        payload += '}'
        return payload


if __name__ == '__main__':
    Dashboard()
