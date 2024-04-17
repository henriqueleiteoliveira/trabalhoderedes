#Este código foi adaptador usando como referencia o código disponibilizado pelo canal do Youtube Engineering Clinic
from xml.etree import ElementTree as ET
import sys
import matplotlib.pyplot as pylab
et=ET.parse(sys.argv[1])
bitrates=[]
losses=[]
delays=[]
for flow in et.findall("FlowStats/Flow"):
	for tpl in et.findall("Ipv4FlowClassifier/Flow"):
		if tpl.get('flowId')==flow.get('flowId'):
			break
	if tpl.get('destinationPort')=='654':
		continue
	losses.append(int(flow.get('lostPackets')))
	
	rxPackets=int(flow.get('rxPackets'))
	if rxPackets==0:
		bitrates.append(0)
	else:
		t0=float(flow.get('timeFirstRxPacket')[:-2])
		t1=float(flow.get("timeLastRxPacket")[:-2])
		duration=(t1-t0)*1e-9
		try:
			bitrates.append(8*int(flow.get("rxBytes"))/duration*1e-3)
			delays.append(float(flow.get('delaySum')[:-2])*1e-9/rxPackets)
		except Exception as e:
			print(f"t0: {t0} t1:{t1} duration:{duration} rxPackets:{rxPackets}")

pylab.subplot(311)
pylab.hist(bitrates,bins=40)
pylab.xlabel("Fluxo de taxa de bits (b/s)")
pylab.ylabel("Numero de fluxos")


pylab.subplot(312)
pylab.hist(bitrates,bins=40)
pylab.xlabel("Numero de pacotes perdidos")
pylab.ylabel("Numero de fluxos")

pylab.subplot(313)
pylab.hist(bitrates,bins=10)
pylab.xlabel("Atraso em segundos")
pylab.ylabel("Numero de fluxos")

pylab.subplots_adjust(hspace=0.4)
pylab.savefig("results.pdf")
