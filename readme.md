# Spellchecker

### Setup

    docker-compose -f docker-compose.yml build web -t web
    docker-compose -f docker-compose.yml run --service-ports web
    docker exec -it <xxxspellcheckerxxx_web_run_....> python loaddata.py 

### Usage

    curl -X GET "http://localhost:31337/spelling/<WORD>/" -H "accept: application/xml"
    
    