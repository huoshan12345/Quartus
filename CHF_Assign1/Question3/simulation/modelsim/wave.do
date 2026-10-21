onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /question3/Z2
add wave -noupdate /question3/Z1
add wave -noupdate /question3/Z0
add wave -noupdate /question3/X1
add wave -noupdate /question3/X0
add wave -noupdate /question3/Y1
add wave -noupdate /question3/Y0
add wave -noupdate /question3/Z2
add wave -noupdate /question3/Z1
add wave -noupdate /question3/Z0
add wave -noupdate /question3/X1
add wave -noupdate /question3/X0
add wave -noupdate /question3/Y1
add wave -noupdate /question3/Y0
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ps} 0}
quietly wave cursor active 0
configure wave -namecolwidth 151
configure wave -valuecolwidth 100
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
configure wave -timelineunits ps
update
WaveRestoreZoom {0 ps} {999 ps}
view wave 
wave clipboard store
wave create -pattern none -portmode out -language vhdl /question3/Z2 
wave create -pattern none -portmode in -language vhdl /question3/X1 
wave create -pattern none -portmode in -language vhdl /question3/X0 
wave create -pattern none -portmode in -language vhdl /question3/Y1 
wave create -pattern none -portmode in -language vhdl /question3/Y0 
wave create -pattern none -portmode out -language vhdl /question3/Z1 
wave create -pattern none -portmode out -language vhdl /question3/Z0 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question3/Y0 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question3/Y1 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question3/X0 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 800ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question3/X1 
WaveCollapseAll -1
wave clipboard restore
