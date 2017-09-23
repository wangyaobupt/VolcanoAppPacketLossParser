import re

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
      