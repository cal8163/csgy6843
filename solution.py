from socket import *
import os
import sys
import struct
import time
import select
import binascii
import ipaddress
import socket


ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise


def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0


    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2


    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff


    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.
    myID = os.getpid() & 0xFFFF  # Return the current process i
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)

    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.


    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end


    # So the function ending should look like this


    packet = header + data
    return packet


def get_route(hostname):
    timeLeft = TIMEOUT

    tracelist1 = [] #This is your list to use when iterating through each trace 
    tracelist2 = [] #This is your list to contain all traces
    reachedtheend = 0


    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)


            #Fill in start
            # Make a raw socket named mySocket
            icmp = getprotobyname("icmp")
            mySocket = socket.socket(AF_INET, SOCK_RAW, icmp)
            #Fill in end


            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)

            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    tracelist1.append(ttl)
                    tracelist1.append("* * * Request timed out.")
                    tracelist2.append(tracelist1)
                    print(tracelist1)
                    tracelist1.clear()
                    #Fill in start

                    #You should add the list above to your all traces list
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    tracelist1.append(ttl)
                    tracelist1.append("* * * Request timed out.")
                    tracelist2.append(tracelist1)
                    print(tracelist1)
                    tracelist1.clear()
                    #Fill in start

                    #You should add the list above to your all traces list
                    #Fill in end
            except timeout:
                continue


            else:
                #Fill in start

                ICMPheader = recvPacket[20:28]
                #Fetch the ICMP header from the IP packet
                types, code, myChecksum, ID, Sequence = struct.unpack("bbHHh", ICMPheader)
                IPheader = recvPacket[:20]
                ip_version, ip_type, ip_length, ip_id, ip_flags, ip_ttl, ipprotocl, ip_checksum, srce_ip, dest_ip \
                    = struct.unpack("!BBHHHBBHII", IPheader)
                ipsource= str(ipaddress.IPv4Address(srce_ip))
                #Fetch the icmp type from the IP packet
                #Fill in end
                try: #try to fetch the hostname
                    #Fill in start
                    hostip = socket.gethostbyaddr(ipsource)[0]


                    #Fill in end
                except herror:   #if the host does not provide a hostname
                    #Fill in start
                    hostip = "hostname not returnable."

                    #Fill in end


                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 +
                    bytes])[0]
                    #Fill in start
                    tracelist1.append(ttl)
                    rtt = (str(howLongInSelect*1000)+"ms")
                    tracelist1.append(rtt)
                    tracelist1.append(ipsource)
                    tracelist1.append(hostip)
                    tracelist2.append(tracelist1)
                    #print(tracelist1)
                    tracelist1.clear()

                    #You should add your responses to your lists here
                    #Fill in end
                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    tracelist1.append(ttl)
                    rtt = (str(howLongInSelect*1000)+"ms")
                    tracelist1.append(rtt)
                    tracelist1.append(ipsource)
                    tracelist1.append(hostip)
                    tracelist2.append(tracelist1)
                    tracelist1.clear()
                    #Fill in start

                    #You should add your responses to your lists here 
                    #Fill in end
                elif types == 0:
                    if reachedtheend == 0:
                        bytes = struct.calcsize("d")
                        timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]

                        #Fill in start
                        tracelist1.append(ttl)
                        rtt = (str(howLongInSelect*1000)+"ms")
                        tracelist1.append(rtt)
                        tracelist1.append(ipsource)
                        tracelist1.append(hostip)
                        tracelist2.append(tracelist1)
                        #print(tracelist1)
                        tracelist1.clear()
                        reachedtheend = 1
                        # Fill in start

                    #You should add your responses to your lists here and return your list if your destination IP is met
                    #Fill in end
                else:
                    #Fill in start
                    break
                    #If there is an exception/error to your if statements, you should append that to your list here
                    #Fill in end

            finally:
                mySocket.close()
                return tracelist2

if __name__ == '__main__':
   get_route("google.com")