      * PROGRAM QA.CREATE.GL.QS
      * 03/10/2006 * LLS * NEW MODULE
      * Based on FS.GL.DUMP.QS.TAPE * Neal Tollisen * 1995
      * Copyright 2006 ADP Dealer Services
      *
      * 4/2010 * RP810 * LLS * localized processing to perform GL conversion
      * of imported QA9nn Quick-Start project.
      *
      * Overview:
      *
      * 1.  This routine first formats pre-GL version of the QS-FILE for GL.
      *
      * 2.  Next, it calls these subroutines:
      *                    QA.SUB.BUILD.ACCT
      *                    QA.SUB.CONV.SCHED
      *                    QA.SUB.CONV.TITLE
      *                    QA.SUB.CONV.ACCTG 
      *
      *     to build these files from pre-GL data:
      *                    QS-aaa/GL.COA
      *                    QS-aaa/GL.SALE.CHN
      *                    QS-aaa/GL.PCL
      *                    QS-aaa/GL.COA.GRP
      *                    QS-aaa/GL.SCHED.SETUP
      *                    QS-aaa/GL.CIB.SETUP
      *                    QS-aaa/GL.DGL.SETUP
      *                    QS-aaa/GL.RPT.SETUP
      *                    QS-aaa/GL.DEPT
      *
      * 3.  Next it build the GL version QS-aaa/PRIVLIB file. 
      *
      ***********************************
      * MAIN PROGRAM
      ***********************************
      *
      EQU AM TO CHAR(254)
      EQU VM TO CHAR(253)
      GOSUB INIT
      GOSUB BUILD.QS.FILE
      * Loop through the manufacturers and build files
      MANUF.CNT = 0
      LOOP MANUF.CNT = MANUF.CNT + 1 WHILE QS.TABLE<1,MANUF.CNT> NE '' DO
         MFG = "QS-":QS.TABLE<1,MANUF.CNT>
         PRINT;PRINT STR("*",70);PRINT
         PRINT "Now processing ":MFG
         PRINT
         GOSUB CREATE.GL.FILES
         GOSUB BUILD.GL.FILES
         *
         PRINT;PRINT "Removing original (pre-convert) GL.DEPT items."
         COMMAND = 'SELECT ':MFG:'/GL.DEPT = "1*]"'
         PERFORM COMMAND RTNLIST GL.DEPT.ITEMS CAPTURING OUTPUT SETTING ERRMSG
         IF ERRMSG<1,1> = "404" THEN
            LOOP WHILE READNEXT DEPTITEM FROM GL.DEPT.ITEMS DO
               COMMAND = "DELETE ":MFG:"/GL.DEPT ":DEPTITEM
               PERFORM COMMAND
            REPEAT
         END
      REPEAT
      *
      * Delete unnecessary files
      COMMAND = "DELETE-FILE JRNL"
      PERFORM COMMAND CAPTURING OUTPUT SETTING ERRMSG
      DELETE.LIST = ""
      DELETE.LIST<-1> = "[/ACCT"
      DELETE.LIST<-1> = "[/BALANCE-FWD"
      DELETE.LIST<-1> = "[/DETAIL-FWD"
      DELETE.LIST<-1> = "[/TITLE"
      DELETE.LIST<-1> = "[/GL.ACCT.MAP"
      DELETE.LIST<-1> = "FS-STATS"
      DELETE.LIST<-1> = "NULL"
      DELETE.LIST<-1> = "TSYM"
      DELETE.LIST<-1> = "SYSCTRL"
      DELETE.CTR = DCOUNT(DELETE.LIST, AM)
      FOR X = 1 TO DELETE.CTR
         COMMAND = 'SELECT MD WITH *A1 "D]" AND WITH *A0 "':DELETE.LIST<X>:'"'
         PERFORM COMMAND RTNLIST FILE.DELETE.LIST CAPTURING OUTPUT SETTING ERRMSG
         IF ERRMSG<1,1> = "404" THEN
            LOOP WHILE READNEXT ID FROM FILE.DELETE.LIST DO
               COMMAND = "DELETE-FILE ":ID
               PERFORM COMMAND
            REPEAT
         END
      NEXT X
      *
