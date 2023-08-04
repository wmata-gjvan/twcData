#Created by Greg Vanderham for Washington Metropolitan Area Transit Authority
#If you have questions feel free to contact me via Teams or 301-648-4403
from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler
import csv
import os
from colorama import Fore
import json
import copy
import requests

#Grab the station data from the csv
stationstuff = csv.reader(open("stationData.csv"))
htmlTemplate = open('train.html').read()
stationData =[]
for row in stationstuff:
    stationData.append(row)
terminalStations = ["A15", "B11", "E10", "D13", "G05", "F11", "C15", "J03", "K08", "N12"]
files = os.listdir("twcData")
paths = [os.path.join("twcData", basename) for basename in files]
latestFile = max(paths, key=os.path.getctime)
#Use case: glenmont = destination(13)
from flask import Flask, Response
from flask import request
app = Flask(__name__, static_url_path='/static')

print(app.instance_path)
#Flask web application routes
@app.route("/")
def home():
    return open('ui.html')
@app.route("/template")
def returnTemplate():
    return htmlTemplate
@app.route("/filelist")
def returnList():
    return json.dumps(os.listdir("twcData"))
@app.route("/process",methods = ['POST', 'GET'])
def load():
    line = request.args.get('line')
    if line == "ANY":
        line = "*"
    station= request.args.get('station')
    if station == "ANY":
        station = "*"
    destination = request.args.get('destination')

    auto = request.args.get('auto')
    if auto == 'true':
        auto = True
    else:
        auto=False
    printT = request.args.get('print')
    if printT == 'true':
        printT = True
    else:
        printT=False
    track = request.args.get('track')
    file = str(request.args.get('file'))
    data = ""
    data = processData(file, printT, station, line, auto, int(destination), track, "-1", request.args.get('route'))
    if data==None:
        data = "No trains match selected criteria!"
    return data
 



