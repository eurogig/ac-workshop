echo "The key is\n"
cat webhook.key | base64 | tr -d '\n'
echo "The cert is\n"
cat webhook.crt | base64 | tr -d '\n'
