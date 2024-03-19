## Project Description
This project is an extension of the previous homework #4, where I wrote a Python script to track the International Space Station (ISS) was developed. The goal of this homework is to transform the ISS tracking script into a full Flask web application. The Flask application provides various routes to interact with the ISS data, including retrieving the entire dataset, querying specific epochs, and calculating instantaneous speed.

## Dataset Description
The ISS data is retrieved from the [NASA public data repository](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml), which provides real-time coordinates and velocity vectors of the ISS.

## Running the Application
To run the Flask application in a Docker container, follow these steps:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/daiarag/daiara-coe332-hws

2. cd daiara-coe332-hws/homework05

3. docker build -t iss-tracker .

4. docker run -d -p 5000:5000 iss-tracker

Docker images:
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS                   PORTS     NAMES
2e992c1c8cc5   daiarag/homework05:1.0   "python iss_tracker.…"   21 seconds ago   Created                            homework05-iss_tracker


