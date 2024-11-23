from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal
from typing import Optional

from src.scripts.generate_data import generate_test_data
from src.database import create_db_and_tables, engine, get_session
from src.models import Product, Sale, Client


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        product_count = session.query(Product).count()
        if product_count == 0:
            try:
                generate_test_data(session)
                print("Test data generated successfully!")
            except Exception as e:
                print(f"Error generating test data: {e}")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/v1/healthcheck")
async def healthcheck():
    return {'status':'ok'}


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def client_purchases(
    request: Request,
    client_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    clients = session.exec(select(Client)).all()
    
    selected_client = None
    sales = []
    products = []
    
    if client_id:
        selected_client = session.get(Client, client_id)
        if selected_client:
            sales = session.exec(
                select(Sale).where(Sale.client_id == client_id)
            ).all()
            products = session.exec(select(Product)).all()
    
    return templates.TemplateResponse(
        "client_purchases.html",
        {
            "request": request,
            "clients": clients,
            "selected_client": selected_client,
            "sales": sales,
            "products": products,
            "Decimal": Decimal
        }
    )

@app.post("/create_purchase")
async def create_purchase(
    client_id: int = Form(...),
    product_id: int = Form(...),
    quantity: Decimal = Form(...),
    delivery_date: str = Form(...),
    session: Session = Depends(get_session)
):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    sale = Sale(
        client_id=client_id,
        product_id=product_id,
        quantity=quantity,
        sale_date=datetime.now(),
        delivery_date=datetime.strptime(delivery_date, "%Y-%m-%d")
    )
    session.add(sale)
    total_purchases = Decimal('0')
    for client_sale in client.sales:
        total_purchases += client_sale.quantity * client_sale.product.price

    if total_purchases > Decimal('5000') and not client.is_regular:
        client.is_regular = True
        session.add(client)
    
    session.commit()
    return RedirectResponse(
        url=f"/?client_id={client_id}",
        status_code=303
    )