END.OF.JOB: *
      WRITEV "1" ON PROJ.MD.FILE, "FINAL-FLAG", 1
      ACCOUNT = "REL-PROD-OP"
      CALL SY.WANDER.SUB(ACCOUNT,"C", ERROR.CODE )
      IF ERROR.CODE # "" THEN
         PRINT "QA.CREATE.GL.QS Error: Could not wander to ":ACCOUNT
         STOP
      END
      STOP
      *
      ***********************************
      * SUBROUTINES
      ***********************************
      *
INIT: 
      * Initialize variables
      * Prompt for source account name
      MY.PORT = SYSTEM(18)
      OPEN 'DICT', 'SYSTEM' TO SYSTEM.FILE ELSE
         PRINTERR 201:AM:"DICT SYSTEM"
         PRINT "QA.CREATE.GL.QS Error: Could not open the SYSTEM file."
         STOP
      END
      PROMPT ""
      PROMPT.FLAG = 0
      LOOP UNTIL PROMPT.FLAG DO
         PRINT
         PRINT "Enter source project number (e.g., QA9xx)...":
         INPUT PROJECT1
         READ SYS.REC FROM SYSTEM.FILE, PROJECT1:'-LOGON' THEN
            PROMPT.FLAG = 1
         END ELSE
            PRINT;PRINT "QA.CREATE.GL.QS Error: Source Project ":PROJECT1:"-LOGON is not on the RPS system."
            PRINT;PRINT "Do you want to exit (y/n)? ":
            INPUT ANSWER:
            ANSWER = TRIM(ANSWER)
            IF ANSWER = 'y' OR ANSWER = "Y" THEN STOP
            PRINT
         END
      REPEAT
      *
      * Since this program works with the files in the
      * QA9XX-LOGON, then wander to it and work there
      ACCOUNT = PROJECT1:"-LOGON"
      CALL SY.WANDER.SUB(ACCOUNT,"C", ERROR.CODE )
      IF ERROR.CODE # "" THEN
         PRINT "QA.CREATE.GL.QS Error: Could not wander to ":ACCOUNT
         STOP
      END
      OPEN "DICT","MD" TO PROJ.MD.FILE ELSE
         PRINTERR 201:AM:"DICT MD"
         PRINT "QA.CREATE.GL.QS Error: Could not open ":ACCOUNT:" MD file."
         STOP
      END
      
      
      PRINT
      PRINT "Now creating DATA QS-FILE file."
      TEST.FILE = "QS-FILE"
      OPEN 'DICT', TEST.FILE TO TEMP.QS THEN
         CLOSE TEMP.QS
      END ELSE
         PRINT "QA.CREATE.GL.QS Error: DICT ":TEST.FILE:" does not exist."
         STOP
      END
      CALL GET.FILE.SIZE (TEST.FILE, ACCOUNT, DICT.BASE, DICT.MOD, DICT.SEP, DATA.BASE, DATA.MOD, DATA.SEP )
      IF DATA.BASE = "" THEN
         STMT = "CREATE-FILE DATA ":TEST.FILE:" 1,1"
         PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
         IF ERRMSG<1,1> # 417 THEN
            PRINT "QA.CREATE.GL.QS Error: Cannot create the file DATA ":TEST.FILE:" in ":ACCOUNT
            STOP
         END
         COMMAND = "SELECT DICT ":TEST.FILE:" # '":TEST.FILE:"'"
         PERFORM COMMAND RTNLIST SELECT.ITEMS CAPTURING OUTPUT SETTING ERRMSG
         IF ERRMSG<1,1> = "404" THEN
            COMMAND = "COPY DICT ":TEST.FILE:" (D)"
            DATA "(":TEST.FILE
            PERFORM COMMAND PASSLIST SELECT.ITEMS CAPTURING OUTPUT
         END
      END
      OPEN "QS-FILE" TO QS.FILE ELSE
         PRINT 'QA.CREATE.GL.QS Error: ':ACCOUNT:' QS-FILE cannot be opened.'
         STOP
      END
      READ FS.DATE FROM QS.FILE,'DATE' ELSE FS.DATE = "9999"
      *
      RETURN
      * end of INIT subroutine
      *
