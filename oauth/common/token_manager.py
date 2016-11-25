# -*- coding: utf-8 -*-
from config import SECRET_KEY, TIMEOUT
import base64, random, time, json, hmac
import redis
from config import RedisHost,RedisPost

class Token_Manager(object):
    '''
        data = {'username':'test','password':'123456'}
        or something other user's data
    '''
    def __init__(self):
        self.host = RedisHost
        self.port = RedisPost
        self.redisobj = redis.StrictRedis(host=self.host,port=self.port, db=0)

    def generate_auth_token(self, data):
        data = data.copy()
        if "salt" not in data:
            data["salt"] = unicode(random.random()).decode("ascii")
        if "expires" not in data:
            data["expires"] = time.time() + TIMEOUT
        payload = json.dumps(data).encode("utf8")
        sig = self._get_signature(payload)
        return self._encode_token_bytes(payload + sig)

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

    def _encode_token_bytes(self, data):
        return base64.urlsafe_b64encode(data)

    def _decode_token_bytes(self, data):
        return base64.urlsafe_b64decode(data)

    def redis_set(self,k,v):
        return self.redisobj.set(k,v)

    def redis_get(self,k):
        return self.redisobj.get(k)

