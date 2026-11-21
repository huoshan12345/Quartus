view wave 
wave clipboard store
wave create -pattern none -portmode in -language vhdl /register16/CLK 
wave create -pattern none -portmode in -language vhdl /register16/LD 
wave create -pattern none -portmode in -language vhdl -range 15 0 /register16/DIN 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ns -dutycycle 50 -starttime 0ns -endtime 1000ns Edit:/register16/CLK 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ns -endtime 1000ns Edit:/register16/LD 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ns -endtime 100ns Edit:/register16/LD 
wave modify -driver freeze -pattern constant -value 1 -starttime 300ns -endtime 400ns Edit:/register16/LD 
wave modify -driver freeze -pattern constant -value 1 -starttime 600ns -endtime 700ns Edit:/register16/LD 
wave modify -driver freeze -pattern constant -value 0000000000000101 -range 15 0 -starttime 0ns -endtime 100ns Edit:/register16/DIN 
wave modify -driver freeze -pattern constant -value 0000000000001001 -range 15 0 -starttime 100ns -endtime 400ns Edit:/register16/DIN 
wave modify -driver freeze -pattern constant -value 0000000000001100 -range 15 0 -starttime 400ns -endtime 700ns Edit:/register16/DIN 
wave modify -driver freeze -pattern constant -value 0000000000000011 -range 15 0 -starttime 700ns -endtime 1000ns Edit:/register16/DIN 
WaveCollapseAll -1
wave clipboard restore
