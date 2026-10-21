onerror {quit -f -code 1}
transcript file native_register_check.log
vmap -c
vlib native_check_work
vmap work native_check_work
vcom -93 -work work register8.vho
vsim work.register8
log sim:/register8/*
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00000101
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 5} {puts "FAIL register8 case 0: LD=1, DIN=5, expected 5, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#00001001
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 5} {puts "FAIL register8 case 1: LD=0, DIN=9, expected 5, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#00001001
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 5} {puts "FAIL register8 case 2: LD=0, DIN=9, expected 5, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00001001
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 9} {puts "FAIL register8 case 3: LD=1, DIN=9, expected 9, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#00001100
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 9} {puts "FAIL register8 case 4: LD=0, DIN=12, expected 9, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00001100
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 12} {puts "FAIL register8 case 5: LD=1, DIN=12, expected 12, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#00000011
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 12} {puts "FAIL register8 case 6: LD=0, DIN=3, expected 12, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#11111111
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 12} {puts "FAIL register8 case 7: LD=0, DIN=255, expected 12, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00000000
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 0} {puts "FAIL register8 case 8: LD=1, DIN=0, expected 0, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#11111111
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 0} {puts "FAIL register8 case 9: LD=0, DIN=255, expected 0, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#11111111
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 255} {puts "FAIL register8 case 10: LD=1, DIN=255, expected 255, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#00000000
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 255} {puts "FAIL register8 case 11: LD=0, DIN=0, expected 255, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00000001
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 1} {puts "FAIL register8 case 12: LD=1, DIN=1, expected 1, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#11111110
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 1} {puts "FAIL register8 case 13: LD=0, DIN=254, expected 1, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00000010
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 2} {puts "FAIL register8 case 14: LD=1, DIN=2, expected 2, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#11111101
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 2} {puts "FAIL register8 case 15: LD=0, DIN=253, expected 2, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00000100
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 4} {puts "FAIL register8 case 16: LD=1, DIN=4, expected 4, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#11111011
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 4} {puts "FAIL register8 case 17: LD=0, DIN=251, expected 4, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00001000
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 8} {puts "FAIL register8 case 18: LD=1, DIN=8, expected 8, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#11110111
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 8} {puts "FAIL register8 case 19: LD=0, DIN=247, expected 8, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00010000
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 16} {puts "FAIL register8 case 20: LD=1, DIN=16, expected 16, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#11101111
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 16} {puts "FAIL register8 case 21: LD=0, DIN=239, expected 16, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#00100000
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 32} {puts "FAIL register8 case 22: LD=1, DIN=32, expected 32, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#11011111
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 32} {puts "FAIL register8 case 23: LD=0, DIN=223, expected 32, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#01000000
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 64} {puts "FAIL register8 case 24: LD=1, DIN=64, expected 64, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#10111111
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 64} {puts "FAIL register8 case 25: LD=0, DIN=191, expected 64, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 1
force -freeze sim:/register8/DIN 2#10000000
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 128} {puts "FAIL register8 case 26: LD=1, DIN=128, expected 128, observed $observed"; quit -f -code 1}
force -freeze sim:/register8/CLK 0
force -freeze sim:/register8/LD 0
force -freeze sim:/register8/DIN 2#01111111
run 50ns
force -freeze sim:/register8/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register8/Q]
if {$observed != 128} {puts "FAIL register8 case 27: LD=0, DIN=127, expected 128, observed $observed"; quit -f -code 1}
puts "PASS register8: 28 native gate-netlist load/hold cases, including every data bit"
quit -sim
vcom -93 -work work register16.vho
vsim work.register16
log sim:/register16/*
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000000101
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 5} {puts "FAIL register16 case 0: LD=1, DIN=5, expected 5, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#0000000000001001
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 5} {puts "FAIL register16 case 1: LD=0, DIN=9, expected 5, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#0000000000001001
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 5} {puts "FAIL register16 case 2: LD=0, DIN=9, expected 5, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000001001
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 9} {puts "FAIL register16 case 3: LD=1, DIN=9, expected 9, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#0000000000001100
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 9} {puts "FAIL register16 case 4: LD=0, DIN=12, expected 9, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000001100
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 12} {puts "FAIL register16 case 5: LD=1, DIN=12, expected 12, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#0000000000000011
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 12} {puts "FAIL register16 case 6: LD=0, DIN=3, expected 12, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 12} {puts "FAIL register16 case 7: LD=0, DIN=65535, expected 12, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 0} {puts "FAIL register16 case 8: LD=1, DIN=0, expected 0, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 0} {puts "FAIL register16 case 9: LD=0, DIN=65535, expected 0, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#1111111111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 65535} {puts "FAIL register16 case 10: LD=1, DIN=65535, expected 65535, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#0000000000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 65535} {puts "FAIL register16 case 11: LD=0, DIN=0, expected 65535, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000000001
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 1} {puts "FAIL register16 case 12: LD=1, DIN=1, expected 1, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111111111110
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 1} {puts "FAIL register16 case 13: LD=0, DIN=65534, expected 1, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000000010
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 2} {puts "FAIL register16 case 14: LD=1, DIN=2, expected 2, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111111111101
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 2} {puts "FAIL register16 case 15: LD=0, DIN=65533, expected 2, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000000100
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 4} {puts "FAIL register16 case 16: LD=1, DIN=4, expected 4, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111111111011
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 4} {puts "FAIL register16 case 17: LD=0, DIN=65531, expected 4, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000001000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 8} {puts "FAIL register16 case 18: LD=1, DIN=8, expected 8, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111111110111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 8} {puts "FAIL register16 case 19: LD=0, DIN=65527, expected 8, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000010000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 16} {puts "FAIL register16 case 20: LD=1, DIN=16, expected 16, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111111101111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 16} {puts "FAIL register16 case 21: LD=0, DIN=65519, expected 16, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000000100000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 32} {puts "FAIL register16 case 22: LD=1, DIN=32, expected 32, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111111011111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 32} {puts "FAIL register16 case 23: LD=0, DIN=65503, expected 32, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000001000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 64} {puts "FAIL register16 case 24: LD=1, DIN=64, expected 64, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111110111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 64} {puts "FAIL register16 case 25: LD=0, DIN=65471, expected 64, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000010000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 128} {puts "FAIL register16 case 26: LD=1, DIN=128, expected 128, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111101111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 128} {puts "FAIL register16 case 27: LD=0, DIN=65407, expected 128, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000000100000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 256} {puts "FAIL register16 case 28: LD=1, DIN=256, expected 256, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111111011111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 256} {puts "FAIL register16 case 29: LD=0, DIN=65279, expected 256, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000001000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 512} {puts "FAIL register16 case 30: LD=1, DIN=512, expected 512, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111110111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 512} {puts "FAIL register16 case 31: LD=0, DIN=65023, expected 512, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000010000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 1024} {puts "FAIL register16 case 32: LD=1, DIN=1024, expected 1024, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111101111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 1024} {puts "FAIL register16 case 33: LD=0, DIN=64511, expected 1024, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0000100000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 2048} {puts "FAIL register16 case 34: LD=1, DIN=2048, expected 2048, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1111011111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 2048} {puts "FAIL register16 case 35: LD=0, DIN=63487, expected 2048, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0001000000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 4096} {puts "FAIL register16 case 36: LD=1, DIN=4096, expected 4096, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1110111111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 4096} {puts "FAIL register16 case 37: LD=0, DIN=61439, expected 4096, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0010000000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 8192} {puts "FAIL register16 case 38: LD=1, DIN=8192, expected 8192, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1101111111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 8192} {puts "FAIL register16 case 39: LD=0, DIN=57343, expected 8192, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#0100000000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 16384} {puts "FAIL register16 case 40: LD=1, DIN=16384, expected 16384, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#1011111111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 16384} {puts "FAIL register16 case 41: LD=0, DIN=49151, expected 16384, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 1
force -freeze sim:/register16/DIN 2#1000000000000000
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 32768} {puts "FAIL register16 case 42: LD=1, DIN=32768, expected 32768, observed $observed"; quit -f -code 1}
force -freeze sim:/register16/CLK 0
force -freeze sim:/register16/LD 0
force -freeze sim:/register16/DIN 2#0111111111111111
run 50ns
force -freeze sim:/register16/CLK 1
run 50ns
set observed [examine -radix unsigned sim:/register16/Q]
if {$observed != 32768} {puts "FAIL register16 case 43: LD=0, DIN=32767, expected 32768, observed $observed"; quit -f -code 1}
puts "PASS register16: 44 native gate-netlist load/hold cases, including every data bit"
quit -sim
quit -f -code 0
