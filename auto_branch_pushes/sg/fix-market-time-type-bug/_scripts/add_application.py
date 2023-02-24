#!/usr/bin/env python3

import argparse
from dataclasses import asdict, dataclass

import oyaml as yaml  # use `oyaml` for preserve the order in original YAML

CHART_PATH="../apps-dev/chart/values.yaml"
ORIGINAL_VALUES_YAML = """
spec:
  destination:
    server: https://kubernetes.default.svc
  source:
    repoURL: https://github.com/ppluto-dev/argocd-test.git
    targetRevision: HEAD
  applications: []
"""

@dataclass
class Application:
    name: str
    path: str
    namespace: str

def addApplication(app: Application, target: str):
    try:
        with open(target, "r") as f:
            data = yaml.safe_load(f)
            # check not valid yaml 
            if type(data) == str or not ("spec" in data and "applications" in data["spec"]): 
                print("Invalid YAML format :", data)
                data = yaml.safe_load(ORIGINAL_VALUES_YAML)         
    except FileNotFoundError as e: 
        print("File not found", e)
        data = yaml.safe_load(ORIGINAL_VALUES_YAML)     

    apps =[_app for _app in data["spec"]["applications"] if _app.get('name') != app.name]
    apps.append(asdict(app))
    data["spec"]["applications"] = apps

    print("############# RESULT #############")
    print(data)
    with open(target, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True, help='The name of the argo application to be deployed')
    parser.add_argument('--path', type=str, required=True, help='The path of the argo application to be deployed')
    parser.add_argument('--namespace', type=str, required=True, help='The namespace of the argo application to be deployed')
    parser.add_argument('--target', type=str, required=True, help='The path of target values.yaml in chart')
    args = parser.parse_args()
    
    app = Application(name=args.name, path=args.path, namespace=args.namespace)
    addApplication(app=app, target=args.target)