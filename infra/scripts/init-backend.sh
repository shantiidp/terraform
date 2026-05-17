#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="rg-terraform-state"
STORAGE_ACCOUNT="stagenticaiterraform"
CONTAINER="tfstate"
LOCATION="eastus2"

echo "Creating resource group for Terraform state..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

echo "Creating storage account for Terraform state..."
az storage account create \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --sku Standard_LRS \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false

echo "Creating blob container..."
az storage container create \
  --name "$CONTAINER" \
  --account-name "$STORAGE_ACCOUNT"

echo "Terraform backend initialized at $STORAGE_ACCOUNT/$CONTAINER"
