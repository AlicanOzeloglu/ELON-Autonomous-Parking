/******************************************************************************
*
* Copyright (C) 2009 - 2014 Xilinx, Inc.  All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* Use of the Software is limited solely to applications:
* (a) running on a Xilinx device, or
* (b) that interact with a Xilinx device through a bus or interconnect.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
* Except as contained in this notice, the name of the Xilinx shall not be used
* in advertising or otherwise to promote the sale, use or other dealings in
* this Software without prior written authorization from Xilinx.
*
******************************************************************************/

/*
 * helloworld.c: simple test application
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */

#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xil_io.h"
#include "motor_ip.h"
#include "hcsr_04_ip.h"
#include <math.h>
#include <capture_to_proc.h>
void * baseaddr_ip = (void *)(0x43C00000);

u32 readValue;
int distance_left,distance_front,distance_right;
float state[3];
int ones,tens;
int * parkingNN_control = (int *)(0x43C00000);
float * parkingNN_in = (float *)(0x43C00010);
float * parkingNN_out = (float *)(0x43C00020);

int * searchingNN_control = (int *)(0x43C10000);
float * searchingNN_in = (float *)(0x43C10010);
float * searchingNN_out = (float *)(0x43C10020);

int parking_is_done=0;
int parking_lot_detected=0;
float distance_left_avg;
float distance_right_avg;
float distance_front_avg;

void turnRight(){
	MOTOR_IP_mWriteReg(0x43C50000, MOTOR_IP_S00_AXI_SLV_REG1_OFFSET, 1);
}

void turnLeft(){
	MOTOR_IP_mWriteReg(0x43C50000, MOTOR_IP_S00_AXI_SLV_REG1_OFFSET, 2);
}

void forward(){
	MOTOR_IP_mWriteReg(0x43C50000, MOTOR_IP_S00_AXI_SLV_REG1_OFFSET, 3);
}

void stop(){
	MOTOR_IP_mWriteReg(0x43C50000, MOTOR_IP_S00_AXI_SLV_REG1_OFFSET, 0);

}
volatile int delay_count;
void delay(){
	int i;
	for(delay_count = 0; delay_count<10000000;delay_count++)
		i = delay_count;
}
void parking_lot(){
	for(int i = 0; i < 500000; i++){
		readValue = CAPTURE_TO_PROC_mReadReg(0x43C60000, 0);
		printf("%x \n", readValue);
		if(readValue == 1 && parking_lot_detected == 0)
			parking_lot_detected = 1;
	}
}
void readSensors(){
	readValue = HCSR_04_IP_mReadReg(0x43C20000, HCSR_04_IP_S00_AXI_SLV_REG2_OFFSET);
	while(readValue == 0){
		readValue = HCSR_04_IP_mReadReg(0x43C20000, HCSR_04_IP_S00_AXI_SLV_REG2_OFFSET);
	}
	ones  = readValue & 0x0000000f;
	tens   = (readValue & 0x000000f0) >>4;
	distance_right = tens*10 + ones;


	readValue = HCSR_04_IP_mReadReg(0x43C30000, HCSR_04_IP_S00_AXI_SLV_REG2_OFFSET);
	while(readValue == 0){
		readValue = HCSR_04_IP_mReadReg(0x43C30000, HCSR_04_IP_S00_AXI_SLV_REG2_OFFSET);
	}
	ones  = readValue & 0x0000000f;
	tens   = (readValue & 0x000000f0) >>4;
	distance_front = tens*10 + ones;


	readValue = HCSR_04_IP_mReadReg(0x43C40000, HCSR_04_IP_S00_AXI_SLV_REG2_OFFSET);
	while(readValue == 0){
		readValue = HCSR_04_IP_mReadReg(0x43C40000, HCSR_04_IP_S00_AXI_SLV_REG2_OFFSET);
	}
	ones  = readValue & 0x0000000f;
	tens   = (readValue & 0x000000f0) >>4;
	distance_left = tens*10 + ones;

}

void searchingNN(){
	searchingNN_in[0] = state[0];
	searchingNN_in[1] = state[1];
	searchingNN_in[2] = state[2];

	searchingNN_control[0] |=0x1;
	while((searchingNN_control[0]&0x2) != 0x2);

	printf("%f %f %f \n", searchingNN_out[0],searchingNN_out[1],searchingNN_out[2]);
	if(searchingNN_out[0] > searchingNN_out[1] && searchingNN_out[0] > searchingNN_out[2]){
		printf("forward\n");
		forward();
		parking_lot();
		stop();
	}
	else if(searchingNN_out[1] > searchingNN_out[0] && searchingNN_out[1] > searchingNN_out[2]){
		printf("left\n");
		turnLeft();
		parking_lot();
		stop();
	}
	else{
		printf("right\n");
		turnRight();
		parking_lot();
		stop();
	}
}

void parkingNN(){
	parkingNN_in[0] = state[0];
	parkingNN_in[1] = state[1];
	parkingNN_in[2] = state[2];

	parkingNN_control[0] |=0x1;
	while((parkingNN_control[0]&0x2) != 0x2);

	printf("%f %f %f %f\n", parkingNN_out[0],parkingNN_out[1],parkingNN_out[2],parkingNN_out[3]);
	if(parkingNN_out[0] > parkingNN_out[1] && parkingNN_out[0] > parkingNN_out[2] && parkingNN_out[0] > parkingNN_out[3]){
		printf("forward\n");
		forward();
		parking_lot();
		stop();
	}
	else if(parkingNN_out[1] > parkingNN_out[0] && parkingNN_out[1] > parkingNN_out[2] && parkingNN_out[1] > parkingNN_out[3]){
		printf("left\n");
		turnLeft();
		parking_lot();
		stop();
	}
	else if(parkingNN_out[2] > parkingNN_out[0] && parkingNN_out[2] > parkingNN_out[1] && parkingNN_out[2] > parkingNN_out[3]){
		printf("right\n");
		turnRight();
		parking_lot();
		stop();
	}
	else{
		printf("stop\n");
		parking_is_done=1;
		stop();
	}
}



int main()
{
    init_platform();
    print("AI CAR ENABLED\n\r");
    stop();
    parking_lot_detected = 0;
    stop();
    sleep(30); //time to put the vehicle in the parking environment after the program is installed

    while(parking_is_done == 0){
		distance_left_avg = 0;
		distance_front_avg = 0;
		distance_right_avg = 0;
    	for(int j = 0; j < 100; j++){ //measuring sensor values ​​100 times
        	readSensors();
    		distance_left_avg += (float)distance_left /100;
    		distance_front_avg += (float)distance_front /100;
    		distance_right_avg += (float)distance_right /100;
    	}
    	if(parking_lot_detected == 1){
    		state[0]=(distance_left_avg)/180;
			state[1]=(distance_front_avg)/180;
			state[2]=(distance_right_avg)/180;
    	}
    	else{
        	state[0]=(distance_left_avg-2)/180;
        	state[1]=(distance_front_avg-2)/180;
        	state[2]=(distance_right_avg-2)/180;
    	}
    	printf("distance left: %d  distance front: %d  distance right: %d \n", distance_left,distance_front,distance_right);

    	if(parking_lot_detected == 1)
    		parkingNN();
    	else
    		searchingNN();
    }

    cleanup_platform();
    return 0;
}
