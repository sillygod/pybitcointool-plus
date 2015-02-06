import pyjsonrpc
from bitcoin import wallet
import json


class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def createWallet(self):
        """Create a random key and a address for
        user
        """
        wt = wallet.Wallet()
        wt.createWallet()

        result = json.dumps({'address': wt.address, 'priv': wt.priv})

        return result




PORT = 8778
DOMAIN = 'localhost'

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=(DOMAIN, PORT),
    RequestHandlerClass=RequestHandler
)


print "Starting HTTP server ..."
print "URL: http://{}:{}".format(DOMAIN, PORT)
http_server.serve_forever()
