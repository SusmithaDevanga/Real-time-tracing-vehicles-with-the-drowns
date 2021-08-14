**************** This code has been done in Windows OS******************
Requirements:
1. HiveMQ - it is MQTT broker (Downlad: https://www.hivemq.com/downloads/hivemq/)
2. python3
3. Mosquitto library (pip install paho-mqtt)


step3: make sure below files are in the same direcctory/folder
	HQ.py
	UAV.py
	uav1.txt
	uav2.txt
	uav3.txt
	uav4.txt
	uav5.txt
	uav6.txt
	vehicle_location.txt
	output.txt
	assign.ps1

step4: 

step4: Open and run the hivemq broker in the browser 
	a. Open the hivemq-4.2.2 folder and open bin folder and run the run.bat file as administrator.
	b. Open browser and type localhost:8080
	c. username- admin
	   password- hivemq

step5: Run the windows powershell in administrator mode 
step6: Go to the particular directory where step3 files are stored. 
step7: and run assign.ps1 by the command ".\assign.ps1"


step8: After all those instances gets completed, please check the output.txt file
step9: Kindly do the step7 again if the output.txt contains any blanks, reason might be any uav instance not opened on time or stuck
          in between due to various reasons.

step10: We can check the connected devices and all other details in the hivemq broker in the browser.
step11: We can check the working of each instace (eg: uav3) in those respective powershells for few minutes even after it is done
	(i.e. after 120 sec according to this given input) with its operations. Otherwise can close them. 
step12: Thank you.