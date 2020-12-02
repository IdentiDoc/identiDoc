$('#uploadForm').submit(function(e) {
    e.preventDefault();
    var formData =new FormData(this);
    var fileInput = document.getElementById('uploadFile');
    var file = fileInput.files[0];
    formData.append('file', file);
  
    $.ajax({
      url: '/upload',
      data: formData,
      processData: false,
      contentType: false,
      type: "POST",
      success: function(data) {
        alert('Text extracted successfully!');

        var blob = new Blob([data], {type: 'text/plain'});
        
        
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'extracted_text.txt';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
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
