import argparse
from dataclasses import asdict, dataclass

import oyaml as yaml  # use `oyaml` for preserve the order in original YAML

@dataclass
class Application:
    name: str
    path: str
    namespace: str

CHART_PATH="../apps/values.yaml"

def addApplication(app: Application):
    with open(CHART_PATH, "r") as f:
        data = yaml.safe_load(f)
    
    if "spec" in data and "applications" in data["spec"] :
        data["spec"]["applications"].append(asdict(app))
    else:
        print("No `.Values.spec.applications` field")
        exit(1)

    print("############# RESULT #############")
    print(data)
    with open(CHART_PATH, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True, help='The name of the argo application to be deployed')
    parser.add_argument('--path', type=str, required=True, help='The path of the argo application to be deployed')
    parser.add_argument('--namespace', type=str, required=True, help='The namespace of the argo application to be deployed')
    args = parser.parse_args()
    
    app = Application(name=args.name, path=args.path, namespace=args.namespace)
    addApplication(app)