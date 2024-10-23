# CUSTOM FLASHER v1.0  
*(Tested on EZPi v4.1.6)*

## Flashing and Provisioning Guide

This guide walks you through the process of flashing your device and configuring BLE provisioning.

### 1. Generate Provisioning JSON
Run the `controller_registration.py` script to generate the provisioning JSON. The file will be saved in the `provisioning_data_folder`.

> **Note:** Before running the script, update your MIOS **username** and **password** in the following section of the script:
```python
payload = json.dumps({
    "call": "login_with_id_and_password",
    "params": {
        # "user_id": "krishna",
        # "user_password": "Krishna123*#"
        "user_id": "Ash",
        "user_password": "Berlin123"
    }
})
```

### 2. Convert JSON to C-style String
- Replace every **`"`** with **`\"`** to format the JSON as a valid C-style string.

### 3. Clean Up the Formatting
- Remove all **`\r`** and replace them with a space.
- Replace **`\n`** with **`\\n`** to ensure proper string formatting for C code.

### 4. Modify the Cloud Server Link
Update the value of the **`cloud_server`** URL in the JSON from:
``` 
https://cloud.ezlo.com:7000
```
to:
``` 
https://cloud.ezlo.com:7000/getserver
```

### 5. Replace the Firmware Code
Replace the existing `ezlopi_service_ble_provisioning.c` file in the Ezlo firmware with the modified file that you generated in previous steps.

### 6. Insert the New Provisioning JSON
Locate **line 198** in `ezlopi_service_ble_provisioning.c` and replace the old JSON with your newly generated provisioning JSON.

