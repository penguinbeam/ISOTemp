# ISOTemp
Python to watch w1 thermometer sensors and trigger an ifttt webhook if temperature is greater than or less that configured metrics

Example temperature capture run:

`ISOTEMPBTMMAC="00:00:00:00:00:06" ISOTEMPDATADIR="." ISOTEMPSENSORPATH=/home/pi/ISOTemp/testdata ISOTEMPBTS=True python temp_logger.py`

Example temperature capture from bluetooth:

`ISOTEMPBTMMAC="00:00:00:00:00:06" ISOTEMPDATADIR="." atemp_recbt_logger.py

Example check and alert:

`IFTTTKEY=abcdefg_abcdefghijklmnopqrstuvwxyzabcdefghi ISOTEMPDATADIR="." python temp_parseNalert.py`

`IFTTTKEY=abcdefg_abcdefghijklmnopqrstuvwxyzabcdefghi ISOTEMPDATADIR="." ISOTEMPBTSRC=True python temp_parseNalert.py`