class destination:
    friendlyName = ""
    id = 80
    code = "/"
    #Fake line color, but this also helps us later in the HTML color
    line = "MAGENTA"
    def __init__(self, code):
        self.id = code

        match code:
            case 1:
                self.friendlyName = "Special"
            case 2:
                self.friendlyName = "No Passengers"
            case 3:
                self.friendlyName = "Union Station"
                self.code = "B03"
                self.line = "RED"
            case 4:
                self.friendlyName = "Rhode Island Avenue"
                self.code = "B04"
                self.line = "RED"
            case 5:
                self.friendlyName = "Farragut North"
                self.code = "A02"
                self.line = "RED"
            case 6:
                self.friendlyName = "NoMa Gallaudet U"
                self.code = "B35"
                self.line = "RED"
            case 7:
                self.friendlyName = "Silver Spring"
                self.code = "B08"
                self.line = "RED"
            case 8:
                self.friendlyName = "Van Ness"
                self.code = "A06"
                self.line = "RED"
            case 9:
                self.friendlyName = "Grosvenor-Strathmore"
                self.code = "A11"
                self.line = "RED"
            case 10:
                self.friendlyName = "Medical Center"
                self.code = "A10"
                self.line = "RED"
            case 11:
                self.friendlyName = "Twinbrook"
                self.code =  "A13"
                self.line = "RED"
            case 12:
                self.friendlyName = "Shady Grove"
                self.code = "A15"
                self.line = "RED"
            case 13:
                self.friendlyName = "Glenmont"
                self.code = "B11"
                self.line = "RED"
            case 14:
                self.friendlyName = "Fort Totten"
                self.code = "B06"
                self.line = "RED"
            case 15:
                self.friendlyName = "Brookland-CUA"
                self.code = "B05"
                self.line = "RED"
            case 16:
                self.friendlyName = "Franconia-Springfield"
                self.code = "J03"
                self.line = "BLUE"
            case 17:
                self.friendlyName = "Ballston-MU"
                self.code = "K04"
                self.line = "ORANGE"
            case 18:
                self.friendlyName = "Rosslyn"  
                self.code = "C05"
                self.line = "ORANGE"
            case 19:
                self.friendlyName = "New Carrollton"
                self.code = "D13"
                self.line = "BLUE"
            case 20:
                self.friendlyName = "New Carrollton"
                self.code = "D13"
                self.line = "ORANGE"
            case 21:
                self.friendlyName = "Huntington"
                self.code = "C15"
                self.line = "BLUE"
            case 22:
                self.friendlyName = "Special"
            case 23:
                self.friendlyName = "Vienna"
                self.code = "K08"
                self.line = "ORANGE"
            case 24:
                self.friendlyName = "Greenbelt"
                self.code = "E10"
                self.line = "YELLOW"
            case 25:
                self.friendlyName = "Arlington Cemetery"
                self.code = "C06"
                self.line = "BLUE"
            case 26:
                self.friendlyName = "Franconia-Springfield"
                self.code = "J03"
                self.line = "YELLOW"
            case 27:
                self.friendlyName = "Reagan National Airport"
                self.code = "C10"
                self.line = "YELLOW"
            case 28:
                self.friendlyName = "Mount Vernon Square"
                self.code = "E01"
                self.line = "YELLOW"
            case 29:
                self.friendlyName = "Fort Totten"
                self.code = "E06"
                self.line = "YELLOW"
            case 30:
                self.friendlyName = "Stadium-Armory"
                self.code = "D08"
                self.line = "YELLOW"
            case 31:
                self.friendlyName = "Huntington"
                self.code = "C15"
                self.line = "YELLOW"
            case 32:
                self.friendlyName = "Rosslyn"
                self.code = "C05"
                self.line = "YELLOW"
            case 33:
                self.friendlyName = "U Street"
                self.code = "E03"
                self.line = "YELLOW"
            case 34:
                self.friendlyName = "Dulles Airport"
                self.code = "N10"
                self.line = "SILVER"
            case 35:
                self.friendlyName = "West Falls Church"
                self.code = "K06"
                self.line = "ORANGE"
            case 36:
                self.friendlyName = "Stadium Armory"
                self.code = "D08"
                self.line = "ORANGE"
            case 37:
                self.friendlyName = "Reagan National Airport"
                self.code = "C10"
                self.line = "BLUE"
            case 38:
                self.friendlyName = "Mount Vernon Square"
                self.code = "E01"
                self.line = "BLUE"
            case 39:
                self.friendlyName = "Franconia-Springfield"
                self.code = "J03"
                self.line = "GREEN"
            case 40:
                self.friendlyName = "Special"
            case 41:
                self.friendlyName = "Fort Totten"
                self.code = "E06"
                self.line = "GREEN"
            case 42:
                self.friendlyName = "Anacostia"
                self.code = "F06"
                self.line = "GREEN"  
            case 43:
                self.friendlyName = "Branch Avenue"
                self.code = "F11"
                self.line = "GREEN"
            case 44:
                self.friendlyName = "Greenbelt"
                self.code = "E10"
                self.line = "GREEN"
            case 45:
                self.friendlyName = "U Street"
                self.code = "E03"
                self.line = "GREEN"
            case 46:
                self.friendlyName = "Mount Vernon Square"
                self.code = "E01"
                self.line = "GREEN"       
            case 47:
                self.friendlyName = "Reagan National Airport"
                self.code = "C10"
                self.line = "GREEN"
            case 48:
                self.friendlyName = "Huntington"
                self.code = "C15"
                self.line = "GREEN"
            case 49:
                self.friendlyName = "Smithsonian"
                self.code = "D02"
                self.line = "ORANGE"
            case 50:
                self.friendlyName = "Special"
            case 51:
                self.friendlyName = "Largo"
                self.code = "G05"
                self.line = "SILVER"
            case 52:
                self.friendlyName = "New Carollton"
                self.code = "D13"
                self.line = "SILVER"
            case 53:
                self.friendlyName = "Stadium Armory"
                self.code = "D08"
                self.line = "SILVER"
            case 54:
                self.friendlyName = "Eastern Market"
                self.code = "D06"
                self.line = "ORANGE"
            case 55:
                self.friendlyName = "Addison Road"
                self.code = "G03"
                self.line = "BLUE"
            case 56:
                self.friendlyName = "Rosslyn"
                self.code = "C05"
                self.line = "BLUE"
            case 57:
                self.friendlyName = "Eastern Market"
                self.code = "D06"
                self.line = "ORANGE"
            case 58:
                self.friendlyName = "Smithsonian"
                self.code = "D02"
                self.line = "BLUE"
            case 59:
                self.friendlyName = "Smithsonian"
                self.code = "D02"
                self.line = "SILVER"
            case 60:
                self.friendlyName = "Special"
            case 61:
                self.friendlyName = "Rosslyn"
                self.line = "SILVER"
                self.code = "C05"
            case 62:
                self.friendlyName = "Ballston-MU"
                self.line = "SILVER"
                self.code = "K04"
            case 63:
                self.friendlyName = "Spring Hill"
                self.line = "SILVER"
                self.code = "N04"
            case 64:
                self.friendlyName = "Wiehle-Reston East"
                self.code = "N06"
                self.line = "SILVER"
            case 65:
                self.friendlyName = "Eastern Market"
                self.code = "D06"
                self.line = "BLUE"
            case 66:
                self.friendlyName = "Stadium Armory"
                self.code = "D08"
                self.line = "BLUE"
            case 67:
                self.friendlyName = "Fort Totten"
                self.code = "E06"
                self.line = "BLUE"
            case 68:
                self.friendlyName = "Ashburn"
                self.line = "SILVER"
            case 69:
                self.friendlyName = "Special"
            case 70:
                self.friendlyName = "East Falls Church"
                self.line = "ORANGE"
                self.code = "K05"
            case 71:
                self.friendlyName = "Greenbelt"
                self.code = "E10"
                self.line = "BLUE"
            case 72:
                self.friendlyName = "Largo"
                self.code = "G05"
                self.line = "BLUE"
            case 73:
                self.friendlyName = "Largo"
                self.code = "G05"
                self.line = "ORANGE"
            case 87:
                self.friendlyName = "Shady Grove Yard"
                self.code = "A99"
            case 98:
                self.friendlyName = "Reagan Nat. Airport Pocket Track"
                self.code = "C10"
            case _:
                self.friendlyName = "No Passengers" 

