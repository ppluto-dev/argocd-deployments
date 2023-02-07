import argparse

import oyaml as yaml  # use `oyaml` for preserve the order in original YAML


def deleteApplication(name: str, target: str):
    try:
        with open(target, "r") as f:
            data = yaml.safe_load(f)
            # check not valid yaml 
            if type(data) == str or not ("spec" in data and "applications" in data["spec"]): 
                print("Invalid YAML format :", data)
                exit(1)         
    except FileNotFoundError as e: 
        print("File not found", e)
        exit(1) 
        
    apps = data["spec"]["applications"]
    apps[:] = [app for app in apps if app.get('name') != name]
        
    print("############# RESULT ############## ")
    print(data)
    with open(target, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True, help='The name of the argo application to be deployed')
    parser.add_argument('--target', type=str, required=True, help='The path of target values.yaml in chart')
    args = parser.parse_args()

    deleteApplication(name=args.name, target=args.target)