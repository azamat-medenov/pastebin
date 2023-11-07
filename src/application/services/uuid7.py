import time
import random

sequenceCounter = 0
_last_v1timestamp = 0
_last_v6timestamp = 0
_last_v7timestamp = 0
_last_v8timestamp = 0
_last_uuid_int = 0
_last_sequence = None
uuidVariant = '10'


def uuid7(devDebugs: bool = False, returnType: str = 'hex') -> str | int:
    """Generates a 128-bit version 7 UUID with nanoseconds precision timestamp and random node
    example: 061cdd23-93a0-73df-a200-6ff3e72d92e9

    format: unixts|subsec_a|version|subsec_b|variant|subsec_seq_node
    """

    global _last_v7timestamp
    global _last_uuid_int
    global _last_sequence
    global sequenceCounter
    global uuidVariant
    uuidVersion = '0111'  # ver 7
    sec_bits = 36  # unixts at second precision
    subsec_bits = 30  # Enough to represent NS
    version_bits = 4  # '0111' for ver 7
    variant_bits = 2  # '10' Static for UUID
    sequence_bits = 8  # Enough for 256 UUIDs per NS
    node_bits = (128 - sec_bits - subsec_bits - version_bits - variant_bits - sequence_bits)  # 48

    ### Timestamp Work
    # Produces unix epoch with nanosecond precision
    timestamp = time.time_ns()  # Produces 64-bit NS timestamp
    # Subsecond Math
    subsec_decimal_digits = 9  # Last 9 digits of are subsection precision
    subsec_decimal_divisor = (10 ** subsec_decimal_digits)  # 1000000000 NS in 1 second
    integer_part = int(timestamp / subsec_decimal_divisor)  # Get seconds
    sec = integer_part
    # Conversion to decimal
    fractional_part = round((timestamp % subsec_decimal_divisor) / subsec_decimal_divisor, subsec_decimal_digits)
    subsec = round(fractional_part * (2 ** subsec_bits))  # Convert to 30 bit int, round

    if devDebugs == True:
        print("Timestamp: " + str(timestamp))
        print("Sec: " + str(sec))
        print("Subsec Int: " + str(subsec))
        print("Subsec Dec: " + "{0:.9f}".format(fractional_part))  # Print with trailing 0s
        test_timestamp = str(sec) + str("{0:.9f}".format(fractional_part)[-9:])  # Concat and drop leading '0.'
        if test_timestamp == str(timestamp):  # Quick test for subsec math
            print("Good subsec math")
        else:
            print("Bad Subsec Math")

    ### Binary Conversions
    ### Need subsec_a (12 bits), subsec_b (12-bits), and subsec_c (leftover bits starting subsec_seq_node)
    unixts = f'{sec:036b}'
    subsec_binary = f'{subsec:030b}'
    subsec_a = subsec_binary[:12]  # Upper 12
    subsec_b_c = subsec_binary[-18:]  # Lower 18
    subsec_b = subsec_b_c[:12]  # Upper 12
    subsec_c = subsec_binary[-6:]  # Lower 6

    ### Sequence Work
    # Sequence starts at 0, increments if timestamp is the same, the sequence increments by 1
    # Resets if timestamp int is larger than _last_v7timestamp used for UUID generation
    # Will be 8 bits for NS timestamp
    if timestamp <= _last_v7timestamp:
        sequenceCounter = int(sequenceCounter) + 1
        if devDebugs == True:
            print("Sequence: Incrementing Sequence to {0}".format(str(sequenceCounter)))
    if timestamp > _last_v7timestamp:
        sequenceCounter = 0
        if devDebugs == True:
            print("Sequence: Setting to {0}".format(str(sequenceCounter)))

    sequenceCounterBin = f'{sequenceCounter:08b}'

    # Set these two before moving on
    _last_v7timestamp = timestamp
    _last_sequence = int(sequenceCounter)

    ### Random Node Work
    randomInt = random.getrandbits(node_bits)
    randomBinary = f'{randomInt:048b}'

    # Create subsec_seq_node
    subsec_seq_node = subsec_c + sequenceCounterBin + randomBinary

    ### Formatting Work
    # Bin merge and Int creation
    UUIDv7_bin = unixts + subsec_a + uuidVersion + subsec_b + uuidVariant + subsec_seq_node
    UUIDv7_int = int(UUIDv7_bin, 2)
    if devDebugs == True:  # Compare previous Int. Should always be higher
        if UUIDv7_int < _last_uuid_int and _last_uuid_int != 0:
            print("Error: UUID went Backwards!")
            print("UUIDv7 Last: " + str(_last_uuid_int))
            print("UUIDv7 Curr: " + str(UUIDv7_int))
    _last_uuid_int = UUIDv7_int

    # Convert Hex to Int then splice in dashes
    UUIDv7_hex = f'{UUIDv7_int:032x}'  # int to hex
    UUIDv7_formatted = '-'.join(
        [UUIDv7_hex[:8], UUIDv7_hex[8:12], UUIDv7_hex[12:16], UUIDv7_hex[16:20], UUIDv7_hex[20:32]])

    if devDebugs == True:
        print("UUIDv7 Con: {0}|{1}|{2}|{3}|{4}|{5}".format(unixts,
                                                           subsec_a,
                                                           uuidVersion,
                                                           subsec_b,
                                                           uuidVariant,
                                                           subsec_seq_node))
        print("UUIDv7 Bin: {0} (len: {1})".format(UUIDv7_bin, len(UUIDv7_bin)))
        print("UUIDv7 Int: " + str(UUIDv7_int))
        print("UUIDv7 Hex: " + UUIDv7_formatted)
        print("\n")

    if returnType.lower() == "bin":
        return UUIDv7_bin
    if returnType.lower() == "int":
        return UUIDv7_int
    if returnType.lower() == "hex":
        return UUIDv7_formatted

    raise ValueError('return type was not specified')