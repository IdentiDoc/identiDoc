$('#uploadForm').submit(function(e) {
    e.preventDefault();
    var formData =new FormData(this);
    var fileInput = document.getElementById('uploadFile');
    var file = fileInput.files[0];
    formData.append('FILE_NAME', file);
  
    $.ajax({
      url: '/upload',
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
