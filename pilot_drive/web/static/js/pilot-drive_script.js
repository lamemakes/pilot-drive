

// Global variables

// Hostname
window.hostname;

// Bluetooth vars
window.track;
window.status;
window.connectedDevice;

// Vehicle vars
window.vehicleInfo;

window.units = "imperial";
window.timeFrmt = 12;


// Util methods, used for the benefit of the script.

// AJAX method to post to an endpoint, then update a specific HTML element with the data
// some requests will be an outlier to this, in which custom ajax call will be needed
function ajaxPost(endpoint, jsonName, elementToUpdate) {
    var req = new XMLHttpRequest();
    var result = document.getElementById(elementToUpdate);
    if (jsonName != undefined || elementToUpdate != undefined){
        req.onreadystatechange = function()
        {
            if(this.readyState == 4 && this.status == 200) {
            var ajaxReturn = JSON.parse(this.responseText);
            result.innerHTML = ajaxReturn[jsonName];
            }
        }
    }

    req.open('POST', endpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}

// System methods

// Time getter function to pull in time
function getTime() {
    var now = new Date();

    // Time formatting
    // Handles 24 hour vs 12 hour format
    // TODO: More intuitive method for this?
    if (window.timeFrmt === 12) {
        if (now.getHours() > 12) {
            hours = now.getHours() - 12;
            daytime = " PM";
        } else if (now.getHours() == 0) {
            hours = 12;
        } else {
            hours = now.getHours();
            daytime = " AM";
        }
    } else if (window.timeFrmt === 24) {
        if (now.getHours() < 10){
            hours = "0" + now.getHours();
        } else {
            hours = now.getHours();
        }
        daytime = "";
    }

    if (now.getMinutes() < 10) {
        minutes = "0" + now.getMinutes();
    } else {
        minutes = now.getMinutes();
    } 


    var currentTime = hours + ":" + minutes + daytime;

    var timeElements = document.getElementsByClassName("time-result");
    
    for(var counter = 0; counter < timeElements.length; counter++){
        timeElements[counter].innerHTML = currentTime
    }

    //timeElement.innerHTML = currentTime
}

// CPU getter function to get load on CPU
function getCPULoad() {
    var cpuEndpoint = "/get-cpuload";
    var cpuJson = "cpu";
    var cpuElement = "cpu-result";
    ajaxPost(cpuEndpoint, cpuJson, cpuElement)
}

function getHostname() {
    var req = new XMLHttpRequest();
    var hostEndpoint = "/get-hostname";
    req.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
        var hostname = JSON.parse(this.responseText);
        window.hostname = hostname["hostname"]
        }
    }

    req.open('POST', hostEndpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}

// Bluetooth methods

// Go to the prev track 
function prevTrack() {
    var prevTrackEndpoint = "/bt-ctl/track-ctl/prev";
    ajaxPost(prevTrackEndpoint);
}

// Go to the next track 
function nextTrack() {
    var nextTrackEndpoint = "/bt-ctl/track-ctl/next";
    ajaxPost(nextTrackEndpoint);
}

// Go to the pause/play
function changePlayback() {
    var playbackEndpoint = "/bt-ctl/track-ctl/playback-change";
    ajaxPost(playbackEndpoint);
}

function getBluetoothInfo() {
    var btInfoEndpoint = "/bt-info";

    var req = new XMLHttpRequest();

    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var bluetoothInfo = JSON.parse(this.responseText);
            if (bluetoothInfo != window.bluetoothInfo){
                if (bluetoothInfo["btInfo"]["connected"]) {
                    updateConnectedDevice(bluetoothInfo["btInfo"]["connectedDevice"]);
                    updateTrackInfo(bluetoothInfo["btInfo"]["track"]);
                    updateTrackStatus(bluetoothInfo["btInfo"]["track"]);
                } else {
                    updateConnectedDevice(null);
                    updateTrackInfo(null);
                    updateTrackStatus(null);
                }
                window.bluetoothInfo = bluetoothInfo;
            }
        }
    }


    req.open('POST', btInfoEndpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}

