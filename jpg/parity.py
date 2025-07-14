UID = '1234'

data_with_parity = []
for char in UID:
    byte = f"{ord(char):08b}"
    parity = byte.count("1") % 2  
    data_with_parity.append(byte + str(parity))
bits = "".join(data_with_parity)
print(bits)

# ------------------------------------ #

# UID = ['00110001', '00110010', '00110011', '00110100']

# data_with_parity = []
# for byte in UID:
#     parity = byte.count("1") % 2 
#     data_with_parity.append(byte + str(parity))
# bits = "".join(data_with_parity)
# print(bits)
