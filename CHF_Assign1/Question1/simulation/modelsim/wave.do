onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /question1/F
add wave -noupdate /question1/W
add wave -noupdate /question1/X
add wave -noupdate /question1/Y
add wave -noupdate /question1/Z
add wave -noupdate /question1/F
add wave -noupdate /question1/W
add wave -noupdate /question1/X
add wave -noupdate /question1/Y
add wave -noupdate /question1/Z
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
WaveRestoreZoom {49 ps} {969 ps}
view wave 
wave clipboard store
wave create -pattern none -portmode out -language vhdl /question1/F 
wave create -pattern none -portmode in -language vhdl /question1/W 
wave create -pattern none -portmode in -language vhdl /question1/X 
wave create -pattern none -portmode in -language vhdl /question1/Y 
wave create -pattern none -portmode in -language vhdl /question1/Z 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question1/Z 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question1/Y 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question1/X 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 800ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question1/W 
WaveCollapseAll -1
wave clipboard restore
