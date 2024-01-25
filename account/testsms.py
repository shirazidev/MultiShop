import ghasedakpack

sms = ghasedakpack.Ghasedak("5d6cefad1e7e9dbddb66e90f224cde86391600b9d1f7254baef7b98c52af4770")
try:
    sms.verification({'receptor': '09385860444','type': '1','template': 'djangoetebar','param1': '1612'})
    print("done")
except:
    print("failed")