import argparse

import oyaml as yaml  # use `oyaml` for preserve the order in original YAML

CHART_PATH="../apps"

def deleteApplication(name: str):
    with open(f"{CHART_PATH}/values.yaml", "r") as f:
        data = yaml.safe_load(f)
    
    if "spec" in data and "applications" in data["spec"] :
        apps = data["spec"]["applications"]
        apps[:] = [app for app in apps if app.get('name') != name]
    else:
        print("No `.Values.spec.applications` field")
        exit(1)
        
    print("############# RESULT ############## ")
    print(data)
    with open("file.yaml", "w") as f:
        yaml.safe_dump(data, f, sort_keys=False) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True, help='The name of the argo application to be deployed')
    args = parser.parse_args()

    deleteApplication(args.name)