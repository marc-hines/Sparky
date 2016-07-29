<?php
/*
 Copyright:     Copyright 2015 CDK Global LLC. All rights reserved.
 File:          class.opt_in_out.php
 Author:        Marc Hines
 Creation Date: 03/18/2015

 Description: Base Data Service class for the SMS Opt-In Opt-Out flags.
              Accounting is storing this data for now on the DMS in
              PostgreSQL. Someday it is expected to move to the hosted
              'Common Consumer'

 Revision history:

 mm/dd/yyyy  ini   description.
 */

if (!class_exists('AccountPaths'))
{
    require_once "/adp/home/www_serv/htdocs/acgl/acct/classes/acct.class.acct.paths.php";
}

require_once AccountPaths::$main . '/includes/class.ds_acc_gen.php';

class opt_in_out extends DSAccGen
{

    public function __construct($securityInfo = null)
    {
        parent::__construct($securityInfo);

        $objQuery = $this->newQuery('opt_in_out_read');
        $objQuery->setOutputName('opt_in_out_read');
        $objQuery->setStatement("select source_bus_unit, customer_nbr, phone_nbr, opt_in_sw, opt_type, created_dt, last_modified_dt, audit_comment from opt_in_out");
        $objParm = $objQuery->newParm('phone_nbr', 'phone_nbr');
        $objParm->_operator = 'IN';
        $objQuery->addParm($objParm);
        $objParm = $objQuery->newParm('source_bus_unit', 'source_bus_unit');
        $objParm->_operator = 'IN';
        $objQuery->addParm($objParm);
        $objParm = $objQuery->newParm('opt_type', 'opt_type');
        $objParm->_operator = 'IN';
        $objQuery->addParm($objParm);

        $this->addQuery($objQuery);

    }

    public function buildReadOptInOut($objParms)
    {
        $queryName = 'opt_in_out_read';
        $objQuery = $this->getQuery($queryName);
        $objQuery->reset();

        if (!empty($objParms['source_bus_unit']))
            $this->setParm($queryName, 'source_bus_unit', $objParms['source_bus_unit']);
        
        if (!empty($objParms['phone_nbr']))
            $this->setParm($queryName, 'phone_nbr', $objParms['phone_nbr']);
        
        if (!empty($objParms['opt_type']))
            $this->setParm($queryName, 'opt_type', $objParms['opt_type']);

        $objQuery->setSort('LIMIT 1');
        
        return $objQuery->getStatement();
    }

    public function readOptInOut($objParms)
    {
        $queryName = 'opt_in_out_read';
        $this->buildReadOptInOut($objParms);
        $this->executeQuery($queryName);

        $ds = $this->getDataSet($queryName);
        
        return $ds;
    }

    public function buildUpdateOptInOut($objParms)
    {
        
        //SELECT * FROM acc.opt_in_out_ins_updt(_cora_acct_cd, _customer_nbr, _phone_nbr, _opt_in_sw, _audit_text, _opt_type)
        
        
        $sqlStatement = "SELECT * FROM acc.opt_in_out_ins_updt(";
        
        if (isset($objParms['cora_acct_cd'])) {
            $sqlStatement .= "'" . $this->escapeForSql($objParms['cora_acct_cd']) . "'";
        } else {
            $sqlStatement .= "'!!error!!'";
        }
        
        if (isset($objParms['customer_nbr'])) {
            $sqlStatement .= ",'" . $this->escapeForSql($objParms['customer_nbr']) . "'";
        } else {
            $sqlStatement .= ",'!!error!!'";
        }
        
        if (isset($objParms['phone_nbr'])) {
            $sqlStatement .= ",'" . $this->escapeForSql($objParms['phone_nbr']) . "'";
        } else {
            $sqlStatement .= ",null";
        }
        
        if (isset($objParms['opt_in_sw'])) {
            if ($objParms['opt_in_sw']) {
                $sqlStatement .= ",true";
            } else {
                $sqlStatement .= ",false";
            }
        } else {
            $sqlStatement .= ",false";
        }
        
        if (isset($objParms['audit_comment'])) {
            $sqlStatement .= ",'" . $this->escapeForSql($objParms['audit_comment']) . "'";
        } else {
            $sqlStatement .= ",null";
        }
        
        if (isset($objParms['opt_type'])) {
            $sqlStatement .= ",'" . $this->escapeForSql($objParms['opt_type']) . "'";
        } else {
            $sqlStatement .= ",'SMSOTHER'";
        }
        
        $sqlStatement .= ")";
        
        return $sqlStatement;
    }

    public function updateOptInOut($objParms)
    {

        $sqlStatement = $this->buildUpdateOptInOut($objParms);
        $ds = $this->executeSQL($sqlStatement, $errorObj);
 
        return $ds;
    }

    public function escapeForSql($target)
    {
        $clean = str_replace("'", "''", $target);
        $clean = str_replace("\\", "\\\\",$clean);
        return $clean;
    }
}
