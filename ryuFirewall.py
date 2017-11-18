#!/usr/bin/bash/env python

#Name: Rishikesh Adusumilli

from flask import Flask, render_template, Markup, request
from flask.helpers import send_file
import os,httplib,json,subprocess

count=1

############################ Module for cURL #######################

def post(cIP,userInput,configType):
    output=apiInt(cIP,userInput,configType,"POST")
    return output

def delete(cIP,userInput,configType):
    output=apiInt(cIP,userInput,configType,"DELETE")
    return output

def apiInt(cIP,userInput,configType,method):
    if(configType.lower()=="static"):
        path="/wm/staticflowpusher/json"
    elif(configType=="ryuFirewall"):
        path="/stats/flowentry/add"

    headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
    }
    userInput = json.dumps(userInput)
    conn = httplib.HTTPConnection(cIP, 8080)
    conn.request(method,path,userInput,headers)
    response = conn.getresponse()
    output = (response.status, response.reason, response.read())
    #print output
    conn.close()
    return output


############################ Module for Flask #######################

app = Flask(__name__)

#Function for index page
@app.route('/')
def startPage():
    bodyText=Markup("<b>SDN Topology Configuration -  User Input</b>")
    return render_template('index.html', bodyText=bodyText)

#page after action performed
@app.route('/actionStatus')
def actionStatus():
    return render_template("actionStatus.html")

#Function for static flow entries
@app.route('/form1')
def form1():
    return render_template("form1.html")

#Function for firewall flow entries
@app.route('/form2')
def form2():
    response=subprocess.check_output(["curl","-X","DELETE","http://192.168.56.101:8080/stats/flowentry/clear/1"], stderr=subprocess.STDOUT, universal_newlines=True)
    response1=subprocess.check_output(["curl","-X","DELETE","http://192.168.56.101:8080/stats/flowentry/clear/2"], stderr=subprocess.STDOUT, universal_newlines=True)
    print(response)
    print(response1)
    return render_template("form2.html")

###############Function to record user input of static flow entries
@app.route('/recordUserInput1', methods=['POST'])
def recordUserInput1():
    DPID1=request.form['DPID1']
    priority1=request.form['priority1']
    inPort1=request.form['inPort1']
    ethType1=request.form['ethType1']
    destIP1=request.form['destIP1']
    action1=request.form['action1']

    DPID2=request.form['DPID2']
    priority2=request.form['priority2']
    inPort2=request.form['inPort2']
    ethType2=request.form['ethType2']
    destIP2=request.form['destIP2']
    action2=request.form['action2']

    if(ethType1=="0x0800"):
        flowStaticARP = {
            "dpid":DPID1,
            "priority":priority1,
            "match":{
                "eth_type":"0x0806",
            },
            "actions":[
                { 
                    "type":"OUTPUT",
                    "port":"FLOOD"
                }
              ]
            }

        print(post("192.168.56.101",flowStaticARP,"ryuFirewall"))

        if(DPID1==DPID2):
                flowStatic = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":inPort1,
                        "ipv4_dst":destIP1,
                        "eth_type":ethType1,
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":action1
                        }
                      ]
                    }

        else:
                flowStatic = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":inPort1,
                        "ipv4_dst":destIP1,
                        "eth_type":ethType1,
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":action1
                        }
                      ]
                    }

                flowStaticReverse = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":action1,
                        "ipv4_dst":destIP2,
                        "eth_type":ethType1,
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort1
                        }
                      ]
                    }
        print(post("192.168.56.101",flowStaticReverse,"ryuFirewall"))

        print(post("192.168.56.101",flowStatic,"ryuFirewall"))

    elif(ethType1=="0x0806"):
        flowStaticARP = {
            "dpid":DPID1,
            "priority":priority1,
            "match":{
                "eth_type":ethType1,
            },
            "actions":[
                {
                    "type":"OUTPUT",
                    "port":action1
                }
              ]
            }

        print(post("192.168.56.101",flowStaticARP,"ryuFirewall"))

    if(ethType2=="0x0800"):
        flowStaticARP = {
            "dpid":DPID2,
            "priority":priority2,
            "match":{
                "eth_type":"0x0806",
            },
            "actions":[
                {
                    "type":"OUTPUT",
                    "port":"FLOOD"
                }
              ]
            }

        print(post("192.168.56.101",flowStaticARP,"ryuFirewall"))

        if(DPID1==DPID2):
                flowStatic = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":inPort2,
                        "ipv4_dst":destIP2,
                        "eth_type":ethType2,
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":action2
                        }
                      ]
                    }

        else:
                flowStatic = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":inPort2,
                        "ipv4_dst":destIP2,
                        "eth_type":ethType2,
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":action2
                        }
                      ]
                    }
                flowStaticReverse = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":action2,
                        "ipv4_dst":destIP1,
                        "eth_type":ethType2,
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort2
                        }
                      ]
                    }
        print(post("192.168.56.101",flowStaticReverse,"ryuFirewall"))

        print(post("192.168.56.101",flowStatic,"ryuFirewall"))

    elif(ethType2=="0x0806"):
        flowStaticARP = {
            "dpid":DPID2,
            "priority":priority2,
            "match":{
                "eth_type":ethType2,
            },
            "actions":[
                {
                    "type":"OUTPUT",
                    "port":action2
                }
              ]
            }

        print(post("192.168.56.101",flowStaticARP,"ryuFirewall"))

    return actionStatus()

