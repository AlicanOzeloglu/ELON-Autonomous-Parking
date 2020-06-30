#set_property PACKAGE_PIN T21 [get_ports parking_led];

set_property PACKAGE_PIN Y11 [get_ports left_0];
set_property PACKAGE_PIN AA11 [get_ports right_0];

set_property PACKAGE_PIN W12 [get_ports echo_0];
set_property PACKAGE_PIN W11 [get_ports trigger_0];

set_property PACKAGE_PIN W8 [get_ports echo_1];
set_property PACKAGE_PIN V10 [get_ports trigger_1];

set_property PACKAGE_PIN V12 [get_ports echo_2];
set_property PACKAGE_PIN W10 [get_ports trigger_2];

set_property IOSTANDARD LVCMOS33 [get_ports -of_objects [get_iobanks 13]];


################ OV7670 ################
# Debounce button and config finished LED
set_property PACKAGE_PIN T18 [get_ports button_debounce];
set_property PACKAGE_PIN T22 [get_ports led_config_finished];
set_property PACKAGE_PIN W22 [get_ports led_out_0];
set_property PACKAGE_PIN U14 [get_ports detect_out];

set_property PACKAGE_PIN T6 [get_ports ov7670_reset];
set_property PACKAGE_PIN R6 [get_ports {ov7670_d[1]}];
set_property PACKAGE_PIN U4 [get_ports {ov7670_d[3]}];
set_property PACKAGE_PIN T4 [get_ports {ov7670_d[5]}];

set_property PACKAGE_PIN AB6 [get_ports ov7670_pwdn];
set_property PACKAGE_PIN AB7 [get_ports {ov7670_d[0]}];
set_property PACKAGE_PIN AA4 [get_ports {ov7670_d[2]}];
set_property PACKAGE_PIN Y4 [get_ports {ov7670_d[4]}];

set_property PACKAGE_PIN W5 [get_ports {ov7670_d[7]}];
set_property PACKAGE_PIN W6 [get_ports ov7670_pclk];
set_property PACKAGE_PIN U5 [get_ports ov7670_vsync];
set_property PACKAGE_PIN U6 [get_ports ov7670_sioc];

set_property PACKAGE_PIN W7 [get_ports {ov7670_d[6]}];
set_property PACKAGE_PIN V7 [get_ports ov7670_xclk];
set_property PACKAGE_PIN V4 [get_ports ov7670_href];
set_property PACKAGE_PIN V5 [get_ports ov7670_siod];

# Voltage levels
set_property IOSTANDARD LVCMOS33 [get_ports button_debounce];
set_property IOSTANDARD LVCMOS33 [get_ports led_config_finished];
set_property IOSTANDARD LVCMOS33 [get_ports led_out_0];
set_property IOSTANDARD LVCMOS33 [get_ports detect_out];
set_property IOSTANDARD LVCMOS33 [get_ports ov7670_sioc];
set_property IOSTANDARD LVCMOS33 [get_ports ov7670_vsync];
set_property IOSTANDARD LVCMOS33 [get_ports ov7670_reset];
set_property IOSTANDARD LVCMOS33 [get_ports ov7670_pwdn];
set_property IOSTANDARD LVCMOS33 [get_ports ov7670_href];
set_property IOSTANDARD LVCMOS33 [get_ports ov7670_xclk];
set_property IOSTANDARD LVCMOS33 [get_ports ov7670_pclk];
set_property IOSTANDARD LVCMOS33 [get_ports ov7670_siod];
set_property IOSTANDARD LVCMOS33 [get_ports {ov7670_d[*]}];


# Magic
set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets ov7670_pclk_IBUF];

