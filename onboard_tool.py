import os
import sys
import json
import base64
import asyncio
from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic

default_wifi_creds = {
    "wifi_ssid": "nepaldigisys",
    "wifi_password": "NDS_0ffice",
    "user_id": "lomas"
}

wifi_service_uuid = "000000e1-0000-1000-8000-00805f9b34fb"
wifi_char_cred_uuid = "0000e101-0000-1000-8000-00805f9b34fb"
wifi_char_stat_uuid = "0000e102-0000-1000-8000-00805f9b34fb"
wifi_char_err_uuid = "0000e103-0000-1000-8000-00805f9b34fb"

security_service_uuid = "000000e2-0000-1000-8000-00805f9b34fb"
security_char_passkey_uuid = "0000e201-0000-1000-8000-00805f9b34fb"
security_char_factory_reset_uuid = "0000e202-0000-1000-8000-00805f9b34fb"

provisioning_service_uuid = "000000e3-0000-1000-8000-00805f9b34fb"
provisioning_char_uuid = "0000e301-0000-1000-8000-00805f9b34fb"
provisioning_status_char_uuid = "0000e302-0000-1000-8000-00805f9b34fb"

device_info_service_uuid = "000000e4-0000-1000-8000-00805f9b34fb"
device_info_char_uuid = "0000e401-0000-1000-8000-00805f9b34fb"

dynamic_config_service_uuid = "000000e5-0000-1000-8000-00805f9b34fb"
dynamic_config_char_uuid = "0000e501-0000-1000-8000-00805f9b34fb"

reboot_service_uuid = "000000e2-0000-1000-8000-00805f9b34fb"
reboot_char_uuid = "0000e202-0000-1000-8000-00805f9b34fb"

ble_connect_flag = False


def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print("Status Details:")
    print("status value: " + str(data[0]))
    if data[0] == 0x01:
        print("WiFi connection successful.")
    else:
        print("WiFi connection failed.")


def notification_handler_error(characteristic: BleakGATTCharacteristic, data: bytearray):
    print("Error Details:")
    print("Error: " + str(data))


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


def callback(sender: int, data: bytearray):
    print(f"{sender}: {data}")


