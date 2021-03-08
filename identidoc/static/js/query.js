

$(document).ready(function () {
    table = $('#queryResultsTable').DataTable({
        columns: [
            {
                title: 'Upload Date',
                data: 'timestamp',
                // data is a UNIX timestamp
                render: function(data, type, row, meta) {
                    var a = new Date(data * 1000);
                    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                    var month = months[a.getMonth()];
                    var date = a.getDate();
                    var year = a.getFullYear();0

                    return month + ' ' + String(date) + ', ' + year;
                }
            },
            {
                title: 'Uploaded File',
                data: 'filename',
                render: function(data, type, row, meta) {
                    var filename = String(row.timestamp) + '.' + data;
                    return '<a href="/api/download/' + filename + '">' + data + '</a>';
                }
            },
            {
                title: 'Document Classification',
                data: 'classification',
                render: function(data, type, row, meta) {
                    switch(data)
                    {
                        case 1:
                            return 'Class 1 - Cost of Attendance Adjustment Request';
                        case 2:
                            return 'Class 2 - Verification of Household';
                        case 3:
                            return 'Class 3 - Verification of Income Student';
                        case 4:
                            return 'Class 4 - CPT Academic Advisor Recommendation';
                        case 5:
                            return 'Class 5 - CPT Student Information'
                        case 0:
                            return 'Unrecognized Document'
                        default:
                            return '';
                    }
                }
            },
            {
                title : 'Signature Present',
                data: 'has_signature',
                render: function(data, type, row, meta) {
                    if(data == 0)
                    {
                        return 'No Signature Present';
                    }

                    return 'Signature Present';
                }
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
