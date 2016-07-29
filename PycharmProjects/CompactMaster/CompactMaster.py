
import os

def convert_to_cora_name(dirty_name: str) -> str:
    """
    Converts linux file names from the RPS
    method of writing CoRa names to the original
    CoRa name.

      FS-_kFIAT_t-MASTER becomes FS-[FIAT]-MASTER
      _ePS143_e          becomes !PS143!
      FERRARI_fOLD       becomes FERRARI/OLD

    """
    clean_name = dirty_name.replace('__','gEc')
    clean_name = clean_name.replace('_a','*')
    clean_name = clean_name.replace('_b','\\')
    clean_name = clean_name.replace('_c','$')
    clean_name = clean_name.replace('_d','"')
    clean_name = clean_name.replace('_e','!')
    clean_name = clean_name.replace('_f','/')
    clean_name = clean_name.replace('_g','>')
    clean_name = clean_name.replace('_h','#')
    clean_name = clean_name.replace('_k','[')
    clean_name = clean_name.replace('_l','<')
    clean_name = clean_name.replace('_p','(')
    clean_name = clean_name.replace('_q',"'")
    clean_name = clean_name.replace('_r',')')
    clean_name = clean_name.replace('_s',';')
    clean_name = clean_name.replace('_t',']')
    clean_name = clean_name.replace('_u','^')
    clean_name = clean_name.replace('_v','|')
    clean_name = clean_name.replace('_A','&')
    clean_name = clean_name.replace('_C',':')
    clean_name = clean_name.replace('_E','=')
    clean_name = clean_name.replace('_G','`')
    clean_name = clean_name.replace('_Q','?')
    clean_name = clean_name.replace('gEc','_')
    return clean_name

def convert_to_compact_master_name(dirty_name: str) -> str:
    """
    Converts linux file name from the RPS
    convention or a CoRa convention name to a
    clean compact master name.

      FS-_kFIAT_t-MASTER becomes FIAT.master
      FS-[GM]-MASTER     becomes GM.master
      FS-LEASE-MASTER    becomes LEASE.master

    """
    clean_name = convert_to_cora_name(dirty_name)
    clean_name = clean_name.replace('-MASTER', '')
    clean_name = clean_name.replace(']', '')
    clean_name = clean_name.replace('FS-', '')
    clean_name = clean_name.replace('[', '')
    return clean_name

def escape_cora_item_to_str(binary_data: bytes ) -> str:
    """
    Converts linux ascii binary_data to an html encoded clean string.
    """
    byte_array = bytearray(binary_data)
    clean_str = ""
    for by in byte_array:
        if (by < 10) or (by > 10 and by < 32) or (by > 127):
            clean_str = clean_str + '&#' + '{:0>3}'.format(str(by)) +';'
        else:
            clean_str = clean_str + chr(by)
    clean_str = clean_str.replace('&amp;', '!AMP!') # already encoded ampersand
    return clean_str

