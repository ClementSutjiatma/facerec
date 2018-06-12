

function DetectFaces(imageData) {
  AWS.region = "us-east-1";
  var rekognition = new AWS.Rekognition();
  var collectionId = "michigan";
  var course = document.getElementById("course").innerHTML;
  var params = {
    CollectionId: collectionId,
    Image: {
      Bytes: imageData
    },
    FaceMatchThreshold: 90.0,
    MaxFaces: 1
  };
  rekognition.searchFacesByImage(params, function(err, data) {
    if (err) {
      console.log(err, err.stack); // an error occurred
      document.getElementById("opResult").innerHTML = "ERROR";
    }
    else { // face is found in collection
      if(data.FaceMatches.length > 0){
        jQuery.ajax({
          type: "POST",
          url: "/confirmStudent",
          data: {
          'FaceId': data.FaceMatches[0].Face.FaceId,
          'Course': course
        },
        success: function(dataString) {
          $("#content").empty();
          document.getElementById("loading").style.display = "none";
          $("#content").prepend("<h2 style='vertical-align: center;'>" + dataString + "</h2>");
        },
        error: function(){
          console.log(data);
          document.getElementById("opResult").innerHTML = "Face not recognized";
          document.getElementById("loading").style.display = "none";
        }
      });
    }
    else{
      document.getElementById("opResult").innerHTML = "Face not recognized";
      document.getElementById("loading").style.display = "none";

      }
    }
  });


}
//Loads selected image and unencodes image bytes for Rekognition DetectFaces API
function ProcessImage(file) {
  $("#loading").css("display", "block");
  // Load base64 encoded image
  var reader = new FileReader();
  reader.onload = (function (theFile) {
    return function (e) {
      //loaderOn();
      var img = document.createElement('img');
      var image = null;
      img.src = e.target.result;
      var jpg = true;
      try {
        image = atob(e.target.result.split("data:image/jpeg;base64,")[1]);
      } catch (e) {
        jpg = false;
      }
      if (jpg == false) {
        try {
          image = atob(e.target.result.split("data:image/png;base64,")[1]);
        } catch (e) {
          alert("Not an image file Rekognition can process");
          return;
        }
      }
      //unencode image bytes for Rekognition DetectFaces API
      var length = image.length;
      imageBytes = new ArrayBuffer(length);
      var ua = new Uint8Array(imageBytes);
      for (var i = 0; i < length; i++) {
        ua[i] = image.charCodeAt(i);
      }
      DetectFaces(imageBytes);
    };
  })(file);
  reader.readAsDataURL(file);
}
