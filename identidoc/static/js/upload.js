$('#uploadForm').submit(function (e) {
  e.preventDefault();
  var formData = new FormData(this);
  var fileInput = document.getElementById('uploadFile');
  var file = fileInput.files[0];
  formData.append('file', file);

  $.ajax({
    url: '/api/upload',
    data: formData,
    processData: false,
    contentType: false,
    type: "POST",
    beforeSend: function () {
      var spinner = document.getElementById('spinner');
      spinner.style.visibility = 'visible';

      document.getElementById('uploadFile').disabled = true;
      document.getElementById('submitFileUploadBtn').disabled = true;
    },
    success: function (data) {
      requestReceived();
      var classification = data.classification;
      var signature = data.signature;

      var alertStr = 'The uploaded document was classified as '

      if (classification == "1") {
        alertStr = alertStr.concat('a 2021-2022 Cost of Attendance (COA) Adjustment Request Form (Class 1)');
      } else if (classification == "2") {
        alertStr = alertStr.concat('a 2021-2022 Verification of Household Form (Class 2)');
      } else if (classification == "3") {
        alertStr = alertStr.concat('a 2021-2022 Verification of Income - Student Form (Class 3)');
      } else if (classification == "4") {
        alertStr = alertStr.concat('an OIE CPT Academic Advisor Recommendation Form (Class 4)');
      } else if (classification == "5") {
        alertStr = alertStr.concat('an OIE CPT Student Information Form (Class 5)');
      } else {
        alertStr = alertStr.concat('an unrecognized document');
      }

      alert(alertStr);

      if (signature == "True") {
        var alertStr = "The uploaded document has a signature";
        alert(alertStr);
      } else if (signature == "False") {
        var alertStr = "The uploaded document does not have a signature";
        alert(alertStr);
      } else if (signature == "NONE") {
        // Don't alert on unknown documents
      } else {
        var alertStr = "Signature Detection Error";
        alert(alertStr);
      }

    },
    error: function (data) {
      requestReceived();
      try {
        alert(data.responseJSON.message);
      } catch (err) {
        alert(data.statusText)
      }
    }
  });
});

document.getElementById('uploadFile').addEventListener('change', async e => {
  var file = e.currentTarget.files[0];
  var filename = file.name.toLowerCase();
  var fileext = filename.split('.').pop();

  if (fileext == 'heic') {
    var blob = new Blob([file], {
      type: 'application/octet-stream'
    });

    heic2any({
      blob,
      toType: "image/jpeg",
      quality: 0.5,
      multiple: false
    }).then((value) => {
      putImageInDocPreview(URL.createObjectURL(value))
    }).catch((e) => {
      alert(e);
    });

  } else if (fileext == 'pdf') {
    var fileURL = URL.createObjectURL(file);
    var loadingTask = pdfjsLib.getDocument(fileURL);
    loadingTask.promise.then(function(pdf) {

      // Only be concerned with the first page of the pdf
      pdf.getPage(1).then(function(page) {
        var scale = 1.5;

        var viewport = page.getViewport({ scale: scale, });

        var invisibleCanvas = document.createElement('canvas');

        // Not sure if this is required, but better safe than sorry
        invisibleCanvas.style.display = 'none';

        var context = invisibleCanvas.getContext('2d');
        
        invisibleCanvas.height = viewport.height;
        invisibleCanvas.width = viewport.width;

        

        var renderContext = {
          canvasContext: context,
          viewport: viewport
        };
        
        var renderTask = page.render(renderContext);

        renderTask.promise.then(function() {
          var imageURL = invisibleCanvas.toDataURL("image/jpeg", 1.0);
          putImageInDocPreview(imageURL);
        });
      });
    });
  } else {
    putImageInDocPreview(URL.createObjectURL(file));
  }



})

/*
async function loadFile(event) {
  var output = document.getElementById('filePreview');
  var selectedFile = document.getElementById('uploadFile').files[0];
  var filename = selectedFile.name;
  var fileext = filename.split('.').pop();

  if (fileext == 'heic') {

  } else if (fileext == 'pdf') {
    let convertApi = ConvertApi.auth({
      secret: 'mR7NDI0iw9pPYFY7'
    })
    let params = convertApi.createParams()
    params.add('file', event.currentTarget.files[0]);
    let result = await convertApi.convert('pdf', 'jpg', params)

  } else {
    output.style.visibility = 'visible';
    output.src = URL.createObjectURL(selectedFile);
    output.onload = function () {
      URL.revokeObjectURL(output.src) // free memory
    }

  }
}
*/
function putImageInDocPreview(imageUrl) {
  var docPreview = document.getElementById('filePreview');
  docPreview.style.clear='both';
  docPreview.style.display = 'block';
  docPreview.src = imageUrl;
  docPreview.onload = function () {
    URL.revokeObjectURL(docPreview.src);
  }
}


function requestReceived() {
  var spinner = document.getElementById('spinner');
  spinner.style.visibility = 'hidden';

  document.getElementById('uploadFile').disabled = false;
  document.getElementById('submitFileUploadBtn').disabled = false;
}