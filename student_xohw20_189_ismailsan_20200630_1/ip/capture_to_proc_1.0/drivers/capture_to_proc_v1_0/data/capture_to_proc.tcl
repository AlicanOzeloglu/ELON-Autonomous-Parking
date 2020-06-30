

proc generate {drv_handle} {
	xdefine_include_file $drv_handle "xparameters.h" "capture_to_proc" "NUM_INSTANCES" "DEVICE_ID"  "C_S00_AXI_BASEADDR" "C_S00_AXI_HIGHADDR"
}
