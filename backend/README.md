# Mechanical Volunteer Backend

The Mechanical Volunteer backend is currently based on pybossa whose various services are managed via Docker containers.  

## Backend structure
The backend area contains the following file/folder structure:

* pybossa: Contains the Dockerfile and dependencies for rebuilding the Mechanical Volunteer Pybossa Docker image.  This includes a plugins folder where custom plugins such as the healthsites-importer are maintained and built into the Docker image.

As other backend services that do not belong in the Pybossa instance are identified, they will be added to this folder