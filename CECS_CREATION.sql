
-- -----------------------------------------------------
-- Create Database CECS
-- -----------------------------------------------------
drop database IF EXISTS CECS;
create database CECS;
use CECS;

-- -----------------------------------------------------
-- Drop tables if they are exist in CECS
-- -----------------------------------------------------
drop table if exists COMPANY;
drop table if exists CONFERENCE_CALL;
drop table if exists PARTICIPANT;
drop table if exists CONCALL_PA;


-- -----------------------------------------------------
-- Create Table CECS.COMPANY
-- -----------------------------------------------------
create table company (
company_id int not null auto_increment primary key,
company_ticker char(10) not null unique,
company_name varchar(255) CHARACTER SET latin1 not null
);

-- -----------------------------------------------------
-- Create Table CECS.CONFERENCE_CALL
-- -----------------------------------------------------
create table CONFERENCE_CALL (
CONCALL_ID    int not null unique primary key,
CO_ID  int not null,
CONCALL_TITLE  varchar(2000) CHARACTER SET latin1 not null,
CONCALL_DATE date not null,
CONCALL_TIME  timestamp not null,
SPEECH  varchar(5000) CHARACTER SET latin1,
PRESENTATION bool not null default 1,
Q_AND_A bool not null default 1,
constraint FK_CO_CON foreign key (CO_ID) references COMPANY(CO_ID)
);

-- -----------------------------------------------------
-- Create Table CECS.PARTICIPANT
-- -----------------------------------------------------
create table PARTICIPANT (
PA_ID    int not null auto_increment primary key,
PA_NAME  varchar(50) not null,
PA_ORG   varchar(100) default null,
PA_TYPE	 varchar(100) not null unique
);
/* PA_ORG will be NULL for company particioants and will have the Organization Name for Conference Call Participations other than company members.*/

-- -----------------------------------------------------
-- Create Table CECS.CONCALL_PA
-- -----------------------------------------------------
create table CONCALL_PA (
CONCALL_ID  int not null,
PA_ID    int not null,
constraint PK_CONCALL_PA primary key (CONCALL_ID, PA_ID),
constraint FK_CCP_PA foreign key (PA_ID) references PARTICIPANT(PA_ID),
constraint FK_CCP_CONCALL foreign key (CONCALL_ID) references CONFERENCE_CALL(CONCALL_ID)
);

-- -----------------------------------------------------
-- Create Table CECS.PARTICIPANT_TITLE
-- -----------------------------------------------------
