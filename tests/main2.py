import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# Cargar variables del .env
load_dotenv()

app = FastAPI()

EXTERNAL_API_URL = "https://api.hubapi.com/crm/v3/objects/contacts"
TICKET_API_URL = "https://api.hubapi.com/crm/v3/objects/tickets"

token = os.getenv("ACCESS_TOKEN")


@app.get("/ver-contacto/{contact_id}")
def get_hubspot_contact_by_id(contact_id: str):

    if not token:
        raise HTTPException(
            status_code=500, detail="No se encontró ACCESS_TOKEN en el archivo .env"
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    url = f"{EXTERNAL_API_URL}/{contact_id}"

    try:
        response = requests.get(url, headers=headers)

        print(response.status_code)
        print(response.text)

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Token inválido.")

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Contacto no encontrado.")

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ver-contactos")
def get_hubspot_contacts():

    if not token:
        raise HTTPException(
            status_code=500, detail="No se encontró ACCESS_TOKEN en el archivo .env"
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(EXTERNAL_API_URL, headers=headers)

        print(response.status_code)
        print(response.text)

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Token inválido.")

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ver-ticket/{ticket_id}")
def get_hubspot_ticket_by_id(ticket_id: str):

    if not token:
        raise HTTPException(
            status_code=500, detail="No se encontró ACCESS_TOKEN en el archivo .env"
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    url = f"{TICKET_API_URL}/{ticket_id}?properties=highly_sensitive,sensitive"

    try:
        response = requests.get(url, headers=headers)

        print(response.status_code)
        print(response.text)

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Token inválido.")

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Ticket no encontrado.")

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ver-tickets")
def get_hubspot_tickets():

    if not token:
        raise HTTPException(
            status_code=500, detail="No se encontró ACCESS_TOKEN en el archivo .env"
        )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{TICKET_API_URL}?properties=highly_sensitive,sensitive", headers=headers
        )

        print(response.status_code)
        print(response.text)

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Token inválido.")

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
