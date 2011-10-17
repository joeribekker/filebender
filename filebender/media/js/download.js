if (!window.BlobBuilder && window.WebKitBlobBuilder)
	window.BlobBuilder = window.WebKitBlobBuilder;

if (!window.BlobBuilder && window.MozBlobBuilder)
	window.BlobBuilder = window.MozBlobBuilder;

if (!window.URL && window.webkitURL)
	window.URL = window.webkitURL;

//if (!window.URL.createObjectURL && window.webkitURL.createObjectURL)
//	window.URL.createObjectURL = window.webkitURL.createObjectURL;


	

function decrypt(URI) {
	var xhr = new XMLHttpRequest();
	xhr.addEventListener("load", downloadComplete, false);
	xhr.addEventListener("error", downloadFailed, false);
	xhr.addEventListener("abort", downloadCanceled, false);
	xhr.open("GET", URI);
	xhr.send();
}

function downloadComplete(evt) {
	var builder = new BlobBuilder();
	var key = prompt("Give key used for file encryption","password");
	try {
		var plain = sjcl.decrypt(key, evt.target.response);	
	} catch(e) {
		alert("wrong key");
		return;
	}
	
	builder.append(plain);
	blob = builder.getBlob();
	url = window.URL.createObjectURL(blob);
	window.location = url;
}

function downloadFailed(evt) {
	alert("There was an error attempting to download the file.");
}

function downloadCanceled(evt) {
	alert("The upload has been canceled by the user or the browser dropped the connection.");
}
