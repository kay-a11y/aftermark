import json

# Create JSON from payload
payload = "{abc}"
json_str = json.dumps(payload)

print(f"Original JSON string: {json_str!r}\n")

# Display binary breakdown of each character
print("Character breakdown:")
for c in json_str:
    print(f"  {c!r} → ord: {ord(c):3} → bin: {ord(c):08b}")
    
# Show binary of '{' and '}'
print("\nCurly braces specifically:")
print(f"  '{{' → ord: {ord('{')} → bin: {ord('{'):08b}")
print(f"  '}}' → ord: {ord('}')} → bin: {ord('}'):08b}")

# Full JSON string to bit string
bit_str = ''.join(f'{ord(c):08b}' for c in json_str) + '00000000'
print(f"\nFull binary bitstring (with end padding):\n{bit_str}")

print("\nVisual as LSB bits in pixel channels:")
for i, bit in enumerate(bit_str):
    print(f"Pixel {i:03} → LSB: {bit}")

