# Discuss AI 
Discuss AI is a PDF parser that finds answers for you by return image snapshots of possible answer in your textbook. The backend API is built on Django and Django Rest Framework with a PostgreSQL database. File storage and textbook searching for answers was done using Azure Storages and Azure's Computer Vision API.
## Django Installation
From command line:
- `pip install Django==3.0.6`

## Clone the repo:
From command line:
- `cd (path to the directory you want)`
- `git clone https://github.com/rolfxli/hackthe6ix2020backend`
You may also use the clone button on the repository along with Github Desktop

## Run the Django server:
From the command line:
- `cd ~/hackthe6ix2020backend/discussAI`
- `python manage.py runserver`
Open a browser, and go to http://127.0.0.1:8000/api/documents/
to view an example of documents 

# Admin Page
Open a browser, and go to http://127.0.0.1:8000/admin.
Enter you credentials and you should be able to edit the models.