function updateTrackInfo(track) {

   var musicInfo = document.getElementById("track-info");
   var waitConnect = document.getElementById("wait-connect");
   var topTime = document.getElementById("top-time");

    if (track != null) {

        if (topTime.style.display != "block") {
            topTime.style.display = "block";
        } 

       if (musicInfo.style.display != "grid") {
           musicInfo.style.display = "grid";
           waitConnect.style.display = "none";
       } 

        var title = document.getElementById("title");
        var album = document.getElementById("album");
        var artist = document.getElementById("artist");

        var trackInfo = track["metadata"];

        title.innerHTML = (trackInfo["title"] != null) ? trackInfo["title"] : "";
        album.innerHTML = (trackInfo["album"] != null) ? trackInfo["album"] : "";
        artist.innerHTML = (trackInfo["artist"] != null) ? trackInfo["artist"] : "";

    } else {
        if (topTime.style.display == "block" || topTime.style.display == "") {
            topTime.style.display = "none";
        }

        if (waitConnect.style.display != "grid") {
            waitConnect.style.display = "grid";
            musicInfo.style.display = "none";
        } 

        waitMsg = document.getElementById("wait-msg");
        if (waitMsg.innerHTML == "") {
            waitMsg.innerHTML = 'To connect, look for  <span class="highlight">' + window.hostname + "</span> in your bluetooth settings.";
        }

    }
}

function updateTrackStatus(track) {

    var statusButtonImg = document.getElementById("status-img");

    var playImg = "static/icons/play_button.png";
    var pauseImg = "static/icons/pause_button.png";

    if (track != null) {

        trackStatus = track["status"];

        if (trackStatus != null) {
            if (trackStatus == "playing") {
                statusButtonImg.src = pauseImg;
            } else {
                statusButtonImg.src = playImg;
            }
        }
    } else {
        statusButtonImg.src = playImg;
    }

}

function updateConnectedDevice(device) {
    var connectedDevice = document.getElementById("connected-name");

    if (device != null) {
        connectedDevice.innerHTML = device["name"];
    } else {
        connectedDevice.innerHTML = "";
    }
}

function getVehicleInfo() {
    var vehicleInfoEndpoint = "/vehicle-info";

    var req = new XMLHttpRequest();

    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var vehicleInfo = JSON.parse(this.responseText);
            if (vehicleInfo != window.vehicleInfo){
                if (vehicleInfo["vehicleInfo"]["connection"]) {

                    var speed = document.getElementById("speed-info");
                    if (window.units === "imperial") {
                        speed.innerHTML = Math.round(vehicleInfo["vehicleInfo"]["speed"] * 0.6213712) + " MPH";
                    } else if (window.units == "metric") {
                        speed.innerHTML = vehicleInfo["vehicleInfo"]["speed"] + " KPH"
                    }

                    var fuel_level = document.getElementById("fuel-info");
                    fuel_level.innerHTML = vehicleInfo["vehicleInfo"]["fuelLevel"] + "%";

                    var voltage = document.getElementById("voltage-info");
                    voltage.innerHTML = vehicleInfo["vehicleInfo"]["voltage"];

                    var rpm = document.getElementById("rpm-info");
                    rpm.innerHTML = vehicleInfo["vehicleInfo"]["rpm"];

                    var eng_load = document.getElementById("load-info");
                    eng_load.innerHTML = vehicleInfo["vehicleInfo"]["engLoad"];

                    var dtc = document.getElementById("dtc-info");
                    dtc.innerHTML = vehicleInfo["vehicleInfo"]["dtc"];

                } else {
                    // Do something when no OBDII is connected
                }
                window.vehicleInfo = vehicleInfo;
            }
        }
    }


    req.open('POST', vehicleInfoEndpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}

function getAdbInfo() {
    var adbInfoEndpoint = "/adb-info";

    var req = new XMLHttpRequest();

    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var adbInfo = JSON.parse(this.responseText);
            if (adbInfo != window.adbInfo){
                document.getElementById("adb-notifs").innerHTML = "";
                if (adbInfo["android"]["connection"]){
                    if (adbInfo["android"]["notifications"] != null){
                        for (var i = 0; i < adbInfo["android"]["notifications"].length; i++){
                            createAdbNotification(adbInfo["android"]["notifications"][i]);
                        }
                        console.log("Full iter!")
                    }
                }

                window.adbInfo = adbInfo;
            }
        }
    }

    req.open('POST', adbInfoEndpoint, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}

