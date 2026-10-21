view wave 
wave clipboard store
wave create -pattern none -portmode out -language vhdl /chf_assign3/Z 
wave create -pattern none -portmode in -language vhdl /chf_assign3/Reset 
wave create -pattern none -portmode in -language vhdl /chf_assign3/CLK 
wave create -pattern none -portmode in -language vhdl /chf_assign3/X 
wave create -pattern none -portmode out -language vhdl /chf_assign3/Y 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/CLK 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern random -initialvalue 0 -period 50ps -random_type Uniform -seed 5 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern random -initialvalue 0 -period 50ps -random_type Uniform -seed 1 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 800ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 100ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 100ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 100ps -endtime 2000ps Edit:/chf_assign3/CLK 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 100ps -endtime 2000ps Edit:/chf_assign3/CLK 
wave modify -driver freeze -pattern constant -value 0 -starttime 0ps -endtime 100ps Edit:/chf_assign3/CLK 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/CLK 
wave modify -driver freeze -pattern constant -value 1 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/Reset 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 800ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 400ps -dutycycle 50 -starttime 0ps -endtime 2000ps Edit:/chf_assign3/X 
WaveCollapseAll -1
wave clipboard restore
