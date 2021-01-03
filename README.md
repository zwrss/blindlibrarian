Blind Librarian

Designed to keep movie and tv-series files organized. Simple educational application.

```
Usage:
  blindlibrarian [ --api-key=<key> ] [ --dry-run ] INPUTPATH OUTPUTPATH
  blindlibrarian -h | --help
  blindlibrarian -v | --version
  
Options:
  -h, --help            Show this screen.
  -v, --version         Show version.
  INPUTPATH             Path to movies directory to be organized.
  OUTPUTPATH            Path to directory where organized movies should be placed. Do not use same directory as in INPUTPATH.
  --dry-run             Do not modify anything, just print the information.
  --api-key=<key>       Open Movie DataBase API Key - greatly increases organization correctness and cleanliness.
```
  
  
  
Dockerfile for dockerizing. Build with:
```
docker build -t blindlibrarian .
```
Dockerized version usage:
```
docker run [--env dry-run=True] [--env api-key=<omdb-key>] -v <input path>:/var/input -v <output path>:/var/output --name blindlibrarian blindlibrarian
```
