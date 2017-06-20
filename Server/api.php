<?php

header('Content-Type: application/json');

try {
	$mysqli = getConnection();
	switch ($_SERVER['REQUEST_METHOD']) {
		case 'GET':
			switch ($_GET['type']) {
				case 'log-in':
					$sql = "SELECT users.user_name, users.password, user_types.type_name FROM users JOIN user_types ON users.user_type = user_types.type_id";
					break;
				case 'admin_get_users':
					$sql = "SELECT users.f_name, users.l_name, users.Phone, users.email, houses.street, houses.house_number, houses.unit_id FROM users JOIN houses ON users.user_id = houses.end_user_id";
					break;
				case 'admin_get_sensors':
					$sql = "SELECT houses.family_id, houses.street, houses.house_number, houses.unit_id, units.unit_id, units.sensor_type_id FROM houses JOIN units ON houses.unit_id = units.unit_id";
					break;
				case 'admin_get_house':
					$sql = "SELECT houses.street, houses.house_number, houses.unit_id FROM houses";
					break;
				case 'local_fd_get_units':
					$sql = "SELECT houses.family_id, houses.street, houses.house_number, houses.unit_id, units.unit_id, units.sensor_type_id FROM houses JOIN units ON houses.unit_id = units.unit_id";
					break;
				case 'local_fd_get_silenced':
					$sql = "SELECT houses.family_id, houses.street, houses.house_number, houses.unit_id, units.sensor_type_id, units.is_silenced FROM houses JOIN units ON houses.unit_id = units.unit_id";
					break;
				case 'local_fd_get_risks':
					$sql = "SELECT houses.family_id, houses.family_name, houses.unit_id, houses.is_at_risk from houses";
					break;
				case 'end_user':
					$sql = "SELECT * FROM users";
					break;
				case 'get_unit_user':
					$sql = "SELECT users.user_id,users.user_name, houses.family_id, houses.unit_id from houses JOIN users on users.user_id = houses.end_user_id";
					break;

				case 'get_alarms':
					$sql = "SELECT houses.family_id, houses.street, houses.house_number, houses.is_alaram FROM houses WHERE is_alaram = 1";
					break;
				case 'last_ten':
					$sql = "SELECT * FROM sensor_data ORDER BY id DESC LIMIT 10";
					break;
				default:
					throw new Exception("invalid type {$_GET['type']}", 404000);
			}
			echo json_encode(selectFromDb($mysqli, $sql));
			exit;
		case 'POST':
			$body = file_get_contents('php://input');
			$bodyArray = json_decode($body, true);
			switch ($bodyArray['type']) {
				case 'admin_add_user':
					$table = 'users';
					$keys = ['user_id', 'user_name', 'password', 'user_type', 'f_name', 'l_name', 'Phone', 'email'];
					break;
				case 'admin_create_unit':
					$table = 'units';
					$keys = ['unit_id', 'sensor_type_id'];
					break;
				case 'admin_add_house':
					$table = 'houses';
					$keys = ['family_id', 'family_name', 'num_of_people', 'street', 'house_number', 'end_user_id', 'unit_id'];
					break;
				case 'user_change_user':
					$sql = "UPDATE users set user_name = {$bodyArray['values'][0]}, password = {$bodyArray['values'][1]}, f_name = {$bodyArray['values'][2]}, l_name = {$bodyArray['values'][3]}, Phone = {$bodyArray['values'][4]}, email = {$bodyArray['values'][5]} WHERE users.user_id = {$bodyArray['values'][6]}";
					updateDb($mysqli, $sql);
					return;
				case 'local_fd_silnence':
					$sql = "UPDATE units set is_silenced = {$bodyArray['values'][0]} WHERE units.unit_id = {$bodyArray['values'][1]} and units.sensor_type_id = {$bodyArray['values'][2]} ";
					updateDb($mysqli, $sql);
					return;
				case 'alarms':
					$sql = "UPDATE houses set is_alaram = {$bodyArray['values'][0]} WHERE houses.unit_id = {$bodyArray['values'][1]}";
					updateDb($mysqli, $sql);
					return;	
				case 'local_fd_risk':
					$sql = "UPDATE houses SET is_at_risk = {$bodyArray['values'][0]} where houses.family_id = {$bodyArray['values'][1]}";
					updateDb($mysqli, $sql);
					return;
				default:
					throw new Exception("invalid type {$bodyArray['type']}", 404000);
			}
			insertToDb($mysqli, $table, $keys, $bodyArray['values']);
			break;
		default:
			header("HTTP/1.0 404 Not Found");
			break;

	}
	$mysqli->close();

} catch (Exception $e) {
	echo $e->getMessage();
	exit;
}
exit;

function getConnection() {
	$mysqli = new mysqli('127.0.0.1', 'root', 'bitnami', 'canarit');
	if ($mysqli->connect_errno) {
		echo "Error: Failed to make a MySQL connection ({$mysqli->connect_error})";
		exit;
	}
	return $mysqli;
}

function insertToDb($mysqli, $table, $keys, $values) {
	$keysString = implode(",",$keys);
	$values = array_map(function ($value) use ($mysqli){
		return "'".mysqli_real_escape_string($mysqli, $value)."'";
	}, $values);
	$valuesString = implode(",", $values);
	$sql = "INSERT INTO $table ($keysString) VALUES ($valuesString)";
	if (!$result = $mysqli->query($sql)) {
		echo "Error: query failed to execute ({$mysqli->error})";
		exit;
	}
}

function updateDb($mysqli, $sql) {
	if (!$result = $mysqli->query($sql)) {
		echo "Error: query failed to execute ({$mysqli->error})";
		exit;
	}
}

function selectFromDb($mysqli, $sql) {
	if (!$result = $mysqli->query($sql)) {
		echo "Error: query failed to execute ({$mysqli->error})";
		exit;
	}
	$rows = [];
	while($r = $result->fetch_assoc()) {
		$rows[] = $r;
	}
	$result->free();
	return $rows;

}

