<?php
$myfile = fopen("newfile.txt", "w") or die("Unable to open file!");
$txt = "Mickey Mouse\n";
fwrite($myfile, $txt);
$txt = "Minnie Mhbhkvouse\n";
fwrite($myfile, $txt);
fclose($myfile);
?>
