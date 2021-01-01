blindlibrarian.

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
  
  
  
  
Dockerfile for dockerizing. Dockerized version usage:

docker run -e 