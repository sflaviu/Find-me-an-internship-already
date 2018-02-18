
CREATE TABLE Company (
                Company_ID INT IDENTITY NOT NULL,
                Name VARCHAR NOT NULL,
                CONSTRAINT Company_ID PRIMARY KEY (Company_ID)
)

CREATE TABLE Location (
                Location_ID INT IDENTITY NOT NULL,
                City VARCHAR NOT NULL,
                CONSTRAINT Location_ID PRIMARY KEY (Location_ID)
)

CREATE TABLE Language (
                Language_ID INT NOT NULL,
                Name VARCHAR NOT NULL,
                CONSTRAINT Language_ID PRIMARY KEY (Language_ID)
)

CREATE TABLE Internship (
                Internship_ID INT IDENTITY NOT NULL,
                Descripition VARCHAR,
                Company_ID INT NOT NULL,
                Location_ID INT NOT NULL,
                Language_ID INT NOT NULL,
                Experience INT NOT NULL,
                Duration INT NOT NULL,
                CONSTRAINT Internship_ID PRIMARY KEY (Internship_ID)
)

CREATE TABLE Client (
                Client_ID INT IDENTITY NOT NULL,
                Username VARCHAR NOT NULL,
                Password_encr VARCHAR NOT NULL,
                Password_salt VARCHAR NOT NULL,
                Experience INT NOT NULL,
                Duration INT NOT NULL,
                CONSTRAINT Client_ID PRIMARY KEY (Client_ID)
)

CREATE TABLE Client_Location (
                Client_ID INT NOT NULL,
                Location_ID INT NOT NULL,
                CONSTRAINT Client_Location_pk PRIMARY KEY (Client_ID, Location_ID)
)

CREATE TABLE Client_Language (
                Language_ID INT NOT NULL,
                Client_ID INT NOT NULL,
                CONSTRAINT Client_Language_pk PRIMARY KEY (Language_ID, Client_ID)
)

ALTER TABLE Internship ADD CONSTRAINT Company_Internship_fk
FOREIGN KEY (Company_ID)
REFERENCES Company (Company_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE Internship ADD CONSTRAINT Location_Internship_fk
FOREIGN KEY (Location_ID)
REFERENCES Location (Location_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE Client_Location ADD CONSTRAINT Location_Client_Location_fk
FOREIGN KEY (Location_ID)
REFERENCES Location (Location_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE Internship ADD CONSTRAINT Language_Internship_fk
FOREIGN KEY (Language_ID)
REFERENCES Language (Language_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE Client_Language ADD CONSTRAINT Language_Client_Language_fk
FOREIGN KEY (Language_ID)
REFERENCES Language (Language_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE Client_Language ADD CONSTRAINT Client_Client_Language_fk
FOREIGN KEY (Client_ID)
REFERENCES Client (Client_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION

ALTER TABLE Client_Location ADD CONSTRAINT Client_Client_Location_fk
FOREIGN KEY (Client_ID)
REFERENCES Client (Client_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION