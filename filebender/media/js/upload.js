
// Google chrome
if (!window.BlobBuilder && window.WebKitBlobBuilder)
	window.BlobBuilder = window.WebKitBlobBuilder;

// Firefox
if (!window.BlobBuilder && window.MozBlobBuilder)
	window.BlobBuilder = window.MozBlobBuilder;


if (!window.BlobBuilder )
	alert("no blobbuilder. Use chrome 8+ or firefox 6+")


function fileSelected() {
	var file = document.getElementById('file').files[0];
	if(file) {
		var fileSize = 0;
		if(file.size > 1024 * 1024)
			fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
		else
			fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

		document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
		document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
		document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
	}
}


function uploadFile() {
	var file = document.getElementById('file').files[0];
	
	var reader = new FileReader();
	//reader.readAsArrayBuffer(file);
	reader.readAsBinaryString(file);
	reader.onload = readComplete;
  	reader.onerror = function(e) { alert(e) };
}

function readComplete(FREvent) {
	result =  FREvent.target.result;  
	//var array = new Uint32Array(result);
	
	var key = document.getElementById('id_key').value;
	var crypt = sjcl.encrypt(key, result);
	var builder = new BlobBuilder();
	builder.append(crypt);
	blob = builder.getBlob();
	var fd = new FormData();
	var xhr = new XMLHttpRequest();
		
 	// TODO: should get it from current form, now gets first csrf token in page
	fd.append("csrfmiddlewaretoken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
	
	fd.append("file", blob);
	xhr.upload.addEventListener("progress", uploadProgress, false);
	xhr.addEventListener("load", uploadComplete, false);
	xhr.addEventListener("error", uploadFailed, false);
	xhr.addEventListener("abort", uploadCanceled, false);
	xhr.open("POST", "/bigfiles/uploadjs/");
	xhr.send(fd);
}

function uploadProgress(evt) {
	if(evt.lengthComputable) {
		var percentComplete = Math.round(evt.loaded * 100 / evt.total);
		document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
	} else {
		document.getElementById('progressNumber').innerHTML = 'unable to compute';
	}
}

function uploadComplete(evt) {
	/* This event is raised when the server send back a response */
	alert(evt.target.responseText);
}

function uploadFailed(evt) {
	alert("There was an error attempting to upload the file.");
}

function uploadCanceled(evt) {
	alert("The upload has been canceled by the user or the browser dropped the connection.");
}