import re

# readBLESeqListFromFile
# read sequence number of each BLE packet from log, which is in format of "ff:ff:ff:01:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx"
# the return value is a list, each element of this list is a tuple. Tuple contains 3 elements:
# 1. BLE packet sequence str, e.g. '01' 
# 2. line number: in which line this packet is located 
# 3. packet number: count the sequence number of this packet, starting from 1
def readBLESeqListFromFile(filename):
  regex = re.compile(r'(?<=ff:ff:ff:)[0-9a-c]{1}[0-9a-f]{1}')
  linecnt=0
  packetCount = 0
  seqList = []
  with open(filename) as f:
    for line in f.readlines():
      #print line
      linecnt = linecnt+1
      matchResult = regex.findall(line)
      if matchResult:        
        for seqStr in matchResult:
          packetCount = packetCount +1
          seqList.append((seqStr, linecnt, packetCount))
          #print seqList[-1]
      
  return seqList

# detect loss
# 'loss' is defined as: if seq1 + 1 != seq2, a loss is detected.
# Exceptional case: the BLE packet sequence number counts from 1 to 200. If seq1 = 200, seq2 = 1, there is no loss.
def scanPacketLossFromPacketList(seqList):
  packetLossList = []
  for idx in range(len(seqList)-1):
    inc = int(seqList[idx+1][0], 16) - int(seqList[idx][0], 16)
    if inc > 1 or (inc < 0 and inc !=-199):
      packetLossList.append((inc-1, seqList[idx], seqList[idx+1]))
  
  return packetLossList

if __name__ == '__main__':
  filenameList = [unicode("LU_.txt","utf8"), unicode("LD_.txt","utf8"), unicode("RU_.txt","utf8"), unicode("RD_.txt","utf8")]
  for filename in filenameList:
    seq_list = readBLESeqListFromFile(filename)
    packetLossList = scanPacketLossFromPacketList(seq_list)
    if packetLossList:
      print "In %s, the packet loss status are as below, in format (numberOfLossPacket, (packetSeqBeforeLoss, linenumberInLogfile, packetNumberInLogFile)): " % filename
      print packetLossList
    else:
      print "In %s, there is no packet loss."%filename
      