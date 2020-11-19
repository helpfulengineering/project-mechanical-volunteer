# Healthsites.io Sample Project

This project takes advantage of the healthsites.io api to perform crowdsourcing tasks on healthcare location data.

This sample contains some simple scripts along with a docker-compose file that allows you to bring up a local instance of Pybossa based on the Dockerfile and plugins described in [backend/pybossa](/backend/pybossa/).  This can be accomplished with the following steps.

* Follow the instructions for getting a [HealthSites API Key](https://github.com/healthsites/healthsites/wiki/API) if you have not already done so

* Run the up.sh script ensuring that the HEALTHSITES_API_KEY environment variable is set with the API Key that you obtained in the first step.  Follow the prompts in the script to setup your admin user and get your personal Pybossa API Key from your new local instance.
```
export HEALTHSITES_API_KEY='put your key here'
./up.sh
```

* Grab your personal Pybossa API Key and store it in an PYBOSSA_API_KEY environment variable to avoid being prompted each time you run the ./up.sh command which will update your instance with any changes to Pybossa and upload updates to the healthsites project.

* To tear-down your local Pybossa instance created by the ./up.sh script, run ./down.sh

This is still a work in progress and is a little clunky yet!!!