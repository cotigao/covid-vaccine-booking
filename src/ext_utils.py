import os
import tempfile
import threading
import requests
import time
from hashlib import sha256

def beep(a, b):
    for x in range(1, 3):
        os.system("aplay res/beep-01a.wav")


def generate_token_OTP_pull(mobile, request_header):
    """
    This function generate OTP and returns a new token or None when not able to get token
    """
    data = {
        "mobile": mobile,
        "secret": "U2FsdGVkX1+z/4Nr9nta+2DrVJSv7KS6VoQUSQ1ZXYDx/CJUkWxFYG6P3iM/VW+6jLQ9RDQVzp/RcZ8kbT41xw==",
    }
    print(f"Requesting OTP with mobile number {mobile}..")
    txnId = requests.post(
        url="https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP",
        json=data,
        headers=request_header,
    )

    if txnId.status_code == 200:
        txnId = txnId.json()["txnId"]
    else:
        print("Unable to Create OTP")
        print(txnId.text)
        time.sleep(5)  # Saftey net againt rate limit
        txnId = None

    if txnId is None:
        return txnId

    time.sleep(10)
    t_end = time.time() + 60 * 3  # try to read OTP for atmost 3 minutes
    tf = os.path.join(tempfile.gettempdir(), str(mobile) + "_cowin_covid_otp")
    while time.time() < t_end:
        if os.path.exists (tf):
            with open(tf) as f:
                OTP = f.read()
            os.remove(tf)
            break

    if not OTP:
        return None

    print("Parsed OTP:" + OTP)

    data = {"otp": sha256(str(OTP.strip()).encode("utf-8")).hexdigest(), "txnId": txnId}
    print(f"Validating OTP..")

    token = requests.post(
        url="https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp",
        json=data,
        headers=request_header,
    )
    if token.status_code == 200:
        token = token.json()["token"]
    else:
        print("Unable to Validate OTP")
        print(token.text)
        return None

    print(f"Token Generated: {token}")
    return token
