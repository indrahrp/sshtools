
import base64
from Crypto.Cipher import AES

BLOCK_SIZE = 10
PADDING = 10

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
cipher = AES.new("abcdefgh12345678")

encrypted_key = EncodeAES(cipher, 'ABC123')
