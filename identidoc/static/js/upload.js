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

      stashResults(data);

      location.href = '/result';
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


function stashResults(data) {

  var classification = data.classification;
  var signature = data.signature;

  sessionStorage.setItem('classification', classification);
  sessionStorage.setItem('signature', signature);
}

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
    loadingTask.promise.then(function (pdf) {

      // Only be concerned with the first page of the pdf
      pdf.getPage(1).then(function (page) {
        var scale = 1.5;

        var viewport = page.getViewport({
          scale: scale,
        });

        var invisibleCanvas = document.createElement('canvas');

        // Not sure if this is required, but better safe than sorry
        invisibleCanvas.style.visibility = 'hidden';

        var context = invisibleCanvas.getContext('2d');

        invisibleCanvas.height = viewport.height;
        invisibleCanvas.width = viewport.width;



        var renderContext = {
          canvasContext: context,
          viewport: viewport
        };

        var renderTask = page.render(renderContext);

        renderTask.promise.then(function () {
          var imageURL = invisibleCanvas.toDataURL("image/jpeg", 1.0);
          putImageInDocPreview(imageURL);
        });
      });
    });
  } else {
    putImageInDocPreview(URL.createObjectURL(file));
  }
})

function putImageInDocPreview(imageUrl) {
  var docPreview = document.getElementById('filePreview');
  docPreview.style.clear = 'both';
  docPreview.style.visibility = 'visible';

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