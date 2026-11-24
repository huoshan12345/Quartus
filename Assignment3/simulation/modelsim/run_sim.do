# ModelSim simulation script for ENGI 9861 Assignment #3 Basic Computer
# Usage in ModelSim GUI:
#   cd {D:/Users/lijing/Documents/Quartus/Assignment3/simulation/modelsim}
#   do run_sim.do

if {[file exists work]} {
    vdel -lib work -all
}
vlib work
vmap work work

vcom -93 -work work basic_computer.vho
vcom -93 -work work tb_basic_computer.vhd

vsim -t 1ps -L altera -L altera_mf -L altera_lnsim -L cyclonev work.tb_basic_computer

if {![batch_mode]} {
    add wave -divider "Clock & Reset"
    add wave -radix binary /tb_basic_computer/clk
    add wave -radix binary /tb_basic_computer/reset

    add wave -divider "Required Outputs (AC, E, Halt S)"
    add wave -radix hexadecimal /tb_basic_computer/ac_q
    add wave -radix binary /tb_basic_computer/e_out
    add wave -radix binary /tb_basic_computer/s_out

    add wave -divider "Affected Memory Locations"
    add wave -radix hexadecimal /tb_basic_computer/mem_103
    add wave -radix hexadecimal /tb_basic_computer/mem_201
    add wave -radix binary /tb_basic_computer/mem_wr_out
    add wave -radix hexadecimal /tb_basic_computer/ar_q
    add wave -radix hexadecimal /tb_basic_computer/bus_data

    add wave -divider "CPU Execution State"
    add wave -radix hexadecimal /tb_basic_computer/pc_q
    add wave -radix hexadecimal /tb_basic_computer/ir_q
    add wave -radix hexadecimal /tb_basic_computer/dr_q
    add wave -radix hexadecimal /tb_basic_computer/mem_q
    add wave -radix unsigned /tb_basic_computer/sc_q

    configure wave -namecolwidth 240
    configure wave -valuecolwidth 100
    configure wave -signalnamewidth 1
}

run -all

if {![batch_mode]} {
    wave zoom full
}
