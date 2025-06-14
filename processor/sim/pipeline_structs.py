# This file must mirror the pipeline_types.sv file

def gets(val, typ, acc):
    """
    Retrieve a value from within an SV Struct

    Args:
        val (): Struct to Retrieve From
        typ (): Typename of the struct
        acc (): Name of the SV struct parameter

    Returns:
        The value within the struct (not an integer)
    """
    return val.value[typ[acc][0]:typ[acc][1]]


IF_ID = {
        "pc": (0, 31),
        "pc4": (32, 63),
        "instruction": (64, 95)
        }
