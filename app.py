from flask_openapi3 import OpenAPI, Info

from flask_cors import CORS

info = Info(title="Verifica Ticket", version="0.0.1",
            description="API da VerificaTicket")
app = OpenAPI(__name__, info=info)
CORS(app)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port="5001")

import controllers