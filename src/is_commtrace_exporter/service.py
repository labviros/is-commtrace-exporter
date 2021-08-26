from opencensus.ext.zipkin.trace_exporter import ZipkinExporter
from opencensus.common.transports.async_ import AsyncTransport
from datetime import datetime, timezone
from .Tracer import Tracer
from .TextFormatPropagator import TextFormatPropagator as tfp
import socket
import sys
import json

def publish_tracer(exporter,received_message=None):
    if received_message is not None:
        received_message = received_message.decode('utf-8')
        json_rcvd_message = json.loads(received_message)
        spanname = "commtime_{}".format(json_rcvd_message['spanname'])
        del json_rcvd_message['spanname']
        tmstmp_send = datetime.utcfromtimestamp(int(json_rcvd_message['timestamp_send'])/1000000.0).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        del json_rcvd_message['timestamp_send']
        tmstmp_rcvd = datetime.utcfromtimestamp(int(json_rcvd_message['timestamp_rcvd'])/1000000.0).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        del json_rcvd_message['timestamp_rcvd']
        timestamps = (tmstmp_send,tmstmp_rcvd)
        spctxt = tfp.from_carrier(json_rcvd_message)
        tracer = Tracer(exporter,spctxt)
        with tracer.span(name=spanname,timestamps=timestamps) as tspan:
            pass
        tc_span_context = tfp.new_span_context(
            trace_id=tspan.context_tracer.trace_id,
            span_id=tspan.span_id,
        )
        carrierString = "{ \"x-b3-flags\": \"0\", \"x-b3-parentspanid\": \"0\", \"x-b3-sampled\": \"0\", \"x-b3-spanid\": \"0\", \"x-b3-traceid\": \"0\" }"
        carrierString = json.loads(carrierString)
        carrierString = tfp.to_carrier(tc_span_context, carrierString)
        returnString = json.dumps(carrierString)
        print(returnString)
        return returnString.encode('latin1')



def main():

    config_file = sys.argv[1] if len(sys.argv) > 1 else '../../etc/conf/config.json'
    config = json.load(open(config_file, 'r'))

    exporter = ZipkinExporter(
        service_name=config["service_name"],
        host_name=config["zipkin_host"], 
        port=config["zipkin_port"],
        transport=AsyncTransport,
        )

    localIP     = ''
    localPort   = config["commtrace_exporter"]["port"]
    bufferSize  = config["commtrace_exporter"]["buffer_size"]
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")
    while(True):
        print("Waiting for Metadata")
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        received_message = bytesAddressPair[0]
        sender_address = bytesAddressPair[1]
        infoToReturn = publish_tracer(exporter,received_message)
        UDPServerSocket.sendto(infoToReturn, sender_address)

if __name__ == '__main__':
    main()