BUILD.QS.FILE: 
      QS.TABLE = ''
      *
      READ FRANCHISES.REC FROM QS.FILE,'FRANCHISES' ELSE
         PRINT "QA.CREATE.GL.QS Error: No item FRANCHISES from QS-FILE on ":ACCOUNT
         STOP
      END
      *
      DEL FRANCHISES.REC<1>
      AM.COUNT = DCOUNT(FRANCHISES.REC,AM)
      FOR AMC = 1 TO AM.COUNT
         MFG.DATA.LINE = FRANCHISES.REC<AMC>
         MFG.CODE = FIELD(MFG.DATA.LINE,'=',1)
         MFG.CODE = TRIM(MFG.CODE)
         LOCATE MFG.CODE IN QS.TABLE<1> SETTING POS ELSE
            INS MFG.CODE BEFORE QS.TABLE<1,POS>
            INS "" BEFORE QS.TABLE<2,POS>
            INS MFG.DATA.LINE BEFORE QS.TABLE<3,POS>
         END
      NEXT AMC
      *
      LINE1.MV.COUNT = DCOUNT(QS.TABLE<1>,VM)
      LINE3.MV.COUNT = DCOUNT(QS.TABLE<3>,VM)
      IF LINE1.MV.COUNT NE LINE3.MV.COUNT THEN
         PRINT "QA.CREATE.GL.QS Error: Mismatch error in FRANCHISES."
         STOP
      END
      WRITE QS.TABLE ON QS.FILE,'QS-TABLE'
      RETURN
      * End of subroutine BUILD.QS.FILE
      
      *
