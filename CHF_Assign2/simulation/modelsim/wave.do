onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /chf_assign2/Cout
add wave -noupdate /chf_assign2/G2
add wave -noupdate /chf_assign2/G1
add wave -noupdate /chf_assign2/G0
add wave -noupdate /chf_assign2/A2
add wave -noupdate /chf_assign2/A1
add wave -noupdate /chf_assign2/A0
add wave -noupdate /chf_assign2/B2
add wave -noupdate /chf_assign2/B1
add wave -noupdate /chf_assign2/B0
add wave -noupdate /chf_assign2/S1
add wave -noupdate /chf_assign2/S0
add wave -noupdate /chf_assign2/Cin
add wave -noupdate /chf_assign2/Cout
add wave -noupdate /chf_assign2/G2
add wave -noupdate /chf_assign2/G1
add wave -noupdate /chf_assign2/G0
add wave -noupdate /chf_assign2/A2
add wave -noupdate /chf_assign2/A1
add wave -noupdate /chf_assign2/A0
add wave -noupdate /chf_assign2/B2
add wave -noupdate /chf_assign2/B1
add wave -noupdate /chf_assign2/B0
add wave -noupdate /chf_assign2/S1
add wave -noupdate /chf_assign2/S0
add wave -noupdate /chf_assign2/Cin
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {1781 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 164
configure wave -valuecolwidth 82
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ps} {3260 ps}
view wave 
wave clipboard store
wave create -pattern none -portmode out -language vhdl /chf_assign2/G0 
wave create -pattern none -portmode in -language vhdl /chf_assign2/A0 
wave create -pattern none -portmode in -language vhdl /chf_assign2/S1 
wave create -pattern none -portmode in -language vhdl /chf_assign2/B0 
wave create -pattern none -portmode in -language vhdl /chf_assign2/S0 
wave create -pattern none -portmode in -language vhdl /chf_assign2/Cin 
wave create -pattern none -portmode out -language vhdl /chf_assign2/G1 
wave create -pattern none -portmode in -language vhdl /chf_assign2/A1 
wave create -pattern none -portmode in -language vhdl /chf_assign2/B1 
wave create -pattern none -portmode out -language vhdl /chf_assign2/G2 
wave create -pattern none -portmode in -language vhdl /chf_assign2/A2 
wave create -pattern none -portmode in -language vhdl /chf_assign2/B2 
wave create -pattern none -portmode out -language vhdl /chf_assign2/Cout 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/Cin 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/S0 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/S1 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/B0 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/B1 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/B2 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 800ps -dutycycle 50 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/A0 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 1600ps -dutycycle 50 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/A1 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 3200ps -dutycycle 50 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/A2 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/Cin 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/Cin 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/Cin 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/S0 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/S1 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/S0 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 4000ps Edit:/chf_assign2/S0 
WaveCollapseAll -1
wave clipboard restore
