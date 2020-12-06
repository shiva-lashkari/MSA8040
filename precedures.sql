INSERT INTO `company` (`company_ticker`, `company_name`) SELECT DISTINCT `company_ticker`, `company_ticker` FROM `rawMainData`
INSERT INTO `conference` (`conference_id`, `company_id`, `conference_title`, `conference_date`, `conference_time`) SELECT `conference_id`, CO.`company_id` ,`conference_Title`, DATE(`conference_date`), TIME(`conference_date`) FROM rawMainData INNER JOIN company as CO using(company_ticker)




1. SELECT conference_id, if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)) as participents  FROM `rawInnerData`

SELECT conference_id, 
if(locate(' / ',companyParticipants)=0,'', substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', 1)) as pa_name , 
if(locate(',',companyParticipants)=0,'', substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', -1)) pa_organization, 'Company Participant' as pa_conferer_type  FROM `rawInnerData`

INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_title_type`, `pa_conferer_type`) 
SELECT conference_id, 
    if(locate(' / ',companyParticipants)=0,'', substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', 1)) as pa_name , 
    if(locate(',',companyParticipants)=0,'', substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 1)), ' - ', -1)) pa_title_type, 
    'Company Participant' as pa_conferer_type  FROM `rawInnerData`

2.SELECT conference_id, substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1) as participents  FROM `rawInnerData`

SELECT conference_id, 
if(locate(' / ',companyParticipants)=0,'', substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1), ' - ', 1)) as pa_name , 
if(locate(',',companyParticipants)=0,'', substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1), ' - ', -1)) pa_organization, 'Company Participant' as pa_conferer_type  FROM `rawInnerData`

INSERT INTO `rawDataParticipant` (`conference_id`, `pa_name`, `pa_title_type`, `pa_conferer_type`) 
SELECT conference_id, 
if(locate(' / ',companyParticipants)=0,'', substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1), ' - ', 1)) as pa_name , 
if(locate(',',companyParticipants)=0,'', substring_index(substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 2)), ' / ', -1), ' - ', -1)) pa_organization, 'Company Participant' as pa_conferer_type  FROM `rawInnerData`



3.SELECT conference_id, substring_index(if(locate(' / ',companyParticipants)=0,'',substring_index(companyParticipants, ' / ', 3)), ' / ', -1) as participents  FROM `rawInnerData`
