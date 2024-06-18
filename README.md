# Air Quality Index Prediction Model Utilizing Random Forest and NodeMCU

## Overview

This project aims to predict the Air Quality Index (AQI) using a Random Forest model and real-time data collected from sensors interfaced with a NodeMCU. The AQI prediction model is deployed on a Flask server, and the data is stored in an SQLite database. The complete research and implementation details are published [here](https://doi.org/10.36227/techrxiv.171863926.61778965/v1).

## Components

1. **NodeMCU**: Collects real-time data from various air quality sensors.
2. **Flask Server**: Receives data from NodeMCU, predicts AQI, and stores the data.
3. **Random Forest Model**: Trained to predict AQI from sensor data.
4. **SQLite Database**: Stores historical AQI data.

## Prerequisites

- Python 3.x
- NodeMCU
- Air quality sensors (e.g., PM2.5, PM10, SO2, NOx, NH3, CO, O3 sensors)
- Arduino IDE

## Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/your-repo/Air-Quality-Index-Prediction-Model-Utilizing-Random-Forest-and-NodeMCU
   cd Air-Quality-Index-Prediction-Model-Utilizing-Random-Forest-and-NodeMCU

2. **Set up the Python environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt

3. **Initialize the SQLite Database**

   ```sh
   python server.py  # This will initialize the database

4. **Upload the Arduino Code**

   - Navigate to the directory where `nodemcu_code.ino` is located.
   - Open `Sensors` in the Arduino IDE.
   - Locate the section of the code where WiFi credentials and server IP address are defined.
   - Update the variables `ssid`, `password`, `serverAddress`, and `serverPort` with your WiFi credentials and server details.
   - Connect your NodeMCU to your computer using a USB cable.
   - Select the appropriate board and port from the Arduino IDE menu.
   - Click on the "Upload" button in the Arduino IDE to compile and upload the code to your NodeMCU.

## Usage

1. **Start the Flask Server**

   ```sh
   python server.py # The server will be available at http://0.0.0.0:5000.

2. **NodeMCU Data Collection**

   - The NodeMCU collects data from sensors and sends it to the Flask server.

## Project Structure

- **server.py**: Flask server code to handle incoming data and store it in the SQLite database.
- **model_train.py**: Script to train the Random Forest model.
- **random_forest_model.pkl**: Trained Random Forest model.
- **Sensors**: Arduino code for NodeMCU to read sensor data and send it to the Flask server.
- **requirements.txt**: Python dependencies.

## Detailed Description

1. **Server Code**

   - The server code sets up a Flask server to handle incoming data from the NodeMCU, predicts AQI using a pre-trained Random Forest model, and stores the data in an SQLite database.

2. **Model Training**

   - The model training script trains a Random Forest model on historical AQI data. The model is saved as **random_forest_model.pkl**. The dataset used for training can be found [here](https://drive.google.com/drive/folders/1yI4jUN4x_kFC7xQqQgSn_TlGoppjQENx?usp=sharing).

3. **NodeMCU Code**

   - The NodeMCU code reads data from various air quality sensors and sends it to the Flask server. The NodeMCU connects to a WiFi network and communicates with the server over HTTP.

4. **Dependencies**

   - The dependencies for this project are listed in the **requirements.txt** file and can be installed using pip.

     
   - ```sh
     pip install -r requirements.txt
## Conclusion

  - This project demonstrates how to use a Random Forest model and NodeMCU to predict and monitor air quality in real-time. The integration of machine learning with IoT devices enables efficient and accurate AQI predictions, which can be crucial for environmental monitoring and public health.


