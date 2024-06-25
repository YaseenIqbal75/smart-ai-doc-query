import jwt
import base64
import datetime

# Secret key and algorithm
key = "arslanwaqar421"
algorithm = "HS256"

def decode_jwt_without_verification(token):
    # Split the token into its parts
    header, payload, signature = token.split('.')
    # Decode the parts
    decoded_header = base64.urlsafe_b64decode(header + '==').decode('utf-8')
    decoded_payload = base64.urlsafe_b64decode(payload + '==').decode('utf-8')
    decoded_signature = base64.urlsafe_b64decode(signature + '==')
    return decoded_header, decoded_payload, decoded_signature

def verify_jwt(token):
    try:
        decoded = jwt.decode(token, key, algorithms=[algorithm])
        return {"status": True, "msg": decoded}
    except jwt.ExpiredSignatureError as e:
        return {"status": False, "msg": "Signature has expired"}
    except jwt.InvalidTokenError as e:
        return {"status": False, "msg": "Invalid token"}

# Tokens for testing
token1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhamlkQGdtYWlsLmNvbSIsImV4cCI6MTcxOTMwNzM1MH0.tw8XeruVTfwJi3wCEYAzAJMhaxKMt7a4IEY4aZCwUu8"  # Authentic token
token2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhamlkQGdtYWlsLmNvbSIsImV4cCI6MTcxOTMwNzM1MH0.tw8XeruVTfwJi3wCEYAzAJMhaxKMt7a4IEY4aZCwUu7"  # Tampered token
token3 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhamlkQGdtYWlsLmNvbSIsImV4cCI6MTcxOTMwNzM1MH0.tw8XeruVTfwJi3wCEYAzAJMhaxKMt7a4IEY4aZCwUu9"  # Tampered token

# Decode tokens without verification
header1, payload1, signature1 = decode_jwt_without_verification(token1)
header2, payload2, signature2 = decode_jwt_without_verification(token2)
header3, payload3, signature3 = decode_jwt_without_verification(token3)

print("Token 1:")
print("Header:", header1)
print("Payload:", payload1)
print("Signature:", signature1)

print("\nToken 2:")
print("Header:", header2)
print("Payload:", payload2)
print("Signature:", signature2)

print("\nToken 3:")
print("Header:", header3)
print("Payload:", payload3)
print("Signature:", signature3)

# Verify tokens
decoded_token1 = verify_jwt(token1)
decoded_token2 = verify_jwt(token2)
decoded_token3 = verify_jwt(token3)

print("\nVerification Results:")
print("Decoded Token 1:", decoded_token1)
print("Decoded Token 2:", decoded_token2)
print("Decoded Token 3:", decoded_token3)
