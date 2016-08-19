"""
This pyton script converts the pre-GL QA repository to a GL level repository.

It duplicates the steps perfromed by these five RPS Pick Basic Programs:

  * QA.CREATE.GL.QS
  * QA.SUB.CONV.ACCT
  * QA.SUB.CONV.ACCTG
  * QA.SUB.CONV.SCHED
  * QA.SUB.CONV.TITLE

This program created the 137K items that formed the initial version of the qa_cora_gl repo.

The goal of this is (in part) to stop making RPS convert the Quick Start data every time the
QA release is build and instead just have them package it up.  The only remaining 'custom' step
will be not to finalize the release so it will not install on a DMS.

The repo paths are currently set for my development mac, and if this get moved to a CI server
the paths will need to be updated.

"""
import os
import datetime

TARGET_PATHS = {}
SOURCE_PATHS = {}
SOURCE_REPO_PATH = "/Users/hinesm/gitrepos/qa_cora"
TARGET_REPO_PATH = "/Users/hinesm/gitrepos/qa_cora_gl"
FS_4_DIGIT_YEAR = 2017
GL_COMPANY_ID = "co_h"
CORA_ASTERIX = "_a"
LAST_MOD_USER = 'CREATION'
LAST_MOD_DATE = '17580'


def clear_one_directory(target_repo_path: str, cora_file_name: str):
    """
    Clears on direcotry, leaving behind a subdirecroty of the same name
    (The equivilant of a CoRa q-pointer) and and hidden files (like .gitkeep)
    :param target_repo_path:
    :param cora_file_name:
    :return:
    """
    raw_file_list = os.listdir(target_repo_path)
    for raw_file_name in raw_file_list:
        if (raw_file_name != cora_file_name) and (raw_file_name[0:1] != '.'):
            os.remove(os.path.join(target_repo_path, raw_file_name))


def copy_one_directory(source_repo_path: str, target_repo_path: str, cora_file_name: str):
    """
    Creates (or clears) a directory, then copies file from source to target paths
    :param source_repo_path:
    :param target_repo_path:
    :param cora_file_name:
    :return:
    """
    source_path = os.path.join(source_repo_path, cora_file_name)
    target_path = os.path.join(target_repo_path, cora_file_name)

    if not os.path.exists(target_path):
        os.makedirs(target_path, mode=0o0777)
    else:
        clear_one_directory(target_path, cora_file_name)

    raw_file_list = os.listdir(source_path)
    for raw_file_name in raw_file_list:
        if (raw_file_name != cora_file_name) and (raw_file_name[0:1] != '.'):
            source_file_obj = open(os.path.join(source_path, raw_file_name), mode='br')
            source_file = source_file_obj.read()
            source_file_obj.close()
            target_file_obj = open(os.path.join(target_path, raw_file_name), mode='bw')
            target_file_obj.write(source_file)
            target_file_obj.close()


def copy_one_cora_dict_file(source_repo_path: str, target_repo_path: str, cora_file_name: str):
    """
    Copy DICT level files
    :param source_repo_path:
    :param target_repo_path:
    :param cora_file_name:
    :return:
    """
    copy_one_directory(source_repo_path, target_repo_path, cora_file_name)


def copy_one_cora_data_file(source_repo_path: str, target_repo_path: str, cora_file_name: str):
    """
    Copy DATA level files
    :param source_repo_path:
    :param target_repo_path:
    :param cora_file_name:
    :return:
    """
    source_path = os.path.join(source_repo_path, cora_file_name)
    target_path = os.path.join(target_repo_path, cora_file_name)
    copy_one_directory(source_path, target_path, cora_file_name)


def create_one_cora_data_file(dict_path: str, data_path: str, file_name: str):
    """
    Create the two directories that imitate the DICT and DATA level of a CoRa repo.
    :param dict_path:
    :param data_path:
    :param file_name:
    :return:
    """
    if not os.path.exists(dict_path):
        os.makedirs(dict_path, mode=0o0777)
    else:
        clear_one_directory(dict_path, file_name)
    if not os.path.exists(data_path):
        os.makedirs(data_path, mode=0o0777)
        target_file_obj = open(os.path.join(data_path, '.gitkeep'), mode='bw')
        target_file_obj.close()
    else:
        clear_one_directory(data_path, "")


def make_binary_from_dictionary(cora_rec_dictionary: dict) -> bytes:
    """
    This function creates a binary/byte_array from the string values
    held in the CoRa-like Dictionry.  It processes all based on the largest
    value with data, doen to position/arrtirbute 1.  This trims 'trailing'
    line feeds.
    :param cora_rec_dictionary:
    :return:
    """
    cora_rec_count = len(cora_rec_dictionary.keys()) + 1
    last_populated_found = False
    while not last_populated_found:
        cora_rec_count -= 1
        if cora_rec_count in cora_rec_dictionary:
            if cora_rec_dictionary[cora_rec_count] != '':
                last_populated_found = True
    byte_array = bytearray()
    byte_array.extend(map(ord, cora_rec_dictionary[1]))
    cora_rec_dictionary_pos = 2
    while cora_rec_count >= cora_rec_dictionary_pos:
        byte_array.append(10)
        if cora_rec_dictionary_pos in cora_rec_dictionary:
            byte_array.extend(map(ord, cora_rec_dictionary[cora_rec_dictionary_pos]))
        cora_rec_dictionary_pos += 1
    byte_array.append(10)
    return bytes(byte_array)


def make_dictionary_from_binary(binary_data: bytes, length: int) -> dict:
    """
    This function takes the binary CoRa file and converts it to uft_8 strings
    in a dictionary with integer keys that match how Pick Basic Dynamic Arrays
    work.  This made the conversion of pick code to Python a lot easier.
    :param binary_data:
    :param length:
    :return:
    """
    byte_array = bytearray(binary_data)
    cora_rec_dictionary = {0: '', 1: ''}
    cora_rec_dictionary_pos = 1
    for by in byte_array:
        if by == 10:
            cora_rec_dictionary_pos += 1
            cora_rec_dictionary[cora_rec_dictionary_pos] = ''
        else:
            cora_rec_dictionary[cora_rec_dictionary_pos] += chr(by)
    while length > cora_rec_dictionary_pos:
        cora_rec_dictionary_pos += 1
        cora_rec_dictionary[cora_rec_dictionary_pos] = ''
    return cora_rec_dictionary


def make_dictionary_from_length(length: int) -> dict:
    """
    Create an empty dictionary with interger keys. Normally used to make
    a dictionary we are going to populate as we process data.
    :param length:
    :return:
    """
    cora_rec_dictionary = {}
    cora_rec_dictionary_pos = 0
    while length >= cora_rec_dictionary_pos:
        cora_rec_dictionary[cora_rec_dictionary_pos] = ''
        cora_rec_dictionary_pos += 1
    return cora_rec_dictionary


def make_dictionary_from_string(input_str: str, seperater_str: str, length: int) -> dict:
    """
    Create an an populated dictionary with interger keys from a string.  The
    delimter string control if the data is seperate by things like spaces or commas.
    :param input_str:
    :param seperater_str:
    :param length:
    :return:
    """
    my_list = input_str.split(seperater_str)
    cora_rec_dictionary = {}
    cora_rec_dictionary_pos = 0
    for my_value in my_list:
        cora_rec_dictionary_pos += 1
        cora_rec_dictionary[cora_rec_dictionary_pos] = str(my_value)
    while length > cora_rec_dictionary_pos:
        cora_rec_dictionary_pos += 1
        cora_rec_dictionary[cora_rec_dictionary_pos] = ''

    return cora_rec_dictionary


