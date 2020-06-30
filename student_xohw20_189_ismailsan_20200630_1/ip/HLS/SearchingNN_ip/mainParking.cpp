#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include "Layer2_w.h"
#include "Layer3_w.h"
#include "Layer4_w.h"
#include "Layer5_w.h"
#include "Biases.h"

float inp_local[3];
float Layer2_neurons[32];
float Layer3_neurons[64];
float Layer4_neurons[32];
//float out_local[4];
float sum;
//float sump[4];

void ParkingNN(float inp[3], float out[4]){
#pragma HLS INTERFACE s_axilite port=inp bundle=neuronAXI
#pragma HLS INTERFACE s_axilite port=out bundle=neuronAXI
#pragma HLS INTERFACE s_axilite port=return bundle=neuronAXI


//#pragma HLS ARRAY_RESHAPE variable=sump complete dim=1
//#pragma HLS ARRAY_RESHAPE variable=Layer4_neurons complete dim=1
#pragma HLS ARRAY_RESHAPE variable=Layer4_neurons block factor=4 dim=1
	int i, j;
//#pragma HLS ARRAY_RESHAPE variable=inp_local complete dim=1
	inp_local[0] = inp[0];
	inp_local[1] = inp[1];
	inp_local[2] = inp[2];

	for(i = 0 ; i < 32 ; i++){
#pragma HLS PIPELINE II=1
		sum = 0;
		for(j = 0 ; j < 3 ; j++)
			sum += inp[j] * Layer2_weights[i][j];
		Layer2_neurons[i] = (sum + Layer2_bias[i]) > 0 ? (sum + Layer2_bias[i]) : 0;
	}
/*
	for(i = 0 ; i < 32 ; i++){
#pragma HLS unroll
		sump[0]= inp_local[0] * Layer2_weights[i][0];
		sump[1]= inp_local[1] * Layer2_weights[i][1];
		sump[2]= inp_local[2] * Layer2_weights[i][2];
		Layer2_neurons[i] = (sump[0]+sump[1]+sump[2] + Layer2_bias[i]) > 0 ? (sump[0]+sump[1]+sump[2] + Layer2_bias[i]) : 0;
	}*/


	for(i = 0 ; i < 64 ; i++){
#pragma HLS PIPELINE II=2
		sum = 0;
		for(j = 0 ; j < 32 ; j++)
			sum += Layer2_neurons[j] * Layer3_weights[i][j];
		Layer3_neurons[i] = (sum + Layer3_bias[i]) > 0 ? (sum + Layer3_bias[i]) : 0;
	}

	for(i = 0 ; i < 32 ; i++){
#pragma HLS PIPELINE II=4
		sum = 0;
		for(j = 0 ; j < 64 ; j++)
			sum += Layer3_neurons[j] * Layer4_weights[i][j];
		Layer4_neurons[i] = (sum + Layer4_bias[i]) > 0 ? (sum + Layer4_bias[i]) : 0;
	}

	for(i = 0 ; i < 4 ; i++){
#pragma HLS PIPELINE II=1
		sum = 0;
		for(j = 0 ; j < 32 ; j++)
			sum += Layer4_neurons[j] * Layer5_weights[i][j];
		out[i] = sum + Layer5_bias[i];
	}



}


