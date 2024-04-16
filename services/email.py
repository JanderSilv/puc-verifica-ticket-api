import os
import resend
from typing import TypedDict, List


resend.api_key = os.environ["RESEND_API_KEY"]


class EmailParams(TypedDict, total=False):
  to: List[str]
  subject: str
  html: str


def send_email(params: EmailParams):
  defaultParams = {
      "from": "VerificaTicket <contato@verificaticket.com.br>",
  }

  defaultParams.update(params)
  result = resend.Emails.send(defaultParams)

  return result
