<?php
/*
 Copyright:     Copyright 2015 CDK Global LLC. All rights reserved.
 File:          opt_in_out_smsfo.php
 Author:        Marc Hines
 Creation Date: 03/20/2015

 Description: Data Service testing page for the Fixed Operations SMS Opt-In Opt-Out flags.

 Revision history:

 mm/dd/yyyy  ini   description.
 */

if (!class_exists('AccountPaths'))
{
    require_once "/adp/home/www_serv/htdocs/acgl/acct/classes/acct.class.acct.paths.php";
}

require AccountPaths::$ofmain . "/of/includes/security.include.php";
require_once AccountPaths::$main . "/includes/data_access/acct/classes/class.opt_in_out_smsfo.php";

global $securityInfo;

$objOptInOutSmsFo = new opt_in_out_smsfo($securityInfo);

/*
 * Sample JSON data for URL to read:
 * json_data={"action":"read","phone_nbr":"5031231234"}
 *
 * Sample JSON data for URL to update:
 * json_data={"action":"update","customer_nbr":"2005","phone_nbr":"5031231234","opt_in_sw":true,"audit_comment":"My comment"}
 *
 */

$aryOptInOutData = $objOptInOutSmsFo->parseJSON($_REQUEST['json_data'], false);

if ($aryOptInOutData->action == 'read') {
    
    $objOptInOutSmsFo->setPhoneNumber($aryOptInOutData->phone_nbr);
    $optInOutFlag = $objOptInOutSmsFo->read();
    
    echo("OptInFlag As Passed: " . $optInOutFlag . "<br>");
    echo("getOptInFlag(): " . $objOptInOutSmsFo->getOptInFlag() . "<br>");
    echo("getAuditComment(): " . $objOptInOutSmsFo->getAuditComment() . "<br>");
    echo("getCustomerNumber(): " . $objOptInOutSmsFo->getCustomerNumber() . "<br>");
    
} elseif ($aryOptInOutData->action == 'update') {
    
    $objOptInOutSmsFo->setPhoneNumber($aryOptInOutData->phone_nbr);
    $objOptInOutSmsFo->setOptInFlag($aryOptInOutData->opt_in_sw);
    $objOptInOutSmsFo->setCustomerNumber($aryOptInOutData->customer_nbr);
    $objOptInOutSmsFo->setAuditComment($aryOptInOutData->audit_comment);
    
    $UpdateOkFlag = $objOptInOutSmsFo->update();
    
    echo("UpdateOkFlag As Passed: " . $UpdateOkFlag . "<br>");
    
}


