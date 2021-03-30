AUTH_URL="https://$1.usetopscore.com/api/oauth/server"
client_id=$2
client_secret=$3
username=$4
password=$5
query=$6
options=$7
curl -s $AUTH_URL -d "grant_type=client_credentials&client_id=$client_id&client_secret=$client_secret" > /dev/null
access_token=$(curl -s $AUTH_URL -d "grant_type=password&client_id=$client_id&client_secret=$client_secret&username=$username&password=$password" | jq -r '.access_token')
curl -s https://pada.usetopscore.com/api/$query -H "Authorization: Bearer $access_token | $options"
