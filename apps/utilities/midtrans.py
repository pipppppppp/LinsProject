# **************************************************************
# IMPORT LIBRARY | START
# **************************************************************
import midtransclient

from flask import current_app
# **************************************************************
# IMPORT LIBRARY | END
# **************************************************************


# **************************************************************
# MIDTRANS SNAP | START
# **************************************************************
def get_snap():
    snap = midtransclient.Snap(
        is_production=current_app.config[
            "MIDTRANS_IS_PRODUCTION"
        ],
        server_key=current_app.config[
            "MIDTRANS_SERVER_KEY"
        ],
        client_key=current_app.config[
            "MIDTRANS_CLIENT_KEY"
        ],
    )

    return snap
# **************************************************************
# MIDTRANS SNAP | END
# **************************************************************