async def main():
    print("scanning for 5 seconds, please wait...")

    try:
        while True:
            ble_discovered_devices = []
            devices = await BleakScanner.discover()

            for d in devices:
                try:
                    ble_device_instance = {
                        "mac": None,
                        "name": None,
                        "rssi": None
                    }

                    if (sys.platform == "win32"):
                        if d.name:
                            ble_device_instance["mac"] = d.address
                            ble_device_instance["name"] = d.name
                            ble_device_instance["rssi"] = d.rssi
                            ble_discovered_devices.append(ble_device_instance)
                    else:
                        ble_device_instance["mac"] = d.address
                        try:
                            ble_device_instance["name"] = d.details["props"]["Name"]
                        except Exception as E:
                            ble_device_instance["name"] = ""
                            print("exception: ", E)
                        ble_device_instance["rssi"] = d.details["props"]["RSSI"]
                        ble_discovered_devices.append(ble_device_instance)



                except Exception as E:
                    print("Exception at discovery:: ", E)
                    pass

            print("-" * 80)
            print(
                "------------------------------ Discovered Devices ------------------------------")
            print("-" * 80)

            print("S.N. \tname \t\t\t\tmac \t\t\trssi")
            for i in range(0, len(ble_discovered_devices)):
                print(
                    f"{str(i+1)} ---- {ble_discovered_devices[i]['name']}", end="")
                print(
                    " " * (32-len(ble_discovered_devices[i]['name'])), end="")
                print(f"{ble_discovered_devices[i]['mac']}", end="")
                print(" " * (24-len(ble_discovered_devices[i]['mac'])), end="")
                print(f"{str(ble_discovered_devices[i]['rssi'])}")

            print("-" * 50)
            print("Please choose device from the above list\n"
                  "eg. enter device S.N. \n"
                  "or Enter any character to rescan")
            selected_device = input()
            if (selected_device.isnumeric()):
                break
            else:
                print("Rescanning...")

        try:
            ble_device = ble_discovered_devices[int(selected_device) - 1]
            print("Selected Device : ")
            print(ble_device)
        except ValueError:
            print("Input value error ! Aborting !")
            pass

        ble_connect_flag = True

        # print("Do you want to connect to the device " +
        #       ble_device["name"] + ": Y/N?")
        # connect_yes_no = input()
        # if (connect_yes_no == 'Y' or connect_yes_no == 'y'):
        #     ble_connect_flag = True
        #     print("Selected Yes, Proceeding for the connection")
        #     pass
        # elif (connect_yes_no == 'N' or connect_yes_no == 'n'):
        #     ble_connect_flag = False
        #     print("Selected No, connection aborted !")
        #     pass
        # else:
        #     ble_connect_flag = False
        #     print("Unknown choice, connection aborted !")
        #     pass

        if (ble_connect_flag):
            async with BleakClient(ble_device["mac"]) as client:
                print(f"Paring - ", ble_device["name"])
                paired = await client.pair(protection_level=2)
                print(f"Paired: {paired}")

                while True:
                    if (paired):
                        print("Enter 1 for WiFi Onboarding")
                        print("Enter 2 for Device provisioning")
                        print("Enter 3 for Reading Device provisioning Info")
                        print("Enter 4 for Writing dynamic-config")
                        print("Enter 5 for Reading dynamic-config")
                        print("Enter 6 to send command to ezlopi controller")
                        print("Enter x to stop this app")

                        menu_onboarding_provisioning = input()

                        if (menu_onboarding_provisioning == '1'):  # Writing Wi-Fi credentials
                            wifi_creds = None
                            print(
                                "Do you want to share default SSID and Password, Y/N?")
                            connect_yes_no = input()
                            if (connect_yes_no == 'Y' or connect_yes_no == 'y'):
                                wifi_creds = default_wifi_creds
                            else:
                                wifi_creds["wifi_ssid"] = input(
                                    "Enter Wi-Fi SSID:")
                                wifi_creds["wifi_password"] = input(
                                    "Enter Wi-Fi Password:")
                                wifi_creds["user_id"] = default_wifi_creds["user_id"]

                            print(f"Sharing SSID: {wifi_creds['wifi_ssid']}")
                            wifi_service = client.services.get_service(
                                wifi_service_uuid)
                            wifi_write_char = wifi_service.get_characteristic(
                                wifi_char_cred_uuid)
                            await client.write_gatt_char(wifi_write_char, json.dumps(default_wifi_creds).encode('utf-8'), False)

                        # Writing device-provisioning info
                        elif (menu_onboarding_provisioning == '2'):
                            available_controllers = os.listdir(
                                path="provisioning_data_folder")

                            print("Select from controllers: ")
                            num_controllers = len(available_controllers)
                            idx = 0

                            while (idx < num_controllers):
                                print(f"{idx}. {available_controllers[idx]}")
                                idx += 1

                            selected_controller = int(input(
                                "Enter the index from avialable controllers:"))

                            if selected_controller < num_controllers:
                                print("Selected: ",
                                      available_controllers[selected_controller])

                                json_file_path = f"provisioning_data_folder/{available_controllers[selected_controller]}"
                                print("json_file_path: ", json_file_path)

                                with open(json_file_path, 'r') as json_file:
                                    try:
                                        json_data = json.load(json_file)
                                        minified_json = json.dumps(
                                            json_data, separators=(',', ':'))
                                        print(minified_json)
                                    except Exception as E:
                                        print("Exception: ", E)
                                    base64_encoded = base64.b64encode(
                                        minified_json.encode('utf-8')).decode('utf-8')
                                    print(base64_encoded)
                                    # Chunk size
                                    chunk_size = 400

                                    # Calculate the number of chunks needed
                                    num_chunks = (len(base64_encoded) +
                                                  chunk_size - 1) // chunk_size

                                    # Divide the Base64 string into chunks
                                    chunks = [base64_encoded[i:i + chunk_size]
                                              for i in range(0, len(base64_encoded), chunk_size)]

                                    # Create a list of dictionaries to store chunks
                                    chunk_list = []

                                    # Populate the list with dictionaries
                                    for idx, chunk in enumerate(chunks, start=1):
                                        chunk_data = {
                                            "total_len": len(base64_encoded),
                                            "len": len(chunk),
                                            "sequence": idx,
                                            "data": chunk
                                        }
                                        chunk_list.append(chunk_data)

                                    # Print the list of dictionaries
                                    for chunk_data in chunk_list:
                                        json_chunk = json.dumps(
                                            chunk_data, separators=(',', ':'))
                                        print(json_chunk)
                                        print("\n")
                                        prov_service = client.services.get_service(
                                            provisioning_service_uuid)
                                        prov_char = prov_service.get_characteristic(
                                            provisioning_char_uuid)

                                        try:
                                            await client.write_gatt_char(prov_char, json_chunk.encode('utf-8'), False)
                                        except Exception as e:
                                            print(
                                                "Error writing to characteristics")
                            else:
                                print("Error: Out of range selection!")

                        # Reading device-provisioning info
                        elif (menu_onboarding_provisioning == '3'):
                            base_64_data = None
                            try:
                                prov_service = client.services.get_service(
                                    device_info_service_uuid)
                                prov_char = prov_service.get_characteristic(
                                    device_info_char_uuid)

                                try:
                                    value = bytes(await client.read_gatt_char(prov_char))
                                    value_str = value.decode('utf-8')
                                    jd_value = json.loads(value_str)
                                    print("Complete json-string data: \r\n",
                                          jd_value)
                                    print("\r\n")

                                except Exception as E:
                                    print("Exception at read: ", E)

                            except Exception as E:
                                print("Exception before read: ", E)

                        elif (menu_onboarding_provisioning == '4'):  # Writing dynamic-config
                            json_file_path = 'dynamic_config.json'
                            with open(json_file_path, 'r') as json_file:
                                json_data = json.load(json_file)
                                minified_json = json.dumps(
                                    json_data, separators=(',', ':'))
                                print(minified_json)
                                base64_encoded = base64.b64encode(
                                    minified_json.encode('utf-8')).decode('utf-8')
                                print(base64_encoded)
                                # Chunk size
                                chunk_size = 400

                                # Calculate the number of chunks needed
                                num_chunks = (len(base64_encoded) +
                                              chunk_size - 1) // chunk_size

                                # Divide the Base64 string into chunks
                                chunks = [base64_encoded[i:i + chunk_size]
                                          for i in range(0, len(base64_encoded), chunk_size)]

                                # Create a list of dictionaries to store chunks
                                chunk_list = []

                                # Populate the list with dictionaries
                                for idx, chunk in enumerate(chunks, start=1):
                                    chunk_data = {
                                        "total_len": len(base64_encoded),
                                        "len": len(chunk),
                                        "sequence": idx,
                                        "data": chunk
                                    }
                                    chunk_list.append(chunk_data)

                                # Print the list of dictionaries
                                for chunk_data in chunk_list:
                                    json_chunk = json.dumps(
                                        chunk_data, separators=(',', ':'))
                                    print(json_chunk)
                                    print("\n")
                                    dynamic_config_service = client.services.get_service(
                                        dynamic_config_service_uuid)
                                    dynamic_config_char = dynamic_config_service.get_characteristic(
                                        dynamic_config_char_uuid)

                                    try:
                                        await client.write_gatt_char(dynamic_config_char, json_chunk.encode('utf-8'), False)
                                    except Exception as e:
                                        print("Error writing to characteristics")

                        elif (menu_onboarding_provisioning == '5'):  # Reading dynamic-config
                            base_64_data = None
                            try:
                                dynamic_config_service = client.services.get_service(
                                    dynamic_config_service_uuid)
                                dynamic_config_char = dynamic_config_service.get_characteristic(
                                    dynamic_config_char_uuid)

                                try:
                                    value = bytes(await client.read_gatt_char(dynamic_config_char))
                                    value_str = value.decode('utf-8')
                                    jd_value = json.loads(value_str)
                                    base_64_data = jd_value["data"]

                                    loop_for = int(
                                        jd_value["total_len"]) // 400
                                    loop_for = (
                                        loop_for + 1) if (int(jd_value["total_len"]) % 400) else loop_for
                                    loop_for -= 1
                                    print("\r\n 0")

                                    for idx in range(loop_for):
                                        value = bytes(await client.read_gatt_char(dynamic_config_char))
                                        value_str = value.decode('utf-8')
                                        jd_value = json.loads(value_str)
                                        base_64_data += jd_value["data"]

                                        print(f" {idx+1}")

                                    print("\r\n")

                                    data_bytes = base64.b64decode(base_64_data)
                                    string_json = data_bytes.decode('utf-8')
                                    # print("Complete json-string data: \r\n",
                                    #       string_json)
                                    data_dict = json.loads(string_json)
                                    j_str_data_dict = json.dumps(
                                        data_dict, indent=4)
                                    print("j_str_data_dict: \r\n",
                                          j_str_data_dict)
                                    print("\r\n")

                                except Exception as E:
                                    print("Exception at read: ", E)

                            except Exception as E:
                                print("Exception before read: ", E)

                        elif (menu_onboarding_provisioning == '6'):
                            try:
                                print(
                                    "-------------- Controller's Commands --------------")
                                print("1 - Reboot")
                                print("2 - Soft reset")
                                print("3 - Hard reset")
                                print("4 - Factory reset")
                                # pritn("5 - Authenticate")
                                command = int(
                                    input("Enter index of the command:"))
                                if (command > 0 and command < 5):
                                    command_pkt = {"cmd": command}
                                    reboot_service = client.services.get_service(
                                        reboot_service_uuid)
                                    reboot_write_char = reboot_service.get_characteristic(
                                        reboot_char_uuid)
                                    await client.write_gatt_char(reboot_write_char, json.dumps(command_pkt).encode('utf-8'), False)
                            except Exception as E:
                                print("Exception reboot controller, Exception: ", E)

                        elif (menu_onboarding_provisioning == 'x'):
                            break

                        else:
                            print("Invalid input!")

                        # status_service = client.services.get_service(device_info_service_uuid)
                        # prov_char = status_service.get_characteristic(device_info_char_uuid)
                        try:
                            read_status = await client.read_gatt_char(device_info_char_uuid)
                            print(read_status)
                        except Exception as E:
                            print("exception: ", E)
                            break

                print("Closing the connection !")
                await client.disconnect()
    except Exception as E:
        print("Exception: ", E)


asyncio.run(main())
