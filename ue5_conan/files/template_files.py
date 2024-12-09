import os

BLANK_TEMPLATE_NAME = 'TP_Blank'
BLANK_TEMPLATE_EDITOR_CONFIG = 'TP_BlankEditor'

def get_template_file(ue_install_dir: str):
    return os.path.join(str(ue_install_dir), 'Templates', BLANK_TEMPLATE_NAME)