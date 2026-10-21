view wave 
wave clipboard store
wave create -pattern none -portmode out -language vhdl /chf_assign4/W0 
wave create -pattern none -portmode in -language vhdl /chf_assign4/CLK 
wave create -pattern none -portmode in -language vhdl /chf_assign4/RxD 
wave create -pattern none -portmode out -language vhdl /chf_assign4/W1 
wave create -pattern none -portmode out -language vhdl /chf_assign4/W2 
wave create -pattern none -portmode out -language vhdl /chf_assign4/W3 
wave create -pattern none -portmode out -language vhdl /chf_assign4/P 
wave create -pattern none -portmode out -language vhdl /chf_assign4/W_OUT 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 100ps -dutycycle 50 -starttime 0ps -endtime 10000ps Edit:/chf_assign4/CLK 
wave modify -driver freeze -pattern clock -initialvalue 0 -period 200ps -dutycycle 50 -starttime 0ps -endtime 10000ps Edit:/chf_assign4/RxD 
WaveCollapseAll -1
wave clipboard restore
