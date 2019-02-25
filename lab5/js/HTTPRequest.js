//Global variable for Http request object
var xmlHttp = createHttpRequestObj(); 

//Create HTTP request object
function createHttpRequestObj(){
	var xmlHttpObj;
	if (window.XMLHttpRequest){
		// code for IE7+, Firefox, Chrome, Opera, Safari
		try{
			xmlHttpObj = new XMLHttpRequest();
		}catch(e){
			xmlHttpObj = false;
		}
	  }
	else{
		// code for IE6, IE5
		try{
			xmlHttpObj=new ActiveXObject("Microsoft.XMLHTTP");
		}catch(e)
		{
			xmlHttpObj =false;
		}
	}
	
	if(!xmlHttpObj)
			alert ("Cannot create the Http request object")
	else	{
		return xmlHttpObj;
	}
}

//Send HTTP request with the URL
//Function handleServerResponse() will be used to interpret the response 
function sendHttpRequest(sURL){
    if (xmlHttp.readyState==0 || xmlHttp.readyState==4)
	{
		xmlHttp.open("GET",sURL,true);
		xmlHttp.onreadystatechange = handleServerResponse;
		xmlHttp.send();
	}
	else{
		setTimeout(function(){sendHttpRequest(sURL);}, 1000);
	}
}

//Handle HTTP response
function handleServerResponse(){
	if(xmlHttp.readyState == 4){
		if(xmlHttp.status == 200){
			
			//xmlResponse is the response from the server in plain text format
			//It would be better to specify JSON format in the request URL
			//The text can be easily parsed by JSON.parse function
			xmlResponse = xmlHttp.responseText;
			
			//Handle the xmlResponse
			handleResponseData(xmlResponse);
		}

	}
}



