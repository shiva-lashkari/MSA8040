
-- SELECT length(companyParticipants) - length(REPLACE(companyParticipants, "/", "")) + 1 as length  FROM `rawInnerData`

-- Company Participents Split
1. 
-- SELECT conference_id, if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)) as participents  FROM `rawInnerData`

-- SELECT conference_id, 
--     substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
--     substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Company Participant' as pa_conferer_type  FROM `rawInnerData`

INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_title_type`, `pa_conferer_type`) 
    SELECT conference_id, 
        substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
        substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Company Participant' as pa_conferer_type  FROM `rawInnerData`

2.
-- SELECT conference_id, substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1) as participents  FROM `rawInnerData`

-- SELECT conference_id, 
--     substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1), ' - ', 1) as pa_name , 
--     substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1), ' - ', -1) pa_title_type, 'Company Participant' as pa_conferer_type  FROM `rawInnerData`

INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_title_type`, `pa_conferer_type`) 
    SELECT conference_id,
        substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1), ' - ', 1) as pa_name , 
        substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1), ' - ', -1) pa_title_type, 'Company Participant' as pa_conferer_type  FROM `rawInnerData` 
        where length(companyParticipants) - length(REPLACE(companyParticipants, "/", "")) > 0

--  Corporate Participents Split
1. 
-- SELECT conference_id, 
--     substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
--     substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Corporate Participant' as pa_conferer_type  FROM `rawInnerData`
--     where length(corporateParticipants) - length(REPLACE(corporateParticipants, "/", "")) > 0
INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_title_type`, `pa_conferer_type`)
    SELECT conference_id, 
        substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
        substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Corporate Participant' as pa_conferer_type  FROM `rawInnerData`
        where length(corporateParticipants) - length(REPLACE(corporateParticipants, "/", "")) > 0

2.
INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_title_type`, `pa_conferer_type`) 
    SELECT conference_id,
        substring_index(substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', 2)), ' / ', -1), ' - ', 1) as pa_name , 
        substring_index(substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', 2)), ' / ', -1), ' - ', -1) pa_title_type, 'Corporate Participant' as pa_conferer_type  FROM `rawInnerData` 
        where length(corporateParticipants) - length(REPLACE(corporateParticipants, "/", "")) > 0


-- Executives
1.
-- SELECT conference_id, 
--     substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
--     substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Executive Participant' as pa_conferer_type  FROM `rawInnerData`
--     where length(executiveParticipants) - length(REPLACE(executiveParticipants, "/", "")) > 0

INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_title_type`, `pa_conferer_type`)
SELECT conference_id, 
    substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
    substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Executive Participant' as pa_conferer_type  FROM `rawInnerData`
    where length(executiveParticipants) - length(REPLACE(executiveParticipants, "/", "")) > 0

2.
-- SELECT conference_id,
--     substring_index(substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 2)), ' / ', -1), ' - ', 1) as pa_name , 
--     substring_index(substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 2)), ' / ', -1), ' - ', -1) pa_title_type, 'Executive Participant' as pa_conferer_type  FROM `rawInnerData` 
--     where length(executiveParticipants) - length(REPLACE(executiveParticipants, "/", "")) > 0

INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_title_type`, `pa_conferer_type`)
SELECT conference_id,
        substring_index(substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 2)), ' / ', -1), ' - ', 1) as pa_name , 
        substring_index(substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 2)), ' / ', -1), ' - ', -1) pa_title_type, 'Executive Participant' as pa_conferer_type  FROM `rawInnerData` 
        where length(executiveParticipants) - length(REPLACE(executiveParticipants, "/", "")) > 0

-- Call Participents
1.
-- SELECT conference_id, 
--     substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
--     substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', 1)), ' - ', -1) pa_organization, 'Call Participant' as pa_conferer_type  FROM `rawInnerData`
--     where length(callParticipants) - length(REPLACE(callParticipants, "/", "")) > 0

INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_organization`, `pa_conferer_type`)
SELECT conference_id, 
    substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
    substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', 1)), ' - ', -1) pa_organization, 'Call Participant' as pa_conferer_type  FROM `rawInnerData`
    where length(callParticipants) - length(REPLACE(callParticipants, "/", "")) > 0

2.
INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_organization`, `pa_conferer_type`)
SELECT conference_id,
        substring_index(substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', 2)), ' / ', -1), ' - ', 1) as pa_name , 
        substring_index(substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', 2)), ' / ', -1), ' - ', -1) pa_organization, 'Call Participant' as pa_conferer_type  FROM `rawInnerData` 
        where length(callParticipants) - length(REPLACE(callParticipants, "/", "")) > 0

-- Check to see how many duplicate participant_names  we have with different participant_id, we need to take care of it
SELECT table1.`participant_id`, table2.`participant_id`, table2.`conference_id`, if(length(table1.`pa_title_type`)>length(table2.`pa_title_type`),table1.`pa_title_type`,table2.`pa_title_type`) as `pa_title_type` FROM `rawDataParticipant` as table1 inner join `rawDataParticipant` as `table2`  on table1.`pa_name` = table2.`pa_name` and table1.`participant_id` != table2.`participant_id`

-- Update participant_id for duplicate records to have uniqu id

UPDATE rawDataParticipant2 AS t1 inner join (select pa_name, min(`participant_id`) as PID from `rawDataParticipant2` group by pa_name) AS t2 SET t1.`participant_id` = t2.PID
WHERE t1.pa_name = t2.pa_name

-- Check to see how many duplicate records  we have with same participant_id,conference_id
SELECT `table1`.`id` FROM `rawDataParticipant` as `table1` inner join `rawDataParticipant` as `table2`  on `table1`.`conference_id` = `table2`.`conference_id` and `table1`.`participant_id` = `table2`.`participant_id` and `table1`.`id` != `table2`.`id`

------------------------------------------------------------------------------------------------------------------------------
-- Filling our designed DataBases
INSERT INTO `company` (`company_ticker`, `company_name`) SELECT DISTINCT `company_ticker`, `company_name` FROM `rawMainData`

INSERT INTO `conference` (`conference_id`, `company_id`, `conference_title`, `conference_date`, `conference_time`)
    SELECT `conference_id`, CO.`company_id` ,`conference_Title`, DATE(`conference_date`), TIME(`conference_date`) FROM rawMainData INNER JOIN company as CO using(company_ticker)

INSERT INTO `participant` (`participant_id`, `pa_name`, `pa_organization`, `pa_title_type`, `pa_conferer_type`) 
    SELECT `pa_name`, `pa_organization`, `pa_title_type`, `pa_conferer_type` FROM `rawDataParticipant`

-- Some times participents have different titles in different conferences, I have added the one that have more information
INSERT INTO `participant` (`participant_id`, `pa_name`, `pa_organization`, `pa_title_type`, `pa_conferer_type`) 
    SELECT t1.`participant_id`, t1.`pa_name`, t1.`pa_organization`, t2.title, t1.`pa_conferer_type` from ( select `pa_name`, max(`pa_title_type`) as title from rawDataParticipant as t2 group by `pa_name` ) t2 join `rawDataParticipant` as t1 on t2.`pa_name` = t1.`pa_name` group by t1.pa_name

INSERT INTO `conference_participant` (`participant_id`, `conference_id`)
    SELECT `participant_id`, `conference_id` FROM `rawDataParticipant`

CREATE OR REPLACE VIEW `conference_participant_withname` AS
SELECT `pa_name`, `participant_id`, `conference_id` FROM `conference_participant` INNER JOIN `participant` USING(`participant_id`)

-- Filling Speech table
INSERT INTO `speech` (`conference_id`, `participant_id`, `textual_info`)
SELECT `rawSpeechData`.`conference_id`, `conference_participant_withname`.`participant_id`, `textual_info` FROM `conference_participant_withname` INNER JOIN `rawSpeechData` ON `rawSpeechData`.`pa_name` = `conference_participant_withname`.`pa_name` AND `rawSpeechData`.`conference_id` = `conference_participant_withname`.`conference_id`



UPDATE `conference` INNER JOIN `rawInnerData` USING(conference_id) SET `conference`.`is_presentation` = `rawInnerData`.`is_presentation`
UPDATE `conference` INNER JOIN `rawInnerData` USING(conference_id) SET `conference`.`is_QA` = `rawInnerData`.`is_QA`