def iconv_date(day_value: int, month_value: int, year_value: int) -> int:
    """
    This logic returns the internal CoRa date value for a Day//Month/Year
    set of values.  The CoRa command that does this is an ICONV, so I used
    the same name to make it more obvious to CoRa coders.
    :param day_value:
    :param month_value:
    :param year_value:
    :return:
    """
    python_date = datetime.date(day = day_value, month = month_value, year = year_value)
    cora_zero_date = datetime.date(day = 31, month = 12, year = 1967)
    cora_date_diff = python_date - cora_zero_date
    return cora_date_diff.days


def add_gl_sale_chn_to_gl_coa(gl_coa_id: str, acct_account_id: str):
    """
    Creates and/or Add account to GL Sale Chain records.
    :param gl_coa_id:
    :param acct_account_id:
    :return:
    """
    target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.COA'], gl_coa_id), mode='br')
    binary_data = target_file_obj.read()
    target_file_obj.close()
    gl_coa_rec = make_dictionary_from_binary(binary_data, 28)
    if gl_coa_rec[20] == '':
        gl_coa_rec[20] = "co#*" + acct_account_id
    else:
        gl_coa_rec[20] += '\xfd' + "co#*" + acct_account_id
    target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.COA'], gl_coa_id), mode='bw')
    target_file_obj.write(make_binary_from_dictionary(gl_coa_rec))
    target_file_obj.close()


def create_gl_coa_grp_item(gl_coa_grp_id: str, gl_coa_grp_value: str):
    """
    This function creates any 'missing' IB or IBS groups that were defined
    but not currently used in the GL.COA (or old ACCT) files.
    :param gl_coa_grp_id:
    :param gl_coa_grp_value:
    :return:
    """
    if not os.path.isfile(os.path.join(TARGET_PATHS['DATA-GL.COA.GRP'], gl_coa_grp_id)):
        gl_coa_grp_rec = make_dictionary_from_length(1)
        gl_coa_grp_rec[1] = gl_coa_grp_value.strip()
        target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.COA.GRP'], gl_coa_grp_id), mode='bw')
        target_file_obj.write(make_binary_from_dictionary(gl_coa_grp_rec))
        target_file_obj.close()


def determine_source_path(mfr_code: str, cora_file_name: str):
    """
    Generates the string values for a Dict/Data set of directories to
    imitate the way CoRa repos are stored in GIT. These are sotred in the
    SOURCE_PATHS dictionary.
    :param mfr_code:
    :param cora_file_name:
    :return:
    """
    manufacturer = 'QS-' + mfr_code
    directory_name = manufacturer + "_f" + cora_file_name
    SOURCE_PATHS['DICT-'+cora_file_name] = os.path.join(SOURCE_REPO_PATH, directory_name)
    SOURCE_PATHS['DATA-'+cora_file_name] = os.path.join(SOURCE_PATHS['DICT-'+cora_file_name], directory_name)


def determine_source_paths(mfr_code: str):
    """
    Generates the string values for the six pre-GL source files
    :param mfr_code:
    :return:
    """
    determine_source_path(mfr_code, "ACCT")
    determine_source_path(mfr_code, "BALANCE-FWD")
    determine_source_path(mfr_code, "DETAIL-FWD")
    determine_source_path(mfr_code, "GL.ACCT.MAP")
    determine_source_path(mfr_code, "GL.DEPT")
    determine_source_path(mfr_code, "PRIVLIB")
    determine_source_path(mfr_code, "TITLE")


def determine_target_path(mfr_code: str, cora_file_name: str):
    """
    Generates the string values for a Dict/Data set of directories to
    imitate the way CoRa repos are stored in GIT. These are sotred in the
    SOURCE_PATHS dictionary.
    :param mfr_code:
    :param cora_file_name:
    :return:
    """
    manufacturer = 'QS-' + mfr_code
    directory_name = manufacturer + "_f" + cora_file_name
    TARGET_PATHS['DICT-'+cora_file_name] = os.path.join(TARGET_REPO_PATH, directory_name)
    TARGET_PATHS['DATA-'+cora_file_name] = os.path.join(TARGET_PATHS['DICT-'+cora_file_name], directory_name)


def determine_target_paths(mfr_code: str):
    """
    Generates the string values for the twelve GL target files
    :param mfr_code:
    :return:
    """
    determine_target_path(mfr_code, "ACR-GL-ACCTS")
    determine_target_path(mfr_code, "GL.CIB.SETUP")
    determine_target_path(mfr_code, "GL.COA")
    determine_target_path(mfr_code, "GL.COA.GRP")
    determine_target_path(mfr_code, "GL.DEPT")
    determine_target_path(mfr_code, "GL.DGL.SETUP")
    determine_target_path(mfr_code, "GL.PCL")
    determine_target_path(mfr_code, "GL.RPT.SETUP")
    determine_target_path(mfr_code, "GL.SALE.CHN")
    determine_target_path(mfr_code, "GL.SCHED.SETUP")
    determine_target_path(mfr_code, "NDOC")
    determine_target_path(mfr_code, "PRIVLIB")
    determine_target_path(mfr_code, "PROD-FILE")


