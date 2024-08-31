# midway_pic_tool
Tool to read and (optionally) modify serial number and/or date from PIC16F57 dump used in many Atari/Midway games  
by Pat Daderko (DogP) based on MAME midway_serial_pic_device::generate_serial_data from midwayic.cpp by Aaron Giles, extra functionalities added by neSneSgB  

**Usage:** midway_pic_tool <filename> [new SN (0-999999)] [new MM (1-12)] [new DD (1-31)] [new YYYY (1980-2155)]  
Enter '-' to leave parameter unchanged
Enter 'random' as a serial number parameter to receive a random number

Repository includes C source code and precompiled Windows executable, and Python port.

**NOTES:**
* Entering new values modifies original file  
* KLOV user neSneSgB successfully tested this tool, though noted that SF Rush 2049 SE errored on boot with "IOASIC PROBLEM" if the first 3 digits of the S/N were changed.
* This version includes a randomization function to provide a random serial, and the ability to modify the first 3 numbers of the serial has been disabled, as some games verify this ID and will refuse to work if it is wrong.

The license for this code is BSD 3-Clause as it uses BSD 3-Clause licensed code from MAME midwayic.cpp by Aaron Giles.
