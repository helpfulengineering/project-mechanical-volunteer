# VaccinateX Sample Project

This project idea stems from the VaccinateCA crowdsourcing initiative started to locate facilities that have vaccines available in California.  The sample pybossa task presenter in this sample mimics their crowdsourcing data collection screen.

This sample contains some simple scripts along with a docker-compose file that allows you to bring up a local instance of Pybossa based on the Dockerfile and plugins described in [backend/pybossa](/backend/pybossa/).  This can be accomplished with the following steps.

* Run the up.sh script.  Follow the prompts in the script to setup your admin user and get your personal Pybossa API Key from your new local instance.
```
./up.sh
```
* Grab your personal Pybossa API Key and store it in an PYBOSSA_API_KEY environment variable to avoid being prompted each time you run the ./up.sh command which will update your instance with any changes to Pybossa and upload updates to the vaccinatex project.

* To tear-down your local Pybossa instance created by the ./up.sh script, run ./down.sh

This is still a work in progress and is a little clunky yet!!!