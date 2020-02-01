<?php

$token = $argv[3];
$domainname = 'http://localhost/moodle';
$functionname = 'mod_assign_get_submission_status';

// REST RETURNED VALUES FORMAT
$restformat = 'json'; 

$params = array('assignid'=>$argv[1],'userid'=>$argv[2]);

/// REST CALL
header('Content-Type: text/plain');
$serverurl = $domainname . '/webservice/rest/server.php'. '?wstoken=' . $token . '&wsfunction='.$functionname;
require_once('curl.php');
$curl = new curl;
//if rest format == 'xml', then we do not add the param for backward compatibility with Moodle < 2.2
$restformat = ($restformat == 'json')?'&moodlewsrestformat=' . $restformat:'';
$resp = $curl->post($serverurl . $restformat, $params);
//print_r($resp->id);
#echo $resp;
$Book=json_decode($resp);
// print_r($Book);
print_r($Book->gradingsummary->participantcount);
print_r(',');
print_r($Book->gradingsummary->submissionssubmittedcount);