def create_target_paths(mfr_code: str):
    """
    Create the destination/target directories if they don't already exist. Clears them
    if the do already exist.
    :param mfr_code:
    :return:
    """

    directory_name = 'QS-' + mfr_code + "_f" + "ACR-GL-ACCTS"
    create_one_cora_data_file(TARGET_PATHS['DICT-ACR-GL-ACCTS'], TARGET_PATHS['DATA-ACR-GL-ACCTS'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.CIB.SETUP"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.CIB.SETUP'], TARGET_PATHS['DATA-GL.CIB.SETUP'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.COA"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.COA'], TARGET_PATHS['DATA-GL.COA'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.COA.GRP"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.COA.GRP'], TARGET_PATHS['DATA-GL.COA.GRP'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.DEPT"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.DEPT'], TARGET_PATHS['DATA-GL.DEPT'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.DGL.SETUP"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.DGL.SETUP'], TARGET_PATHS['DATA-GL.DGL.SETUP'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.PCL"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.PCL'], TARGET_PATHS['DATA-GL.PCL'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.RPT.SETUP"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.RPT.SETUP'], TARGET_PATHS['DATA-GL.RPT.SETUP'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.SALE.CHN"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.SALE.CHN'], TARGET_PATHS['DATA-GL.SALE.CHN'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "GL.SCHED.SETUP"
    create_one_cora_data_file(TARGET_PATHS['DICT-GL.SCHED.SETUP'], TARGET_PATHS['DATA-GL.SCHED.SETUP'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "NDOC"
    create_one_cora_data_file(TARGET_PATHS['DICT-NDOC'], TARGET_PATHS['DATA-NDOC'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "PRIVLIB"
    create_one_cora_data_file(TARGET_PATHS['DICT-PRIVLIB'], TARGET_PATHS['DATA-PRIVLIB'], directory_name)
    directory_name = 'QS-' + mfr_code + "_f" + "PROD-FILE"
    create_one_cora_data_file(TARGET_PATHS['DICT-PROD-FILE'], TARGET_PATHS['DATA-PROD-FILE'], directory_name)


def create_missing_ib_and_ibs_items():
    """
    Add any missing IB and IBS codes not currently used in ACCT or Gl.COA
    :return:
    """
    source_title_list = os.listdir(SOURCE_PATHS['DATA-TITLE'])
    for source_title_id in source_title_list:
        if source_title_id[0:4] == 'GRP-':
            source_file_obj = open(os.path.join(SOURCE_PATHS['DATA-TITLE'], source_title_id), mode='br')
            binary_data = source_file_obj.read()
            source_file_obj.close()
            title_rec = make_dictionary_from_binary(binary_data, 1)
            ibs_code = source_title_id[4:99]
            ib_id = GL_COMPANY_ID + CORA_ASTERIX + 'IB' + CORA_ASTERIX + ibs_code
            create_gl_coa_grp_item(ib_id, title_rec[1])
            ib_id = GL_COMPANY_ID + CORA_ASTERIX + 'IBS' + CORA_ASTERIX + ibs_code
            create_gl_coa_grp_item(ib_id, ibs_code)


def create_dgl_setup_item():
    """
    We have to populate the first position of gl_dgl_setup_rec, in
    a left handed sort to match the old code, so we do that here.
    :return:
    """
    gl_dgl_setup_rec = make_dictionary_from_length(7)
    gl_dgl_setup_rec[0] = GL_COMPANY_ID + CORA_ASTERIX + '1'
    source_acct_list = os.listdir(SOURCE_PATHS['DATA-ACCT'])
    for acct_account_id in sorted(set(source_acct_list)):
        if acct_account_id[0:1] != '.':
            # Read the old ACCT record and convert it into a Dictionary for easy access
            source_file_obj = open(os.path.join(SOURCE_PATHS['DATA-ACCT'], acct_account_id), mode='br')
            binary_data = source_file_obj.read()
            source_file_obj.close()
            acct_rec = make_dictionary_from_binary(binary_data, 57)
            # Turn Attribue 4 of old ACCT into a Dictionary for easy access
            acct_rec_attr_4 = make_dictionary_from_string(acct_rec[4], ' ', 8)
            if acct_rec_attr_4[8] == '2':
                if gl_dgl_setup_rec[1] == '':
                    gl_dgl_setup_rec[1] = acct_account_id
                else:
                    gl_dgl_setup_rec[1] += '\xfd' + acct_account_id
    if gl_dgl_setup_rec[1] != '':
        gl_dgl_setup_rec[2] = '1'
        gl_dgl_setup_rec[3] = 'J\xfdR\xfdC'
        gl_dgl_setup_rec[4] = 'N'
        gl_dgl_setup_rec[5] = 'Y'
        gl_dgl_setup_rec[6] = LAST_MOD_USER
        gl_dgl_setup_rec[7] = LAST_MOD_DATE
        target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.DGL.SETUP'], gl_dgl_setup_rec[0]), mode='bw')
        target_file_obj.write(make_binary_from_dictionary(gl_dgl_setup_rec))
        target_file_obj.close()


def create_sale_chain_references(chain_from_sale_accts: dict, chain_from_cost_accts: dict):
    """
    Update sale account chains in GL.SALE.CHN from the two 'chain_from-xxx' dictionaries
    :param chain_from_sale_accts:
    :param chain_from_cost_accts:
    :return:
    """
    sale_account_list = chain_from_sale_accts.keys()
    for acct_account_id in sorted(sale_account_list, key=int):
        chain_from_sale_acct = chain_from_sale_accts[acct_account_id]
        cost_key = chain_from_sale_acct['chain_acct']
        gl_sale_chain_rec = make_dictionary_from_length(6)
        gl_sale_chain_rec[0] = GL_COMPANY_ID + CORA_ASTERIX + acct_account_id
        gl_sale_chain_rec[2] = cost_key
        gl_sale_chain_rec[3] = '0'
        if cost_key in chain_from_cost_accts:
            chain_from_cost_acct = chain_from_cost_accts[chain_from_sale_acct['chain_acct']]
            if chain_from_cost_acct['chain_acct'] in chain_from_cost_accts:
                gl_sale_chain_rec[4] = chain_from_cost_acct['chain_acct']
                chain_from_cost_acct = chain_from_cost_accts[chain_from_cost_acct['chain_acct']]
            gl_sale_chain_rec[3] = chain_from_cost_acct['percent']
            gl_sale_chain_rec[5] = 'co#'
            gl_sale_chain_rec[6] = chain_from_cost_acct['chain_acct']
        target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.SALE.CHN'], gl_sale_chain_rec[0]), mode='bw')
        target_file_obj.write(make_binary_from_dictionary(gl_sale_chain_rec))
        target_file_obj.close()

        # Update GL.COA atrribute 20 with GL.SALE.CHN references
        gl_coa_id = GL_COMPANY_ID + CORA_ASTERIX + acct_account_id
        add_gl_sale_chn_to_gl_coa(gl_coa_id, acct_account_id)

        if gl_sale_chain_rec[2] != '':
            gl_coa_id = GL_COMPANY_ID + CORA_ASTERIX + gl_sale_chain_rec[2]
            add_gl_sale_chn_to_gl_coa(gl_coa_id, acct_account_id)

        if gl_sale_chain_rec[4] != '':
            gl_coa_id = GL_COMPANY_ID + CORA_ASTERIX + gl_sale_chain_rec[4]
            add_gl_sale_chn_to_gl_coa(gl_coa_id, acct_account_id)

        if gl_sale_chain_rec[6] != '':
            gl_coa_id = GL_COMPANY_ID + CORA_ASTERIX + gl_sale_chain_rec[6]
            add_gl_sale_chn_to_gl_coa(gl_coa_id, acct_account_id)


def create_productivity_item():
    """
    Add company numbers to PRIVLIB PRODUCTIVITY item
    :return:
    """
    if os.path.isfile(os.path.join(SOURCE_PATHS['DICT-PRIVLIB'], "PRODUCTIVITY")):
        source_file_obj = open(os.path.join(SOURCE_PATHS['DICT-PRIVLIB'], "PRODUCTIVITY"), mode='br')
        binary_data = source_file_obj.read()
        source_file_obj.close()
        privlib_productivity_rec = make_dictionary_from_binary(binary_data, 2)
        my_list = privlib_productivity_rec[1].split(' ')
        privlib_productivity_rec[1] = ''
        for my_value in my_list:
            if privlib_productivity_rec[1] == '':
                privlib_productivity_rec[1] = 'co#*' + my_value
            else:
                privlib_productivity_rec[1] += ' ' + 'co#*' + my_value
        privlib_productivity_rec[2] = '\x0a\x0a\x0a'  # Matches old CoRa program output
        target_file_obj = open(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], "PRODUCTIVITY"), mode='bw')
        target_file_obj.write(make_binary_from_dictionary(privlib_productivity_rec))
        target_file_obj.close()


def create_new_ar_file_two():
    """
    The AR-FILE2 file format is different for GL.  This function reformats it to the
    new layout.
    :return:
    """
    source_file_obj = open(os.path.join(SOURCE_PATHS['DICT-PRIVLIB'], "AR-FILE2"), mode='br')
    binary_data = source_file_obj.read()
    source_file_obj.close()
    privlib_ar_file2_rec = make_dictionary_from_binary(binary_data, 1)
    new_privlib_ar_file2_rec = {}
    ar_file_index = 1
    while ar_file_index in privlib_ar_file2_rec:
        work_rec = make_dictionary_from_string(privlib_ar_file2_rec[ar_file_index], ' ', 8)
        if work_rec[2] == '':
            new_privlib_ar_file2_rec[ar_file_index] = privlib_ar_file2_rec[ar_file_index]
        else:
            new_privlib_ar_file2_rec[ar_file_index] = work_rec[1] + ' ' + work_rec[2] \
                                          + ' ' + work_rec[3] + ' ' + work_rec[4] + ' ' \
                                          + work_rec[5] + ' ' + work_rec[8] + ' 1 0'
        ar_file_index += 1
    target_file_obj = open(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], 'AR-FILE2'), mode='bw')
    target_file_obj.write(make_binary_from_dictionary(new_privlib_ar_file2_rec))
    target_file_obj.close()


def create_new_acr_gl_items():
    """
    Build new PRIVLIB ACR-GL-ACCTS item from two old PRIVLIB items and one TITLE item
    :return:
    """
    source_file_obj = open(os.path.join(SOURCE_PATHS['DICT-PRIVLIB'], "INT-ACCT"), mode='br')
    binary_data = source_file_obj.read()
    source_file_obj.close()
    privlib_int_acct_rec = make_dictionary_from_binary(binary_data, 1)

    source_file_obj = open(os.path.join(SOURCE_PATHS['DICT-PRIVLIB'], "SCHED-FILE2"), mode='br')
    binary_data = source_file_obj.read()
    source_file_obj.close()
    privlib_shed_file = make_dictionary_from_binary(binary_data, 1)

    privlib_shed_file_count = len(privlib_shed_file.keys())
    privlib_shed_file_pos = 0
    while privlib_shed_file_count >= privlib_shed_file_pos:
        privlib_shed_file_pos += 1
        if privlib_shed_file_pos in privlib_shed_file:
            if privlib_shed_file[privlib_shed_file_pos][0:6] == 'SCH-AR':
                ar_sched_line_rec = make_dictionary_from_string(privlib_shed_file[privlib_shed_file_pos], ' ', 0)
                cora_rec_count = len(ar_sched_line_rec.keys()) + 1
                ar_columns_list = ''
                while cora_rec_count >= 12:
                    if cora_rec_count in ar_sched_line_rec:
                        if ar_sched_line_rec[cora_rec_count] != 'T' and ar_sched_line_rec[cora_rec_count][0:5] != 'OVER-':
                            if ar_columns_list == '':
                                ar_columns_list = ar_sched_line_rec[cora_rec_count]
                            else:
                                ar_columns_list = ar_sched_line_rec[cora_rec_count] + '\xfd' + ar_columns_list
                    cora_rec_count -= 1

                privlib_int_acct_rec_pos = 1
                privlib_int_acct_rec_match_found = False
                while privlib_int_acct_rec_pos in privlib_int_acct_rec and not privlib_int_acct_rec_match_found:
                    privlib_int_acct = make_dictionary_from_string(privlib_int_acct_rec[privlib_int_acct_rec_pos], ' ', 6)
                    if privlib_int_acct[1] == ar_sched_line_rec[3]:
                        privlib_int_acct_rec_match_found = True
                    privlib_int_acct_rec_pos += 1

                # Determine title for ACR-GL-ACCTS item
                title_id = 'S' + CORA_ASTERIX + ar_sched_line_rec[3]
                if os.path.isfile(os.path.join(SOURCE_PATHS['DATA-TITLE'], title_id)):
                    source_file_obj = open(os.path.join(SOURCE_PATHS['DATA-TITLE'], title_id), mode='br')
                    binary_data = source_file_obj.read()
                    source_file_obj.close()
                    title_rec = make_dictionary_from_binary(binary_data, 1)
                else:
                    title_rec = make_dictionary_from_length(1)

                # Create and write out an ACR-GL-ACCTS item
                if ar_sched_line_rec[3] != '':
                    posting_desc = "FINANCE CHARGE"
                    gl_acr_accts_rec = make_dictionary_from_length(14)
                    gl_acr_accts_rec[0] = ar_sched_line_rec[3]
                    gl_acr_accts_rec[1] = title_rec[1]                    # Account Description
                    gl_acr_accts_rec[2] = 'co#'                           # AR Company
                    gl_acr_accts_rec[3] = privlib_int_acct[2]             # AR Account
                    gl_acr_accts_rec[4] = posting_desc                    # Posting Description
                    gl_acr_accts_rec[5] = ar_columns_list
                    gl_acr_accts_rec[6] = ar_columns_list
                    # Attribute 7 is left empty
                    gl_acr_accts_rec[8] = 'co#'                           # FC Company
                    gl_acr_accts_rec[9] = privlib_int_acct[4]             # FC Journal
                    gl_acr_accts_rec[10] = posting_desc                   # Posting Description
                    gl_acr_accts_rec[11] = 'co#'                          # FC Account Company
                    gl_acr_accts_rec[12] = privlib_int_acct[3]            # FC Account
                    gl_acr_accts_rec[13] = posting_desc                   # Posting Description
                    gl_acr_accts_rec[14] = ar_sched_line_rec[1]           # AR Sched type
                    target_file_obj = open(os.path.join(TARGET_PATHS['DATA-ACR-GL-ACCTS'], gl_acr_accts_rec[0]), mode='bw')
                    target_file_obj.write(make_binary_from_dictionary(gl_acr_accts_rec))
                    target_file_obj.close()


def leftsort(key):
    """
    Used to get alpha numeric account numbers to sort the same way they do in CoRa
    :param key:
    :return:
    """
    return str(key).zfill(15)


def convert_one_quick_start(mfr_code: str):
    """
    This function does the bulks of the processing (or calls the functions above to
    get things processed).  It starts by sorting the old ACCT data and begins the conversion
    of the data into GL.COA and other supporting files.
    :param mfr_code:
    :return:
    """

    # init local variables
    chain_from_sale_accts = {}
    chain_from_cost_accts = {}

    manufacturer = 'QS-' + mfr_code

    print(manufacturer)

    cora_fiscal_begin = str(iconv_date(1, 1, FS_4_DIGIT_YEAR))

    # Determine source and target paths & create target paths
    determine_source_paths(mfr_code)
    determine_target_paths(mfr_code)
    create_target_paths(mfr_code)

    # Copy the dict level of the source PRIVLIB to the data level of the target PRIVLIB
    directory_name = manufacturer + "_f" + "PRIVLIB"
    copy_one_directory(SOURCE_REPO_PATH, TARGET_PATHS['DICT-PRIVLIB'], directory_name)

    # Remove GLJRNL from target PRIVLIB
    if os.path.isfile(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], 'GLJRNL')):
        os.remove(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], 'GLJRNL'))

    # Remove SCHED-FILE2 from target PRIVLIB
    if os.path.isfile(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], 'SCHED-FILE2')):
        os.remove(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], 'SCHED-FILE2'))

    # Rename & update FS setup item in target PRIVLIB
    old_fs_setup_id = 'FS-' + mfr_code + '-1'
    new_fs_setup_id = 'FS-' + mfr_code + '-fs_h-' + str(cora_fiscal_begin)
    if os.path.isfile(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], old_fs_setup_id)):
        source_file_obj = open(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], old_fs_setup_id), mode='br')
        binary_data = source_file_obj.read()
        source_file_obj.close()
        fs_setup_rec = make_dictionary_from_binary(binary_data, 0)
        for key in fs_setup_rec.keys():
            clean_mfr_code = mfr_code.replace('_k', '[')
            clean_mfr_code = clean_mfr_code.replace('_t', ']')
            fs_setup_rec[key] = fs_setup_rec[key].replace(clean_mfr_code + '*1', clean_mfr_code + '*fs#')
        target_file_obj = open(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], new_fs_setup_id), mode='bw')
        target_file_obj.write(make_binary_from_dictionary(fs_setup_rec))
        target_file_obj.close()
        os.remove(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], old_fs_setup_id))

    # Read source PRIVLIB GLJRNL item and build the privlib_gl_jrnl dictionary from it
    source_file_obj = open(os.path.join(SOURCE_PATHS['DICT-PRIVLIB'], "GLJRNL"), mode='br')
    binary_data = source_file_obj.read()
    source_file_obj.close()
    privlib_gl_jrnl = make_dictionary_from_binary(binary_data, 20)

    retained_earnings_id = privlib_gl_jrnl[17]

    # Create the basic GL.COA files based on the Pre-GL ACCT file.  Accounts can be alpha-numeric.
    source_acct_list = os.listdir(SOURCE_PATHS['DATA-ACCT'])
    for acct_account_id in sorted(set(source_acct_list), key=leftsort):
        if acct_account_id[0:1] != '.':

            # Read the old ACCT record and convert it into a Dictionary for easy access
            source_file_obj = open(os.path.join(SOURCE_PATHS['DATA-ACCT'], acct_account_id), mode='br')
            binary_data = source_file_obj.read()
            source_file_obj.close()
            acct_rec = make_dictionary_from_binary(binary_data, 57)
            acct_rec[0] = acct_account_id

            # Turn Attribue 4 of old ACCT into a Dictionary for easy access
            acct_rec_attr_4 = make_dictionary_from_string(acct_rec[4], ' ', 8)

            # AR Schedule code
            ar_sched_code = acct_rec_attr_4[8]
            if ar_sched_code < 'A' or ar_sched_code > 'Y':
                ar_sched_code = ''

            # Set the account type and sub types
            account_type = acct_rec_attr_4[3]
            account_sub_type = ''
            name_code_type = acct_rec_attr_4[7]
            if account_type == "V":
                account_type = "A"
                if name_code_type == "5":
                    account_sub_type = "VI"
            elif account_type == "D":
                account_type = "X"
            elif account_type == "P":
                account_type = "Q"
                account_sub_type = 'PR'
            elif acct_rec[0] == retained_earnings_id:
                account_type = "Q"
                account_sub_type = 'RE'
            elif account_type == "0":
                account_type = "Q"
                account_sub_type = 'OP'
            elif account_type == "A":
                schedules = acct_rec_attr_4[8].split(',')
                for schedule in schedules:
                    if schedule >= 'A' and schedule <= 'M':
                        account_sub_type = 'OR'
                    if schedule >= 'N' and schedule <= 'V':
                        account_sub_type = 'BR'

            if os.path.isfile(os.path.join(SOURCE_PATHS['DATA-GL.ACCT.MAP'], acct_account_id)):
                source_file_obj = open(os.path.join(SOURCE_PATHS['DATA-GL.ACCT.MAP'], acct_account_id), mode='br')
                binary_data = source_file_obj.read()
                source_file_obj.close()
                acct_map_rec = make_dictionary_from_binary(binary_data, 4)
                if acct_map_rec[3] != '':
                    account_type = acct_map_rec[3]
                if acct_map_rec[4] != '':
                    account_sub_type = acct_map_rec[4]

            # Determine Contol Type
            control_type = '0'
            if account_sub_type == 'IC':
                control_type = '9'
            else:
                if acct_rec_attr_4[1] != '4':
                    if acct_rec_attr_4[7] == 'X' and acct_rec_attr_4[1] == '1':
                        control_type = '12'
                    else:
                        if acct_rec_attr_4[7] == '0' and acct_rec_attr_4[1] == '1':
                            control_type = '10'
                        else:
                            control_type = acct_rec_attr_4[7]
                            if control_type == '' or control_type == 'X':
                                control_type = '0'

            # Determine Prod Type
            prod_type = '0'
            if acct_rec_attr_4[1] == '4' and (acct_rec_attr_4[7] == '7' or acct_rec_attr_4[7] == '8'):
                prod_type = acct_rec_attr_4[7]

            # Determine Stat Count Type
            stat_count_type = acct_rec_attr_4[2]
            if stat_count_type == '1':
                stat_count_type = '2'
            elif stat_count_type == '2':
                stat_count_type = '1'
            if account_type == 'A' and account_sub_type == 'VI' and stat_count_type == '0':
                stat_count_type = '2'

            # Build new GL.COA item using gathered pre-GL data, write to disk
            gl_coa_rec = make_dictionary_from_length(32)
            gl_coa_rec[0] = GL_COMPANY_ID + CORA_ASTERIX + acct_account_id
            gl_coa_rec[1] = acct_rec[13]         # Description
            gl_coa_rec[2] = cora_fiscal_begin    # ICONV fiscal year begin
            # Position 3 is left empty
            gl_coa_rec[4] = account_type         # Account type
            gl_coa_rec[5] = account_sub_type     # Account sub type
            gl_coa_rec[6] = control_type         # Control Type
            gl_coa_rec[7] = prod_type            # Prod type
            gl_coa_rec[8] = '0'                  # Control Type 2
            gl_coa_rec[9] = '0'                  # Post Desc Flag
            gl_coa_rec[10] = stat_count_type     # Stat count type
            gl_coa_rec[11] = ar_sched_code       # AR Schedule code
            gl_coa_rec[12] = acct_rec[9]         # Dept / Activity id
            # Position 13 is left empty          # Franchise id
            # Position 14 is left empty          # Pattern
            # Position 15 is left empty          # BF sched
            # Position 16 is left empty          # DF sched
            # Position 17 is left empty          # Prod sched
            # Position 18 is left empty          # CM sched
            # Position 19 is left empty          # GL expense allocation id
            # Position 20 is populated later     # GL.SALE.CHN id(s)
            gl_coa_rec[21] = acct_rec[10]        # IB Group
            gl_coa_rec[22] = acct_rec[11]        # IBS Group
            gl_coa_rec[23] = acct_rec[8]         # UNA Group
            # Position 24 is left empty          # Report group
            # Position 25 is left empty          # Post retain
            gl_coa_rec[26] = acct_rec[56]        # IH Type
            gl_coa_rec[27] = cora_fiscal_begin   # ICONV fiscal year begin
            gl_coa_rec[28] = LAST_MOD_DATE       # ICONV system date
            if acct_rec_attr_4[8] == '2':
                gl_coa_rec[32] = '1'
            target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.COA'], gl_coa_rec[0]), mode='bw')
            target_file_obj.write(make_binary_from_dictionary(gl_coa_rec))
            target_file_obj.close()

            # Populate the two 'chain_from-xxx' dictionaries
            sale_chain_acct = acct_rec_attr_4[4]
            if sale_chain_acct != '0' and sale_chain_acct != '' and sale_chain_acct != '99999':
                if account_type == 'S':
                    chain_from_sale_accts[acct_account_id] = {'chain_acct': sale_chain_acct}
                elif account_type == 'C':
                    sale_chain_pct = acct_rec_attr_4[5]
                    if int(sale_chain_pct) != 0:
                        sale_chain_pct = str(int(sale_chain_pct)*10)
                    chain_from_cost_accts[acct_account_id] = {'chain_acct': sale_chain_acct,
                                                              'percent': sale_chain_pct}

            # Build GL.PCL item(s) and write to disk
            gl_pcl_rec = make_dictionary_from_length(1)
            acct_pcl_index = 1
            acct_pcl_codes = acct_rec[53].split('\xfd')  # Value mark separated
            for acct_pcl_code in acct_pcl_codes:
                if acct_pcl_code != '':
                    if acct_pcl_index == 1:
                        gl_pcl_rec[0] = GL_COMPANY_ID + CORA_ASTERIX + acct_account_id \
                                        + CORA_ASTERIX + "fs_h" + CORA_ASTERIX \
                                        + cora_fiscal_begin
                    else:
                        gl_pcl_rec[0] = GL_COMPANY_ID + CORA_ASTERIX + acct_account_id \
                                        + CORA_ASTERIX + "fs" + str(acct_pcl_index) \
                                        + CORA_ASTERIX + cora_fiscal_begin
                    gl_pcl_rec[1] = acct_pcl_code
                    target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.PCL'], gl_pcl_rec[0]), mode='bw')
                    target_file_obj.write(make_binary_from_dictionary(gl_pcl_rec))
                    target_file_obj.close()
                    acct_pcl_index += 1

            # Build GL.COA.GRP UNA item and write to disk if not already present
            if acct_rec[8] != '' and acct_rec[13] != '':
                gl_coa_grp_id = GL_COMPANY_ID + CORA_ASTERIX + "UNA" + CORA_ASTERIX + acct_rec[8]
                create_gl_coa_grp_item(gl_coa_grp_id, acct_rec[13])

            # Build GL.COA.GRP IB item and write to disk if not already present
            if acct_rec[10] != '':
                title_id = 'GRP-' + acct_rec[10]
                if os.path.isfile(os.path.join(SOURCE_PATHS['DATA-TITLE'], title_id)):
                    source_file_obj = open(os.path.join(SOURCE_PATHS['DATA-TITLE'], title_id), mode='br')
                    binary_data = source_file_obj.read()
                    source_file_obj.close()
                    title_rec = make_dictionary_from_binary(binary_data, 1)
                else:
                    title_rec = {}
                    title_rec[1] = acct_rec[10]
                gl_coa_grp_id = GL_COMPANY_ID + CORA_ASTERIX + "IB" + CORA_ASTERIX + acct_rec[10]
                gl_coa_grp_value = title_rec[1]
                create_gl_coa_grp_item(gl_coa_grp_id, gl_coa_grp_value)

            # Build GL.COA.GRP IBS item and write to disk if not already present
            if acct_rec[11] != '':
                gl_coa_grp_id = GL_COMPANY_ID + CORA_ASTERIX + "IBS" + CORA_ASTERIX + acct_rec[11]
                gl_coa_grp_value = acct_rec[11]
                create_gl_coa_grp_item(gl_coa_grp_id, gl_coa_grp_value)

            # Build or copy old GL.DEPT item and write to disk
            if acct_rec[9] != '':
                gl_dept_id = GL_COMPANY_ID + CORA_ASTERIX + acct_rec[9]
                if not os.path.isfile(os.path.join(TARGET_PATHS['DATA-GL.DEPT'], gl_dept_id)):
                    source_gl_dept_id = '1' + CORA_ASTERIX + acct_rec[9]
                    if os.path.isfile(os.path.join(SOURCE_PATHS['DATA-GL.DEPT'], source_gl_dept_id)):
                        source_file_obj = open(os.path.join(SOURCE_PATHS['DATA-GL.DEPT'], source_gl_dept_id), mode='br')
                        binary_data = source_file_obj.read()
                        source_file_obj.close()
                        gl_dept_rec = make_dictionary_from_binary(binary_data, 3)
                        #gl_dept_rec[1] = gl_dept_rec[1][0:30]
                        gl_dept_rec[1] = gl_dept_rec[1]
                    else:
                        gl_dept_rec = make_dictionary_from_length(1)
                        gl_dept_rec[1] = 'Dept ' + acct_rec[9]
                    target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.DEPT'], gl_dept_id), mode='bw')
                    target_file_obj.write(make_binary_from_dictionary(gl_dept_rec))
                    target_file_obj.close()

    cash_in_bank_setup_accounts = ''  # Multi valued account list for GL.CIB.SETUP item
    cib_gl_setup_report_format = ''

    # Read source PRIVLIB SCHED-FILE2 item
    if os.path.isfile(os.path.join(SOURCE_PATHS['DICT-PRIVLIB'], 'SCHED-FILE2')):
        source_file_obj = open(os.path.join(SOURCE_PATHS['DICT-PRIVLIB'], 'SCHED-FILE2'), mode='br')
        binary_data = source_file_obj.read()
        source_file_obj.close()
        privlib_shed_file = make_dictionary_from_binary(binary_data, 1)
    else:
        privlib_shed_file = make_dictionary_from_length(1)
        privlib_shed_file[1] = '.'

    privlib_sched_file_pos = 1
    current_sched_line = privlib_shed_file[privlib_sched_file_pos]
    while current_sched_line != '.':
        current_sched = make_dictionary_from_string(current_sched_line, " ", 20)
        sched_name = current_sched[1]
        sched_file = current_sched[2]
        sched_title_id = current_sched[6]
        sched_special = current_sched[7]
        sched_type = 0
        sort_type = ''
        def_sched_code = ''
        if sched_name == "SCH-6":
            sched_type = 4  # Current month
            def_sched_code = 'AGRS'
            sort_type = 'CR\xfdD\xfdR'
        elif sched_name == "SCH-5":
            sched_type = 5  # Cash in bank
            def_sched_code = 'AGRC'
            sort_type = 'J\xfdR\xfdD\xfdC'
        elif sched_name == "SCH-DGL" or sched_name == "SCH-DGL2" or sched_name == "SCH-DGL3" \
                or sched_name == "SCH-DGL4" or sched_name == "SCH-DGL5" or sched_file == "DGL":
            sched_type = 6  # Detail GL schedule
            def_sched_code = 'AGRD'
            sort_type = 'J\xfdR\xfdC'
        elif sched_file == "BF":
            sched_type = 1  # Balance Forward
            def_sched_code = 'AGRS'
            sort_type = 'CR\xfdJ\xfdR'
        elif sched_file == "DF":
            sched_type = 2  # Detail forward
            def_sched_code = 'AGRS'
            sort_type = 'CR\xfdD\xfdR'

        # Populate the GL.RPT.SETUP file with it's three types of data.
        if sched_type >= 1 and sched_type <= 4 and def_sched_code == 'AGRS':
            gl_rpt_col_setup = make_dictionary_from_length(6)
            gl_rpt_hdr_setup = make_dictionary_from_length(6)
            gl_rpt_col_setup[1] = '1\xfd2\xfd4\xfd5'
            gl_rpt_col_setup[5] = LAST_MOD_USER
            gl_rpt_col_setup[6] = LAST_MOD_DATE
            gl_rpt_hdr_setup[5] = LAST_MOD_USER
            gl_rpt_hdr_setup[6] = LAST_MOD_DATE
            target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.RPT.SETUP'], GL_COMPANY_ID + CORA_ASTERIX
                                                + str(privlib_sched_file_pos) + CORA_ASTERIX
                                                + def_sched_code + '.COL.SETUP'), mode='bw')
            target_file_obj.write(make_binary_from_dictionary(gl_rpt_col_setup))
            target_file_obj.close()
            target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.RPT.SETUP'], GL_COMPANY_ID + CORA_ASTERIX
                                                + str(privlib_sched_file_pos) + CORA_ASTERIX
                                                + def_sched_code + '.HDR.SETUP'), mode='bw')
            target_file_obj.write(make_binary_from_dictionary(gl_rpt_hdr_setup))
            target_file_obj.close()
        if sched_type == 5 and def_sched_code == 'AGRC':
            gl_rpt_col_setup = make_dictionary_from_length(6)
            gl_rpt_col_setup[1] = '1\xfd2\xfd3\xfd4\xfd6\xfd9'
            gl_rpt_col_setup[5] = LAST_MOD_USER
            gl_rpt_col_setup[6] = LAST_MOD_DATE
            target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.RPT.SETUP'], GL_COMPANY_ID + CORA_ASTERIX
                                                + '1' + CORA_ASTERIX
                                                + def_sched_code + '.COL.SETUP'), mode='bw')
            target_file_obj.write(make_binary_from_dictionary(gl_rpt_col_setup))
            target_file_obj.close()
        if sched_type == 6 and def_sched_code == 'AGRD' and mfr_code != '_kSPRINT_t':
            gl_rpt_col_setup = make_dictionary_from_length(6)
            gl_rpt_col_setup[1] = '1\xfd2\xfd4\xfd5\xfd6'
            gl_rpt_col_setup[5] = LAST_MOD_USER
            gl_rpt_col_setup[6] = LAST_MOD_DATE
            target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.RPT.SETUP'], GL_COMPANY_ID + CORA_ASTERIX
                                                + '1' + CORA_ASTERIX
                                                + def_sched_code + '.COL.SETUP'), mode='bw')
            target_file_obj.write(make_binary_from_dictionary(gl_rpt_col_setup))
            target_file_obj.close()

        # Read the title for the GL.SCHED.SETUP item
        source_file_obj = open(os.path.join(SOURCE_PATHS['DATA-TITLE'], sched_title_id.replace('*', CORA_ASTERIX)), mode='br')
        binary_data = source_file_obj.read()
        source_file_obj.close()
        title_file_rec = make_dictionary_from_binary(binary_data, 1)
        title_file_rec_count = len(title_file_rec.keys())

        # Build Account Listing
        title_file_pos = 3
        account_listing = {}
        account_listing_count = 0
        while title_file_pos <= title_file_rec_count:
            if title_file_pos in title_file_rec:
                if title_file_rec[title_file_pos] != '':
                    account_listing_count += 1
                    account_listing[account_listing_count] = title_file_rec[title_file_pos]
            title_file_pos += 1

        sched_dict_pos = 10
        column_listing = {}
        sched_count = len(current_sched.keys())
        column_listing_pos = 0
        while sched_dict_pos <= sched_count and column_listing_pos < account_listing_count:
            if sched_dict_pos in current_sched:
                dtl_fwd_dict_id = current_sched[sched_dict_pos]
                if dtl_fwd_dict_id != 'T':
                    column_listing_pos += 1
                    value = account_listing[column_listing_pos]
                    if os.path.isfile(os.path.join(SOURCE_PATHS['DICT-DETAIL-FWD'], dtl_fwd_dict_id)):
                        source_file_obj = open(os.path.join(SOURCE_PATHS['DICT-DETAIL-FWD'], dtl_fwd_dict_id), mode='br')
                        binary_data = source_file_obj.read()
                        source_file_obj.close()
                        detail_fwd_rec = make_dictionary_from_binary(binary_data, 3)
                        if detail_fwd_rec[3] != '':
                            value = detail_fwd_rec[3]
                    column_listing[column_listing_pos] = value
            sched_dict_pos += 1

        cntrl_type = ''
        cntrl2_type = ''
        prod_type = ''
        account_vm_list = ''
        account_listing_index = 1
        while account_listing_index <= account_listing_count:
            acct_account_id = account_listing[account_listing_index]
            if account_vm_list == '':
                account_vm_list = acct_account_id
            else:
                account_vm_list += '\xfd' + acct_account_id
            gl_coa_id = GL_COMPANY_ID + CORA_ASTERIX + acct_account_id
            if os.path.isfile(os.path.join(TARGET_PATHS['DATA-GL.COA'], gl_coa_id)):
                target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.COA'], gl_coa_id), mode='br')
                binary_data = target_file_obj.read()
                target_file_obj.close()
                gl_coa_rec = make_dictionary_from_binary(binary_data, 32)
                if cntrl_type == '':
                    cntrl_type = gl_coa_rec[6]
                    cntrl2_type = '0'
                    prod_type = gl_coa_rec[7]

                if sched_type >= 1 and sched_type <= 4:
                    if sched_type == 1:
                        sched_attr_pos = 15
                    elif sched_type == 2:
                        sched_attr_pos = 16
                    elif sched_type == 3:
                        sched_attr_pos = 17
                    else:
                        sched_attr_pos = 18
                    if gl_coa_rec[sched_attr_pos] == '':
                        gl_coa_rec[sched_attr_pos] = str(privlib_sched_file_pos)
                    else:
                        gl_coa_rec[sched_attr_pos] += '\xfd' + str(privlib_sched_file_pos)
                    target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.COA'], gl_coa_id), mode='bw')
                    target_file_obj.write(make_binary_from_dictionary(gl_coa_rec))
                    target_file_obj.close()

            account_listing_index += 1

        column_vm_names = ''
        if sched_special == "M-ACCT":
            column_listing_index = 1
            while column_listing_index <= account_listing_count:
                if column_vm_names == '':
                    column_vm_names = column_listing[column_listing_index]
                else:
                    column_vm_names += '\xfd' + column_listing[column_listing_index]
                column_listing_index += 1

        gl_setup_report_format = 'SA'
        inverse_current_sched = dict(zip(current_sched.values(), current_sched.keys()))  # Swap Values for IDs
        if sched_special == "AGED":
            if 'OVER-120' in inverse_current_sched:
                gl_setup_report_format = 'A1'
            elif 'TOTAL-120' in inverse_current_sched:
                gl_setup_report_format = 'A1'
            elif 'OVER-90' in inverse_current_sched:
                gl_setup_report_format = 'A9'
            elif 'TOTAL-90' in inverse_current_sched:
                gl_setup_report_format = 'A9'
            elif 'OVER-60' in inverse_current_sched:
                gl_setup_report_format = 'A6'
            elif 'TOTAL-60' in inverse_current_sched:
                gl_setup_report_format = 'A6'
            else:
                gl_setup_report_format = 'A3'
        elif sched_special == "M-ACCT":
            gl_setup_report_format = 'MS'
        elif sched_special == "DRCR":
            if 'AMOUNT' in inverse_current_sched:
                gl_setup_report_format = 'SB'
            else:
                gl_setup_report_format = 'SD'
        elif sched_special == ",":
            if 'DEBITS' in inverse_current_sched:
                gl_setup_report_format = 'SB'
            elif 'CREDITS' in inverse_current_sched:
                gl_setup_report_format = 'SB'

        # Write out the GL.SCHED.SETUP item
        if sched_type >= 1 and sched_type <= 4:
            gl_sched_setup = make_dictionary_from_length(14)
            gl_sched_setup[1] = str(sched_type)                  # Sched Type
            gl_sched_setup[2] = title_file_rec[1][0:30]          # Sched Title
            gl_sched_setup[3] = prod_type                        # Prod Type
            gl_sched_setup[4] = cntrl_type                       # Control type
            gl_sched_setup[5] = cntrl2_type                      # Control type 2
            gl_sched_setup[6] = gl_setup_report_format           # GL report format code
            gl_sched_setup[7] = account_vm_list                  # Multi-valued list of accounts
            gl_sched_setup[8] = column_vm_names                  # Multi-valued list of columns
            gl_sched_setup[9] = sort_type                        # Sort Types
            gl_sched_setup[10] = str(privlib_sched_file_pos*10)  # Print Sequence
            gl_sched_setup[11] = '1'                             # Required to Close
            gl_sched_setup[12] = '13'                            # Amount Width
            gl_sched_setup[13] = LAST_MOD_USER                   # Last Mod User
            gl_sched_setup[14] = LAST_MOD_DATE                   # Last Mod CoRa date
            target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.SCHED.SETUP'], GL_COMPANY_ID + CORA_ASTERIX
                                                + str(privlib_sched_file_pos)), mode='bw')
            target_file_obj.write(make_binary_from_dictionary(gl_sched_setup))
            target_file_obj.close()

        if sched_type == 5:
            if cash_in_bank_setup_accounts == '':
                cash_in_bank_setup_accounts = account_vm_list
                cib_gl_setup_report_format = gl_setup_report_format
            else:
                cash_in_bank_setup_accounts += '\xfd' + account_vm_list

        privlib_sched_file_pos += 1
        current_sched_line = privlib_shed_file[privlib_sched_file_pos]

    # Write out single GL.CIB.SETUP item
    if cash_in_bank_setup_accounts != '':
        if cib_gl_setup_report_format == 'SD':
            amount_format = 3
        elif cib_gl_setup_report_format == 'SB':
            amount_format = 2
        else:
            amount_format = 1
        gl_cib_setup_rec = make_dictionary_from_length(7)
        gl_cib_setup_rec[1] = cash_in_bank_setup_accounts    # List of Cash in Bank accounts
        gl_cib_setup_rec[2] = str(amount_format)             # Formatting code of some kind
        gl_cib_setup_rec[3] = 'J\xfdR\xfdD\xfdC'             # Sort Order
        gl_cib_setup_rec[4] = 'Y'                            # Journal Break in Y/N format
        gl_cib_setup_rec[5] = 'Y'                            # Require Close in Y/N format
        gl_cib_setup_rec[6] = LAST_MOD_USER                  # Last Mod User
        gl_cib_setup_rec[7] = LAST_MOD_DATE                  # Last Mod CoRa date
        target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.CIB.SETUP'], GL_COMPANY_ID + CORA_ASTERIX + '1'), mode='bw')
        target_file_obj.write(make_binary_from_dictionary(gl_cib_setup_rec))
        target_file_obj.close()

    create_new_acr_gl_items()
    create_new_ar_file_two()
    create_productivity_item()
    create_sale_chain_references(chain_from_sale_accts, chain_from_cost_accts)
    create_dgl_setup_item()
    create_missing_ib_and_ibs_items()

    response = input("Please Add these manfacturer changes to Git, then press return: ")


