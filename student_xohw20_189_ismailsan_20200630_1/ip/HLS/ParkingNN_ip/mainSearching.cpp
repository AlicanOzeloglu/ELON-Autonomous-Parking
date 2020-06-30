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
float Layer2_neurons[24];
float Layer3_neurons[48];
float Layer4_neurons[24];
//float out[3];
float sum;
void SearchingNN(float inp[3], float out[3]){
#pragma HLS INTERFACE s_axilite port=inp bundle=neuronAXI
#pragma HLS INTERFACE s_axilite port=out bundle=neuronAXI
#pragma HLS INTERFACE s_axilite port=return bundle=neuronAXI

#pragma HLS ARRAY_RESHAPE variable=inp_local complete dim=1
#pragma HLS ARRAY_RESHAPE variable=Layer4_neurons block factor=4 dim=1
	int i, j;

	inp_local[0] = inp[0];
	inp_local[1] = inp[1];
	inp_local[2] = inp[2];

	for(i = 0 ; i < 24 ; i++){
#pragma HLS PIPELINE II=1
		sum = 0;
		for(j = 0 ; j < 3 ; j++)
			sum += inp_local[j] * Layer2_weights[i][j];
		Layer2_neurons[i] = (sum + Layer2_bias[i]) > 0 ? (sum + Layer2_bias[i]) : 0;
	}

	for(i = 0 ; i < 48 ; i++){
#pragma HLS PIPELINE II=2
		sum = 0;
		for(j = 0 ; j < 24 ; j++)
			sum += Layer2_neurons[j] * Layer3_weights[i][j];
		Layer3_neurons[i] = (sum + Layer3_bias[i]) > 0 ? (sum + Layer3_bias[i]) : 0;
	}

	for(i = 0 ; i < 24 ; i++){
#pragma HLS PIPELINE II=4
		sum = 0;
		for(j = 0 ; j < 48 ; j++)
			sum += Layer3_neurons[j] * Layer4_weights[i][j];
		Layer4_neurons[i] = (sum + Layer4_bias[i]) > 0 ? (sum + Layer4_bias[i]) : 0;
	}

	for(i = 0 ; i < 3 ; i++){
#pragma HLS PIPELINE II=1
		sum = 0;
		for(j = 0 ; j < 24 ; j++)
			sum += Layer4_neurons[j] * Layer5_weights[i][j];
		out[i] = sum + Layer5_bias[i];
	}


}








