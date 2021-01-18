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

<!--- TODO - ADD SECTION TO DESCRIBE THE DOCUMENTS THAT ARE IDENTIFIED USING IDENTIDOC -->

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

### Database

sqlite is used for the identiDoc database due to its ease of use and integration within python3. A database module handles all database interactions and honors CQS principles. Data is validated prior to executing the SQL query or command for security purposes.
