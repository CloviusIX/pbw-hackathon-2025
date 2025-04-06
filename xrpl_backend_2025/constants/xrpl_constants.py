from xrpl.models import PathStep

RLUSD_CURRENCY = "524C555344000000000000000000000000000000"
RLUSD_ISSUER = "rQhWct2fv4Vc4KRjRgMrxa8xPN9Zx9iLKV"

XRP_PATH_STEP = PathStep(currency="XRP")
RLUSD_PATH_STEP = PathStep(currency=RLUSD_CURRENCY, issuer=RLUSD_ISSUER)
