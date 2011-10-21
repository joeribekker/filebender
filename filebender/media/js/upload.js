
  

formatSize = function(size) {
    if(size > 1024 * 1024 * 1024)
        return (Math.round(size * 100 / (1024 * 1024 * 1024)) / 100).toString() + 'GB';
    else if(size > 1024 * 1024)
        return (Math.round(size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
    else
        return (Math.round(size * 100 / 1024) / 100).toString() + 'KB'; 
}


var upload = {
    completed: 0,
    blockSize: 5000000,
    file: null,
    type: null,
    reader: new FileReader(),
    plainChunk: null,
    cryptChunk: null,
    fileid: null,
    key: null,
    
    states: {
        READY: 'ready',
        STARTED: 'started',
        PROGRESS: 'progress',
        COMPLETE: 'complete',
        ABORT: 'abort',
        ERROR: 'error'
    },
};


upload.state = upload.states.READY;
upload.reader.onerror = function(e) { alert(e) };

upload.selected = function() {
	this.file = document.getElementById('id_file').files[0];
	
	if(this.file) {
		document.getElementById('fileName').innerHTML = 'Name: ' + this.file.name;
		document.getElementById('fileSize').innerHTML = 'Size: ' + formatSize(this.file.size);
		document.getElementById('fileType').innerHTML = 'Type: ' + this.file.type;
	}
}


upload.start = function() {
	if(!this.file) {
	    alert("no file selected");
	    return;
	}
	

	this.key = document.getElementById('id_key').value;
	this.state = this.states.STARTED;
    upload.nextChunk();
}


upload.nextChunk = function() {
    start = this.completed;
    end = Math.min(this.blockSize, this.file.size);
    // make blob slice generic
    if (this.file.mozSlice) { // firefox
        this.slice = this.file.mozSlice(start, end);
    } else if (this.file.webkitSlice) { // chrome
        this.slice = this.file.webkitSlice(start, end);
    } else {
        alert("cant slice a blob!");
        return;
    }
    this.reader.readAsBinaryString(this.slice);
    
    this.reader.onload = function(FREvent) {
        upload.plainChunk = FREvent.target.result;
        upload.cryptChunk();
    }
}


upload.cryptChunk = function() {
    this.cryptChunk = sjcl.encrypt(this.key, this.plainChunk);
    upload.initUpload();    
}


upload.initUpload = function() {

	var builder = new BlobBuilder();
	builder.append(this.cryptChunk);
	blob = builder.getBlob();
	var fd = new FormData();
	var xhr = new XMLHttpRequest();
		
 	// TODO: should get it from current form, now gets first csrf token in page
	fd.append("csrfmiddlewaretoken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
	
	fd.append("file", blob);
	xhr.upload.addEventListener("progress", upload.uploadProgress, false);
	xhr.addEventListener("load", upload.uploadComplete, false);
	xhr.addEventListener("error", upload.uploadFailed, false);
	xhr.addEventListener("abort", upload.uploadCanceled, false);
	xhr.open("POST", "/bigfiles/upload.json/");
	xhr.send(fd);
}


upload.uploadProgress = function(evt) {
	if(evt.lengthComputable) {
		var percentComplete = Math.round(evt.loaded * 100 / evt.total);
		document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
	} else {
		document.getElementById('progressNumber').innerHTML = '??';
	}
}


upload.uploadComplete = function(evt) {
	var response = JSON.parse(evt.target.responseText);
	
	if(!upload.fileid) {
	    if (!response['fileid']) {
	       alert("didnt receive a fileID after first chunk");
	       return; 
	    }
	    upload.fileid = response['fileid']; 
	}
	
    upload.completed = upload.completed + Math.min(upload.blockSize, upload.file.size);
    if(upload.completed < upload.file.size) {
        upload.nextChunk();    
    } else {
        alert("upload complete!");
    }
    
}


upload.uploadFailed = function(evt) {
	alert("There was an error attempting to upload the file.");
}


upload.uploadCanceled = function(evt) {
	alert("The upload has been canceled by the user or the browser dropped the connection.");
}