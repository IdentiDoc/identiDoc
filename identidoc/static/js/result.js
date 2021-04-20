$(document).ready(function () {
    var docPreview = document.getElementById('filePreview');

    docPreview.src = '/static/img/yolo_prediction.jpg?' + new Date().getTime();

    var classification = sessionStorage.getItem('classification');
    var signature = sessionStorage.getItem('signature');

    var classStr = 'The uploaded document was classified as '

    if (classification == "1") {
        classStr = classStr.concat('a 2021-2022 Cost of Attendance (COA) Adjustment Request Form (Class 1)');
    } else if (classification == "2") {
        classStr = classStr.concat('a 2021-2022 Verification of Household Form (Class 2)');
    } else if (classification == "3") {
        classStr = classStr.concat('a 2021-2022 Verification of Income - Student Form (Class 3)');
    } else if (classification == "4") {
        classStr = classStr.concat('an OIE CPT Academic Advisor Recommendation Form (Class 4)');
    } else if (classification == "5") {
        classStr = classStr.concat('an OIE CPT Student Information Form (Class 5)');
    } else {
        classStr = classStr.concat('an unrecognized document.');
    }

    if (signature == "True") {
        classStr += ' with a signature.';
    } else if (signature == "False") {
        classStr += ' without a signature.';
    }

    var result = document.getElementById('classificationResult');
    result.innerHTML = classStr;
});