CREATE.GL.FILES: 
      PRINT
      PRINT "Now creating GL Quick-Start files."
      STMT = "CREATE-FILE ":MFG:"/GL.COA 1,1 101,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.COA in ":ACCOUNT
         STOP
      END
      *
      STMT = "CREATE-FILE ":MFG:"/GL.SALE.CHN 1,1 5,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.SALE.CHN in ":ACCOUNT
         STOP
      END
      *
      STMT = "CREATE-FILE ":MFG:"/GL.PCL 1,1 29,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.PCL in ":ACCOUNT
         STOP
      END
      *
      STMT = "CREATE-FILE ":MFG:"/GL.COA.GRP 1,1 7,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.COA.GRP in ":ACCOUNT
         STOP
      END
      *
      STMT = "CREATE-FILE ":MFG:"/GL.SCHED.SETUP 1,1 7,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.SCHED.SETUP in ":ACCOUNT
         STOP
      END
      *
      STMT = "CREATE-FILE ":MFG:"/GL.CIB.SETUP 1,1 1,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.CIB.SETUP in ":ACCOUNT
         STOP
      END
      *
      STMT = "CREATE-FILE ":MFG:"/GL.DGL.SETUP 1,1 1,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.DGL.SETUP in ":ACCOUNT
         STOP
      END
      *
      STMT = "CREATE-FILE ":MFG:"/GL.RPT.SETUP 1,1 7,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.RPT.SETUP in ":ACCOUNT
         STOP
      END
      *
      OPEN MFG:"/GL.DEPT" TO GL.DEPT.FILE ELSE
         STMT = "CREATE-FILE ":MFG:"/GL.DEPT 1,1 1,1"
         PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
         IF ERRMSG<1,1> # 417 THEN
            PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/GL.DEPT in ":ACCOUNT
            STOP
         END
      END
      *
      PRINT
      PRINT "Now creating DATA ":MFG:"/PRIVLIB file."
      TEST.FILE = MFG:"/PRIVLIB"
      OPEN 'DICT', TEST.FILE TO TEMP.PRIV THEN
         CLOSE TEMP.PRIV
      END ELSE
         PRINT "QA.CREATE.GL.QS Error: DICT ":TEST.FILE:" does not exist."
         STOP
      END
      CALL GET.FILE.SIZE (TEST.FILE, ACCOUNT, DICT.BASE, DICT.MOD, DICT.SEP, DATA.BASE, DATA.MOD, DATA.SEP )
      IF DATA.BASE = "" THEN
         STMT = "CREATE-FILE DATA ":TEST.FILE:" 7,1"
         PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
         IF ERRMSG<1,1> # 417 THEN
            PRINT "QA.CREATE.GL.QS Error: Cannot create the file DATA ":MFG:"/PRIVLIB in ":ACCOUNT
            STOP
         END
         COMMAND = "SELECT DICT ":TEST.FILE:" # '":TEST.FILE:"'"
         PERFORM COMMAND RTNLIST SELECT.ITEMS CAPTURING OUTPUT SETTING ERRMSG
         IF ERRMSG<1,1> = "404" THEN
            COMMAND = "COPY DICT ":TEST.FILE:" (D)"
            DATA "(":TEST.FILE
            PERFORM COMMAND PASSLIST SELECT.ITEMS CAPTURING OUTPUT
         END
      END
      *
      *
      OPEN MFG:"/NDOC" TO NDOC.FILE ELSE
         STMT = "CREATE-FILE ":MFG:"/NDOC 1,1 31,1"
         PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
         IF ERRMSG<1,1> # 417 THEN
            PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/NDOC in ":ACCOUNT
            STOP
         END
      END
      *
      STMT = "CREATE-FILE ":MFG:"/PROD-FILE 1,1 3,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/PROD-FILE in ":ACCOUNT
         STOP
      END
      *
      STMT = "CREATE-FILE ":MFG:"/ACR-GL-ACCTS 1,1 1,1"
      PERFORM STMT CAPTURING OUTPUT SETTING ERRMSG
      IF ERRMSG<1,1> # 417 THEN
         PRINT "QA.CREATE.GL.QS Error: Cannot create the file ":MFG:"/ACR-GL-ACCTS in ":ACCOUNT
         STOP
      END
      *
      RETURN
      * end of CREATE.GL.FILES subroutine
      *
