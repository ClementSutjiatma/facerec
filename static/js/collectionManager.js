function loaderOn(){
    $("#loading").show();
    $("#content").hide();
}
function loaderOff(){
    $("#loading").hide();
    $("#content").show();
}

//Calls DetectFaces API and shows estimated ages of detected faces
function addCollection() {
  loaderOn();
  AWS.region = "us-east-1";
  var rekognition = new AWS.Rekognition();
  var collectionId = document.getElementById("Collection").value;
  var params = {
    CollectionId: collectionId
  };
  rekognition.createCollection(params, function(err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else {
      if (data.StatusCode == 200){
        /*data = {
        CollectionArn: "aws:rekognition:us-west-2:123456789012:collection/myphotos",
        StatusCode: 200
        }*/
        document.getElementById("opResult").innerHTML = "Collection: " + collectionId  + " successfully added to Rekognition";
        jQuery.ajax({
          type: "POST",
          url: "/addCollection",
          data: {'CollectionName': collectionId,
                 'CollectionArn': data.CollectionArn
                },
        success: function(dataString) {
          $('#opResult').html("<p>" + dataString + "</p>");
        },
        error: function(){
          document.getElementById("opResult").innerHTML = "Face not recognized";
        }
      });
    }
        else {
          document.getElementById("opResult").innerHTML = "Check console for error";
        }
      }
    });
    loaderOff();
}

function delCollection() {
  loaderOn();
  AWS.region = "us-east-1";
  var rekognition = new AWS.Rekognition();
  var collectionId = document.getElementById("Collection").value;
  var params = {
    CollectionId: collectionId
  };
  rekognition.deleteCollection(params, function(err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else {
      if (data.StatusCode == 200){
        document.getElementById("opResult").innerHTML = "Collection: " + collectionId  + " successfully deleted";

        var collname=document.createElement('input');
        jQuery.ajax({
          type: "POST",
          url: "/delCollection",
          data: {'CollectionName': collectionId
        },
        success: function(dataString) {
          $('#opResult').html("<p>" + dataString + "</p>");

        },
        error: function(){
          document.getElementById("opResult").innerHTML = "Face not recognized";
        }
      });
    }
  }     // successful response
    /*
    data = {
    StatusCode: 200
  }
  */
});
loaderOff();
}

function listCollections() {
  loaderOn();
  AWS.region = "us-east-1";
  var rekognition = new AWS.Rekognition();
  var params = {};
  rekognition.listCollections(params, function(err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else { // successful response
      /*
      data = {
      CollectionIds: [
      "myphotos"]
      }
      */
      var table = "<tr><th><strong>Collection Names</strong></th></tr><br>";
      for(var i = 0; i < data.CollectionIds.length; ++i){
        table += "<tr><th>" + data.CollectionIds[i] + "</th></tr><br>";
      }

      document.getElementById("opResult").innerHTML = table;

    }
});
loaderOff();
}


function IndexFace(imageData){
  AWS.region = "us-east-1";
  var rekognition = new AWS.Rekognition();
  var collectionId = document.getElementById("curCollection").value;
  var umid = document.getElementById("umid").value;
  var uniqname = document.getElementById("uniqname").value;
  var first = document.getElementById("first").value;
  var last = document.getElementById("last").value;

  if(collectionId && umid && uniqname && first && last){
  var params = {
    CollectionId: collectionId,
    DetectionAttributes: [],
    ExternalImageId: umid,
    Image: {
        Bytes: imageData
      }
  }

  rekognition.indexFaces(params, function(err, data) {
    if (err) console.log(err, err.stack);
    else {
      console.log(data);
      var faceid = data.FaceRecords[0].Face.FaceId;
        jQuery.ajax({
            type: "POST",
            url: "/addFace",
            data: {'curCollection': collectionId,
                  'umid': umid,
                  'uniqname': uniqname,
                  'first': first,
                  'last': last,
                  'faceid': faceid
            },
            success: function(dataString) {
                $('#opResult').html('<p>' + dataString + '</p>');
                console.log(first + ' ' + last + '\' face added to collection: ' + collectionId);
            },
            error: function(){
              document.getElementById("opResult").innerHTML = "Face not added";
            }
        });
    }
  });
}
else{
  document.getElementById("opResult").innerHTML = "All fields are required";
}
}

//Loads selected image and unencodes image bytes for Rekognition DetectFaces API
function ProcessImage() {
  loaderOn();
  var control = document.getElementById("fileToUpload");
  var file = control.files[0];

  // Load base64 encoded image
  var reader = new FileReader();
  reader.onload = (function (theFile) {
    return function (e) {
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
      //Call Rekognition
      IndexFace(imageBytes);
      loaderOff();
    };
  })(file);
  reader.readAsDataURL(file);
}
