#!/bin/sh
HOST='172.29.211.163'
USER='adp'
PASSWD='Ndac10ud'
SOURCEREALBASE='/adp/masterdbases/reality1/H.qMUFbMACQb'
TARGETREALBASE='/adp/masterdbases/reality1/H.qMUFbMACQb'

ACCTNAME='QS-_BMW_:1'
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

ACCTNAME='QS-IND'
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

ACCTNAME='QS-_PORCAN_'
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

ACCTNAME='QS-_PORSCHE_'
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

ACCTNAME='QS-LEASE'
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

ACCTNAME='QS-MACK'
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

ACCTNAME='QS-MACKLSE'
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

ACCTNAME='QS-MASER'
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

ACCTNAME='QS-MCLAR'
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

ACCTNAME='QS-MCLARCAN'
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

ACCTNAME='QS-PACCAR'
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

ACCTNAME='QS-REC'
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

ACCTNAME='QS-SELTRK'
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

ACCTNAME='QS-STD'
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

ACCTNAME='QS-SUZCAN'
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

ACCTNAME='QS-TRK'
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

ACCTNAME='QS-_ACURACAN_'
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

ACCTNAME='QS-_AUDICAN_'
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

ACCTNAME='QS-_AUDI_'
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

ACCTNAME='QS-_BENCAN_'
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

ACCTNAME='QS-_FORD_'
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

ACCTNAME='QS-_GMCAN_'
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

ACCTNAME='QS-=5BACURA=5D'
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

ACCTNAME='QS-=5BDTNA=5D'
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

ACCTNAME='QS-FISKER'
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

ACCTNAME='QS-HONDAMC'
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

ACCTNAME='QS-_GM_'
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

ACCTNAME='QS-_HONDACAN_'
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

ACCTNAME='QS-_HONDA_'
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

ACCTNAME='QS-_HONDPCAN_'
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

ACCTNAME='QS-_HYUCAN_'
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

ACCTNAME='QS-_HYU_'
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

ACCTNAME='QS-_INFINCAN_'
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

ACCTNAME='QS-_INFIN_'
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

ACCTNAME='QS-_ISUZU_'
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

ACCTNAME='QS-_JAG_'
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

ACCTNAME='QS-_KIACAN_'
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

ACCTNAME='QS-_KIA_'
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

ACCTNAME='QS-_LAM_'
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

ACCTNAME='QS-_LEXCAN_'
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

ACCTNAME='QS-_LEX_'
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

ACCTNAME='QS-_LR_'
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

ACCTNAME='QS-_MAZDACAN_'
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

ACCTNAME='QS-_MAZDA_'
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

ACCTNAME='QS-_BEN_'
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

ACCTNAME='QS-_BMWMC_'
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

ACCTNAME='QS-_MBCAN_'
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

ACCTNAME='QS-_SPRINT_'
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

ACCTNAME='QS-_SUBCAN_'
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

ACCTNAME='QS-_SUB_'
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

ACCTNAME='QS-_SUZ_'
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

ACCTNAME='QS-_TOYCAN_'
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

ACCTNAME='QS-_TOY_'
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

ACCTNAME='QS-_VOLVO_'
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

ACCTNAME='QS-_VWCAN_'
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

ACCTNAME='QS-_VW_'
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

ACCTNAME='QS-_CHRYCAN_'
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

ACCTNAME='QS-_CHRY_'
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

ACCTNAME='QS-_FERRARI_'
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

ACCTNAME='QS-_FIAT_'
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

ACCTNAME='QS-_FIAT_'
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

ACCTNAME='QS-_MB_'
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

ACCTNAME='QS-_MITCAN_'
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

ACCTNAME='QS-_MIT_'
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

ACCTNAME='QS-_NCVCAN_'
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

ACCTNAME='QS-_NISCAN_'
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

ACCTNAME='QS-_NIS_'
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

ACCTNAME='QS-_NSTAR_'
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

################################################################
################################################################
################################################################

ACCTNAME='BARB'
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

ACCTNAME='DIANE'
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

ACCTNAME='RICK'
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

ACCTNAME='PETE'
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

ACCTNAME='HV-A'
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

ACCTNAME='HV-CM'
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

ACCTNAME='HV-P'
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

ACCTNAME='HVC-FI'
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

ACCTNAME='HVC-I'
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

ACCTNAME='HVH-S'
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

ACCTNAME='HVH-SL'
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

ACCTNAME='HVH-V'
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

ACCTNAME='HVH-FI'
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

ACCTNAME='HVH-I'
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

ACCTNAME='HVH-P'
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

ACCTNAME='HVH-S'
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

ACCTNAME='HVH-SL'
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

ACCTNAME='HVH-V'
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

exit 0



