
CREATE TABLE Company (
                Company_ID INT AUTO_INCREMENT NOT NULL,
                Name VARCHAR(100) NOT NULL,
                PRIMARY KEY (Company_ID)
);


CREATE TABLE Location (
                Location_ID INT AUTO_INCREMENT NOT NULL,
                City VARCHAR(100) NOT NULL,
                PRIMARY KEY (Location_ID)
);


CREATE TABLE Language (
                Language_ID INT NOT NULL,
                Name VARCHAR(100) NOT NULL,
                PRIMARY KEY (Language_ID)
);


CREATE TABLE Internship (
                Internship_ID INT AUTO_INCREMENT NOT NULL,
                Descripition VARCHAR(1000),
                Company_ID INT NOT NULL,
                Location_ID INT NOT NULL,
                Language_ID INT NOT NULL,
                Experience INT NOT NULL,
                Duration INT NOT NULL,
                PRIMARY KEY (Internship_ID)
);


CREATE TABLE Client (
                Client_ID INT AUTO_INCREMENT NOT NULL,
                Username VARCHAR(100) NOT NULL,
                Password_encr VARCHAR(100) NOT NULL,
                Password_salt VARCHAR(100) NOT NULL,
                Experience INT NOT NULL,
                Duration INT NOT NULL,
                PRIMARY KEY (Client_ID)
);


CREATE TABLE Client_Location (
                Client_ID INT NOT NULL,
                Location_ID INT NOT NULL,
                PRIMARY KEY (Client_ID, Location_ID)
);


CREATE TABLE Client_Language (
                Language_ID INT NOT NULL,
                Client_ID INT NOT NULL,
                PRIMARY KEY (Language_ID, Client_ID)
);


ALTER TABLE Internship ADD CONSTRAINT company_internship_fk
FOREIGN KEY (Company_ID)
REFERENCES Company (Company_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Internship ADD CONSTRAINT location_internship_fk
FOREIGN KEY (Location_ID)
REFERENCES Location (Location_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Client_Location ADD CONSTRAINT location_client_location_fk
FOREIGN KEY (Location_ID)
REFERENCES Location (Location_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Internship ADD CONSTRAINT language_internship_fk
FOREIGN KEY (Language_ID)
REFERENCES Language (Language_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Client_Language ADD CONSTRAINT language_client_language_fk
FOREIGN KEY (Language_ID)
REFERENCES Language (Language_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Client_Language ADD CONSTRAINT client_client_language_fk
FOREIGN KEY (Client_ID)
REFERENCES Client (Client_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Client_Location ADD CONSTRAINT client_client_location_fk
FOREIGN KEY (Client_ID)
REFERENCES Client (Client_ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
