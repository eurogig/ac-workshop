#!/usr/bin/env bash
# setup.sh
#
# Sets up and deploys in the correct order, the files required to deploy the admission controller in a cluster

set -euo pipefail

kubectl create secret generic admission-tls -n ac-workshop --type=Opaque --from-file=webhook.key --from-file=webhook.crt --dry-run=client -o yaml > ../ac-manifest/secret.yaml

# Apply everything in the bridgecrew directory in the correct order
kubectl apply -f ../ac-manifest/secret.yaml
kubectl apply -f ../ac-manifest/service.yaml
kubectl apply -f ../ac-manifest/deployment.yaml
kubectl apply -f ../ac-manifest/admissionconfiguration.yaml
