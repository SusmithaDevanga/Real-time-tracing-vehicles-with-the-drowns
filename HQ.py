import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import json



rev_uav=[]
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker HQ")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed Return Code : ",rc)
        
        
#to store the vehicle numbers that our UAVs tracing for that time stamps        
to_dic={'1':'','2':'','3':'','4':'','5':'','6':''}


def on_message(client, userdata, message):
    #storing into the index 'X' of dictionary when HQ receive message from UAV 'X'
    global to_dic
    print("\nMessage Received is : " + str(message.payload))
    print("Message Received on Topic " + str(message.topic))
    rec_uavstr= str(message.topic)
    rec_uavid = int(rec_uavstr[-1])
    if (rec_uavid==1):
       to_dic['1']=  (str(message.payload))[2:3]
    elif rec_uavid==2:
       to_dic['2']=  (str(message.payload))[2:3]
    elif rec_uavid==3:
       to_dic['3']=  (str(message.payload))[2:3]
    elif rec_uavid==4:
       to_dic['4']=  (str(message.payload))[2:3]
    elif rec_uavid==5:
       to_dic['5']=  (str(message.payload))[2:3]
    elif rec_uavid==6:
       to_dic['6']=  (str(message.payload))[2:3]
   # print(str(to_dic))
   

    
    
    

#accessing vehicle_location.txt file and storing values into a list
#each index in list stores each row of the file
file1 = open("vehicle_location.txt","r") 
vehicle_locations= file1.readlines()
#print(vehicle_locations)






Connected = False  # global variable for the state of the connection
client_name="HQ"
broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port

client = mqttClient.Client(client_name)  # create new instance


client.on_connect = on_connect  # attach function to callback

client.connect(host= broker_address, port=port)  # connect to broker
client.on_message = on_message  # attach function to callback


client.loop_start()  # start the loop


while Connected != True:  # Wait for connection
    time.sleep(0.1)
    
#subcribing to all the UAVs    
client.subscribe("vehicletraced/+")    
time.sleep(5)
time_seq=0 #to access each index from vehicle_location list
count=0 #to iterate while loop
curr_loc=0 
new_str="" # the output of each time stamp will be stored in this string
while count< len(vehicle_locations):

        
       
        file2= open("output.txt", "a")
        to_list= list(to_dic.values())
        for x in range(0,6):
            new_str= new_str+str(to_list[x])+" "
            #extracting traced vehicle number from to_list and concatinating to this string
        if count!=0:  
            file2.write(new_str)
            file2.write("\n")
        file2.close()
        new_str="" # empyting the output string i.e."new_str" after appending to the file "output.txt"


        to_dic['1']=''
        to_dic['2']=''
        to_dic['3']=''
        to_dic['4']=''
        to_dic['5']=''
        to_dic['6']=''
        
        curr_loc=vehicle_locations[time_seq]
        #taking values of one time stamp each time
        #publishing the vehicle locatioins of particular time stamp
        print('\n\npublishing the locations of vehicles at timestamp ',(time_seq-1))
        client.publish("location/HQ",curr_loc)
        time_seq+=1
        count=count+1
        time.sleep(10)

    
    
#to write the last results which were not able to write in the while loop    
file2= open("output.txt", "a")
        
#to extract values
to_list= list(to_dic.values())
for x in range(0,6):
    new_str= new_str+str(to_list[x])+" "

file2.write(new_str)
file2.write("\n")
file2.close()
new_str=""


print("exiting")
client.disconnect()
client.loop_stop()
time.sleep(100)