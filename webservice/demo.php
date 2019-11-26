<?php
$token = '4e90ca89f1ebbcfccd5ea54696165671';
$domainname = 'http://localhost/moodle';
$functionname = 'gradereport_user_get_grade_items';

// REST RETURNED VALUES FORMAT
$restformat = 'json'; 
// $user1 = new stdClass();
// $user1->courseid ='2';
// $user1->userid='2';
$params = array('courseid' => $argv[1],'userid'=> $argv[2],'groupid'=> 0);

/// REST CALL
header('Content-Type: text/plain');
$serverurl = $domainname . '/webservice/rest/server.php'. '?wstoken=' . $token . '&wsfunction='.$functionname;
require_once('curl.php');
$curl = new curl;
//if rest format == 'xml', then we do not add the param for backward compatibility with Moodle < 2.2
$restformat = ($restformat == 'json')?'&moodlewsrestformat=' . $restformat:'';
$resp = $curl->post($serverurl . $restformat, $params);
//print_r($resp->id);
//echo $resp;

$Book=json_decode($resp);
for($i=0;$i<count($Book->usergrades[0]->gradeitems);$i++){
  print_r($Book->usergrades[0]->gradeitems[$i]->itemname);
  print_r(":");
  print_r($Book->usergrades[0]->gradeitems[$i]->gradeformatted);
  print_r(",");
  
  
  
}



