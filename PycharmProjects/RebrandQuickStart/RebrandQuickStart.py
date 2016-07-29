"""
This pyton script rebrands the dateS of the GL level QA repository.


"""
import os
import datetime

TARGET_PATHS = {}
SOURCE_REPO_PATH = "/Users/hinesm/gitrepos/qa_cora"
TARGET_REPO_PATH = "/Users/hinesm/gitrepos/qa_cora_gl"
FS_4_DIGIT_YEAR = 2017
GL_COMPANY_ID = "co_h"
CORA_ASTERIX = "_a"


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
    determine_target_path(mfr_code, "PRIVLIB")
    determine_target_path(mfr_code, "GL.PCL")
    determine_target_path(mfr_code, "GL.COA")


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



def convert_one_quick_start(mfr_code: str):
    """
    This function does the bulks of the processing (or calls the functions above to
    get things processed).  It starts by sorting the old ACCT data and begins the conversion
    of the data into GL.COA and other supporting files.
    :param mfr_code:
    :return:
    """

    # init local variables

    manufacturer = 'QS-' + mfr_code

    print(manufacturer)

    cora_fiscal_begin = str(iconv_date(1, 1, FS_4_DIGIT_YEAR))
    previous_cora_fiscal_begin = str(iconv_date(1, 1, FS_4_DIGIT_YEAR-1))

    # Determine source and target paths
    determine_target_paths(mfr_code)

    gl_pcl_list = os.listdir(TARGET_PATHS['DATA-GL.PCL'])
    for gl_pcl_id in set(gl_pcl_list):
        if gl_pcl_id[0:1] != '.':
            source_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.PCL'], gl_pcl_id), mode='br')
            source_file = source_file_obj.read()
            source_file_obj.close()
            os.remove(os.path.join(TARGET_PATHS['DATA-GL.PCL'], gl_pcl_id))
            new_gl_pcl_id = gl_pcl_id.replace(previous_cora_fiscal_begin, cora_fiscal_begin)
            target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.PCL'], new_gl_pcl_id), mode='bw')
            target_file_obj.write(source_file)
            target_file_obj.close()

    privlib_fs_id = 'FS-' + mfr_code + '-fs_h-' + previous_cora_fiscal_begin

    if os.path.isfile(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], privlib_fs_id)):
        source_file_obj = open(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], privlib_fs_id), mode='br')
        source_file = source_file_obj.read()
        source_file_obj.close()
        os.remove(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], privlib_fs_id))
        new_privlib_fs_id = privlib_fs_id.replace(previous_cora_fiscal_begin, cora_fiscal_begin)
        target_file_obj = open(os.path.join(TARGET_PATHS['DATA-PRIVLIB'], new_privlib_fs_id), mode='bw')
        target_file_obj.write(source_file)
        target_file_obj.close()

    gl_coa_list = os.listdir(TARGET_PATHS['DATA-GL.COA'])
    for gl_coa_id in set(gl_coa_list):
        if gl_coa_id[0:1] != '.':
            source_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.COA'], gl_coa_id), mode='br')
            source_file = source_file_obj.read()
            source_file_obj.close()
            gl_coa_rec = make_dictionary_from_binary(source_file, 27)
            gl_coa_rec[2] = cora_fiscal_begin
            gl_coa_rec[27] = cora_fiscal_begin
            target_file_obj = open(os.path.join(TARGET_PATHS['DATA-GL.COA'], gl_coa_id), mode='bw')
            target_file_obj.write(make_binary_from_dictionary(gl_coa_rec))
            target_file_obj.close()

    response = input("Please Add these manfacturer changes to Git, then press return: ")


"""
    Here is where work is laid out and run from.  We process the two supporting
    files first, then convert each of the 63 manufacturers.
"""

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

