Team number: xohw20_189

Project name: ELON: Autonomous Parking via Deep Q Learning: A SoC Solution

Date: 30.06.2020

Version of uploaded archive: 1

University name: Eskişehir Technical University

Supervisor name: Asst. Prof. İsmail SAN

Supervisor e-mail: isan@eskisehir.edu.tr

Participant(s): Alican ÖZELOĞLU

Email: alicanozeloglu@gmail.com

Participant(s): İsmihan Gül GÜRBÜZ

Email: ismihanglgrbz@gmail.com

Board used: ZedBoard Zynq-7000

Software Version: Vivado 2017.4, Vivado HLS 2017.4

Brief description of project:In this project, the vehicle that can detect and park the parking area was implemented with the deep q learning method.
Trained neural networks have been accelerated on hardware design. SoC architecture tested on prototype model car.

Link to project repository: https://github.com/AlicanOzeloglu/ELON-Autonomous-Parking

Description of archive (explain directory structure, documents and source files):

deep_q_learning_with_python --> This file includes Python3 codes for deep q learning part of our project.
ip --> This file includes IP files and IP source files to create IPs which were used in project.
src --> This file includes C, VHDL and ardunio code that we used in the project.
block_diagram.pdf --> Block diagram of our project.
source_hierarchy.PNG --> Source hierarchy of the SoC design.
Prototype_car --> A picture of our prototype car.
ELON_Project_Report --> Report of our project.


Instructions to build and test project


######  Creating IP with HLS ######

Open Vivado HLS 2017.4
Create New Project
Name of the top function should be "SearchingNN" for seaching neural network IP.
				   "ParkingNN" for parkingneural network IP.
Right click on Source and click add files.
Select student_xohw20_189_ismailsan_20200630_1/ip/HLS/SearchingNN_ip for searching neural network.
       student_xohw20_189_ismailsan_20200630_1/ip/HLS/ParkingNN_ip for parking neural network.
Click C synthesis.
When synthesis is finished, click Export RTL.


######  Creating SoC Design with All Components  ######
Open Vivado 2017.4
Create RTL Project
Choose ZedBoard Development Kit as destination board
Create block design
Add ip --> zynq processing system
Add ip --> clock wizard
Add source --> Add or create design source --> Add files --> student_xohw20_189_ismailsan_20200630_1/src/vhdl --> select all files --> click OK and Finish
In Source window, Design Sources --> right click on ov7670_controller, ov7670_capture, debounce and click add module to block design
Click Window --> Add ip catalog --> click right click on list --> select student_xohw20_189_ismailsan_20200630_1/ip --> click OK
Click Window --> Add ip catalog --> select ip files which you created with HLS
Click Add ip --> select 3 hcsr_04_ip_v1.0 , select motor_ip_v1.0, capture_to_proc_v1.0, SearchingNN_0, ParkingNN_0
Make neccessary connections as seen in student_xohw20_189_ismailsan_20200630_1/block_diagram.pdf, make sure the connections are exactly the same with block_diagram.pdf
Make sure that your souce hierarchy is same as student_xohw20_189_ismailsan_20200630_1/source_hierarchy
Click Generate Bitstream
Click Add Sources --> Add or create constraints --> Add file --> select student_xohw20_189_ismailsan_20200630_1/src/vhdl/ SocXilinxPin.xdc --> Finish
Right click on design file and click Create HDL Wrapper.
Right click on design and click Generate Output Products.
Click on Generate Bitstream.
When generate bitstream finished, export hardware (include bitstream should be marked) and launch SDK.
Create new Hello World application project in SDK.
Replace the contents of the Hello world project with student_xohw20_189_ismailsan_20200630_1/src/c/helloworld.c
Ready to run.

########################
Link to YouTube Video(s): https://www.youtube.com/watch?v=sdin0O2WmTE
########################
