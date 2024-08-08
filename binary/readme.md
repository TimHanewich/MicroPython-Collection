# binary
A lightweight module for converting bytes to and from bits.

## Example Usage
```
>>> import binary
>>> bits = binary.byte_to_bits(232)
>>> bits
[True, True, True, False, True, False, False, False]
>>> byte = binary.bits_to_byte(bits)
>>> byte
232
```