-- Test Queries
-- a. How many conference calls in your database occurred in 2020? Answer: 9228

SELECT count(*) FROM `conference` WHERE conference_date like '2020%'

-- b. Print their ticker name and date

SELECT conference_date, Co.company_ticker FROM `conference` INNER JOIN  company as Co USING(company_id)  WHERE conference_date like '2020%'

-- c. Among those participants, how many are company participants and how many are conference call participants? 

SELECT pa_conferer_type, COUNT(*) FROM participant GROUP BY pa_conferer_type

-- Can you print his/her speech, given the name of this participants, along with the ticker name and date

SELECT pa_name, textual_info FROM speech INNER JOIN `participant` using(participant_id ) 
WHERE pa_name = 'Kevin Miller' AND conference_id IN (SELECT conference_id FROM conference 
where company_id = (SELECT company_id FROM company where company_ticker = 'MNR') AND conference_date = '2020-11-24')