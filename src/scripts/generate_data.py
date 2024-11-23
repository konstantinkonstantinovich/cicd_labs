from faker import Faker
from sqlmodel import Session
from decimal import Decimal
import random
from datetime import timedelta
from typing import List
from src.models import Product, Client, Sale, UnitEnum

fake = Faker('en_US')

def generate_test_data(session: Session):
    products: List[Product] = []
    product_names = [
        "Laptop", "Smartphone", "Tablet", "Headphones", "Monitor",
        "Keyboard", "Mouse", "Printer", "Scanner", "Speaker"
    ]
    
    for name in product_names:
        product = Product(
            name=name,
            price=Decimal(str(random.uniform(100, 2000))).quantize(Decimal("0.01")),
            unit=random.choice(list(UnitEnum))
        )
        session.add(product)
        products.append(product)
    session.commit()

    clients: List[Client] = []
    for _ in range(20):
        client = Client(
            last_name=fake.last_name(),
            first_name=fake.first_name(),
            middle_name=fake.first_name(),
            address=fake.address(),
            phone=fake.phone_number(),
            email=fake.email(),
            is_regular=random.choice([True, False])
        )
        session.add(client)
        clients.append(client)
    session.commit()

    for _ in range(50):
        sale_date = fake.date_time_between(start_date='-1y', end_date='now')
        sale = Sale(
            product_id=random.choice(products).id,
            client_id=random.choice(clients).id,
            sale_date=sale_date,
            delivery_date=sale_date + timedelta(days=random.randint(1, 14)),
            quantity=Decimal(str(random.uniform(1, 10))).quantize(Decimal("0.001"))
        )
        session.add(sale)
    session.commit()