class TrainInStation:   

    def __init__(self, trainID):
        #Default values
        self.id = trainID
        self.trainBerth = False
        self.arrivalTime = datetime.now()
        self.departureTime = datetime.now()
        self.doorsOpenTime = 0
        self.doorsCloseTime = 0
        self.doorsOpenAuto = False
        self.doorsOpenSide = "NOT"
        self.oddDoors = False
        self.pss = False
        self.ato = False
        self.atp = False
        self.trainBerth = False
        self.destination = destination(0)
        self.location = ""
        self.track = 1
        self.length = 0
        self.rawBits = ""
        self.wrongSide = False
    def print(self):
        print("===")
        match self.destination.line:
            case "BLUE":
                lineColor = Fore.BLUE
            case "YELLOW":
                lineColor = Fore.YELLOW
            case "GREEN":
                lineColor = Fore.GREEN
            case "SILVER":
                lineColor = Fore.LIGHTBLACK_EX
            case "RED":
                lineColor = Fore.RED
            case "ORANGE":
                lineColor = Fore.LIGHTRED_EX
            case _:
                lineColor = Fore.MAGENTA

        returnstr = Fore.YELLOW + "ID: " + Fore.WHITE + str(self.id) + Fore.YELLOW + " Destination: " + lineColor + self.destination.friendlyName + "/" + str(self.destination.id) + Fore.YELLOW + " Current Location: " + Fore.WHITE + self.location.code + "-" + self.location.track + "/" + self.location.friendlyName + Fore.YELLOW + " Length: " + Fore.RESET+ str(self.length) + "\n"
        returnstr += Fore.GREEN + "ATO:" + Fore.WHITE + str(self.ato)+ Fore.GREEN + " Berth:" + Fore.WHITE + str(self.trainBerth)+ Fore.GREEN + " ATP:" + Fore.WHITE + str(self.atp) + Fore.GREEN + " PSS:" + Fore.WHITE + str(self.pss) + "\n"
        returnstr += Fore.BLUE + "First Arrived: " + Fore.RESET + str(self.arrivalTime) + Fore.BLUE + " Departed: " + Fore.RESET + str(self.departureTime) + "\n"
        if self.doorsOpenTime == 0 and self.doorsCloseTime == 0:
            returnstr += Fore.MAGENTA + "Doors did not open" + "\n"
        else:
            doorsStr = ""
            if self.doorsOpenAuto:
                doorsStr =  Fore.MAGENTA + " AUTOMATICALLY" + Fore.RESET + " on the " + self.doorsOpenSide
            else:
                doorsStr = Fore.MAGENTA + " MANUALLY" + Fore.RESET + " on the " + self.doorsOpenSide
            returnstr += Fore.MAGENTA + "Doors opened: " + Fore.RESET + str(self.doorsOpenTime) + doorsStr  + Fore.MAGENTA + " and closed at: " + Fore.RESET + str(self.doorsCloseTime)
            print(returnstr)
            return returnstr
    def html(self):
        template = htmlTemplate
        #Replacing the placeholder values with our real values.
        template = template.replace("/COLOR/", self.destination.line.lower())
        template =template.replace("{ID}", str(self.id))
        template =template.replace("{DEST}", str(self.destination.id) + "/" + self.destination.friendlyName)
        template =template.replace("{LOCATION}", self.location.code + "-" + self.location.track + "/" + self.location.friendlyName)
        template =template.replace("{LEN}", str(self.length))
        template =template.replace("{ATO}", str(self.ato))
        template =template.replace("{BERTH}", str(self.trainBerth))
        template =template.replace("{ATP}", str(self.atp))
        template =template.replace("{PSS}", str(self.pss))
        template =template.replace("{ARR}", str(self.arrivalTime))
        template =template.replace("{DEPT}", str(self.departureTime))
        template =template.replace("{DO}", str(self.doorsOpenTime))
        template =template.replace("{DA}", str(self.doorsOpenAuto))
        template =template.replace("{DS}", str(self.doorsOpenSide))
        template =template.replace("{DC}", str(self.doorsCloseTime))
        
        return template
    def serialize(self):
        selfCopy = copy.deepcopy(self)
        selfCopy.arrivalTime = selfCopy.arrivalTime.isoformat(" ")
        selfCopy.departureTime = selfCopy.departureTime.isoformat(" ")
        if selfCopy.doorsOpenTime != 0:
            selfCopy.doorsOpenTime = selfCopy.doorsOpenTime.isoformat(" ")
        if selfCopy.doorsCloseTime != 0:
            selfCopy.doorsCloseTime = selfCopy.doorsCloseTime.isoformat(" ")
        return json.dumps(selfCopy, default=lambda obj: obj.__dict__,)
