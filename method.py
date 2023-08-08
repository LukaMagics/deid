def set_method_by_code(code):
    
    LABELS = ["PS_NAME", "PS_NICKNAME", "DT_BIRTH", "QT_AGE", "CV_SEX", "QT_LENGTH", "QT_WEIGHT", "TM_BLOOD_TYPE", "OGG_RELIGION", "LCP_COUNTRY", "OGG_CLUB", "LC_ADDRESS", "LC_PLACE",
                 "QT_RESIDENT_NUMBER", "QT_ALIEN_NUMBER", "QT_PASSPORT_NUMBER", "QT_DRIVER_NUMBER", "QT_MOBILE", "QT_PHONE", "QT_CARD_NUMBER", "QT_ACCOUNT_NUMBER", "TMI_EMAIL", 
                 "QT_PLATE_NUMBER", "OG_WORKPLACE", "OG_DEPARTMENT", "CV_POSITION", "OGG_EDUCATION", "QT_GRADE", "FD_MAJOR", "PS_ID", "TMI_SITE", "QT_IP", "CV_MILITARY_CAMP"]
    
    METHOD_POLICY = {}

    # Masking
    if code == "all-masking":
        for L in LABELS:
            METHOD_POLICY[L] = "masking"

    return METHOD_POLICY