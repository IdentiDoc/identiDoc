# identiDoc - The Future of Document Classification

identiDoc is a Senior Design Project for The University of Texas at Arlington for the 2020-2021 Academic Year and sponsored by State Farm. identiDoc is a document identification solution in which a user will be able to upload a file for classification into different document classes and will also be able to detect whether or not a signature is present on the document.

identiDoc uses the Flask framework.

### Team Members

The identiDoc Development Team consists of the following members

* *Jonathan Marek, Scrum Master and Developer*
* *Roshan Shrestha, Product Owner and Developer*
* *Pawan Khadka, Developer*
* *Sandesh Koirala, Developer*
* *Abhinaw Shahi, Developer*

### Environment Setup

identiDoc is written primarily in python3 and utilizes a virtual environment to properly run. The environment is set up by running the setup script with the following command:

```bash
. setup_env.sh
```

identiDoc is primarily developed and hosted using ubuntu 20.04. This is not a hard requirement, but apt is used to install dependencies. In theory, identiDoc should run on other operating systems, but they are not officially supported.

### DevOps

identiDoc uses CircleCI to support a robust CI/CD pipeline. Whenever commits are pushed to any remote branch, the continuous integration pipeline automatically creates a test environment and runs all unit tests which are stored in the tests directory. Any failures are quickly reported to the development team, so they can be fixed at the source. Whenever a pull request is created and approved to merge a branch into the main branch, the continuous deployment pipeline deploys the changes automatically. In production, identiDoc is served using uWSGI and nginx. The production server can be found at http://68.183.142.39/

### API

The identiDoc API is a RESTful API developed using the Flask-RESTful library.
* GET /api/query/\<date\>/\<classification\>/\<signature\>
-- This endpoint sends in parameters for the query which receives classification results. The user will receive a JSON response of results in the database.
-- date is a string of this form "YYYY-MM-DD" or the string "None"
-- classification is a string that is a single number in the range -1 to 5 inclusive. "-1" represents no filtering, "0" is an unrecognized document, and "1" - "5" is the class of the document
-- signature is a string equal to "-1", "0", or "1". "-1" represents no filtering, "0" is no signature present, and "1" is a present signature.

* POST /api/upload - This endpoint allows the user to upload a file for classification.
-- A file is attached to this request for upload under the header "file"

* GET /api/download/\<filename\> - This endpoint will allow the user to download the classified file. Note - this endpoint should only be used within a query. A timestamp is necessary to use this endpoint appropriately. See identidoc/static/js/query.js for an example

### Database

sqlite is used for the identiDoc database due to its ease of use and integration within python3. A database module handles all database interactions and honors CQS principles. Data is validated prior to executing the SQL query or command for security purposes.

### Document Preprocessing

Once a document has been uploaded, it is converted into a cv2 image. Then, its orientation is checked. If the orientation is not right, the image is rotated to the correct orientation. The rotated image is converted to a gray-scaled image and then to a final binary image. Finally, the binary image is fed to the python tesseract model and the extracted text is fed into the document classification module.

### Document Classification

### Signature Detection

identiDoc uses YOLOV3 (You Only Look Once Version 3), a real time object detection system, to detect whether or not a signature is present on a recognized document. Once a document is classified as a recognized document, it is passed to the signature detection module to check for signature presence. If a signature is detected with a confidence value of at least 50%.