def append_data_to_compact_master(target_file_obj , source_path: str, source_name: str , data_level: str, compact_master_name: str):
    """

    """
    raw_file_list = os.listdir(source_path)

    for raw_file_name in sorted(set(raw_file_list)):
        if (raw_file_name != source_name) and (raw_file_name[0:1] != '.'):
            source_file_obj = open(os.path.join(source_path, raw_file_name), mode='br')
            source_file = escape_cora_item_to_str(source_file_obj.read())
            source_file_obj.close()
            clean_file_name = convert_to_cora_name(raw_file_name)
            if (data_level == 'DATA'):
                if (clean_file_name[0:1] == '!'):
                    file_type = 'ORD'
                else:
                    file_type = 'PLC'
            else:
                if (source_file[0:1] == 'A') or (source_file[0:1] == 'S'):
                    file_type = 'DICT'
                elif (clean_file_name[0:1] >= '0') and (clean_file_name[0:1] <= '9'):
                    file_type = 'PCL'
                elif (clean_file_name[0:6] == 'TBLRCS'):
                    file_type = 'TBLRCS'
                elif (clean_file_name[0:8] == 'EDIT-TBL'):
                    file_type = 'EDITTBL'
                elif (clean_file_name[0:8] == 'XMIT.TBL'):
                    file_type = 'XMITTBL'
                elif (clean_file_name == 'USER.SPECIALS.TABLE'):
                    file_type = 'USERSPECIALS'
                elif (clean_file_name == 'STD-PCL-CODES'):
                    file_type = 'STDPCLCODES'
                elif (clean_file_name == 'FORMS'):
                    file_type = 'FORMS'
                elif (clean_file_name == 'FORMSWEB'):
                    file_type = 'FORMSWEB'
                elif (clean_file_name == 'DISP.TABLE'):
                    file_type = 'DISPTBL'
                elif (clean_file_name == 'PERCENT.TABLE'):
                    file_type = 'PERTBL'
                elif (clean_file_name == 'FRANCHISE.PAGING.TABLE'):
                    file_type = 'FPAGETBL'
                elif (clean_file_name == 'PCL.CONVERSION.TABLE'):
                    file_type = 'CONVPCL'
                elif (clean_file_name == 'MEMO.PCL.LIST'):
                    file_type = 'MEMOPCL'
                elif (clean_file_name == 'OPTIONAL.PAGES'):
                    file_type = 'OPTPGS'
                elif (clean_file_name == 'PCL.TABLE'):
                    file_type = 'PCLTBL'
                elif (clean_file_name == 'RE.PCL'):
                    file_type = 'REPCL'
                elif (clean_file_name == 'PROFIT.PCL'):
                    file_type = 'PROFITPCL'
                elif (clean_file_name[len(clean_file_name)-5:len(clean_file_name)] == '-STAT'):
                    file_type = 'STAT'
                elif (clean_file_name[len(clean_file_name)-9:len(clean_file_name)] == '-SPECIALS'):
                    file_type = 'MFRSPECIALS'
                elif (clean_file_name == 'CHECK-SUM'):
                    file_type = 'CHKSUM'
                elif (clean_file_name == 'DATE'):
                    file_type = 'DATE'
                elif (clean_file_name == 'AMDSG.NEGATIVE.ACCTS'):
                    file_type = 'AMDSGNEGACCTS'
                elif (clean_file_name == 'AMDSG.PRINT.MASKS'):
                    file_type = 'AMDSGPRTMASKS'
                elif (clean_file_name == 'AMDSG.ROUNDED.FLAG'):
                    file_type = 'AMDSGROUNDEDFLAG'
                elif (clean_file_name == 'DET.TBL'):
                    file_type = 'DETTBL'
                elif (clean_file_name[len(clean_file_name)-4:len(clean_file_name)] == '.OLD'):
                    file_type = 'TXT'
                elif (clean_file_name[len(clean_file_name)-8:len(clean_file_name)] == 'XMIT.URL'):
                    file_type = 'XMITURL:' + compact_master_name
                else:
                    print(convert_to_cora_name(source_name) + ": " + clean_file_name)
                    file_type = 'MFR:' + compact_master_name
            target_file_obj.write("<<<" + data_level + ":"
                                  + clean_file_name + ":"
                                  + file_type
                                  + ">>>" + chr(10))
            target_file_obj.write(source_file)

def compact_one_master(source_master_name: str):

    source_repo_path = "/Users/hinesm/gitrepos/fs_cora"
    source_master_dict_path = os.path.join(source_repo_path, source_master_name)
    source_master_data_path = os.path.join(os.path.join(source_repo_path, source_master_name), source_master_name)

    target_compact_master_path = "/Users/hinesm/gitrepos/fs_masters/17533/"
    target_master_name = convert_to_cora_name(source_master_name)
    target_compact_master_name = convert_to_compact_master_name(source_master_name)

    target_file_obj = open(os.path.join(target_compact_master_path, target_compact_master_name) + '.master', mode='w', encoding='ascii')
    target_file_obj.write("<<<<MASTER:" + target_master_name + ">>>>" + chr(10))
    target_file_obj.write("<<<<VERSION:17533:00001>>>>" + chr(10))
    append_data_to_compact_master(target_file_obj, source_master_dict_path,
                                  source_master_name, 'DICT', target_compact_master_name)
    append_data_to_compact_master(target_file_obj, source_master_data_path,
                                  source_master_name, 'DATA', target_compact_master_name)
    target_file_obj.write("<<<<END>>>>" + chr(10))
    target_file_obj.close()

