<!DOCTYPE html>
<html>
<body>

<?php
$age = array("Peter" => "35", "Ben" => "37", "Joe" => "43");
echo "Peter is " . $age['Peter'] . " years old. <br>";
$length_age=count($age);
foreach($age as $x => $x_value)
{
	echo "Key = " . $x . ", Value = " . $x_value . ".";
    echo "<br>";
}
$firstarray=array("XOXO","BMW","ROLLER");
$length=count($firstarray);
for($i=0; $i<$length ; $i++)
{
	echo $firstarray[$i];
    echo "<br>";
}
echo "The first item is " . $firstarray[0] . ".<br>"," The second item is " . $firstarray[1] . ".<br>"," The third item is " . $firstarray[2] . ".<br>";

$logins = array
(
	array("Elnur","Badalov",19),
    array("Elmir","Hajizade",20),
    array("Elman","Karimov",24),
    array("Eldar","Dadasov",34)
);
$multilength = count($logins);
for($row=0;$row<$multilength;$row++)
{
	echo "<p><b>Row number $row</b></p>";
  	echo "<ul>";
  	for ($col = 0; $col < 3; $col++) {
    	echo "<li>".$logins[$row][$col]."</li>";
  	}
  	echo "</ul>";
}
echo $logins[0][0] . " " , $logins[0][1] . " ", $logins[0][2] ."<br>" ;
echo $logins[1][0] . " " , $logins[1][1] . " ", $logins[1][2] ."<br>";
echo $logins[2][0] . " " , $logins[2][1] . " ", $logins[2][2] ."<br>";
?>

</html>
</body>