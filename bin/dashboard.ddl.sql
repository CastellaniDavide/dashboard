-- DASHBOARD

DROP DATABASE IF EXIST dashboard
CREATE DATABASE dashboard;
USE dashboard;

CREATE TABLE IF NOT EXISTS machine (
    mac varchar(17),
    machine_name varchar(20),
    os varchar(20),
    os_version varchar(20),
    DHCP boolean,
    timestamp time,
    PRIMARY KEY (mac)
);

CREATE TABLE IF NOT EXISTS business_value (
    name varchar(20),
    priority int,
    timestamp time,
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS test (
    id int AUTO_INCREMENT,
    priority int,
    service varchar(20),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS services (
    id int AUTO_INCREMENT,
    service varchar(20),
    port int,
    mac_id varchar(17),
    business_value varchar(20),
    PRIMARY KEY (id),
    FOREIGN KEY (business_value) REFERENCES business_value(name),
    FOREIGN KEY (mac_id) REFERENCES machine(mac)
);

CREATE TABLE test_services (
    id int AUTO_INCREMENT,
    test_id int,
    service_id int,
    extra text,
    PRIMARY KEY (id),
    FOREIGN KEY (test_id) REFERENCES test(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);

CREATE TABLE log_output (
    id int AUTO_INCREMENT,
    test_service int,
    stato int,
    PRIMARY KEY (id),
    FOREIGN KEY (test_service) REFERENCES test_services(id)
    FOREIGN KEY (stato) REFERENCES stato(id)
);

CREATE TABLE stato (
    id int AUTO_INCREMENT,
    nome varchar(255),
    colore varchar(255),
    PRIMARY KEY (id)
);
