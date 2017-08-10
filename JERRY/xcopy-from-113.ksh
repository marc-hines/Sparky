#!/bin/sh
HOST='172.29.207.113'
USER='adp'
PASSWD='*********'

SOURCEREALBASE='/adp/masterdbases/reality1/H.ffApcvab5p'
TARGETREALBASE='/adp/masterdbases/reality1/H.OedcMqbiq'

ACCTNAME='JERRY'
rm $TARGETREALBASE/$ACCTNAME/*
ftp -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
binary
prompt
lcd $TARGETREALBASE/$ACCTNAME
cd $SOURCEREALBASE/$ACCTNAME
mget *
quit
END_SCRIPT


