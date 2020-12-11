use cecs;

-- a
SELECT count(*) as Total_CC_2020 FROM conference WHERE year(conference_date) = 2020;

-- b
SELECT co.company_ticker, conference_date FROM conference INNER JOIN  company as co USING(company_id)  WHERE year(conference_date) = 2020;

-- c - how many:
select co.company_ticker, conference_date, count(participant_id) as Total_Participant 
from  company co inner join conference cc using(company_id)
inner join speech using(conference_id)
inner join  participant using(participant_id)
where company_ticker = 'MNR' and conference_date = '2020-11-24'
group by  co.company_ticker, conference_date;

-- c - who are them
select pa_name, pa_conferer_type, 
case when pa_organization is null then co.company_name else pa_organization end as 'Company_Organization',
case when pa_organization is null then pa_title_type end as 'Title_Type'
from  company co inner join conference cc using(company_id)
inner join speech using(conference_id)
inner join  participant using(participant_id)
where company_ticker = 'MNR' and conference_date = '2020-11-24';

-- c - how many company_participants / conference_call_participant
select 
COUNT(CASE WHEN pa_organization is null then 1 ELSE NULL END) as "company_participants",
COUNT(CASE WHEN pa_organization is not null then 1 ELSE NULL END) as "conference_call_participant"
from  company co inner join conference cc using(company_id)
inner join speech using(conference_id)
inner join  participant using(participant_id)
where company_ticker = 'MNR' and conference_date = '2020-11-24';

/* pa_organization will be NULL for company particioants and will have the Organization Name for Conference Call Participations other than company members.*/
/*we don't need group by  co.company_ticker, conference_date because we have where company_ticker = 'MNR' and conference_date = '2020-11-24' */

-- c - printh his/her speech
select textual_info 
from  company co inner join conference cc using(company_id)
inner join speech using(conference_id)
inner join participant using(participant_id)
where pa_name = 'Kevin Miller' and company_ticker = 'MNR' and conference_date = '2020-11-24'
order by speech_id;

