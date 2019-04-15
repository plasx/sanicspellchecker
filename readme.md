# Spellchecker
This is a spellchecker which compares to a preloaded list of word from a file into redis in Sanic.
Runs on port 31337.
Return 404 if the word is not found.
Return 200 if the word is found.

### Setup

    docker-compose -f docker-compose.yml build web -t web
    docker-compose -f docker-compose.yml run --service-ports web
    docker exec -it <xxxspellcheckerxxx_web_run_....> python loaddata.py 

### Usage

    curl -X GET "http://localhost:31337/spelling/<WORD>/" -H "accept: application/xml"
    
### Unit Tests
After you build and run the application, to run unit tests, simply run:

    docker exec -it <xxxspellcheckerxxx_web_run_....> python -m unittest tests.py` 
