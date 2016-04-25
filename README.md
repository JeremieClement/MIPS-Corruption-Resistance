MIPS-Corruption-Resistance
==========================
Contains a Python script that allows to create a verification vector, using the "multi-lock" method described in
Software-Only Fault-Protected MIPS Programs presented in .
This vector allows to protect a MIPS program against alterations on up to three instructions

Usage :
-------

```
python testvector.py <name_of_the_hex_MIPS_file>
```

An example of input (inputP.hex) and output (outputP.hex) files have been provided
