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
        alertStr = alertStr.concat('an unrecognizable document');
      }

      alert(alertStr);

      if (signature == "True") {
        var alertStr = "The uploaded document has a signature";
      } else if (signature == "False") {
        var alertStr = "The uploaded document does not have a signature";
      } else {
        var alertStr = "Signature Detection Error";
      }

      alert(alertStr);
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
  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function () {
    URL.revokeObjectURL(output.src) // free memory
  }
}

function requestReceived() {
  var spinner = document.getElementById('spinner');
  spinner.style.visibility = 'hidden';
}