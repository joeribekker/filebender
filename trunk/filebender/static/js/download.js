
if (!window.URL && window.webkitURL)
	window.URL = window.webkitURL;

	

function decrypt(URI) {
	var xhr = new XMLHttpRequest();
	xhr.addEventListener("load", downloadComplete, false);
	xhr.addEventListener("error", downloadFailed, false);
	xhr.addEventListener("abort", downloadCanceled, false);
	xhr.open("GET", URI);
	xhr.send();
}

function downloadComplete(evt) {
	//todo: check for server response errors etc
	
	var builder = new BlobBuilder();
	var key = prompt("Give key used for file encryption","password");
	try {
		var plain = sjcl.decrypt(key, evt.target.response);	
	} catch(e) {
		alert("wrong key");
		return;
	}
	
    var byteArray = new Uint8Array(plain.length);
    for (var i = 0; i < plain.length; i++) {
        byteArray[i] = plain.charCodeAt(i) & 0xff;
    }
	
	builder.append(byteArray.buffer);
	blob = builder.getBlob();
	saveAs(blob, "bla");
	//url = window.URL.createObjectURL(blob);
	//window.location = url;
}

function downloadFailed(evt) {
	alert("There was an error attempting to download the file.");
}

function downloadCanceled(evt) {
	alert("The upload has been canceled by the user or the browser dropped the connection.");
}
