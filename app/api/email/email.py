from fastapi import FastAPI
from typing import List
from email_test import sendMails
from replace import getMail
from pydantic import BaseModel


class MailShema(BaseModel):
    TypeModel : int
    From : str
    Subject: str
    To: str
    Args: List[str] = []

app = FastAPI()

@app.get("/sendMail/")
async def sendEmail(mail: MailShema):
    getMail(mail.TypeModel, mail.Args)
    sendMails(mail.From, mail.To, mail.Subject)
    return {"message": "Mail Send"}