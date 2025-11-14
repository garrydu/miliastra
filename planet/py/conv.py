import base64

base64_str = "EgFjGAgiJgiSThABIgcIAaIGAggI6gYVChMIAhABIgcIAaIGAggDsgYDCK4ROAZABg=="
# Decode Base64 to bytes
byte_data = base64.b64decode(base64_str)
# Convert each byte to an integer
ints = list(byte_data)
print(ints)
