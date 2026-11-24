load_package project
source {C:/intelFPGA_lite/20.1/quartus/common/tcl/internal/nativelink/qnativelinkflow.tcl}
project_open -revision register16 {D:/Users/lijing/Documents/Quartus/Assignment2/assignment2}
set selected_tool [get_global_assignment -name EDA_SIMULATION_TOOL]
set executable [::quartus::nativelinkflow::resolve_tool_path sim vsim $selected_tool]
puts "SELECTED_TOOL=$selected_tool"
puts "RESOLVED_EXECUTABLE=$executable"
if {$executable eq "" || ![file exists $executable]} {
    error {NativeLink could not resolve the simulator executable}
}
puts "VERSION=[exec $executable -version]"
project_close
