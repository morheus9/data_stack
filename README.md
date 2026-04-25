# Data Stack

Production grade data processing platform running on Kubernetes with ArgoCD GitOps.

## Architecture

```
              ┌───────────────────┐
              │      Argo CD      │
              └─────────┬─────────┘
              ┌─────────┴─────────┐
              │ Root Apps of Apps │
              └─────────┬─────────┘
            ┌───────────┴───────────┐
┌───────────▼─────────┐   ┌─────────▼───────────┐
│  Development        │   │  Production         │
│                     │   │                     │
│  ┌──────────────┐   │   │   ┌──────────────┐  │
│  │    Kafka     │   │   │   │    Kafka     │  │
│  └──────────────┘   │   │   └──────────────┘  │
│  ┌──────────────┐   │   │   ┌──────────────┐  │
│  │   Airflow    │   │   │   │   Airflow    │  │
│  └──────────────┘   │   │   └──────────────┘  │
│  ┌──────────────┐   │   │   ┌──────────────┐  │
│  │   Producer   │   │   │   │   Producer   │  │
│  └──────────────┘   │   │   └──────────────┘  │
│  ┌──────────────┐   │   │   ┌──────────────┐  │
│  │   Consumer   │   │   │   │   Consumer   │  │
│  └──────────────┘   │   │   └──────────────┘  │
└─────────────────────┘   └─────────────────────┘
```

## Components

| Component      | Technology                            | Version        | Purpose                                    |
| -------------- | ------------------------------------- | -------------- | ------------------------------------------ |
| Message Broker | **Apache Kafka** via Strimzi Operator | 4.2.0 / 0.51.0 | Distributed streaming platform             |
| Orchestration  | **Apache Airflow**                    | 3.1.8          | Workflow scheduler and pipeline manager    |
| GitOps Engine  | **Argo CD**                           | 3.3.7          | Declarative continuous deployment          |
| Data Producer  | Python Service                        | Python 3.14.4  | Generates and sends test messages to Kafka |
| Data Consumer  | Python Service                        | Python 3.14.4  | Reads and processes messages from Kafka    |

## Quick Start

### Prerequisites

- Kubernetes cluster v1.27+
- kubectl configured and connected to cluster

### Install Argo CD

```bash
# Install Argo CD 3.3.7
kubectl create namespace argocd
kubectl apply -n argocd -f https://github.com/argoproj/argo-cd/releases/download/v3.3.7/install.yaml

# Wait for Argo CD to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s
```

### Deploy Development Environment

```bash
# Deploy DEV environment only
kubectl apply -f argocd/root-apps/dev-app-of-apps.yaml

# Wait 3-5 minutes for full deployment
kubectl get applications -n argocd
```

### Deploy Production Environment

```bash
# Deploy PROD environment only
kubectl apply -f argocd/root-apps/prod-app-of-apps.yaml
```

### Remove Environment

```bash
# Remove DEV completely
kubectl delete -f argocd/root-apps/dev-app-of-apps.yaml
```

## Project Structure

```
📁 data_stack/
├── 📁 apps/                          # Native Kubernetes manifests
│   ├── 📁 log-consumer/             # Consumer service deployment
│   └── 📁 log-producer/             # Producer service deployment
├── 📁 argocd/
│   ├── 📁 applications/             # Argo CD Application definitions
│   │   ├── 📁 airflow/
│   │   ├── 📁 kafka/
│   │   ├── 📁 log-consumer/
│   │   └── 📁 log-producer/
│   ├── 📁 projects/                 # Argo CD Project definitions
│   └── 📁 root-apps/                # Root App of Apps entrypoints
├── 📁 infra/
│   └── 📁 terraform/                # Infrastructure as Code
└── 📁 services/
    ├── 📁 log-consumer/             # Consumer service source code
    └── 📁 log-producer/             # Producer service source code
```

## Usage

After deployment Kafka will be available at:

```
kafka-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092
```

## Configuration

All environment specific configuration located in:

```
argocd/applications/{component}/values/{env}.yaml
```

## Production Configuration

- Kafka: 3 brokers, 100Gi storage, replication factor 3
- No automatic topic creation
- Proper resource limits and requests
- Self healing and automated pruning enabled
- All security best practices applied

---

Maintained as Infrastructure as Code. All changes go through pull requests.
