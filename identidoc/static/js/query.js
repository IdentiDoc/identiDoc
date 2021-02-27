$('#queryForm').submit(function (e) {
    // Get the values from the form
    var date = document.getElementById('classificationDate').value;
    var docClass = document.getElementById('documentClass').value;
    var sigPresence = document.getElementById('signatureStatus').value;

    if(date == "")
    {
        date = "None";
    }

    /* 
        Format of data for the form values:
        
        date = Either "" if no date is selected or "yyyy-mm-dd"
        
        docClass = "-1" - "5"
            "-1" :      Not selected
            "0" :       Unrecognized Document
            "1"-5" :    Corresponding class number
        
        sigPresence = "-1" - "1"
            "-1" :  Not selected
            "0" :   No Signature Detected
            "1" :   Signature Detected
    */

    $.ajax({
        url: '/api/query/' + date + '/' + docClass + '/' + sigPresence,
        processData: false,
        contentType: false,
        type: "GET",
        success: function (data) {
            alert('SUCCESS');
        },
        error: function (data) {
            alert('ERROR');
        }
    });
});