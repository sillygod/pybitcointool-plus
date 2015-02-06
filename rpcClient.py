import pyjsonrpc

DOMAIN = 'localhost'
PORT = 8778

http_client = pyjsonrpc.HttpClient(
    url="http://{}:{}".format(DOMAIN, PORT),
    username="",
    password=""
)

# It is also possible to use the *method* name as *attribute* name.
print http_client.createWallet()
