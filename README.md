# Muscle Strain Classification System

## Project Overview

This project implements a time series deep learning model to classify strained/damaged muscles from regular/normal muscles. The system uses EMG (Electromyography) sensor data, processes it through a neural network, and provides classification results. This technology can be applied in various settings, including:

- Gyms
- Physical therapy clinics
- Sports medicine facilities
- Occupational health offices
- Ergonomic assessment in workplaces
- Home health monitoring

## System Architecture

```mermaid
graph TD
    A[EMG Sensor] -->|Raw data| B[ESP8266 Microcontroller]
    B -->|WiFi| C[Supabase Database]
    C -->|API| D[Web Application]
    D -->|Display| E[User Interface]
    F[Neural Network Model] -->|Classification| D
    G[Feature Extraction] -->|Processed data| F
    C -->|Raw data| G
```

## Prerequisites

- Conda environment with the following packages:
  - numpy
  - tensorflow-keras
  - plotly
  - scikit-learn
  - scipy
  - pandas
  - supabase-py
- Supabase account for cloud database
- ESP8266 microcontroller with WiFi module
- EMG sensor (or simulated data for testing)

## Project Components

1. **Data Processing**: Raw EMG data is processed to extract features such as mean, max, min, frequency over duration, and duration of test.

2. **Neural Network Model**: A deep learning model is created and trained on the extracted features to classify muscle strain.

3. **Model Persistence**: The trained neural network model and scalar file (for data preprocessing) are saved for future use.

4. **Database Integration**: Supabase cloud database is used to store and retrieve EMG readings.

5. **Web Application**: A web interface is provided to display graphical reports of EMG readings and classification results.

6. **Microcontroller Code**: Arduino code for the ESP8266 to send EMG readings to the database.

### Data tab from webpage where it fetches the data and can terminate the process any time
![data](https://github.com/user-attachments/assets/e66d9660-43e0-4708-a8b7-1e208d671e4a)

### Report tab for detail information with visual representation and the test result
![report](https://github.com/user-attachments/assets/f2d14f7d-4745-4b2b-94b6-2248bd516704)

### Visual studio, Supabase and Arduino IDE
![snippets](https://github.com/user-attachments/assets/b2dfd97d-2363-4d29-b27a-b6572d2bff0b)

### Reading table where the EMG data is pushed from ESP8266 and retrieved to server
![readings table](https://github.com/user-attachments/assets/bdf7004c-2675-4459-bc92-aa43757f245f)

### Status table works as flag to know the availabilty to fetch and push
![status table](https://github.com/user-attachments/assets/19b01f8b-6551-472b-addf-d86c031e8119)


## Setup and Installation

1. Clone this repository:
   ```
   git clone https://github.com/MST-369/First-Aid-Recommender.git
   cd First-Aid-Recommender
   ```

2. Set up the Conda environment:
   ```
   conda create --name muscle_class python=3.8
   conda activate muscle_class
   conda install numpy tensorflow-keras plotly scikit-learn scipy pandas
   pip install supabase
   ```

3. Set up your Supabase project and note down the API key and URL.

4. Update the configuration file with your Supabase credentials.

5. Upload the Arduino code to your ESP8266 microcontroller.

## Usage

1. Collect EMG data using the sensor and ESP8266 setup.
2. Run the feature extraction script:
   ```
   python feature_extraction.py
   ```
3. Train the model:
   ```
   python model.py
   ```
4. Start the web application:
   ```
   streamlit run <file path>
   ```
5. Access the web interface to view results and classifications.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

[Insert your chosen license here]

## Contact

[Mani Surya Teja] - [manisuryatejak@gmail.com]

Project Link: https://github.com/MST-369/First-Aid-Recommender.git
