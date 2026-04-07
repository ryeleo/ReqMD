# Variables — match your subscription
SUBSCRIPTION_ID="8bee3016-0a58-4c85-bcd9-b1b8b1205ae0"
STATE_RG="rqmd-tfstate-rg"
STATE_LOCATION="westus2"
STATE_ACCOUNT="rqmdtfstate$(openssl rand -hex 3)"  # must be globally unique
STATE_CONTAINER="tfstate"

# Create the state resource group
az group create \
  --subscription "$SUBSCRIPTION_ID" \
  --name "$STATE_RG" \
  --location "$STATE_LOCATION"

# Create the storage account (LRS is cheapest, ~$0.01/mo for a few KB of state)
az storage account create \
  --subscription "$SUBSCRIPTION_ID" \
  --resource-group "$STATE_RG" \
  --name "$STATE_ACCOUNT" \
  --sku Standard_LRS \
  --kind StorageV2 \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false

# Create the container
az storage container create \
  --account-name "$STATE_ACCOUNT" \
  --name "$STATE_CONTAINER" \
  --auth-mode login

# Print the account name — you'll need it for the next step
echo "STATE_ACCOUNT=$STATE_ACCOUNT"

# Then I ran the following:
#
# az role assignment create \
#   --assignee "1d8f7ec3-40d6-4151-8a45-eb396c5cf9a9" \
#   --role "Storage Blob Data Contributor" \
#   --scope "/subscriptions/8bee3016-0a58-4c85-bcd9-b1b8b1205ae0/resourceGroups/rqmd-tfstate-rg/providers/Microsoft.Storage/storageAccounts/rqmdtfstate2d2e34"