<?php
require_once 'vendor/autoload.php';
//header('Content-Type: application/json');


//2 more queries. one to display html table with the sensors data, made for demonstration/
// the second query is for inserting the data from the sensors to the DB
try {
	$mysqli = getConnection();
	switch ($_SERVER['REQUEST_METHOD']) {
		case 'GET':
			$sql = "SELECT sensor_data.unit_id, sensor_types.sensor_name, sensor_data.sensor_value, sensor_data.time_stamp from sensor_types, sensor_data where sensor_data.sensor_type = sensor_types.sensor_type_id order by time_stamp ASC, sensor_data.unit_id ASC";
			if (!$result = $mysqli->query($sql)) {
				echo "Error: query failed to execute ({$mysqli->error})";
				exit;
			}
			//TEST
			$rows = rsToArray($result);
			echo "<html><body><table border='1'><th>unit_id</th><th>sensor_name</th><th>sensor_value</th><th>timestamp</th>";
			foreach ($rows as $row) {
				echo "<tr><td>{$row['unit_id']}</td><td>{$row['sensor_name']}</td><td>{$row['sensor_value']}</td><td>{$row['time_stamp']}</td></tr>";
			}
			echo "</table>";
			$result->free();
			break;
		case 'POST':
			$body = file_get_contents('php://input');
			$rows = json_decode($body, true);
			foreach ($rows as $row) {
				insertToDb($mysqli, (int)$row[0], (int)$row[1], (float)$row[2]);
				checkValues((int)$row[1], (float)$row[2]);
			}
			$mysqli->close();
			break;
		default:
			header("HTTP/1.0 404 Not Found");
			break;

	}

} catch (Exception $e) {
	echo $e->getMessage();
	exit;
}
exit;

//try to connect to the DB
function getConnection() {
	$mysqli = new mysqli('127.0.0.1', 'root', 'bitnami', 'canarit');
	if ($mysqli->connect_errno) {
		echo "Error: Failed to make a MySQL connection ({$mysqli->connect_error})";
		exit;
	}
	return $mysqli;
}
//insert data to the DB
function insertToDb($mysqli, $unitId, $sensorType, $sensorValue) {
	$sql = "INSERT INTO sensor_data (unit_id, sensor_type, sensor_value) VALUES ($unitId, $sensorType, $sensorValue)";
	if (!$result = $mysqli->query($sql)) {
		echo "Error: query failed to execute ({$mysqli->error})";
		exit;
	}
}
//convert from json to array
function rsToArray($rs) {
	$results = [];
	while($r = $rs->fetch_assoc()) {
		$results[] = $r;
	}
	return $results;
}

//check the values. in case of unusual values - send an email adress
function checkValues($sensorType, $sensorValue) {
	$flame = $lpg = $smoke = $temp = false;
	if ($sensorType == 1 && $sensorValue > 250) {
		$flame = true;
	}
	if ($sensorType == 2 && $sensorValue > 800) {
		$lpg = true;
	}
	if ($sensorType == 3 && $sensorValue > 800) {
		$smoke = true;
	}
	if ($sensorType == 5 && $sensorValue > 50) {
		$temp = true;
	}
	if ($flame || $lpg || $smoke || $temp) {
		$subject = 'alarm';
		$body = 'unusual value detected';
		$from = 'canarit.alarms@gmail.com';
		$to = 'canarit.gfd@gmail.com';
		$transport = Swift_SmtpTransport::newInstance('smtp.gmail.com', 465, "ssl")
			->setUsername('canarit.alarms@gmail.com')
			->setPassword('canarit2017');

		$mailer = Swift_Mailer::newInstance($transport);

		$message = Swift_Message::newInstance($subject)
			->setFrom(array($from => 'CANARIT'))
			->setTo(array($to))
			->setBody($body);

		$result = $mailer->send($message);
	}

}