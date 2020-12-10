
-- -----------------------------------------------------
-- Create Database CECS
-- -----------------------------------------------------
drop database IF EXISTS CECS;
create database CECS;
use CECS;

-- -----------------------------------------------------
-- Drop tables if they are exist in CECS
-- -----------------------------------------------------
drop table if exists company;
drop table if exists conference;
drop table if exists participant;
drop table if exists conference_participant;
drop table if exists speech;


-- -----------------------------------------------------
-- Create Table CECS.company
-- -----------------------------------------------------
create table company (
company_id int not null auto_increment primary key,
company_ticker char(10) not null unique,
company_name varchar(255) not null
);

-- -----------------------------------------------------
-- Create Table CECS.conference
-- -----------------------------------------------------
create table conference (
conference_id    int not null unique primary key,
company_id  int not null,
conference_title  varchar(255) not null,
conference_url  varchar(255),
conference_date date not null,
conference_time  timestamp not null default current_timestamp on update current_timestamp,
is_presentation bool not null default 1,
is_QA bool not null default -1,
constraint FK_CC foreign key (company_id) references company(company_id)
);

-- -----------------------------------------------------
-- Create Table CECS.participant
-- -----------------------------------------------------
create table participant (
participant_id    int not null auto_increment primary key,
pa_name  varchar(50) character set latin1 not null,
pa_organization   varchar(100) character set latin1 default null,
pa_title_type	 varchar(100) character set latin1,
pa_conferer_type varchar(50) character set latin1
);
/* pa_organization will be NULL for company particioants and will have the Organization Name for Conference Call Participations other than company members.*/
/* pa_title_type is the title of company participant like CEO, staff , ... */
/* pa_conferer_type is one of these four: "Conference Call Participant", "Company Participant", "Executive", "Corporate Participate"  */

-- -----------------------------------------------------
-- Create Table CECS.speech
-- -----------------------------------------------------
create table speech (
speech_id    int not null unique primary key,
conference_id  int not null,
participant_id  int,
textual_info text character set latin1,
constraint FK_S_CON foreign key (conference_id) references conference(conference_id),
constraint FK_S_PA foreign key (participant_id) references participant(participant_id)
);
/*when participant_id is null it means "operator" */