def convert_qs_file():
    """
    Copies the QS-FILE from DICT in the soruce to DATA in the target, then creates
    the new file QS-TABLE based on the contents of the FRANCHISES file.
    :return:
    """
    directory_name = 'QS-FILE'
    print(directory_name)
    target_qs_dict_path = os.path.join(TARGET_REPO_PATH, directory_name)
    target_qs_data_path = os.path.join(target_qs_dict_path, directory_name)
    create_one_cora_data_file(target_qs_dict_path, target_qs_data_path, directory_name)
    # Copy dict level files from source into data level in the target
    copy_one_directory(SOURCE_REPO_PATH, target_qs_dict_path, directory_name)
    # Convert the FRANCHISES item to the QS-TABLE item
    if os.path.isfile(os.path.join(target_qs_data_path, 'FRANCHISES')):
        qs_table_rec =  make_dictionary_from_length(3)
        source_file_obj = open(os.path.join(target_qs_data_path, 'FRANCHISES'), mode='br')
        binary_data = source_file_obj.read()
        source_file_obj.close()
        franchises_rec = make_dictionary_from_binary(binary_data, 2)
        franchises_rec_count = len(franchises_rec.keys())
        franchises_rec_index = 1  # Skip the first value, real data starts in the second position
        while franchises_rec_index <= franchises_rec_count:
            franchises_rec_index += 1
            if franchises_rec_index in franchises_rec:
                franchises_line = make_dictionary_from_string(franchises_rec[franchises_rec_index], ' ', 1)
                if franchises_line[1] != '':
                    if qs_table_rec[1] == '':
                        qs_table_rec[1] = franchises_line[1]
                        qs_table_rec[3] = franchises_rec[franchises_rec_index]
                    else:
                        qs_table_rec[1] += '\xfd' + franchises_line[1]
                        qs_table_rec[2] += '\xfd'
                        qs_table_rec[3] += '\xfd' + franchises_rec[franchises_rec_index]
            target_file_obj = open(os.path.join(target_qs_data_path, 'QS-TABLE'), mode='bw')
        target_file_obj.write(make_binary_from_dictionary(qs_table_rec))
        target_file_obj.close()