class currentLocation:
    friendlyName = ""
    code = ""
    track = ""
    platformStyle = ""
    normalDoorsOpen = ""
    terminal = False
    def __init__(self, code) -> None:
        splitStr = code.split("-")
        self.track = splitStr[1]
        self.code = splitStr[0]
        for row in stationData:
            if row[0] == splitStr[0]:
                self.friendlyName = row[2].title()
                self.platformStyle = row[3]
                if self.platformStyle == "ISLAND":
                    self.normalDoorsOpen = "LEFT"
                if self.platformStyle == "SPLIT":
                    self.normalDoorsOpen = "RIGHT"
                break
        if terminalStations.count(self.code) > 0:
            self.terminal = True

        
            
                     
def convertTime(time):
    #This datetime format matches that of the date provided by the MetroRail TWC tool
    timeformat = '%Y %b %d %H:%M:%S'
    #I use str.replace here to remove the unnecessary "EDT" string that was throwing the conversion here
    timeObj = datetime.strptime(time.replace(" EDT", ""), timeformat)
    return timeObj




#Processing the data from the tool
def processData(file, printData=False, code="*", line="*",autoOnly=False, destID=-1, track="0", trainID="-1", route="Any"):   
    reader = csv.reader(open("twcData/" + file))
    trainsList = []
    i=0
    rows = []
    #Apply the filter as we are opening the file. Saves memory and cuts complexity of the program :)
    for row in reader:
        try:
            if not route=="Any":
                if row[1][0] != route:
                    continue
            if not row[5].isdigit():
                continue
            if code != "*" and code != row[1].split("-")[0]:
                continue
            #Checks if track matches the filter applied
            if row[1].split("-")[1] != track and track != "0":       
                continue
            dest = destination(int(row[6]))
            if line != "*":      
                if line != dest.line:
                    continue
            if destID != -1 and dest.id != destID:
                continue
            if autoOnly == True:
                if row[9] != "1":
                    continue 
            if trainID != "-1" and row[5] != trainID:
                print(trainID + "Isnot" + row[5])
                continue          
            #If the code execution gets to here, then the train passed all of the filters      
            rows.append(row)
        except:
            print("Issue with row. Incomplete data")
    if len(rows) == 0:
        print(Fore.RED + "ERROR: No Trains Match Selected Criteria!" + Fore.RESET)
        return
    for row in rows:       
        j=len(trainsList)-1
        if int(row[5]) != 0:
            if len(trainsList)==0:
                trainsList.append(TrainInStation(int(row[5])))
                j+=1
                trainsList[j].arrivalTime = convertTime(row[0]) 
                trainsList[j].location = currentLocation(row[1]) 
            if int(row[5]) != trainsList[j].id:
                #This removes the one line trains that usually are the result of an issue with the equipment at a particular location
                if trainsList[j].length == 0 or trainsList[j].arrivalTime == trainsList[j].departureTime:
                    trainsList.pop()
                    j-=1
                #The next train has begun because the ID has changed.
                trainsList.append(TrainInStation(int(row[5])))
                j+=1
                trainsList[j].arrivalTime = convertTime(row[0]) 
                trainsList[j].location = currentLocation(row[1]) 
            #A length of less than 6 is kind of suspicious, but it does happen sometimes so just continually update to make sure it isn't a fluke
            if (trainsList[j].length < 6 or trainsList[j].length > 8) and row[7].isdigit():
                trainsList[j].length = int(row[7])
            #Set our destination
            if int(row[5]) != 0:
                trainsList[j].destination = destination(int(row[6]))
            #Check for PSS
            if int(row[8]) == 1:
                trainsList[j].pss = True
            #Check for ATO (ATO shows up when a train is keyed up and keyed down, so to check for automatic operation you need to see if it is actually moving when the ATO bit is picked)
            if int(row[9]) == 1 and int(row[14]) == 1:
                trainsList[j].ato = True
            #Check for ATP
            if int(row[10]) ==1:
                trainsList[j].atp = True
            #Check for train berth
            if int(row[13])==1:
                trainsList[j].trainBerth = True
            if (int(row[11])==1 or int(row[11]) ==2) and trainsList[j].doorsCloseTime == 0:
                #Doors are open. We only check the first time the doors open because sometimes the doors report as having reopened
                #falsely
                if trainsList[j].doorsOpenTime == 0:
                    #This means that the doors just opened, so let's take note of that
                    if trainsList[j].arrivalTime == convertTime(row[0]):
                        #Essentially, if a train reports immediately that the doors are open upon entry, it is a bug in the TWC system
                        continue
                    trainsList[j].doorsOpenTime = convertTime(row[0])
                    #At the time the doors opened, did it happen manually?
                    if int(row[15]) == 0:
                        trainsList[j].doorsOpenAuto = True           
                if int(row[11]) ==1 and trainsList[j].doorsOpenSide == "NOT":
                    #Doors open right
                    trainsList[j].doorsOpenSide = "RIGHT"
                if int(row[11])==2 and trainsList[j].doorsOpenSide == "NOT":
                    #Doors open left
                    trainsList[j].doorsOpenSide = "LEFT"
                #These if statements should tease out the odd behavior that is sometimes seen at certain stations, momentarily reporting the doors having
                #opened on the wrong side.
                if int(row[11])==1 and trainsList[j].doorsOpenSide == "LEFT":
                    trainsList[j].oddDoors=True
                if int(row[11])==2 and trainsList[j].doorsOpenSide == "RIGHT":
                    trainsList[j].oddDoors=True
            if int(row[11])==3 and trainsList[j].doorsOpenTime != 0 and trainsList[j].doorsCloseTime ==0:
                #The doors were open and now are closed, so take note of that
                trainsList[j].doorsCloseTime = convertTime(row[0])
            #Each time we see an entry for a specific train, we set it as departed then because you never know if you'll see it again!
            trainsList[j].departureTime = convertTime(row[0])

            if trainsList[j].doorsOpenSide != trainsList[j].location.normalDoorsOpen and trainsList[j].destination.code != trainsList[j].location.code and trainsList[j].location.terminal == False and trainsList[j].doorsOpenSide != "NOT":
                trainsList[j].wrongSide = True
                print("yes")
            #Finally, add this row as part of the raw bits of the train object:
            trainsList[j].rawBits += str(row).replace(',', "</td><td>").replace("'", "").replace("[", "<tr><td>").replace("]", "</td></tr>")
        else:
            continue
    pss = 0
    atp = 0
    ato = 0
    berth = 0
    eight_car = 0
    six_car = 0
    autoDoors = 0
    i=0
    wrongSide=0
    suspectLocations = []
    returnstr = ""
    trainsList = sorted(trainsList, key=lambda x: x.arrivalTime)
    for train in trainsList:
        #Calculating success rates

        if True:
            if len(returnstr) > 0:
                returnstr += "&" + train.serialize()
            else:
                returnstr += train.serialize()
        if train.pss:
            pss +=1
        if train.atp:
            atp +=1
        if train.ato:
            ato +=1
        if train.trainBerth:
            berth +=1
            suspectLocations.append(train.location.code)
        if train.doorsOpenAuto:
            autoDoors +=1
        if train.length == 8:
            eight_car +=1
        if train.length == 6:
            six_car +=1
        if train.wrongSide:
            wrongSide +=1
            #returnstr += "&" + train.serialize()

        i+=1 
    stats = dict(pss = str(round(pss/len(trainsList) * 100, 2)), ato = str(round(ato/len(trainsList) * 100, 2)), atp= str(round(atp/len(trainsList) * 100, 2)),
                 berth=str(round(berth/len(trainsList) * 100, 2)),
                 ado=str(round(berth/len(trainsList) * 100, 2)),
                 wrongSide=wrongSide,
                 eight=str(eight_car),
                 six=str(six_car))
    returnstr += "&" + json.dumps(stats)
    return returnstr


sched = BackgroundScheduler()

def fetchData():
    timeRequest = datetime.now()
    print(Fore.BLUE + "Beginning data download..." + Fore.RESET)
    r = requests.get('http://rocsgraph/cgi-bin/twcaimcsv24hrs'.rstrip())
    print(r.status_code)
    fileName = "twcData/" + timeRequest.strftime("%d-%m-%Y") + ".csv"
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(r.text)
        f.close()
    print("Request took (seconds):" + str(r.elapsed.total_seconds()))
    print(Fore.BLUE + "Data download complete. The next data download will occur: " + str(job.next_run_time) + Fore.RESET)
    latestFile = "twdData/" + fileName
today = date.today()
job = sched.add_job(fetchData, trigger='cron', hour='0', minute='0')

sched.start()

print(Fore.BLUE + "The next data download will occur:" + str(job.next_run_time) + Fore.RESET)








        









