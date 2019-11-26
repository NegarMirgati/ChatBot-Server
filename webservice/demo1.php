<?php
// This file is NOT a part of Moodle - http://moodle.org/
//
// This client for Moodle 2 is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//

/**
 * REST client for Moodle 2
 * Return JSON or XML format
 *
 * @authorr Jerome Mouneyrac
 */

/// SETUP - NEED TO BE CHANGED
$token = $argv[6];#'4e90ca89f1ebbcfccd5ea54696165671';
$domainname = 'http://localhost/moodle';
$functionname = 'core_user_create_users';

// REST RETURNED VALUES FORMAT
$restformat = 'json'; //Also possible in Moodle 2.2 and later: 'json'
                     //Setting it to 'json' will fail all calls on earlier Moodle version

//////// moodle_user_create_users ////////

/// PARAMETERS - NEED TO BE CHANGED IF YOU CALL A DIFFERENT FUNCTION
$user1 = new stdClass();
$user1->username = $argv[1];
$user1->auth = 'manual';
$user1->password = $argv[2];
$user1->firstname = $argv[3];
$user1->lastname = $argv[4];
$user1->email = $argv[5];


//$user1->mailformat = 0;
//$preferencename1 = 'preference1';
//$preferencename2 = 'preference2';
//$user1->preferences = array(
 //   array('type' => $preferencename1, 'value' => 'preferencevalue1'),
  //  array('type' => $preferencename2, 'value' => 'preferencevalue2'));
// $user2 = new stdClass();
// $user2->username = 'testusername2';
// $user2->password = '1375Zahra@';
// $user2->firstname = 'testfirstname2';
// $user2->lastname = 'testlastname2';
// $user2->email = 'testemail2@moodle.com';
$users = array($user1);
$params = array('users' => $users);

/// REST CALL
header('Content-Type: text/plain');
$serverurl = $domainname . '/webservice/rest/server.php'. '?wstoken=' . $token . '&wsfunction='.$functionname;
require_once('curl.php');
$curl = new curl;
//if rest format == 'xml', then we do not add the param for backward compatibility with Moodle < 2.2
$restformat = ($restformat == 'json')?'&moodlewsrestformat=' . $restformat:'';
$resp = $curl->post($serverurl . $restformat, $params);
print_r($resp);



