# Spellchecker

### Setup

    docker-compose -f docker-compose.yml build web
    docker-compose -f docker-compose.yml run --service-ports web

### Usage

    curl URL: http://localhost:31337/spelling/<WORD>
    
    
    