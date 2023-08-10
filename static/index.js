var mainTemplate;
var trainsList = [];
var idSortMode = false;
const req = new XMLHttpRequest();
function onload() {
    req.open("GET", "/filelist", false);
    req.send()
    var selectList = document.getElementById("file")
    var files = JSON.parse(req.response)
    for(let i in files) {
        var option = document.createElement("option");
        option.text = files[i]
        option.id = files[i]
        selectList.add(option)
    }
    req.open("GET", "/template", false);
    req.send();
    mainTemplate = req.response
}
function showLoadingState() {
    document.getElementById("results").innerHTML = ""
    var img = document.createElement("img");
    img.src = "static/loading.gif";
    document.getElementById("results").appendChild(img)
}
function getData() {
    idSortMode = false
    trainsList = []
    document.getElementById("results").innerHTML = ""
    var request = "./process?line={0}&station={1}&destination={2}&auto={3}&print={4}&track={5}&file={6}&train={7}&route={8}";
    var ato=document.getElementById("atoOnly").checked;
    var printAll= document.getElementById("showAll").checked;
    var line = document.getElementById('line').value
    var station = document.getElementById('stationID').value
    var trackID = document.getElementById('trackID').value
    var destinationID = document.getElementById('destID').value
    var file = document.getElementById('file').value
    var trainID = document.getElementById('trainID').value
    var route = document.getElementById('route').value
    
    showLoadingState()

    if (isNaN(trackID) || trackID == "") {
        trackID = 0
    }
    if (isNaN(destinationID) || destinationID == "") {
        destinationID = -1
    }
    if (station == "") {
        station = "*"
    }
    request = request.replace("{0}", line)
    request = request.replace("{1}", station)
    request = request.replace("{2}", destinationID)
    request = request.replace("{3}", ato.toString())
    request = request.replace("{4}", printAll.toString())
    request = request.replace("{5}", trackID)
    request = request.replace("{6}", file)
    request = request.replace("{7}", trainID)
    request = request.replace("{8}", route)

    req.open("GET", request, true);
    req.send();
    req.addEventListener("loadend", loadEnd);
    

}

function loadEnd(e) {
    if (req.response == "No trains match selected criteria!") {
        document.getElementById('results').innerHTML = `<h3 style="color:red;">No trains match selected criteria</h3>`
        document.getElementById('stats').hidden = true
        return
    }
    response = req.response.split("&")
    var dataLimit = 250
    document.getElementById('stats').hidden = false
    document.getElementById("results").innerHTML = `<h3>${response.length-1} Results</h3>`
    if (response.length > dataLimit && document.getElementById("showAll").checked) {
        document.getElementById("results").innerHTML += `<h2>Limiting data display to 250 for performance reasons</h2>`
    }
    for (line in response) {
        trainsList.push(JSON.parse(response[line]))
    }
    var stats = JSON.parse(response[response.length-1])
    document.getElementById("8").innerHTML = stats.eight
    document.getElementById("6").innerHTML =  stats.six
    document.getElementById("ato").innerHTML =  stats.ato
    document.getElementById("atp").innerHTML =  stats.atp
    document.getElementById("ado").innerHTML =  stats.ado
    document.getElementById("berth").innerHTML = stats.berth
    document.getElementById("wdo").innerHTML =  stats.wrongSide
    if (document.getElementById("showAll").checked) {
    for (let i in trainsList) {
        if (i > dataLimit) {
            break
        }
        setTimeout(updateUI(trainsList[i]), 0)
    }
}
}

function updateUI(self) {
        template = mainTemplate.replace("{Color}", self.destination.line).replace("{ID}", self.id).replace("{DEST}", self.destination.id + "/" + self.destination.friendlyName).replace("{LOCATION}", self.location.code + "-" + self.location.track + "/" + self.location.friendlyName)
        template =template.replace("{LEN}", self.length)
        template =template.replace("{ATO}", self.ato)
        template =template.replace("{BERTH}", self.trainBerth)
        template =template.replace("{ATP}", self.atp)
        template =template.replace("{PSS}", self.pss)
        template =template.replace("{ARR}", self.arrivalTime)
        template =template.replace("{DEPT}", self.departureTime)
        template =template.replace("{DO}", self.doorsOpenTime)
        if (self.doorsOpenAuto) {
            template =template.replace("{DA}", "Automatically")
        }else {
            template =template.replace("{DA}", "Manually")
        }
        template =template.replace("{DS}", self.doorsOpenSide)
        template =template.replace("{DC}", self.doorsCloseTime)
        template =template.replace("{RD}", self.rawBits)
        document.getElementById('results').innerHTML += template

        
        if (self.doorsOpenTime == "0") {
            list = document.getElementsByName('doors')
            if (list.length == 0) {
                return
            }
            list[list.length -1].innerHTML = "<div style='color:firebrick'>Doors did not open</div>"
        }
}

function showDoorsClosed(jsonObj) {
    document.getElementById("results").innerHTML = "<h2>Trains with doors open on wrong side:</h2>"
    for (i in trainsList) {
        if (trainsList[i].wrongSide == true) {
            setTimeout(updateUI(trainsList[i]), 0)
        }
    }
}

function rawButtonClicked(element) {
    element.parentElement.querySelector('[name="rawdata"]').hidden = !element.parentElement.querySelector('[name="rawdata"]').hidden
}
function showAllFromID(element) {
    id = element.innerHTML
    if (idSortMode) {
        return
    }
    setTimeout(showLoadingState(), 0)
    document.getElementById("results").innerHTML = `<h2>Train ID: ${id}</h2>`
    for (i in trainsList) {
        if (trainsList[i].id == id) {
            setTimeout(updateUI(trainsList[i]), 0)
        }
    }
    idSortMode = true
}