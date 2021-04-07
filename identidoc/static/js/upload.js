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

function loadFile(event) {
  var output = document.getElementById('filePreview');
  var selectedFile = event.target.files[0];
  var filename = selectedFile.name;
  var fileext = filename.split('.').pop();

  if (fileext == 'heic') {

  } else if (fileext == 'pdf') {

  } else {
    output.style.visibility = 'visible';
    output.src = URL.createObjectURL(selectedFile);
    output.onload = function () {
      URL.revokeObjectURL(output.src) // free memory
    }

  }
}

function requestReceived() {
  var spinner = document.getElementById('spinner');
  spinner.style.visibility = 'hidden';

  document.getElementById('uploadFile').disabled = false;
  document.getElementById('submitFileUploadBtn').disabled = false;
}