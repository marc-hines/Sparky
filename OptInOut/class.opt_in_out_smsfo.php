<?php
/*
 Copyright:     Copyright 2015 CDK Global LLC. All rights reserved.
 File:          class.opt_in_out_smsfo.php
 Author:        Marc Hines
 Creation Date: 03/19/2015

 Description: Data Service class for the Fixed Operatioons SMS Opt-In Opt-Out
              flags. Accounting is storing this data for now on the DMS in
              PostgreSQL. Someday it is expected to move to the hosted
              'Common Consumer'

 Revision history:

 mm/dd/yyyy  ini   description.
 */

if (!class_exists('AccountPaths'))
{
    require_once "/adp/home/www_serv/htdocs/acgl/acct/classes/acct.class.acct.paths.php";
}

require_once AccountPaths::$main . "/includes/data_access/acct/classes/class.opt_in_out.php";

class opt_in_out_smsfo
{
    protected $_securityInfo;
    private $_objOptInOut;
    private $_opt_type = 'SMSFO';
    private $_cora_acct_cd;
    private $_phone_nbr = '';
    private $_customer_nbr = '';
    private $_opt_in_sw = false;
    private $_audit_comment = '';

    public function __construct($securityInfo)
    {
        $this->_securityInfo = $securityInfo;
        
        $this->_objOptInOut = new opt_in_out($securityInfo);

        /*
         * Find the 'parent' Fixed Operations parts accounts for the current group
         */
        
        $aryAccounts = $securityInfo->getProperty('ACCOUNTS');
        $parentCoraAcctCode = $aryAccounts['O'];
        
        /*
         * Check if this is a body shop group (last character is numeric in the
         * group name) and if it is try find the parent group by looking up the
         * 'real parent' fixed operation parts account from the base group
         *
         *    Groups:  | GM   | GM2       |
         *    Type:    | FO   | Body Shop |
         *    Service: | GM-S | GM-SB     |
         *    Parts:   | GM-I | GM-IB     |
         *
         *    GM-I is the 'parent' FO account where the inventory for
         *    GM-I, GM-S, GM-IB & GM-SB is kept. FO SMS Opt-In/Opt-Out settings
         *    are stored by the base inventory account (GM-I in this example)
         */
        
        $groupName = $securityInfo->getProperty('DEFGROUP');
        if (is_numeric(substr($groupName, -1))) {
            $parentGroupName = substr($groupName, 0, -1);
            $aryAccounts = $securityInfo->getUserAccounts($parentGroupName);
            if (isset($aryAccounts['O'])) {
                $parentCoraAcctCode = $aryAccounts['O'];
            }
        }
        
        $this->_cora_acct_cd = $parentCoraAcctCode;
        
    }
    
    public function read()
    {
        $aryOptInOutData = array();
        
        $this->_opt_in_sw = false;
        
        $aryOptInOutData['opt_type'] = $this->_opt_type;
        $aryOptInOutData['cora_acct_cd'] = $this->_cora_acct_cd;
        $aryOptInOutData['phone_nbr'] = $this->_phone_nbr;
        
        $ds = $this->_objOptInOut->readOptInOut($aryOptInOutData);
        
        if(isset($ds)) {
            $rowData = $ds->get_next();
            if(isset($rowData)) {
                
                if(isset($rowData['opt_in_sw']))
                    $this->_opt_in_sw = $rowData['opt_in_sw'];
                
                if(isset($rowData['audit_comment']))
                    $this->_audit_comment = $rowData['audit_comment'];
                
                if(isset($rowData['customer_nbr']))
                    $this->_customer_nbr = $rowData['customer_nbr'];

            }
        }

        return $this->_opt_in_sw;
        
    }
    
    public function update()
    {
        $aryOptInOutData = array();
        
        $updateOkFlag = true;
    
        $aryOptInOutData['opt_type'] = $this->_opt_type;
        $aryOptInOutData['cora_acct_cd'] = $this->_cora_acct_cd;
        $aryOptInOutData['phone_nbr'] = $this->_phone_nbr;
        $aryOptInOutData['customer_nbr'] = $this->_customer_nbr;
        $aryOptInOutData['audit_comment'] = $this->_audit_comment;
        $aryOptInOutData['opt_in_sw'] = $this->_opt_in_sw;
    
        $ds = $this->_objOptInOut->updateOptInOut($aryOptInOutData);
        
        if(isset($ds)) {
            $rowData = $ds->get_next();
            if(isset($rowData)) {
                if(isset($rowData['status_nbr'])) {
                    if($rowData['status_nbr'] != 0) {
                        $updateOkFlag = false;
                    }
                }
            }
        }
        return $updateOkFlag;
    
    }
    
    public function parseJSON($strJSON, $blnAsArray=true) 
    {
        return $this->_objOptInOut->parseJSON($strJSON, $blnAsArray);
    }
    
    public function getPhoneNumber()
    {
        return $this->_phone_nbr;
    }
    
    public function setPhoneNumber($phoneNumber)
    {
        $this->_phone_nbr = $phoneNumber;
    }
    
    public function getOptInFlag()
    {
        return $this->_opt_in_sw;
    }
    
    public function setOptInFlag($optInFlag)
    {
        $this->_opt_in_sw = $optInFlag;
    }
    
    public function getCustomerNumber()
    {
        return $this->_customer_nbr;
    }
    
    public function setCustomerNumber($customerNumber)
    {
        $this->_customer_nbr = $customerNumber;
    }
    
    public function getAuditComment()
    {
        return $this->_audit_comment;
    }
    
    public function setAuditComment($auditComment)
    {
        $this->_audit_comment = $auditComment;
    }
}