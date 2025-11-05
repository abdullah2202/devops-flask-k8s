# Containerized Flask App on Kubernetes with End-to-End Monitoring

## Description

This project showcases a full-stack DevOps workflow by deploying a containerized Flask application onto a local Kubernetes cluster (Kind) and implementing robust monitoring using the Prometheus/Grafana stack.

* **Docker:** Containerizing a Python application using a multi-stage `Dockerfile`.
* **Kubernetes (K8s):** Defining deployments, services, and ingress using declarative YAML manifests. Utilizing Liveness and Readiness Probes.
* **Networking:** Configuring Kubernetes Services (`ClusterIP`) and external exposure via an **Ingress Controller**.
* **Observability (DevOps):** Implementing Prometheus (metrics scraping) and Grafana (data visualization) to monitor application and cluster health.
* **Tooling:** Using **Kind** for local cluster simulation and **Helm** for package management.

## Prerequisites

To deploy and test this project locally, you must have the following tools installed on your server:

1.  **Git**
2.  **Docker**
3.  **Kind**
4.  **kubectl**
5.  **Helm**

## Deployment Steps (One-Time Setup)

Follow these steps on your Ubuntu server to deploy the entire stack.

### 1. Clone Repository and Build Image

```bash
# Clone the repository
git clone https://github.com/abdullah2202/devops-flask-k8s
cd devops-flask-K8S

# Build the Flask Docker image
docker build -t yourname/flask-app:v1 ./app
```

### 2. Start Kind Cluster and Load Image

This command ensures the cluster is ready and the image is available to all Kubernetes nodes.

```bash

# Create the local single-node cluster (named 'kind')
kind create cluster

# Load the built Docker image into the Kind cluster nodes
kind load docker-image yourname/flask-app:v1
```


### 3. Deploy Application Manifests

Apply the Kubernetes YAML files to deploy the app with 3 replicas, service, and ingress. Note: Ensure you installed the NGINX Ingress Controller on your Kind cluster first (as per initial setup).

```bash
# Deploy the core app components
kubectl apply -f k8s/
```


### 4. Deploy Monitoring Stack (Prometheus & Grafana)

We use Helm to install the industry-standard monitoring solution.

```bash
# Add Helm repo, create namespace, and install the kube-prometheus-stack
helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)
helm repo update
kubectl create namespace monitoring
helm install monitoring-stack prometheus-community/kube-prometheus-stack --namespace monitoring
```

### 5. Configure Prometheus to Scrape Flask Metrics

Apply the ServiceMonitor Custom Resource to tell Prometheus how to find and scrape the metrics from your Flask application's service.

```bash
kubectl apply -f monitoring/servicemonitor.yaml
```

## Verification & Access
### 1. Access the Application

The NGINX Ingress Controller routes external traffic to your service. You can test the endpoints by executing a command on the Kind node itself:

```bash
# Get the IP of the Kind node (usually 172.18.0.2 in default Kind)
KIND_IP=$(docker inspect -f '{{.NetworkSettings.IPAddress}}' kind-control-plane)

# Test the home endpoint
curl http://$KIND_IP/

# Test the metrics endpoint
curl http://$KIND_IP/metrics
```

### 2. Access Grafana Dashboard

To view the monitoring data, you must port-forward the Grafana service to your local machine:

Start Port Forward:

```bash
kubectl port-forward svc/monitoring-stack-grafana 3000:80 -n monitoring
```
Access: Open your browser to http://localhost:3000.

Login:

Username: admin
Password: Retrieve the dynamically generated password:

```bash
kubectl get secret --namespace monitoring monitoring-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

Once logged in, you can import the custom dashboard using the monitoring/grafana-dashboard.json file.

## Cleanup
To destroy the cluster and free up resources:

```bash
helm uninstall monitoring-stack -n monitoring
kubectl delete namespace monitoring
kind delete cluster
```




