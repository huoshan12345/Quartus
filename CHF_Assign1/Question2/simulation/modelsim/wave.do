onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /question2/F
add wave -noupdate /question2/X4
add wave -noupdate /question2/X3
add wave -noupdate /question2/X2
add wave -noupdate /question2/X1
add wave -noupdate /question2/X0
add wave -noupdate /question2/F
add wave -noupdate /question2/X4
add wave -noupdate /question2/X3
add wave -noupdate /question2/X2
add wave -noupdate /question2/X1
add wave -noupdate /question2/X0
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ps} 0}
quietly wave cursor active 0
configure wave -namecolwidth 150
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
WaveRestoreZoom {51 ps} {1643 ps}
view wave 
wave clipboard store
wave create -pattern none -portmode out -language vhdl /question2/F 
wave create -pattern none -portmode in -language vhdl /question2/X4 
wave create -pattern none -portmode in -language vhdl /question2/X1 
wave create -pattern none -portmode in -language vhdl /question2/X2 
wave create -pattern none -portmode in -language vhdl /question2/X3 
wave create -pattern none -portmode in -language vhdl /question2/X0 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/question2/X0 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/question2/X1 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/question2/X2 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 800ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/question2/X3 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 1600ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/question2/X4 
WaveCollapseAll -1
wave clipboard restore
