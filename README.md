# Rideau Canal Skateway - Real-Time Monitoring System

## Scenario Description

The Rideau Canal Skateway, as the world's largest naturally frozen skating rink, requires close environmental monitoring to ensure safety and usability. This project addresses the challenge of monitoring conditions like ice thickness and surface temperature in real-time using a simulated IoT-based cloud solution. The system simulates sensor data, processes it in real time, and stores output data in Azure Blob Storage for analysis.

---

## System Architecture

The system consists of:

- Simulated IoT sensors generating environmental telemetry data.
- Azure IoT Hub ingesting this data.
- Azure Stream Analytics processing the data using SQL-based filters.
- Azure Blob Storage storing the filtered output in JSON format.
```
+------------------------------+
|   Python Sensor Simulator    |
| (simulate_sensors.py script) |
|  - Generates JSON payloads   |
|  - Sends data every 10 sec   |
+------------------------------+
               |
               v
+------------------------------+
|         Azure IoT Hub        |
| - Receives telemetry data    |
| - Device: simulator001       |
| - Endpoint: messages/events  |
+------------------------------+
               |
               v
+-----------------------------------------+
|     Azure Stream Analytics Job          |
| - Input: iothubinput (from IoT Hub)     |
| - Query: SELECT ... WHERE ice < 20      |
| - Output: bloboutput (to Blob Storage)  |
+-----------------------------------------+
               |
               v
+-----------------------------------------+
|         Azure Blob Storage              |
| - Container: canaldata                  |
| - Path: output/{date}/{time}/           |
| - Format: JSON                          |
| - Sample: output.json                   |
+-----------------------------------------+

```
---

## Implementation Details

### IoT Sensor Simulation

Python scripts were used to simulate temperature, snow accumulation, ice thickness, and external temperature from three locations: Dow’s Lake, Fifth Avenue, and NAC. Each device sends data every 10 seconds in the following JSON structure:

```json
{
  "location": "Dow's Lake",
  "iceThickness": 18,
  "surfaceTemperature": -4.2,
  "snowAccumulation": 10,
  "externalTemperature": -15.3,
  "timestamp": "2025-04-13T18:07:52Z"
}
```

The simulator script is located in the `sensor-simulation/` directory.

### Azure IoT Hub Configuration

- A free-tier IoT Hub was created.
- A device `simulator001` was registered.
- The connection string was used in the Python script to authenticate and send telemetry.
- Default endpoint (`messages/events`) was used.

### Azure Stream Analytics Job

- **Input**: IoT Hub (alias `iothubinput`)
- **Output**: Azure Blob Storage (alias `bloboutput`)
- **Query Logic**:

```sql
SELECT
    location,
    iceThickness,
    surfaceTemperature,
    snowAccumulation,
    externalTemperature,
    timestamp
INTO
    bloboutput
FROM
    iothubinput
WHERE
    iceThickness < 20
```

### Azure Blob Storage

- A container named `canaldata` was created.
- Output is stored in the path format: `output/{date}/{time}/`.
- Files are stored in JSON format with UTF-8 encoding.

---

## Usage Instructions

### Running the IoT Sensor Simulation

1. Install Python 3.13 and Azure IoT SDK:  
   `pip install azure-iot-device`
2. Navigate to the `sensor-simulation` directory.
3. Run the script:  
   `python simulate_sensors.py`

### Configuring Azure Services

1. Create IoT Hub and register a device.
2. Create a Stream Analytics Job.
3. Set the input to the IoT Hub and output to Blob Storage.
4. Use the provided SQL query.
5. Start the job and monitor messages in Azure.

### Accessing Stored Data

- Navigate to Azure Storage → `canaldata` container.
- Locate files in `output/yyyy/mm/dd/hh` structure.
- Files are in JSON format and downloadable.

---

## Results

- The system filters and stores only the readings where `iceThickness < 20`.
- A sample output is shown below:

```json
{"location":"Dow's Lake","iceThickness":14,"surfaceTemperature":-9.5,"snowAccumulation":16,"externalTemperature":-12.2,"timestamp":"2025-04-13T18:10:08Z"}
{"location":"Fifth Avenue","iceThickness":13,"surfaceTemperature":-3.1,"snowAccumulation":5,"externalTemperature":-6.9,"timestamp":"2025-04-13T18:10:19Z"}
```

Full output is stored in: `sample-output/output.json`

---

## Reflection

This project involved learning Azure’s IoT and analytics workflow from scratch. Configuring Stream Analytics also wasn’t straightforward. I had to make sure the input/output aliases matched exactly, and the query syntax had to be carefully written or the job wouldn't run.

---
