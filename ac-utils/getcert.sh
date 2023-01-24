
openssl req -x509 -sha256 -newkey rsa:2048 -keyout webhook.key -out webhook.crt -days 1024 -nodes -extensions SAN -config <(cat ac-workshop.cnf <(printf "[SAN]\nsubjectAltName=DNS.1:validate.ac-workshop.svc"))