def convert_car_desc_file():
    """
    Copies the CAR-DESC file from source to target repos.  No data transformation takes place.
    :return:
    """
    directory_name = 'CAR-DESC'
    print(directory_name)
    target_car_desc_dict_path = os.path.join(TARGET_REPO_PATH, directory_name)
    target_car_desc_data_path = os.path.join(target_car_desc_dict_path, directory_name)
    create_one_cora_data_file(target_car_desc_dict_path, target_car_desc_data_path, directory_name)
    copy_one_cora_dict_file(SOURCE_REPO_PATH, TARGET_REPO_PATH, directory_name)
    copy_one_cora_data_file(SOURCE_REPO_PATH, TARGET_REPO_PATH, directory_name)


"""
    Here is where work is laid out and run from.  We process the two supporting
    files first, then convert each of the 62 manufacturers.
"""

convert_qs_file()
convert_car_desc_file()

response = input("Please Add these supporting file changes to Git, then press return: ")


convert_one_quick_start("HONDAMC")         # OK
convert_one_quick_start("IND")             # OK
convert_one_quick_start("MACK")            # OK
convert_one_quick_start("MASER")           # OK
convert_one_quick_start("MCLAR")           # OK
convert_one_quick_start("PACCAR")          # OK
convert_one_quick_start("REC")             # OK
convert_one_quick_start("SELTRK")          # OK
convert_one_quick_start("STD")             # OK
convert_one_quick_start("SUZCAN")          # OK

