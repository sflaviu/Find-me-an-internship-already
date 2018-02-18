#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql
import thread

import rpyc

from rpyc.utils.server import ThreadedServer

global assignedIp

class Client:

    def __init__(self):
        self.id = 0
        self.userName = ''
        self.experience = 0
        self.duration = 0
        self.password_encr = ''
        self.password_salt = ''
        self.locations = []
        self.languages = []


class Internship:

    def __init__(self):
        self.id = 0
        self.company = 0
        self.location = 0
        self.language = 0
        self.experience = 0
        self.duration = 0

    def __str__(self):
        stri = str(self.id) + ' ' + str(self.company) + ' +' \
            + str(self.location) + ' ' + str(self.language) + ' ' \
            + str(self.experience) + ' ' + str(self.duration)
        return stri

    def clone(self):
        internship2 = Internship()
        internship2.id = self.id
        internship2.company = self.company
        internship2.location = self.location
        internship2.language = self.language
        internship2.experience = self.experience
        internship2.duration = self.duration
        return internship2


class Company:

    def __init__(self):
        self.id = 0
        self.name = ''


class Location:

    def __init__(self):
        self.id = 0
        self.city = ''


class Language:

    def __init__(self):
        self.id = 0
        self.name = ''


class DBConnectionService(rpyc.Service):

    class exposed_DBConnection(object):

        def __init__(self):
            self.host = 'localhost'
            self.user = 'root'
            self.password = '10lase'
            self.dbName = 'internship'
            self.connection = None
            self.cursor = None

        def connect(self):
            self.connection = pymysql.connect(self.host, self.user,
                    self.password, self.dbName)

        def isConnected(self):
            if self.connection is None:
                return False
            return True

        def exposed_getClients(self):
            self.connect()
            self.cursor = self.connection.cursor()
            clients = []
            self.cursor.execute('SELECT * FROM Client')
            resultSet = self.cursor.fetchall()
            for row in resultSet:
                client = Client()
                client.id = row[0]
                client.userName = row[1]
                client.experience = row[4]
                client.duration = row[5]
                self.cursor.execute('SELECT * FROM Client_Language WHERE client_id='
                                     + str(client.id))
                resultSet2 = self.cursor.fetchall()
                for e in resultSet2:
                    client.languages.append(e[0])
                self.cursor.execute('SELECT * FROM Client_Location WHERE client_id='
                                     + str(client.id))
                resultSet2 = self.cursor.fetchall()
                for e in resultSet2:
                    client.languages.append(e[1])
                clients.append(client)
            self.cursor.close()
            self.connection.close()
            return clients

        def exposed_getInternships(self):
            self.connect()
            self.cursor = self.connection.cursor()
            internships = []
            self.cursor.execute('SELECT * FROM Internship')
            resultSet = self.cursor.fetchall()
            for row in resultSet:
                internship = Internship()
                internship.id = row[0]
                internship.company = row[2]
                internship.location = row[3]
                internship.language = row[4]
                internship.experience = row[5]
                internship.duration = row[6]
                internships.append(internship)
            self.cursor.close()
            self.connection.close()
            return internships

        def exposed_getCompanies(self):
            self.connect()
            self.cursor = self.connection.cursor()
            companies = []
            sql = 'SELECT * FROM Company'
            self.cursor.execute(sql)
            resultSet = self.cursor.fetchall()
            for row in resultSet:
                company = Company()
                company.id = row[0]
                company.name = row[1]
                companies.append(company)
            self.cursor.close()
            self.connection.close()
            return companies
        
        def exposed_getCompanyName(self, id):
            self.connect()
            self.cursor = self.connection.cursor()
            company = None
            sql = "SELECT Name FROM Company where Company_ID = %d" % id
            self.cursor.execute(sql)
            resultSet = self.cursor.fetchall()
            if len(resultSet)>0:
                company = resultSet[0]
            self.cursor.close()
            self.connection.close()
            return company[0]

        def exposed_getLocationName(self, id):
            self.connect()
            self.cursor = self.connection.cursor()
            location = None
            sql = "SELECT City FROM Location where Location_ID = %d" % id
            self.cursor.execute(sql)
            resultSet = self.cursor.fetchall()
            if len(resultSet)>0:
                location = resultSet[0]
            self.cursor.close()
            self.connection.close()
            return location[0]

        def exposed_getLanguageName(self, id):
            self.connect()
            self.cursor = self.connection.cursor()
            language = None
            sql = "SELECT Name FROM Language where Language_ID = %d" % id
            self.cursor.execute(sql)
            resultSet = self.cursor.fetchall()
            if len(resultSet)>0:
                language = resultSet[0]
            self.cursor.close()
            self.connection.close()
            return language[0]

        def exposed_getLocations(self):
            self.connect()
            self.cursor = self.connection.cursor()
            locations = []
            sql = 'SELECT * FROM Location'
            self.cursor.execute(sql)
            resultSet = self.cursor.fetchall()
            for row in resultSet:
                location = Location()
                location.id = row[0]
                location.city = row[1]
                locations.append(location)
            self.cursor.close()
            self.connection.close()
            return locations

        def exposed_getLanguages(self):
            self.connect()
            self.cursor = self.connection.cursor()
            languages = []
            sql = 'SELECT * FROM Language'
            self.cursor.execute(sql)
            resultSet = self.cursor.fetchall()
            for row in resultSet:
                language = Language()
                language.id = row[0]
                language.name = row[1]
                languages.append(language)
            self.cursor.close()
            self.connection.close()
            return languages

        def exposed_insertClient(self, client):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = \
                """INSERT INTO Clieant(client_id, username, password_encr, password_salt, 
            experience, duration) VALUES ('%d','%s','%s','%s','%d','%d')""" \
                % (
                client.id,
                client.userName,
                client.password_encr,
                client.password_salt,
                client.experience,
                client.duration,
                )
            self.cursor.execute(sql)
            for l in client.languages:
                sql = \
                    """INSERT INTO Client_Language(language_id, client_id)
                VALUES ('%d', '%d')""" \
                    % (l, client.id)
                self.cursor.execute(sql)
            for l in client.locations:
                sql = \
                    """INSERT INTO Client_Location(client_id, location_id)
                VALUES ('%d', '%d')""" \
                    % (client.id, l)
                self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_insertInternship(self, internship):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = \
                """INSERT INTO Internship (internship_id, company_id,
            location_id, language_id, experience, duration) values ('%d', '%d',
            '%d', '%d', '%d', '%d')""" \
                % (
                internship.id,
                internship.company,
                internship.location,
                internship.language,
                internship.experience,
                internship.duration,
                )
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_insertLanguage(self, language):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = \
                """INSERT INTO Language (language_id, name)
            values ('%d', '%s')""" \
                % (language.id, language.name)
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_insertLocation(self, location):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = \
                """INSERT INTO Location (location_id, city)
            values ('%d', '%s')""" \
                % (location.id, location.city)
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_insertCompany(self, company):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = \
                """INSERT INTO Company (company_id, name)
            values ('%d', '%s')""" \
                % (company.id, company.name)
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_deleteClient(self, client):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = "DELETE FROM Client_Location WHERE client_id='%d'" \
                % client.id
            self.cursor.execute(sql)
            sql = "DELETE FROM Client_Language WHERE client_id='%d'" \
                % client.id
            self.cursor.execute(sql)
            sql = "DELETE FROM Client WHERE client_id='%d'" % client.id
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_deleteInternship(self, internship):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = "Delete FROM Internship where internship_id = '%d'" \
                % internship.id
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_deleteLanguage(self, language):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = "DELETE FROM Internship WHERE language_id='%d'" \
                % language.id
            self.cursor.execute(sql)
            sql = "DELETE FROM Client_Language WHERE language_id='%d'" \
                % language.id
            self.cursor.execute(sql)
            sql = "DELETE FROM Language WHERE language_id='%d'" \
                % language.id
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_deleteLocation(self, location):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = "DELETE FROM Client_Location WHERE location_id='%d'" \
                % location.id
            self.cursor.execute(sql)
            sql = "DELETE FROM Internship WHERE location_id='%d'" \
                % location.id
            self.cursor.execute(sql)
            sql = "DELETE FROM Location WHERE location_id='%d'" \
                % location.id
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_deleteCompany(self, company):
            self.connect()
            self.cursor = self.connection.cursor()
            sql = "DELETE FROM Internship WHERE company_id='%d'" \
                % company.id
            self.cursor.execute(sql)
            sql = "DELETE FROM Company WHERE company_id='%d'" \
                % company.id
            self.cursor.execute(sql)
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        def exposed_Sal(self):
            print 'PaBafta'


class DBIpChecker(rpyc.Service):
    
    global assignedIp
    def exposed_check_ip(self, sIp):
        if(assignedIp==sIp):
            return True
        return False


def server_start():
    ThreadedServer(DBConnectionService, port=1234,
                   protocol_config={'allow_public_attrs': True,
                   'allow_all_attrs': True}).start()


def launch_Ip_checker(portS):
    ThreadedServer(DBIpChecker,port=5555,protocol_config={"allow_public_attrs": True, "allow_all_attrs": True}).start()

def get_Ip():
    conn=rpyc.connect("10.142.0.6",port=4321,config={"allow_all_attrs": True})
    return conn.root.chooseIp("10.142.0.2")

if __name__ == '__main__':

    ip = get_Ip()

    assignedIp = ip[0]

    print "My assigned IP is " + assignedIp

    thread.start_new_thread(launch_Ip_checker, (ip[1],))
    thread.start_new_thread(server_start, ())
    while 1 == 1:
        pass
