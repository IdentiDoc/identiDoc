$(document).ready(function () {
    var classification = sessionStorage.getItem('classification');
    var signature = sessionStorage.getItem('signature');

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
        alertStr = alertStr.concat('an unrecognized document.');
    }

    if (signature == "True") {
        alertStr += ' with a signature.';
    } else if (signature == "False") {
        alertStr += ' without a signature.';
    }

    alert(alertStr);
});