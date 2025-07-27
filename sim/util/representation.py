def to_signed32(n):
    """Convert unsigned 32-bit int to signed 32-bit."""
    n = n & 0xFFFFFFFF
    return n if n < 0x80000000 else n - 0x100000000