function createAdbNotification(notification){
    var adbNotifs = document.getElementById("adb-notifs");

    var notificationDiv = document.createElement("div");
    notificationDiv.classList.add('notification');

    var notificationTextDiv = document.createElement("div");
    notificationTextDiv.classList.add("notification-text");

    var notificationImgDiv = document.createElement("div");
    var notificationImg = document.createElement("img");

    if (notification["icon_path"] != null){
        console.log(notification["icon_path"]);
        notificationImg.src = notification["icon_path"]
    }

    notificationImgDiv.classList.add("notification-img");

    notificationImgDiv.append(notificationImg);

    if (notification["android.title"] != null) {

        var notifTitle = document.createElement("h3");
        notifTitle.innerHTML = notification["android.title"]
        notificationTextDiv.append(notifTitle);

        if (notification["tickerText"] != null){
            var tickerText = document.createElement("p");
            tickerText.innerHTML = notification["tickerText"];
            notificationTextDiv.append(tickerText);
        }
    }


    notificationDiv.append(notificationImgDiv);
    notificationDiv.append(notificationTextDiv);

    adbNotifs.append(notificationDiv);

}

function openTab(evt, TabName) {
    // Declare all variables
    var i, tabContent, tabLinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
      tabContent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tabLinks = document.getElementsByClassName("tab-links");
    for (i = 0; i < tabLinks.length; i++) {
      tabLinks[i].className = tabLinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(TabName).style.display = "flex";
    evt.currentTarget.className += " active";
  } 


function selectDefault() {
    // For default tab
    document.getElementById("default-tab").click();

    // For settings (probably better ways to do this)
    if (window.units === "metric") {
        document.getElementById("metric-btn").click();
    } else if (window.units === "imperial") {
        document.getElementById("imperial-btn").click();
    }

    if (window.timeFrmt === 12) {
        document.getElementById("twelve-btn").click();
    } else if (window.timeFrmt === 24) {
        document.getElementById("twentyfour-btn").click();
    }
}

// Settings methods

function changeUnits(unitId) {
    imperialBtn = document.getElementById("imperial-btn");
    metricBtn = document.getElementById("metric-btn");


    if (unitId === "metric-btn") {
        window.units = "metric";
        imperialBtn.style.backgroundColor = "white";
        metricBtn.style.backgroundColor = "#a0a0a0";
    } else if (unitId === "imperial-btn") {
        window.units = "imperial";
        imperialBtn.style.backgroundColor = "#a0a0a0";
        metricBtn.style.backgroundColor = "white";
    }
}

function changeTimeFrmt(timeFrmtId) {
    twelveBtn = document.getElementById("twelve-btn");
    twentyfourBtn = document.getElementById("twentyfour-btn");

    if (timeFrmtId === "twelve-btn") {
        window.timeFrmt = 12;
        console.log(window.timeFrmt);
        twentyfourBtn.style.backgroundColor = "white";
        twelveBtn.style.backgroundColor = "#a0a0a0";
    } else if (timeFrmtId === "twentyfour-btn") {
        window.timeFrmt = 24;
        console.log(window.timeFrmt);
        twentyfourBtn.style.backgroundColor = "#a0a0a0";
        twelveBtn.style.backgroundColor = "white";
    }
}


function checkForUpdate() {
    update_endpoint = "/check-updates"
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            var ajaxReturn = JSON.parse(this.responseText);
            if (this.responseText.includes("error")){
                alert("Error: " + ajaxReturn["error"])
            } else {
                var dialog = confirm(ajaxReturn["update"]);
                if(dialog) {
                    var conf = new XMLHttpRequest();
                    conf.open('POST', update_endpoint + "/confirm-update", true);
                    conf.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
                    conf.send();
                }
            }
        }
    }

    req.open('POST', update_endpoint + "/get-updates", true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send();
}