// Google chrome
if (!window.BlobBuilder && window.WebKitBlobBuilder)
	window.BlobBuilder = window.WebKitBlobBuilder;

// Firefox
if (!window.BlobBuilder && window.MozBlobBuilder)
	window.BlobBuilder = window.MozBlobBuilder;
	

function decrypt(URI) {
	var xhr = XMLHttpRequest();
	xhr.addEventListener("load", downloadComplete, false);
	xhr.addEventListener("error", downloadFailed, false);
	xhr.addEventListener("abort", downloadCanceled, false);
	xhr.open("GET", URI);
	xhr.send();
}

function downloadComplete(evt) {
	var builder = new BlobBuilder();
	builder.append(evt.target.response);
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
