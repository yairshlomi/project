<?php
require_once 'vendor/autoload.php';
//header('Content-Type: application/json');

//in case of emergency, send an email message

sendEmail();

function sendEmail() {

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
			->setBcc('idoelad@gmail.com')
			->setBody($body);
		$result = $mailer->send($message);

}