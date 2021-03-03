

$(document).ready(function () {
    table = $('#queryResultsTable').DataTable({
        columns: [
            {
                title: 'Uploaded File',
                data: 'filename'
            },
            {
                title: 'Document Classification',
                data: 'classification'
            },
            {
                title : 'Signature Present',
                data: 'has_signature'
            }
        ]
    });
});

function submitQuery() {
    // Get the values from the form
    var date = document.getElementById('classificationDate').value;
    var docClass = document.getElementById('documentClass').value;
    var sigPresence = document.getElementById('signatureStatus').value;

    if (date == "") {
        date = "None";
    }

    /* 
        Format of data for the form values:
        
        date = Either "None" if no date is selected or "yyyy-mm-dd"
        
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
            populateTable(data);
        },
        error: function (data) {
            alert('ERROR');
        }
    });
}

function populateTable(jsonResponse) {
    table.clear().rows.add(jsonResponse.results).draw();
}