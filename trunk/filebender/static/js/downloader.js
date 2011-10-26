
if (!window.URL && window.webkitURL)
	window.URL = window.webkitURL;


var downloader = {
    xhr: new XMLHttpRequest(),
    filename: null,
};


downloader.start = function(URI, filename) {
    downloader.filename = filename;
    downloader.xhr.addEventListener("progress", downloader.progress, false);
    downloader.xhr.addEventListener("load", downloader.complete, false);
    downloader.xhr.addEventListener("error", downloader.failed, false);
    downloader.xhr.addEventListener("abort", downloader.canceled, false);
	downloader.xhr.open("GET", URI);
	downloader.xhr.send();
};


downloader.complete = function (evt) {
	//todo: check for server response errors etc
	
	var builder = new BlobBuilder();
	var key = prompt("Give key used for file encryption", "password");
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
	saveAs(blob, downloader.filename);
}

 
downloader.progress = function (evt) {  
    if (evt.lengthComputable) {  
        var percentComplete = evt.loaded / evt.total;  
    } else {  
        pass;
    }  
}  


downloader.failed = function(evt) {
	alert("There was an error attempting to download the file.");
}


downloader.canceled = function(evt) {
	alert("The upload has been canceled by the user or the browser dropped the connection.");
}