convert_one_quick_start("TRK")             # OK
convert_one_quick_start("_kACURACAN_t")    # OK
convert_one_quick_start("_kACURA_t")       # OK
convert_one_quick_start("_kAUDICAN_t")     # OK
convert_one_quick_start("_kAUDI_t")        # OK
convert_one_quick_start("_kBENCAN_t")      # OK
convert_one_quick_start("_kBEN_t")         # OK
convert_one_quick_start("_kBMWMC_t")       # OK
convert_one_quick_start("_kBMW_t")         # OK
convert_one_quick_start("_kCHRYCAN_t")     # OK

convert_one_quick_start("_kCHRY_t")        # OK
convert_one_quick_start("_kDTNA_t")        # OK
convert_one_quick_start("_kFERRARI_t")     # OK
convert_one_quick_start("_kFIAT_t")        # OK
convert_one_quick_start("_kFORD_t")        # OK
convert_one_quick_start("_kGMCAN_t")       # OK
convert_one_quick_start("_kGM_t")          # OK
convert_one_quick_start("_kHONDACAN_t")    # OK
convert_one_quick_start("_kHONDA_t")       # OK
convert_one_quick_start("_kHONDPCAN_t")    # OK

convert_one_quick_start("_kHYUCAN_t")      # OK
convert_one_quick_start("_kHYU_t")         # OK
convert_one_quick_start("_kINFINCAN_t")    # OK
convert_one_quick_start("_kINFIN_t")       # OK
convert_one_quick_start("_kISUZU_t")       # OK
convert_one_quick_start("_kJAG_t")         # OK
convert_one_quick_start("_kKIACAN_t")      # OK
convert_one_quick_start("_kKIA_t")         # OK
convert_one_quick_start("_kLAM_t")         # OK
convert_one_quick_start("_kLEXCAN_t")      # OK