> **Example of the JSON string to insert:**
```c
"{\"serial\": 102003467, \"provision_server\": \"https://req-disp-at0m.mios.com/\", \"cloud_server\": \"https://cloud.ezlo.com:7000/getserver\", \"provision_token\": \"5f438a1e1d016505a987b1b7fc0f01c95545945b525dea726e2ea0f277dd4f4c20620685b6e11b1dec3a529ae6d33c3eeff63e62b03d4ec8aee14431ad6ae74f9a83d999ecc5f4e949d04f646258a44e544ac61052d585a5a9ef47990655ee039fa8218a4259a5de5039573116df25d4639bf625b4d5a078f39007a1d35d0566\", \"ssl_private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgPRH2/sNrCMcB0tclqMAL\\nvPFbDpbZZeP2RV76k4X4efqhRANCAATEF+tILMmc2c355lwnZOro78Sf2RhlIyaE\\n2baBtH9/VE1dv2q82SEJEzbzo/stRsmAVJrKwe7fJpTt1ZzAS7zW\\n-----END PRIVATE KEY-----\\n\", \"ssl_public_key\": \"-----BEGIN PUBLIC KEY-----\\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAExBfrSCzJnNnN+eZcJ2Tq6O/En9kYZSMm\\nhNm2gbR/f1RNXb9qvNkhCRM286P7LUbJgFSaysHu3yaU7dWcwEu81g==\\n-----END PUBLIC KEY-----\", \"ssl_shared_key\": \"\\n-----BEGIN CERTIFICATE-----\\nMIICCzCCAbKgAwIBAgIDBIs4MAoGCCqGSM49BAMCMIGQMQswCQYDVQQGEwJVUzEU\\nMBIGA1UECAwLIE5ldyBKZXJzZXkxEDAOBgNVBAcMB0NsaWZ0b24xDzANBgNVBAoM\\nBklUIE9wczEPMA0GA1UECwwGSVQgT3BzMRQwEgYDVQQDDAtlWkxPIExURCBDQTEh\\nMB8GCSqGSIb3DQEJARYSc3lzYWRtaW5zQGV6bG8uY29tMCAXDTIzMTExNTA5MDI1\\nNloYDzIyOTcwODI5MDkwMjU2WjCBjDELMAkGA1UEBhMCVVMxEzARBgNVBAgMCk5l\\ndyBKZXJzZXkxEDAOBgNVBAcMB0NsaWZ0b24xEzARBgNVBAoMCmNvbnRyb2xsZXIx\\nLTArBgNVBAsMJGM0NmNiYjUwLTgzOTUtMTFlZS04ODg5LTBmNTYwOTFlNzYzOTES\\nMBAGA1UEAwwJMTAyMDAzNDY3MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAExBfrSCzJ\\nnNnN+eZcJ2Tq6O/En9kYZSMmhNm2gbR/f1RNXb9qvNkhCRM286P7LUbJgFSaysHu\\n3yaU7dWcwEu81jAKBggqhkjOPQQDAgNHADBEAiANFoDtpo/ZlSyWsHa4QbybFZDf\\n7LVJQ1YnUD0MNyb4+AIga0wOQSknTlSTKBsqVEFR1vGtC9aV+TlfuPX1Qvk+IRw=\\n-----END CERTIFICATE-----\\n\", \"signing_ca_certificate\": \"-----BEGIN CERTIFICATE-----\\nMIICbDCCAhGgAwIBAgIJAOByzaI7aHY9MAoGCCqGSM49BAMDMIGQMQswCQYDVQQG\\nEwJVUzEUMBIGA1UECAwLIE5ldyBKZXJzZXkxEDAOBgNVBAcMB0NsaWZ0b24xDzAN\\nBgNVBAoMBklUIE9wczEPMA0GA1UECwwGSVQgT3BzMRQwEgYDVQQDDAtlWkxPIExU\\nRCBDQTEhMB8GCSqGSIb3DQEJARYSc3lzYWRtaW5zQGV6bG8uY29tMCAXDTE5MDUz\\nMTE3MDE0N1oYDzIxMTkwNTA3MTcwMTQ3WjCBkDELMAkGA1UEBhMCVVMxFDASBgNV\\nBAgMCyBOZXcgSmVyc2V5MRAwDgYDVQQHDAdDbGlmdG9uMQ8wDQYDVQQKDAZJVCBP\\ncHMxDzANBgNVBAsMBklUIE9wczEUMBIGA1UEAwwLZVpMTyBMVEQgQ0ExITAfBgkq\\nhkiG9w0BCQEWEnN5c2FkbWluc0BlemxvLmNvbTBWMBAGByqGSM49AgEGBSuBBAAK\\nA0IABHLQdhLDYsafIFY8pZh96aDGqVm6E4r8nW9s4CfdpXaa/R4CnjaVpDQI7UmQ\\n9vVDGZn8mcmm7VjKx+TSCS0MIKOjUzBRMB0GA1UdDgQWBBRiTl8Ez1l94jaqcxbi\\nyxkVC0FkBTAfBgNVHSMEGDAWgBRiTl8Ez1l94jaqcxbiyxkVC0FkBTAPBgNVHRMB\\nAf8EBTADAQH/MAoGCCqGSM49BAMDA0kAMEYCIQD7EUs8j50jKFd/46Zo95NbrPYQ\\nPtLTHH9YjUkMEkYD5gIhAMP4y7E1aB78nQrmd3IX8MM32k9dM8xT0MztR16OtsuV\\n-----END CERTIFICATE-----\\n\"}"
```

### 7. Flash the Device
Build the firmware with the newly modified file and flash the device using the compiled binaries.

### 8. Connect via Bluetooth
- Establish a Bluetooth connection with the device.
- Use **Service 0x00E3** and **Characteristic 0xE301**.

### 9. Trigger

 BLE Provisioning
To start BLE provisioning, send an empty JSON object (`{}`) to the Bluetooth characteristic.

### 10. Restart the Device
After successful provisioning, restart the device.

### 11. Revert Firmware Changes
Once provisioning is complete and the device is registered, revert the changes made to the `ezlopi_service_ble_provisioning.c` file by restoring the original version.
