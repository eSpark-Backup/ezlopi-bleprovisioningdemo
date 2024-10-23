# CUSTOM FLASHER v1.0 (Tested on EZPi v4.1.6)

## Steps for Flashing and Provisioning

### 1. Generate Provisioning JSON
Run `controller_registration.py` to generate the required provisioning JSON. file will be added in `provisioning_data_folder`.

### 2. Convert JSON to C-style String
- Replace every **`"`** with **`\"`** to format it as a C-style string.

### 3. Clean up Formatting
- Remove **`\r`** by replacing it with a space.
- Replace **`\n`** with **`\\n`** for proper string formatting in C.

### 4. Modify Cloud Server Link
Append **`/getserver`** to the cloud server link in the firmware.

### 5. Update Firmware Code
Replace the existing `ezlopi_service_ble_provisioning.c` file in Ezlo's firmware with the modified C file generated from the previous steps.

### 6. Flash the Device
Build the firmware with the modified file and flash the device.

### 7. Connect to Bluetooth
- Establish a Bluetooth connection with your device.
- Use **Service 0x00E3** and **Characteristic 0xE01**.

### 8. Trigger BLE Provisioning
Send the text **`{}`** (empty JSON) to the Bluetooth characteristic to trigger BLE provisioning.

### 9. Restart the Device
Once the new provisioning is successfully written, restart the device.
