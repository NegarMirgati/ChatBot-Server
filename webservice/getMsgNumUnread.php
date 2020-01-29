<?php
header('Content-Type: text/html; charset=UTF-8');

$domainname = 'http://localhost/moodle';
$functionname = 'core_message_get_unread_conversation_counts';

// REST RETURNED VALUES FORMAT
$restformat = 'json'; 
$token = $argv[2];
$params = array('userid'=> $argv[1]);
ini_set('default_charset', 'utf-8');

/// REST CALL
$serverurl = $domainname . '/webservice/rest/server.php'. '?wstoken=' . $token . '&wsfunction='.$functionname;
require_once('curl.php');
$curl = new curl;
//if rest format == 'xml', then we do not add the param for backward compatibility with Moodle < 2.2
$restformat = ($restformat == 'json')?'&moodlewsrestformat=' . $restformat:'';
$resp = $curl->post($serverurl . $restformat, $params);

$info=json_decode($resp);
foreach($info as $item) {
    if(is_array($item) || is_object($item)){
    foreach ($item as $key => $value) {
        if($key == "1"){
        echo  $value;
        return;
        }
    }
}
}
?>


