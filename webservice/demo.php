<?php
header('Content-Type: text/html; charset=UTF-8');
$file = '/tmp/json-file';

$domainname = 'http://localhost/moodle';
$functionname = 'gradereport_user_get_grade_items';

// REST RETURNED VALUES FORMAT
$restformat = 'json'; 
$token = $argv[3];
$params = array('courseid' => $argv[1],'userid'=> $argv[2],'groupid'=> 0);
ini_set('default_charset', 'utf-8');
function hex2str($hex) {
  $str = '';
  for($i=0;$i<strlen($hex);$i+=2) $str .= chr(hexdec(substr($hex,$i,2)));
  return $str;
}

/// REST CALL

$serverurl = $domainname . '/webservice/rest/server.php'. '?wstoken=' . $token . '&wsfunction='.$functionname;
require_once('curl.php');
$curl = new curl;
//if rest format == 'xml', then we do not add the param for backward compatibility with Moodle < 2.2
$restformat = ($restformat == 'json')?'&moodlewsrestformat=' . $restformat:'';
$resp = $curl->post($serverurl . $restformat, $params);

$Book=json_decode($resp);
for($i=0;$i<count($Book->usergrades[0]->gradeitems);$i++){
  if($Book->usergrades[0]->gradeitems[$i]->itemname == "")
    return;
  print_r($Book->usergrades[0]->gradeitems[$i]->itemname);
  print_r(":");
  print_r($Book->usergrades[0]->gradeitems[$i]->gradeformatted);
  print_r(",");
}


