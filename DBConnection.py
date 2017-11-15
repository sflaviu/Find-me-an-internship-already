import pymysql


class Client:
    def __init__(self):
        self.id = 0
        self.userName = ""
        self.experience = 0
        self.duration = 0
        self.password_encr = ""
        self.password_salt = ""
        self.locations = []
        self.languages = []

class Internship:
    def __init__(self):
        self.id = 0
        self.company = ""
        self.location = 0
        self.language = 0
        self.experience = 0
        self.duration = 0


class DBConnection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "10lase"
        self.dbName = "internship"
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(self.host, self.user, self.password, self.dbName)
        self.cursor = self.connection.cursor()

    def isConnected(self):
        if self.connection is None:
            return False
        return True

    def getClients(self):
        clients = []
        self.cursor.execute("SELECT * FROM client")
        resultSet = self.cursor.fetchall()
        for row in resultSet:
            client = Client()
            client.id = row[0]
            client.userName = row[1]
            client.experience = row[4]
            client.duration  = row[5]
            self.cursor.execute("SELECT * FROM client_language WHERE client_id=" + str(client.id))
            resultSet2 = self.cursor.fetchall()
            for e in resultSet2:
                client.languages.append(e[0])
            self.cursor.execute("SELECT * FROM client_location WHERE client_id=" + str(client.id))
            resultSet2 = self.cursor.fetchall()
            for e in resultSet2:
                client.languages.append(e[1])
            clients.append(client)
        return clients

    def getInternships(self):
        internships = []
        self.cursor.execute("SELECT * FROM internship")
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
        return internships

    def insertClient(self, client):
        sql = """INSERT INTO CLIENT(client_id, username, password_encr, password_salt, 
        experience, duration) VALUES ('%d','%s','%s','%s','%d','%d')""" % \
              (client.id, client.userName, client.password_encr,client.password_salt, \
               client.experience, client.duration)
        self.cursor.execute(sql)
        for l in client.languages:
            sql = """INSERT INTO CLIENT_LANGUAGE(language_id, client_id)
            VALUES ('%d', '%d')""" % (l, client.id)
            self.cursor.execute(sql)
        for l in client.locations:
            sql = """INSERT INTO CLIENT_LOCATION(client_id, location_id)
            VALUES ('%d', '%d')""" % (client.id, l)
            self.cursor.execute(sql)
        self.connection.commit()

    def deleteClient(self, client):
        sql = "DELETE FROM CLIENT_LOCATION WHERE client_id='%d'" % (client.id)
        self.cursor.execute(sql)
        sql = "DELETE FROM CLIENT_LANGUAGE WHERE client_id='%d'" % (client.id)
        self.cursor.execute(sql)
        sql = "DELETE FROM CLIENT WHERE client_id='%d'" % (client.id)
        self.cursor.execute(sql)
        self.connection.commit()

    def closeConnection(self):
        self.connection.close()







