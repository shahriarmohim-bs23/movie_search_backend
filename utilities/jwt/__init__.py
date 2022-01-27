import jwt
from datetime import datetime,timedelta


jwt_secret = 'jaissadebhaikonosomossanai'
jwt_algorithm = 'HS256'


def encode(payload):
    issued_time = datetime.utcnow()
    expired_time = issued_time+timedelta(minutes=15)
    payload['iat'] = issued_time
    payload['exp'] = expired_time
    encoded_string = jwt.encode(payload=payload,key=jwt_secret,algorithm=jwt_algorithm)
    return encoded_string



def decode(encoded_string):
    decoded_payload = jwt.decode(jwt=encoded_string, key=jwt_secret, algorithms=[jwt_algorithm])
    return decoded_payload
