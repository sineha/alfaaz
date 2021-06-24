
const recordButton = document.querySelector('button#record');
const stopButton = document.querySelector('button#stop');
const videoContainer = document.querySelector('video#gum');
var container =  document.getElementById('container');
var output = document.getElementById('output');

let mediaRecorder;
let recordedBlobs;

var chunks = [];

document.querySelector('button#start').addEventListener('click', async () => {
    const constraints = {
      video: {
        width: 1280, height: 720
      }
    };
    // console.log('Using media constraints:', constraints);
    await init(constraints);
  });

async function init(constraints) {
    try { 
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      handleSuccess(stream);
    } catch (e) {
      console.error('navigator.getUserMedia error:', e);
      errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
    }
}

function handleSuccess(stream) {
    // console.log('getUserMedia() got stream:', stream);
    window.stream = stream;
    output.innerHTML = ""
    container.style.display = 'none'
    videoContainer.style.width = '95%';
    videoContainer.style.height = '100%';
    const gumVideo = document.querySelector('video#gum');
    videoContainer.style.display = 'block'
    gumVideo.srcObject = stream;
}

recordButton.addEventListener('click', () => {
    if (recordButton.textContent === 'Record') {
      startRecording();
    } else {
      stopRecording();
      recordButton.textContent = 'Record';
    }
  });

  function startRecording() {
    recordedBlobs = [];
    let options = {mimeType: 'video/webm;codecs=vp9,opus'};
    try {
      mediaRecorder = new MediaRecorder(window.stream, options);
    } catch (e) {
      console.error('Exception while creating MediaRecorder:', e);
      errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(e)}`;
      return;
    }
  
    // console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
    recordButton.textContent = 'Next';
    mediaRecorder.onstop = (event) => {
      // console.log('Recorder stopped: ', event);
      // console.log('Recorded Blobs: ', recordedBlobs);
    };
    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.start();
    // console.log('MediaRecorder started', mediaRecorder);
}

function handleDataAvailable(event) {
    // console.log('handleDataAvailable', event);
    if (event.data && event.data.size > 0) {
      recordedBlobs.push(event.data);
    }
}

function stopRecording() {
    mediaRecorder.stop();
    mediaRecorder.onstop = function(e) {
        // console.log("data available after MediaRecorder.stop() called.");
        
        var clipName = 'video';
    
        var clipContainer = document.createElement('article');
        var clipLabel = document.createElement('p');
        var video = document.createElement('video');
        var deleteButton = document.createElement('button');
    
        clipContainer.classList.add('clip');
        video.setAttribute('controls', '');
        deleteButton.innerHTML = "Delete";
        clipLabel.innerHTML = clipName;
    
        clipContainer.appendChild(video);
        clipContainer.appendChild(clipLabel);
        clipContainer.appendChild(deleteButton);
        // soundClips.appendChild(clipContainer);

        video.controls = true;
        console.log("recorded Blob ",chunks);
        const blob = new Blob(chunks, {type: 'video/mp4'});
        console.log("start sending binary data...");

        
         // To convert to base64 
        var reader = new FileReader(); 
        reader.readAsDataURL(blob); 
        // var base64String;
        reader.onloadend = function () { 
        var base64String = reader.result; 
        let compressedImg = base64String.split('').reduce((o, c) => {
          if (o[o.length - 2] === c && o[o.length - 1] < 35) o[o.length - 1]++;
          else o.push(c, 0);
          return o;
        },[]).map(_ => typeof _ === 'number' ? _.toString(36) : _).join('');
        $.ajax({
          type: "GET",
          url: '/Blob_Receive',
          data: {
              "result":compressedImg  ,
          },
          dataType: "json",
          success: function (data) {
              // any process in data
              alert("successfull",data)
          },
          failure: function () {
              alert("failure");
          }
      });
        // console.log('Base64 String - ', base64String); 
        // Simply Print the Base64 Encoded String, 
        // without additional data: Attributes. 
        // console.log('Base64 String without Tags- ',  
        // base64String.substr(base64String.indexOf(', ') + 1)); 
        }


        // Sending to python
        // console.log('Base64 String - ', base64String); 
      //   $.ajax({
      //     type: "GET",
      //     url: '/Blob_Receive',
      //     data: {
      //         "result":base64String ,
      //     },
      //     dataType: "json",
      //     success: function (data) {
      //         // any process in data
      //         alert("successfull",data)
      //     },
      //     failure: function () {
      //         alert("failure");
      //     }
      // });





        // To convert to base64 
        // var reader = new FileReader(); 
        // reader.readAsDataURL(blob); 
        // reader.onloadend = function () { 
        // var base64String = reader.result; 
        // console.log('Base64 String - ', base64String); 
        // // Simply Print the Base64 Encoded String, 
        // // without additional data: Attributes. 
        // console.log('Base64 String without Tags- ',  
        // base64String.substr(base64String.indexOf(', ') + 1)); 
        // }


      // Ajax code 
      // console.log("start sending binary data...");
      //   var form = new FormData();
      //   form.append('audio', blob);
      //   $.ajax({
      //   url: 'http://localhost:8000/videos/',
      //   type: 'POST',
      //   data: form,
      //   processData: false,
      //   contentType: false,
      //   success: function (data) {
      //       console.log('response' + JSON.stringify(data));
      //   },
      //   error: function () {
      //  // handle error case here
      //  console.log("error")
      //   }
      //   });




        // var blob = new Blob(chunks, { 'type' : 'videomp4; codecs=opus' });
        // chunks = [];
        // var audioURL = URL.createObjectURL(blob);
        // video.src = audioURL;
        // console.log("recorder stopped");

        // let videoURL = window.URL.createObjectURL(blob);
        // console.log("Video URL : ", videoURL)
        // deleteButton.onclick = function(e) {
        //   evtTgt = e.target;
        //   evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
        // }
      }
      mediaRecorder.ondataavailable = function(e) {
        chunks.push(e.data);
      }
}

stopButton.addEventListener('click', () => {
    // const blob = new Blob(recordedBlobs, {type: 'video/mp4'});
    // const url = window.URL.createObjectURL(blob);
    // const a = document.createElement('a');
    // a.style.display = 'none';
    // a.href = url;
    // a.download = 'video.mp4';
    // document.body.appendChild(a);
    // a.click();
    // setTimeout(() => {
    //   document.body.removeChild(a);
    //   window.URL.revokeObjectURL(url);
    // }, 100);
    stream.getTracks().forEach(function(track) {
        track.stop();
      });
    
    videoContainer.style.display = 'none'
    container.style.display = 'block'
    output.innerHTML = "Output will go here !"
  });