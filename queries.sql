-- Test Queries
-- 1. How many conference calls happen on the Q1, 2020

SELECT count(*) FROM `conference` WHERE conference_date BETWEEN '2019-01-01' AND '2020-03-31'  

-- 2. Given a ticker name, e.g., FUV, how many conference calls are in 2020


SELECT count(*) FROM `conference` WHERE company_id = (SELECT company_id FROM company WHERE company_ticker = 'FUV') AND conference_date LIKE '2020%'

-- 3. how many participants in the conference call 

SELECT count(*) FROM `participant` where participant_id IN (SELECT participant_id FROM `conference_participant` WHERE conference_id = (SELECT conference_id FROM `conference` WHERE company_id = (SELECT company_id FROM company WHERE company_ticker = 'FUV') AND conference_date = '2020-11-16'))

-- and who are them?

SELECT * FROM `participant` where participant_id IN (SELECT participant_id FROM `conference_participant` WHERE conference_id = (SELECT conference_id FROM `conference` WHERE company_id = (SELECT company_id FROM company WHERE company_ticker = 'FUV') AND conference_date = '2020-11-16'))

-- And further display their speech, given the name of a participents

SELECT * FROM `speech` where participant_id IN (SELECT participant_id FROM `participant` 
    where participant_id IN (SELECT participant_id FROM `conference_participant` WHERE conference_id = (SELECT conference_id FROM `conference` 
    WHERE company_id = (SELECT company_id FROM company WHERE company_ticker = 'FUV') AND conference_date = '2020-11-16'))) 
    AND conference_id = (SELECT conference_id FROM `conference` WHERE company_id = (SELECT company_id FROM company WHERE company_ticker = 'FUV') 
    AND conference_date = '2020-11-16')