BUILD.GL.FILES: 
      MANUF = QS.TABLE<1,MANUF.CNT>
      ORIG.MANUF = MANUF
      IF MANUF[1,2] EQ "GM" AND LEN(MANUF) EQ 3 THEN
         ORIG.MANUF = "GM"
         BEGIN CASE
         CASE MANUF[3,1] EQ "1"
            MANUF = "BUICK"
         CASE MANUF[3,1] EQ "2"
            MANUF = "CAD"
         CASE MANUF[3,1] EQ "3"
            MANUF = "CHEV"
         CASE MANUF[3,1] EQ "4"
            MANUF = "OLDS"
         CASE 1
            MANUF = "PONTIAC"
         END CASE
      END
      ACCTG.LOGON.ID = "QS-":MANUF
      * update GL-PRIVLIB with amended name for specials item
      * GLJRNL is included so CONV.ACCT routine has it; then deleted
      * SCHED-FILE2 is included for SCHED conversions, then deleted
      * PRINT "STMT IS: COPY ":ACCTG.LOGON.ID:"/PRIVLIB AR-FILE2 SCHED-FILE2 INT-ACCT MISFORM DOCTBL PRODUCTIVITY GLJRNL"
      OPEN '', ACCTG.LOGON.ID:"/PRIVLIB" TO SRC.FILE ELSE
         PRINT "QA.CREATE.GL.QS Error: Unable to open source file ":ACCTG.LOGON.ID:"/PRIVLIB":"."
         STOP
      END
      *
      OPEN '', MFG:'/PRIVLIB' TO GL.PRIVLIB.FILE ELSE
         PRINT "QA.CREATE.GL.QS Error: Unable to open target file ":MFG:"/PRIVLIB."
         STOP
      END
      *
      *      DATA "(":MFG:"/PRIVLIB"
      *      PERFORM "COPY ":ACCTG.LOGON.ID:"/PRIVLIB":" AR-FILE2 SCHED-FILE2 INT-ACCT MISFORM DOCTBL PRODUCTIVITY GLJRNL"
      *
      * PRINT "STMT IS: COPY ":ACCTG.LOGON.ID:"/PRIVLIB FS-":ORIG.MANUF:"-1"
      PRINT;PRINT "Processing SPECIALS item."
      DATA "(":MFG:"/PRIVLIB FS-":ORIG.MANUF:"-fs#"
      PERFORM "COPY ":ACCTG.LOGON.ID:"/PRIVLIB ":" FS-":ORIG.MANUF:"-1 (D)"
      *
      *
      * Check for FS-SETUP file references
      READ SPECIALS.ITEM FROM GL.PRIVLIB.FILE,"FS-":ORIG.MANUF:"-fs#" THEN
         IF INDEX(SPECIALS.ITEM,"FS-SETUP",1) NE 0 THEN
            SPECIALS.ATTR = 0
            LOOP SPECIALS.ATTR = SPECIALS.ATTR + 1 WHILE SPECIALS.ITEM<SPECIALS.ATTR> NE '' DO
               IF INDEX(SPECIALS.ITEM<SPECIALS.ATTR>,"FS-SETUP",1) NE 0 THEN
                  AST.LOC = INDEX(SPECIALS.ITEM<SPECIALS.ATTR>,"*",1)
                  SPECIALS.ITEM<SPECIALS.ATTR> = SPECIALS.ITEM<SPECIALS.ATTR>[1,AST.LOC]:"fs#":SPECIALS.ITEM<SPECIALS.ATTR>[AST.LOC+2,99]
               END
            REPEAT
            WRITE SPECIALS.ITEM ON GL.PRIVLIB.FILE,"FS-":ORIG.MANUF:"-fs#"
         END
         DELETE GL.PRIVLIB.FILE,"FS-":ORIG.MANUF:"-fs#"
         WRITE SPECIALS.ITEM ON GL.PRIVLIB.FILE,"FS-":ORIG.MANUF:"-fs#-":FS.DATE
      END
      *
      IF ORIG.MANUF[1,2] EQ "GM" AND LEN(ORIG.MANUF) LT 4 THEN
         DATA "(":MFG:"/PRIVLIB FS-GM[FACTS]-fs2"
         PERFORM "COPY ":ACCTG.LOGON.ID:"/PRIVLIB FS-GM[FACTS]-2 (D)"
         * Check for FS-SETUP file references
         READ SPECIALS.ITEM FROM GL.PRIVLIB.FILE,"FS-GM[FACTS]-fs2" THEN
            IF INDEX(SPECIALS.ITEM,"FS-SETUP",1) NE 0 THEN
               SPECIALS.ATTR = 0
               LOOP SPECIALS.ATTR = SPECIALS.ATTR + 1 WHILE SPECIALS.ITEM<SPECIALS.ATTR> NE '' DO
                  IF INDEX(SPECIALS.ITEM<SPECIALS.ATTR>,"FS-SETUP",1) NE 0 THEN
                     AST.LOC = INDEX(SPECIALS.ITEM<SPECIALS.ATTR>,"*",1)
                     SPECIALS.ITEM<SPECIALS.ATTR> = SPECIALS.ITEM<SPECIALS.ATTR>[1,AST.LOC]:"fs2":SPECIALS.ITEM<SPECIALS.ATTR>[AST.LOC+2,99]
                  END
               REPEAT
               WRITE SPECIALS.ITEM ON GL.PRIVLIB.FILE,"FS-GM[FACTS]-fs2"
            END
            DELETE GL.PRIVLIB.FILE,"FS-GM[FACTS]-fs2"
            WRITE SPECIALS.ITEM ON GL.PRIVLIB.FILE,"FS-GM[FACTS]-fs2-":FS.DATE
         END
      END
      IF ORIG.MANUF[1,5] EQ "GMCAN" THEN
         DATA "(":MFG:"/PRIVLIB FS-[FACTS]-fs2"
         PERFORM "COPY ":ACCTG.LOGON.ID:"/PRIVLIB FS-[FACTS]-2 (D)"
         * Check for FS-SETUP file references
         READ SPECIALS.ITEM FROM GL.PRIVLIB.FILE,"FS-[FACTS]-fs2" THEN
            IF INDEX(SPECIALS.ITEM,"FS-SETUP",1) NE 0 THEN
               SPECIALS.ATTR = 0
               LOOP SPECIALS.ATTR = SPECIALS.ATTR + 1 WHILE SPECIALS.ITEM<SPECIALS.ATTR> NE '' DO
                  IF INDEX(SPECIALS.ITEM<SPECIALS.ATTR>,"FS-SETUP",1) NE 0 THEN
                     AST.LOC = INDEX(SPECIALS.ITEM<SPECIALS.ATTR>,"*",1)
                     SPECIALS.ITEM<SPECIALS.ATTR> = SPECIALS.ITEM<SPECIALS.ATTR>[1,AST.LOC]:"fs2":SPECIALS.ITEM<SPECIALS.ATTR>[AST.LOC+2,99]
                  END
               REPEAT
               WRITE SPECIALS.ITEM ON GL.PRIVLIB.FILE,"FS-[FACTS]-fs2"
            END
            DELETE GL.PRIVLIB.FILE,"FS-[FACTS]-fs2"
            WRITE SPECIALS.ITEM ON GL.PRIVLIB.FILE,"FS-[FACTS]-fs2-":FS.DATE
         END
      END
      *
      PRINT;PRINT "Now performing ACCT conversion."
      CALL QA.SUB.CONV.ACCT(PROJ.MD.FILE,ACCTG.LOGON.ID,FS.DATE,ERROR)
      IF ERROR  # "" THEN 
         PRINT ERROR
         PRINT "QA.CREATE.GL.QS: Error returned from QA.SUB.CONV.ACCT."
         STOP
      END
      *
      DELETE GL.PRIVLIB.FILE,'GLJRNL'
      PRINT;PRINT "Now performing SCHED conversion."
      CALL QA.SUB.CONV.SCHED(PROJ.MD.FILE,ACCTG.LOGON.ID,ERROR)
      IF ERROR  # "" THEN
         PRINT ERROR
         PRINT "QA.CREATE.GL.QS: Error returned from QA.SUB.CONV.SCHED."
         STOP
      END
      *
      PRINT;PRINT "Now performing TITLE conversion."
      CALL QA.SUB.CONV.TITLE(PROJ.MD.FILE,ACCTG.LOGON.ID,ERROR)
      IF ERROR # "" THEN
         PRINT ERROR
         PRINT "QA.CREATE.GL.QS: Error returned from QA.SUB.CONV.TITLE."
         STOP
      END
      *
      PRINT;PRINT "Now performing ACCTG conversion."
      CALL QA.SUB.CONV.ACCTG(PROJ.MD.FILE,ACCTG.LOGON.ID,ERROR)
      DELETE GL.PRIVLIB.FILE,'SCHED-FILE2'
      IF ERROR # "" THEN
         PRINT ERROR
         PRINT "QA.CREATE.GL.QS: Error returned from QA.SUB.CONV.ACCTG."
         STOP
      END
      RETURN
      * End of subroutine BUILD.GL.FILES
      
      
