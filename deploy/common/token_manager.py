from config import SECRET_KEY, TIMEOUT
import base64, random, time, json, hmac

class Token_Manager(object):
    '''
        data = {'username':'test','password':'123456'}
        or something other user's data
    '''
    def __init__(self):
        pass

    def verify_auth_token(self, token):
        decoded_token = self._decode_token_bytes(str(token))
        payload = decoded_token[:-16]
        sig = decoded_token[-16:]
        expected_sig = self._get_signature(payload)
        if sig != expected_sig:
            return 401
        data = json.loads(payload.decode("utf8"))
        if data.get('expires') >= time.time():
            return data
        return 408

    def _get_signature(self, value):
        return hmac.new(SECRET_KEY, value).digest()

    def _decode_token_bytes(self, data):
        return base64.urlsafe_b64decode(data)





