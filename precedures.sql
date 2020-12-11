
-- Split Company Participants Split Name and Type ande insert into rawDataParticipants
delimiter $$
create procedure sp_rawdata_pr()
begin

declare ln_max_1 int unsigned default 0;
declare ln_max_2 int unsigned default 0;
declare ln_max_3 int unsigned default 0;
declare ln_max_4 int unsigned default 0;
declare counter_1 int unsigned default 2;
declare counter_2 int unsigned default 2;
declare counter_3 int unsigned default 2;
declare counter_4 int unsigned default 2;

-- Split Company Participants Split Name and Type ande insert into rawDataParticipants
INSERT INTO rawDataParticipant (conference_id, pa_name, pa_title_type, pa_conferer_type) 
SELECT conference_id, substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Company Participant' as pa_conferer_type  FROM rawInnerData;

select length(companyParticipants) - length(REPLACE(companyParticipants, "/", "")) as ln_max_1 from rawInnerData;
  while counter_1 <= ln_max_1 do
  
    INSERT INTO rawDataParticipant (conference_id, pa_name, pa_title_type, pa_conferer_type) 
    SELECT conference_id,
        substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', counter_1)), ' / ', -1), ' - ', 1) as pa_name , 
        substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', counter_1)), ' / ', -1), ' - ', -1) pa_title_type, 'Company Participant' as pa_conferer_type  FROM rawInnerData 
        where length(companyParticipants) - length(REPLACE(companyParticipants, "/", "")) > (counter_1-2);
   
    set counter_1 = counter_1 + 1;
  end while;

-- Split Corporate Participants Split Name and Type ande insert into rawDataParticipants
INSERT INTO rawDataParticipant (conference_id, pa_name, pa_title_type, pa_conferer_type) 
SELECT conference_id, substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Corporate Participant' as pa_conferer_type  FROM rawInnerData;

select length(corporateParticipants) - length(REPLACE(corporateParticipants, "/", "")) as ln_max_2 from rawInnerData;
  while counter_2 <= ln_max_2 do
  
    INSERT INTO rawDataParticipant (conference_id, pa_name, pa_title_type, pa_conferer_type) 
    SELECT conference_id,
        substring_index(substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', counter_2)), ' / ', -1), ' - ', 1) as pa_name , 
        substring_index(substring_index(if(locate(' / ',corporateParticipants)=0,'',substring_index(corporateParticipants, ' / ', counter_2)), ' / ', -1), ' - ', -1) pa_title_type, 'Corporate Participant' as pa_conferer_type  FROM rawInnerData 
        where length(corporateParticipants) - length(REPLACE(corporateParticipants, "/", "")) > (counter_2-2);
   
    set counter_2 = counter_2 + 1;
  end while;
  
-- Split Executives Participants Split Name and Type ande insert into rawDataParticipants
INSERT INTO rawDataParticipant (conference_id, pa_name, pa_title_type, pa_conferer_type) 
SELECT conference_id, substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Executive Participant' as pa_conferer_type  FROM rawInnerData;

select length(executiveParticipants) - length(REPLACE(executiveParticipants, "/", "")) as ln_max_3 from rawInnerData;
  while counter_3 <= ln_max_3 do
  
    INSERT INTO rawDataParticipant (conference_id, pa_name, pa_title_type, pa_conferer_type) 
    SELECT conference_id,
        substring_index(substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', counter_3)), ' / ', -1), ' - ', 1) as pa_name , 
        substring_index(substring_index(if(locate(' / ',executiveParticipants)=0,'',substring_index(executiveParticipants, ' / ', counter_3)), ' / ', -1), ' - ', -1) pa_title_type, 'Executive Participant' as pa_conferer_type  FROM rawInnerData 
        where length(executiveParticipants) - length(REPLACE(executiveParticipants, "/", "")) > (counter_3-2);
   
    set counter_3 = counter_3 + 1;
  end while;

-- Split Call Participants Split Name and Type ande insert into rawDataParticipants
INSERT INTO rawDataParticipant (conference_id, pa_name, pa_title_type, pa_conferer_type) 
SELECT conference_id, substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', 1)), ' - ', 1) as pa_name , 
substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', 1)), ' - ', -1) pa_title_type, 'Call Participant' as pa_conferer_type  FROM rawInnerData;

select length(callParticipants) - length(REPLACE(callParticipants, "/", "")) as ln_max_3 from rawInnerData;
  while counter_3 <= ln_max_3 do
  
    INSERT INTO rawDataParticipant (conference_id, pa_name, pa_title_type, pa_conferer_type) 
    SELECT conference_id,
        substring_index(substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', counter_3)), ' / ', -1), ' - ', 1) as pa_name , 
        substring_index(substring_index(if(locate(' / ',callParticipants)=0,'',substring_index(callParticipants, ' / ', counter_3)), ' / ', -1), ' - ', -1) pa_title_type, 'Call Participant' as pa_conferer_type  FROM rawInnerData 
        where length(callParticipants) - length(REPLACE(callParticipants, "/", "")) > (counter_3-2);
   
    set counter_3 = counter_3 + 1;
  end while;


-- Update participant_id for duplicate records to have uniqu id
-- #We can not use participent ID as a key because somethimes some participents may be in more than one conference

UPDATE `rawDataParticipant` SET `participant_id` = `id`;
DELETE FROM rawDataParticipant WHERE pa_name = "";

UPDATE rawDataParticipant AS t1 inner join (select pa_name, min(participant_id) as PID, max(pa_title_type) as PTitle from rawDataParticipant group by pa_name) AS t2 
ON t1.pa_name = t2.pa_name
SET t1.participant_id = t2.PID , t1.pa_title_type = t2.PTitle
where t1.pa_name = t2.pa_name;
-- Fill Company Table
INSERT INTO `company` (`company_ticker`, `company_name`) SELECT DISTINCT `company_ticker`, `company_name` FROM `rawMainData`;

-- Fill Conference Table
INSERT INTO `conference` (`conference_id`, `conference_url`, `company_id`, `conference_title`, `conference_date`, `conference_time`)
SELECT `conference_id`, `conference_url`, CO.`company_id` ,`conference_Title`, DATE(`conference_date`), TIME(`conference_date`) FROM rawMainData INNER JOIN company as CO using(company_ticker);


-- Fill participant Table
INSERT INTO `participant` (`participant_id`, `pa_name`, `pa_organization`, `pa_title_type`, `pa_conferer_type`) 
    SELECT `participant_id`, `pa_name`, `pa_organization`, `pa_title_type`, `pa_conferer_type` FROM `rawDataParticipant` GROUP BY `participant_id`, `pa_name`, `pa_organization`, `pa_title_type`, `pa_conferer_type`;

INSERT INTO `speech` (`participant_id`, `conference_id`)
    SELECT `participant_id`, `conference_id` FROM `rawDataParticipant`;

Update speech Inner JOIN (SELECT `textual_info`, `conference_id`, `participant`.`participant_id` FROM `participant` INNER JOIN `rawSpeechData` ON `rawSpeechData`.`pa_name` = `participant`.`pa_name`) T1 on `speech`.`conference_id` = `T1`.`conference_id` AND `T1`.`participant_id` = `speech`.`participant_id` SET `speech`.`textual_info` = `T1`.`textual_info`;

end$$
delimiter ;

call sp_rawdata_pr();



