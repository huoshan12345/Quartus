view wave 
wave clipboard store
wave create -pattern none -portmode in -language vhdl -range 15 0 /bus16_mux8/D0 
wave create -pattern none -portmode in -language vhdl -range 15 0 /bus16_mux8/D1 
wave create -pattern none -portmode in -language vhdl -range 15 0 /bus16_mux8/D2 
wave create -pattern none -portmode in -language vhdl -range 15 0 /bus16_mux8/D3 
wave create -pattern none -portmode in -language vhdl -range 15 0 /bus16_mux8/D4 
wave create -pattern none -portmode in -language vhdl -range 15 0 /bus16_mux8/D5 
wave create -pattern none -portmode in -language vhdl -range 15 0 /bus16_mux8/D6 
wave create -pattern none -portmode in -language vhdl -range 15 0 /bus16_mux8/D7 
wave create -pattern none -portmode in -language vhdl -range 2 0 /bus16_mux8/SEL 
wave modify -driver freeze -pattern constant -value 0000000000001010 -range 15 0 -starttime 0ns -endtime 800ns Edit:/bus16_mux8/D0 
wave modify -driver freeze -pattern constant -value 0000000000010100 -range 15 0 -starttime 0ns -endtime 800ns Edit:/bus16_mux8/D1 
wave modify -driver freeze -pattern constant -value 0000000000011110 -range 15 0 -starttime 0ns -endtime 800ns Edit:/bus16_mux8/D2 
wave modify -driver freeze -pattern constant -value 0000000000101000 -range 15 0 -starttime 0ns -endtime 800ns Edit:/bus16_mux8/D3 
wave modify -driver freeze -pattern constant -value 0000000000110010 -range 15 0 -starttime 0ns -endtime 800ns Edit:/bus16_mux8/D4 
wave modify -driver freeze -pattern constant -value 0000000000111100 -range 15 0 -starttime 0ns -endtime 800ns Edit:/bus16_mux8/D5 
wave modify -driver freeze -pattern constant -value 0000000001000110 -range 15 0 -starttime 0ns -endtime 800ns Edit:/bus16_mux8/D6 
wave modify -driver freeze -pattern constant -value 0000000001010000 -range 15 0 -starttime 0ns -endtime 800ns Edit:/bus16_mux8/D7 
wave modify -driver freeze -pattern constant -value 000 -range 2 0 -starttime 0ns -endtime 100ns Edit:/bus16_mux8/SEL 
wave modify -driver freeze -pattern constant -value 001 -range 2 0 -starttime 100ns -endtime 200ns Edit:/bus16_mux8/SEL 
wave modify -driver freeze -pattern constant -value 010 -range 2 0 -starttime 200ns -endtime 300ns Edit:/bus16_mux8/SEL 
wave modify -driver freeze -pattern constant -value 011 -range 2 0 -starttime 300ns -endtime 400ns Edit:/bus16_mux8/SEL 
wave modify -driver freeze -pattern constant -value 100 -range 2 0 -starttime 400ns -endtime 500ns Edit:/bus16_mux8/SEL 
wave modify -driver freeze -pattern constant -value 101 -range 2 0 -starttime 500ns -endtime 600ns Edit:/bus16_mux8/SEL 
wave modify -driver freeze -pattern constant -value 110 -range 2 0 -starttime 600ns -endtime 700ns Edit:/bus16_mux8/SEL 
wave modify -driver freeze -pattern constant -value 111 -range 2 0 -starttime 700ns -endtime 800ns Edit:/bus16_mux8/SEL 
WaveCollapseAll -1
wave clipboard restore
