# =====================================================
# ENVIRONMENT
# =====================================================

TESTNET = False


AUTO_START = os.getenv(

    "AUTO_START",

    "true"

).lower() == "true"



TIMEZONE = os.getenv(

    "TIMEZONE",

    "Asia/Seoul"

)