##############Function to record user input of firewall flow entries
@app.route('/recordUserInput2', methods=['POST'])
def recordUserInput2():
    DPID1=request.form['DPID1']
    priority1=request.form['priority1']
    inPort1=request.form['inPort1']
    ethType1=request.form['ethType1']
    srcIP1=request.form['srcIP1']
    destIP1=request.form['destIP1']
    l4Protocol1=request.form['l4Protocol1'].upper()

    DPID2=request.form['DPID2']
    priority2=request.form['priority2']
    inPort2=request.form['inPort2']
    ethType2=request.form['ethType2']
    srcIP2=request.form['srcIP2']
    destIP2=request.form['destIP2']
    l4Protocol2=request.form['l4Protocol2'].upper()

    global count

    if((ethType1=="")and((l4Protocol2=="ICMP")or(l4Protocol2=="TCP")or(l4Protocol2=="UDP"))):
        flowStaticARP = {
            "dpid":DPID1,
            "priority":priority1,
            "match":{
                "eth_type":"0x0806",
            },
            "actions":[
                { 
                    "type":"OUTPUT",
                    "port":"FLOOD"
                }
              ]
            }

        print(post("192.168.56.101",flowStaticARP,"ryuFirewall"))

        if(DPID1==DPID2):
            if(l4Protocol1=="UDP"):
                flowStatic = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":inPort1,
                        "ipv4_src":srcIP1,
                        "ipv4_dst":destIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x11",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort2
                        }
                      ]
                    }
            elif(l4Protocol1=="TCP"):
                flowStatic = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":inPort1,
                        "ipv4_src":srcIP1,
                        "ipv4_dst":destIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x06",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort2
                        }
                      ]
                    }
            elif(l4Protocol1=="ICMP"):
                flowStatic = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":inPort1,
                        "ipv4_src":srcIP1,
                        "ipv4_dst":destIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x1",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort2
                        }
                      ]
                    }

        else:
            if(l4Protocol1=="UDP"):
                flowStatic = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":inPort1,
                        "ipv4_src":srcIP1,
                        "ipv4_dst":destIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x11",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":3
                        }
                      ]
                    }
            elif(l4Protocol1=="TCP"):
                flowStatic = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":inPort1,
                        "ipv4_src":srcIP1,
                        "ipv4_dst":destIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x06",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":3
                        }
                      ]
                    }
            elif(l4Protocol1=="ICMP"):
                flowStatic = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":inPort1,
                        "ipv4_src":srcIP1,
                        "ipv4_dst":destIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x1",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":3
                        }
                      ]
                    }

            if(l4Protocol1=="UDP"):
                flowStaticReverse = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":3,
                        "ipv4_src":destIP1,
                        "ipv4_dst":srcIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x11",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort1
                        }
                      ]
                    }
            elif(l4Protocol1=="TCP"):
                flowStaticReverse = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":3,
                        "ipv4_src":destIP1,
                        "ipv4_dst":srcIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x06",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort1
                        }
                      ]
                    }
            elif(l4Protocol1=="ICMP"):
                flowStaticReverse = {
                    "dpid":DPID1,
                    "priority":priority1,
                    "match":{
                        "in_port":3,
                        "ipv4_src":destIP1,
                        "ipv4_dst":srcIP1,
                        "eth_type":"0x0800",
                        "ip_proto":"0x1",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort1
                        }
                      ]
                    }
            print(post("192.168.56.101",flowStaticReverse,"ryuFirewall"))

        print(post("192.168.56.101",flowStatic,"ryuFirewall"))

    elif((ethType1=="0x0806")and(l4Protocol2=="")):
        flowStaticARP = {
            "dpid":DPID1,
            "priority":priority1,
            "match":{
                "eth_type":"0x0806",
            },
            "actions":[
                {
                    "type":"OUTPUT",
                    "port":"FLOOD"
                }
              ]
            }

        print(post("192.168.56.101",flowStaticARP,"ryuFirewall"))

    if((ethType2=="")and((l4Protocol2=="ICMP")or(l4Protocol2=="UDP")or(l4Protocol2=="TCP"))):
        flowStaticARP = {
            "dpid":DPID2,
            "priority":priority2,
            "match":{
                "eth_type":"0x0806",
            },
            "actions":[
                {
                    "type":"OUTPUT",
                    "port":"FLOOD"
                }
              ]
            }

        print(post("192.168.56.101",flowStaticARP,"ryuFirewall"))

        if(DPID1==DPID2):
            if(l4Protocol1=="UDP"):
                flowStatic = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":inPort2,
                        "ipv4_src":srcIP2,
                        "ipv4_dst":destIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x11",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort1
                        }
                      ]
                    }
            elif(l4Protocol1=="TCP"):
                flowStatic = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":inPort2,
                        "ipv4_src":srcIP2,
                        "ipv4_dst":destIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x06",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort1
                        }
                      ]
                    }
            elif(l4Protocol1=="ICMP"):
                flowStatic = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":inPort2,
                        "ipv4_src":srcIP2,
                        "ipv4_dst":destIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x1",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort1
                        }
                      ]
                    }

        else:
            if(l4Protocol1=="UDP"):
                flowStatic = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":inPort2,
                        "ipv4_src":srcIP2,
                        "ipv4_dst":destIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x11",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":3
                        }
                      ]
                    }
            elif(l4Protocol1=="TCP"):
                flowStatic = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":inPort2,
                        "ipv4_src":srcIP2,
                        "ipv4_dst":destIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x06",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":3
                        }
                      ]
                    }
            elif(l4Protocol1=="ICMP"):
                flowStatic = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":inPort2,
                        "ipv4_src":srcIP2,
                        "ipv4_dst":destIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x1",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":3
                        }
                      ]
                    }

            if(l4Protocol1=="UDP"):
                flowStaticReverse = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":3,
                        "ipv4_src":destIP2,
                        "ipv4_dst":srcIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x11",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort2
                        }
                      ]
                    }
            elif(l4Protocol1=="TCP"):
                flowStaticReverse = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":3,
                        "ipv4_src":destIP2,
                        "ipv4_dst":srcIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x06",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort2
                        }
                      ]
                    }
            elif(l4Protocol1=="ICMP"):
                flowStaticReverse = {
                    "dpid":DPID2,
                    "priority":priority2,
                    "match":{
                        "in_port":3,
                        "ipv4_src":destIP2,
                        "ipv4_dst":srcIP2,
                        "eth_type":"0x0800",
                        "ip_proto":"0x1",
                    },
                    "actions":[
                        { 
                            "type":"OUTPUT",
                            "port":inPort2
                        }
                      ]
                    }
            print(post("192.168.56.101",flowStaticReverse,"ryuFirewall"))

        print(post("192.168.56.101",flowStatic,"ryuFirewall"))

    elif((ethType2=="0x0806")and(l4Protocol2=="")):
        flowStaticARP = {
            "dpid":DPID2,
            "priority":priority2,
            "match":{
                "eth_type":"0x0806",
            },
            "actions":[
                {
                    "type":"OUTPUT",
                    "port":"FLOOD"
                }
              ]
            }

        print(post("192.168.56.101",flowStaticARP,"ryuFirewall"))

    return actionStatus()

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8888)
