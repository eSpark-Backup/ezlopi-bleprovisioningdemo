import os
import json
import requests

url = "https://api-cloud.ezlo.com/v1/request"

payload = json.dumps({
    "call": "login_with_id_and_password",
    "params": {
        # "user_id": "krishna",
        # "user_password": "Krishna123*#"
        "user_id": "Ash",
        "user_password": "Berlin123"
    }
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
j_login_response = json.loads(response.text)

if (1 == j_login_response["status"] and 1 == j_login_response["complete"]):
    print("Login successful\r\n")
    new_controller_name = input("Enter your controller's name: ")
    print("Creating controller: ", new_controller_name)
    j_data = j_login_response["data"]
    j_token = j_data["token"]
    # print("Token:\r\n", j_token)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {j_token}',
    }

    payload = json.dumps({
        "call": "self_provision_request",
        "params": {
            "description": f"{new_controller_name}",
            "meta": {}
        }
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    j_controller_registration_response = json.loads(response.text)
    print(response.text)

    # testing-purpose only
    # j_controller_registration_response = json.loads(
    #     '{"status":1,"complete":1,"data":{"uuid":"c5645e21-edc5-49a2-9854-b15fc8da5434"}}')

    if (1 == j_controller_registration_response["status"] and 1 == j_controller_registration_response["complete"]):
        try:
            j_data = j_controller_registration_response["data"]
            new_controller_uuid = j_data["uuid"]
            print(f"{new_controller_name} registered as UUID: {new_controller_uuid}.")

            payload = json.dumps({
                "call": "self_provision_get",
                "params": {
                    "uuid": f"{new_controller_uuid}"
                }
            })

            response = requests.request(
                "POST", url, headers=headers, data=payload)

            j_controller_provisioning_data = json.loads(response.text)
            # print(j_controller_provisioning_data)

            if (1 == j_controller_provisioning_data["status"] and 1 == j_controller_provisioning_data["complete"]):
                j_data = j_controller_provisioning_data["data"]

                controller_uuid = j_data["controller_uuid"]
                timestamp = j_data["timestamp"]
                description = j_data["description"]

                provision_data = json.loads(j_data["provision_data"])

                try:
                    uuid = provision_data["uuid"]
                    cloud_uuid = provision_data["cloud_uuid"]
                    order_uuid = provision_data["order_uuid"]
                    config_version = provision_data["config_version"]
                    zwave_region = provision_data["zwave_region"]
                    provision_server = provision_data["provision_server"]
                    cloud_server = provision_data["cloud_server"]
                    provision_token = provision_data["provision_token"]
                    provision_order = provision_data["provision_order"]
                    ssl_private_key = provision_data["ssl_private_key"]
                    ssl_public_key = provision_data["ssl_public_key"]
                    ssl_shared_key = provision_data["ssl_shared_key"]
                    signing_ca_certificate = provision_data["signing_ca_certificate"]
                    default_wifi_ssid = provision_data["default_wifi_ssid"]
                    default_wifi_password = provision_data["default_wifi_password"]
                    default_ssh_password = provision_data["default_ssh_password"]

                    file_location = f"provisioning_data_folder/{provision_data['id']}.json"

                    try:
                        os.remove(file_location)
                    except Exception as E:
                        pass
                    with open(file_location, 'w') as file:
                        prov_file_data = {}
                        prov_file_data["serial"] = provision_data["id"]
                        prov_file_data["provision_server"] = provision_data["provision_server"]
                        prov_file_data["cloud_server"] = provision_data["cloud_server"]
                        prov_file_data["provision_token"] = provision_data["provision_token"]
                        prov_file_data["ssl_private_key"] = provision_data["ssl_private_key"]
                        prov_file_data["ssl_public_key"] = provision_data["ssl_public_key"]
                        prov_file_data["ssl_shared_key"] = provision_data["ssl_shared_key"]
                        prov_file_data["signing_ca_certificate"] = provision_data["signing_ca_certificate"]
                        prov_file_data["uuid"] = provision_data["uuid"]
                        prov_file_data["user_id"] = "krishna"
                        prov_file_data["device_name"] = new_controller_name
                        prov_file_data["brand"] = "Ezlo-Pi"
                        prov_file_data["manufacturer_name"] = "Nepal Digital System"
                        prov_file_data["model_number"] = "NT-3.0.4.x"
                        prov_file_data["mac"] = "11:22:33:44:55:66"
                        prov_file_data["uuid_provisioning"] = provision_data["cloud_uuid"]
                        prov_file_data["device_type_ezlopi"] = "generic"

                        print("Controller-Serial: ", provision_data["id"])

                        j_str_file_data = json.dumps(prov_file_data)

                        if file.write(j_str_file_data) > 0:
                            print(
                                "Successfully saved provisioning-info of new controller.")
                        else:
                            print("Error: Failed to save provisoing-info!")

                except Exception as E:
                    print("Exception: ", E)

        except Exception as E:
            print("Error: failed creating new controller")
            print("Exception: ", E)
