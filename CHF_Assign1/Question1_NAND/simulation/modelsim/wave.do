onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /question1_nand/F
add wave -noupdate /question1_nand/W
add wave -noupdate /question1_nand/X
add wave -noupdate /question1_nand/Y
add wave -noupdate /question1_nand/Z
add wave -noupdate /question1_nand/F
add wave -noupdate /question1_nand/W
add wave -noupdate /question1_nand/X
add wave -noupdate /question1_nand/Y
add wave -noupdate /question1_nand/Z
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ps} 0}
quietly wave cursor active 0
configure wave -namecolwidth 168
configure wave -valuecolwidth 60
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
WaveRestoreZoom {0 ps} {1029 ps}
view wave 
wave clipboard store
wave create -pattern none -portmode out -language vhdl /question1_nand/F 
wave create -pattern none -portmode in -language vhdl /question1_nand/W 
wave create -pattern none -portmode in -language vhdl /question1_nand/X 
wave create -pattern none -portmode in -language vhdl /question1_nand/Y 
wave create -pattern none -portmode in -language vhdl /question1_nand/Z 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question1_nand/Z 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question1_nand/Y 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question1_nand/X 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 800ps -dutycycle 50 -starttime 0ps -endtime 1000ps Edit:/question1_nand/W 
WaveCollapseAll -1
wave clipboard restore
