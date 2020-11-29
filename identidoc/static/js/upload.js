$('#uploadForm').submit(function(e) {
    e.preventDefault();
    var formData =new FormData(this);
    var fileInput = document.getElementById('uploadFile');
    var file = fileInput.files[0];
    formData.append('FILE_NAME', file);
  
    $.ajax({
      url: 'http://127.0.0.1:5000/upload',
      dataType: 'json',
      data: formData,
      processData: false,
      contentType: false,
      type: "POST",
      success: function(data) {
        alert('SUCCESS');
      },
      error: function(data) {
        alert('ERROR');
      }
    });  
});
