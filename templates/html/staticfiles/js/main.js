//get the value of the dropdown menu
function getSelectedFileType(){
 var e = document.getElementById("fileFormat");
 return e.selectedIndex
}

//Get the form field value
function getURL(){
 var e = document.getElementById('URLField');
 return e.value
}

// check if the url is correct form
function ValidURL(userInput) {
    var res = userInput.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
    if(res == null)
        return false;
    else
        return true;
}

//test if the form contain the correct values
function testForm(){
/* if (!captchaResult){
    toggleCaptcha();
    return;
 }*/

 var params='';
 var ficURL = getURL();
 if (ficURL == "" || !ValidURL(ficURL)){ //if the url is empty or in wrong form mark it red
     //alert("badLink");
     document.getElementById("URLField").className = "searchTermError";
     return
 }else{
          //alert("goodLink");
          var URLField = document.getElementById("URLField")
          URLField.className = "searchTerm";
          params += "ficURL=" + ficURL;
 }
 var ficFormat = getSelectedFileType();
 if (ficFormat == 0){ //if the no format is selecetd mark in red
     document.getElementById("fileFormat").className = "searchCategoryError";
     return
 }else{
      document.getElementById("fileFormat").className = "searchCategory";
      params += "&ficFormat=" + ficFormat;
 }
 addRow(); //add new row in the table for the status
 if (submitForm(params)){ //send the request to the server
     URLField.value = ""; //Clear the url box for new download
 }
}

function submitForm(params) {
    var http = new XMLHttpRequest();
    http.rowID = rowsIndex - 1; // rowsIndex is increased affter new is added but we need the previous value
                                // and we need the XMLHttpRequest to have the rowID
    http.open("POST", serverURL+"download", true);
    http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    http.onprogress = function () {
      var testStr = http.responseText; // response from the server
                                       // str format name - Autor;;;LASTChater;;;CorrentDownloadedChapter
      var res = testStr.split(";;;");
      storyName = res[0];
      maxCapters = res[1];
      currentChapter = res[res.length - 2]; // When the download is finished we get the download ID and for few shor seconds there is an ugly long string
                                            // to solve this we just get the not last value
      if (currentChapter == -1){ // If the download is complete get the status of the convertion
          status = res[res.length - 3];
      }else{                     // else show x of y chapters done
          status = currentChapter + " of " + maxCapters;
      }
      changeText(0,storyName, this.rowID); // put the text in the table arguments are cellID, Text, rowID
      changeText(1,status, this.rowID); // put the text in the table arguments are cellID, Text, rowID
    }
    http.onload = function() {
      //Add the download link when done
      if ( http.status == 200 ) {
          var testStr = http.responseText;
          var res = testStr.split(";;;");
          var downloadID = res[res.length - 1];
          var downloadURL = serverURL + "getFile?fileID="+downloadID;
          var link = '<a class="dark-blue-text"  href="'+downloadURL+'">Download</a>'; //put the download link in the tabble
          changeText(1, link,  this.rowID);
          var a = document.createElement("a");
          document.body.appendChild(a);
          a.href = downloadURL;
          a.onclick = function () {
              setTimeout(function () {
                 window.URL.revokeObjectURL(a.href);
             }, 1500);
          };
          a.click();
      } else {
          changeText(0, ' ',  this.rowID); // Show this on error.
          changeText(1, 'An error occured. :(',  this.rowID); //
      }
    }

    http.onerror= function(e) {
        //alert("Error fetching " + http.responseText); //Show error
          changeText(0, ' ',  this.rowID); //Show this on error.
          changeText(1, 'An error occured. :(',  this.rowID); //
    }

    checkCaptcha(false); //Check if session is still alive
    if (!captchaResult){
       deleteRow()
       toggleCaptcha();
       return false;
    }

    http.send(params); // send the http reqest
    return true;
}

var serverURL = getServerURL(); //gloabal valieble to get the address from the browser
                                //this ensures that the script will work with ip/fqdn

function getServerURL(){
    serverURL = document.location.href;
    lastIndex = serverURL.lastIndexOf("/");
    serverURL = serverURL.substring(0, lastIndex + 1);
    return serverURL;
}

//messeges do be disbaled in the modal div
var messeges = {
                supportedSites:`<h4>Supported Sites</h4>
<ul>
   <li>fanfiction.net</li>
   <li>fictionpress.com</li>
   <li>adult-fanfiction.org</li>
   <li>TODO hpfanficarchive.com</li>
   <li>TODO asianfanfics.com (currently having issues)</li>
</ul>`,
                changelog:`<h4>Changelog</h4>
<ul>
<li>15.01.19 First version downloading from addult-fanfiction</li>
<li>25.01.19 Enabled convertion to other formats (txt, pdf, mobi, etc)</li>
<li>05.02.19 Added support for fictionpress and fanfiction </li>
</ul>`,
                error:'Error'
};

//show hide the modal div
function toggleHidden(divId) {
  modal.style.display = "block";
  document.getElementById("modal-text").innerHTML = messeges[divId];
}



function changeText(cellNumber, textMesg, rowId) {
  var rowId = "row"+rowId;
  var row = document.getElementById(rowId); // get the table row each row has a uniqe ID
  row.cells[cellNumber].innerHTML = textMesg; // change the cell content
}

function addRow() {
  var table = document.getElementById("downloads");
  var row = table.insertRow(rowsIndex);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  row.id = "row"+rowsIndex;
  cell1.innerHTML = "Fiction title"; //place holder
  cell2.innerHTML = "Status"; //place holder
  rowsIndex++;
}

function deleteRow() {
  var table = document.getElementById("downloads");
  rowsIndex--;
  var row = table.deleteRow(rowsIndex);
}

//Captcha

var sesionId = "";
var captchaUserInput = "";
var captchaResult = false;

function httpGet(theUrl){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send(null);

    var myObj = JSON.parse(xmlHttp.responseText);
    sesionId = myObj.id;
    return myObj;
}

function checkCaptcha(toggleInput){
    var xmlHttp = new XMLHttpRequest();
    var params = ""
    xmlHttp.open( "POST", '/checkCaptha', true ); // false for synchronous request
    xmlHttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    params += "sesionID=" + sesionId;
    if (toggleInput){
        captchaUserInput = document.getElementById("cpatcha").value;
    }
    params += "&userText=" + captchaUserInput;

    xmlHttp.onload = function() {
      if ( xmlHttp.status == 200 ) {
          if (parseInt(xmlHttp.responseText) < 0){
                document.getElementById("cpatcha").className = "searchTermError-cpatcha";
                captchaResult = false;
          }
          else{
                document.getElementById("cpatcha").className = "searchTerm-cpatcha";
                modal.style.display = "none";
                captchaResult = true;
          }
      } else {
          document.getElementById("cpatcha").className = "searchTermError-cpatcha";
      }
    }

    xmlHttp.send(params); // send the http reqest
}

function toggleCaptcha() {
  var data = httpGet("/getCaptchImg")
  modal.style.display = "block";
  var htmlCode = `<div class="center-cpatcha">
  <img src="{1}"><br>
  <input type="text" id="cpatcha" class="searchTerm-cpatcha">
  <button onclick="checkCaptcha(true)" class="searchButton-cpatcha">Go!</button>
  <button onclick="toggleCaptcha()" class="searchButton-cpatcha">New</button>`;
  var imgHtmlCode = htmlCode.replace('{1}', data.img)
  document.getElementById("modal-text").innerHTML = imgHtmlCode;
}