convert_one_quick_start("_kLEX_t")         # OK
convert_one_quick_start("_kLR_t")          # OK
convert_one_quick_start("_kMAZDACAN_t")    # OK
convert_one_quick_start("_kMAZDA_t")       # OK
convert_one_quick_start("_kMBCAN_t")       # OK
convert_one_quick_start("_kMB_t")          # OK
convert_one_quick_start("_kMITCAN_t")      # OK
convert_one_quick_start("_kMIT_t")         # OK
convert_one_quick_start("_kNISCAN_t")      # OK
convert_one_quick_start("_kNIS_t")         # OK

convert_one_quick_start("_kNSTAR_t")       # OK
convert_one_quick_start("_kPORCAN_t")      # OK
convert_one_quick_start("_kPORSCHE_t")     # OK
convert_one_quick_start("_kSPRINT_t")      # OK
convert_one_quick_start("_kSUBCAN_t")      # OK
convert_one_quick_start("_kSUB_t")         # OK
convert_one_quick_start("_kSUZ_t")         # OK
convert_one_quick_start("_kTOYCAN_t")      # OK
convert_one_quick_start("_kTOY_t")         # OK
convert_one_quick_start("_kVOLVO_t")       # OK

convert_one_quick_start("_kVWCAN_t")       # OK
convert_one_quick_start("_kVW_t")          # OK