compact_one_master("FS-_kACURA_t-MASTER")
compact_one_master("FS-_kACURACAN_t-MASTER")
compact_one_master("FS-_kAUDI_t-MASTER")
compact_one_master("FS-_kAUDICAN_t-MASTER")
compact_one_master("FS-_kBEN_t-MASTER")
compact_one_master("FS-_kBENCAN_t-MASTER")
compact_one_master("FS-_kBMW_t-MASTER")
compact_one_master("FS-_kBMWMC_t-MASTER")
compact_one_master("FS-_kCHRY_t-MASTER")
compact_one_master("FS-_kCHRYCAN_t-MASTER")
compact_one_master("FS-_kDTNA_t-MASTER")
compact_one_master("FS-_kFERRARI_t-MASTER")
compact_one_master("FS-_kFIAT_t-MASTER")
compact_one_master("FS-_kFORD_t-MASTER")
compact_one_master("FS-_kGM_t-MASTER")
compact_one_master("FS-_kGMCAN_t-MASTER")
compact_one_master("FS-_kHONDA_t-MASTER")
compact_one_master("FS-_kHONDACAN_t-MASTER")
compact_one_master("FS-_kHONDPCAN_t-MASTER")
compact_one_master("FS-_kHYU_t-MASTER")
compact_one_master("FS-_kHYUCAN_t-MASTER")
compact_one_master("FS-_kINFIN_t-MASTER")
compact_one_master("FS-_kINFINCAN_t-MASTER")
compact_one_master("FS-_kISUZU_t-MASTER")
compact_one_master("FS-_kJAG_t-MASTER")
compact_one_master("FS-_kKIA_t-MASTER")
compact_one_master("FS-_kKIACAN_t-MASTER")
compact_one_master("FS-_kLAM_t-MASTER")
compact_one_master("FS-_kLEX_t-MASTER")
compact_one_master("FS-_kLEXCAN_t-MASTER")
compact_one_master("FS-_kLR_t-MASTER")
compact_one_master("FS-_kMAZDA_t-MASTER")
compact_one_master("FS-_kMAZDACAN_t-MASTER")
compact_one_master("FS-_kMB_t-MASTER")
compact_one_master("FS-_kMBCAN_t-MASTER")
compact_one_master("FS-_kMIT_t-MASTER")
compact_one_master("FS-_kMITCAN_t-MASTER")
compact_one_master("FS-_kNIS_t-MASTER")
compact_one_master("FS-_kNISCAN_t-MASTER")
compact_one_master("FS-_kNSTAR_t-MASTER")
compact_one_master("FS-_kPORCAN_t-MASTER")
compact_one_master("FS-_kPORSCHE_t-MASTER")
compact_one_master("FS-_kSPRINT_t-MASTER")
compact_one_master("FS-_kSUB_t-MASTER")
compact_one_master("FS-_kSUBCAN_t-MASTER")
compact_one_master("FS-_kSUZ_t-MASTER")
compact_one_master("FS-_kTOY_t-MASTER")
compact_one_master("FS-_kTOYCAN_t-MASTER")
compact_one_master("FS-_kVOLVO_t-MASTER")
compact_one_master("FS-_kVW_t-MASTER")
compact_one_master("FS-_kVWCAN_t-MASTER")
compact_one_master("FS-FISKER-MASTER")
compact_one_master("FS-HONDAMC-MASTER")
compact_one_master("FS-IND-MASTER")
compact_one_master("FS-LEASE-MASTER")
compact_one_master("FS-MACK-MASTER")
compact_one_master("FS-MASER-MASTER")
compact_one_master("FS-MCLAR-MASTER")
compact_one_master("FS-PACCAR-MASTER")
compact_one_master("FS-REC-MASTER")
compact_one_master("FS-SELTRK-MASTER")
compact_one_master("FS-STD-MASTER")
compact_one_master("FS-SUZCAN-MASTER")
compact_one_master("FS-TRK-MASTER")

