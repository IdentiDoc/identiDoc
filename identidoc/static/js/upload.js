alert('DEPLOYMENT SUCCESSFUL');

$('#uploadForm').submit(function(e) {
    e.preventDefault();
    var formData =new FormData(this);
    var fileInput = document.getElementById('uploadFile');
    var file = fileInput.files[0];
    formData.append('file', file);
  
    $.ajax({
      url: '/upload',
      dataType: 'json',
      data: formData,
      processData: false,
      contentType: false,
      type: "POST",
      success: function(data) {
        alert(data.message);
      },
      error: function(data) {
        try {
          alert(data.responseJSON.message);
        }

        catch(err) {
          alert(data.statusText)
        }
      }
    });  
});
