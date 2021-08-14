import paho.mqtt.client as mqttClient
import time
import random
import math
import sys
import json

all_uavs=[]
for i in range(1,7):
    all_uavs.append('uav'+str(i))
    
    
completed_veh_ids=[] #to store the vehicle numbers/ids which are already tracing by other 
#vehicles for that time stamp
global distance_list #to store distance b/w this uav and all vehicles for that time stamp
distance_list=[]


count=0
def distance(curr,to):  #to calculate distance b/w this uav and particular vehicle
    #print('curr uav loc is',curr)
    #print('comparing with', to,'\n')
    return math.sqrt((to['x']-curr['x'])**2+(to['y']-curr['y'])**2)



def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker",client_name)
            global Connected  # Use global variable
            Connected = True  # Signal connection
        else:
           print("Connection failed and returned",rc)
           
           
           
           
           
global curr_uav_loc #to store this uav loaction for the respective time stamp
global into_rows         
def supply_loc(count): #to get the location of this uav for the particular time stamp
    global into_rows
    if pre_client==1:
        curr_uav_loc = open("uav1.txt","r") 
        into_rows= curr_uav_loc.readlines()
        with_spaces= into_rows[count].split()
        curr= {'x':int(with_spaces[0]),'y':int(with_spaces[1])}

    elif pre_client==2:
        curr_uav_loc = open("uav2.txt","r") 
        into_rows= curr_uav_loc.readlines()
        with_spaces= into_rows[count].split()
        curr= {'x':int(with_spaces[0]),'y':int(with_spaces[1])}

    elif pre_client==3:
        curr_uav_loc = open("uav3.txt","r") 
        into_rows= curr_uav_loc.readlines()
        with_spaces= into_rows[count].split()
        curr= {'x':int(with_spaces[0]),'y':int(with_spaces[1])}

    elif pre_client==4:
        curr_uav_loc = open("uav4.txt","r") 
        into_rows= curr_uav_loc.readlines()
        with_spaces= into_rows[count].split()
        curr= {'x':int(with_spaces[0]),'y':int(with_spaces[1])}
        
    elif pre_client==5:
        curr_uav_loc = open("uav5.txt","r") 
        into_rows= curr_uav_loc.readlines()
        with_spaces= into_rows[count].split()
        curr= {'x':int(with_spaces[0]),'y':int(with_spaces[1])}

    elif pre_client==6:
        curr_uav_loc = open("uav6.txt","r") 
        into_rows= curr_uav_loc.readlines()
        with_spaces= into_rows[count].split()
        curr= {'x':int(with_spaces[0]),'y':int(with_spaces[1])}
    return curr

def cal_min_dis():  #this function will calculate minimum value that is stored in 
#distace_list.....simply gives minimum distance and the vehicle id that is giving that minimum distance
    global min_dist_id #stored vehicle number which has minimum distance with this uav
    global min_dist #store that minimum distance
    global distance_list  
    #print("dist are", distance_list)
    min_dist=10000
    # this for loop calculates that minimum distanced vehicle
    for i in range(0,6):
        if( distance_list[i]<min_dist):
            #print( i )
            min_dist= distance_list[i]
            min_dist_id= i+1
    #print("min dist is ", min_dist," with vehicle is ", min_dist_id)
    
    
    
def check_others(): #this function checks whether any other uav is also tracing the 
#min_dist_id vehicle 
    ret_val=0
    global min_dist_id
    #print("completed are ", completed_veh_ids," here id is ",min_dist_id)
    for i in completed_veh_ids:
        if min_dist_id==i:
            ret_val=1
            return ret_val
    return ret_val 

def next_min(rem):  #If any other uav is tracing the same vehicle then this uav 
# has to trace the next minimum distanced vehicle; this function finds out that 
#next minimum vehicle
    global distance_list
    distance_list[rem-1] =100000
    global min_dist
    min_dist=10000
    global min_dist_id
    for i in range(0,6):
        if(distance_list[i]<min_dist):
            min_dist= distance_list[i]
            min_dist_id=i+1

    




curr=0
min_dist_id=0
def on_message(client, userdata, message):
    #this function will be called whenever this uav code receives a message 
    # from its subscriptions
    #this uav code has been subscribed to 2 kinds of messages that are
    # 1. vehicle locations from HQ.py 
    # 2. the traced vehicle details from other uavs except this own uav
    
    global min_dist_id
    print("\nMessage Received is : " + str(message.payload))
    print("Message Received on Topic " + str(message.topic))
    str_topic= str(message.topic)
    
    #this if process the  type 2 messages
    if(("uav" in str_topic) and int(str_topic[-1])!=int(client_name[-1]) ):
        #print("uav number ", str(message.topic))
        global completed_veh_ids
        # this completed_veh_ids is a list that store the vehicle numbers that are already
        # tracing by other uav for this time stamp
        completed_veh_ids.append((int)((str(message.payload))[2]))
        #print("and it is following ", (int)((str(message.payload))[2]))
        
        
    
    #this elif process the message from HQ.py    
    elif("uav" not in str_topic):
        #this section calculates distance b/w this uav and all vehicles
        # and stores in  distance_list 
        to_list= list((str(message.payload))[2:].split())
        min_dist=10000
        global count
        curr= supply_loc(count)
        count=count+1
            
        for j in range(0,11,2):
           res={'x':int(to_list[j]),'y':int(to_list[j+1])}
           temp= distance(curr,res )
           distance_list.append(temp)
           completed_veh_ids=[]
           

Connected = False
client_name=sys.argv[1]

broker_address = "127.0.0.1"  # Broker address
port = 1883  # Broker port
user = "admin"  # Connection username
password = "hivemq"  # Connection password



print(client_name)
#Task-2 Write code here
# create new instance MQTT client 
client = mqttClient.Client(client_name)  # create new instance


client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback


client.connect(host= broker_address, port=port)  # connect to broker


client.loop_start()  # start the loop

while Connected != True:  # Wait for connection
    time.sleep(0.1)




client.subscribe("location/HQ")
client.subscribe("vehicletraced/+")



pre_client= int(client_name[-1])
 

distance_list
loop_count=0
global into_rows
waste=supply_loc(0) #this is just to calculate number of time stamps that has given
#print('number of rows are ',len(into_rows))


while loop_count< (len(into_rows)+1): #this while loop calculates the minimum
# distance with conflict resolution and publishes the vehicle number that it is
# tracing
    if(loop_count>0): 
        cal_min_dis()  # calculates min distance
        while (check_others()==1): #checking if any other uav is tracing the same vehicle
            next_min(min_dist_id) #if yes then find out next minimum
    print(client_name,' tracing the vehicle ', min_dist_id,'\n')
    
    client.publish("vehicletraced/"+client_name,min_dist_id)
    distance_list=[]
    time.sleep(10)
    loop_count=loop_count+1
    

print(client_name,' tracing the vehicle ', min_dist_id,'\n')
client.publish("vehicletraced/"+client_name,min_dist_id)

print("exiting")
client.disconnect()
client.loop_stop()
time.sleep(100)


    
 
