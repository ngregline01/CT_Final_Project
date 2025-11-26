from flask import Flask
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy import select, ForeignKey

#create the the base database
class Base(DeclarativeBase):
    pass

#The db to bridge the database and the python code
db = SQLAlchemy(model_class=Base)

#The joint table
service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))
)

#The customers model
class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(364), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False, unique=True)
    services:Mapped[List["Service_Tickets"]] = db.relationship(back_populates="customer_service")
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)

#The Service Tickets table
class Service_Tickets(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False, unique=True)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_desc: Mapped[str] = mapped_column(db.String(100), nullable=False)
    customer_service: Mapped["Customers"] = db.relationship(back_populates="services")
    mechanic_services:Mapped[List["Mechanics"]] = db.relationship(secondary=service_mechanics, back_populates="tickets")
    parts_used: Mapped[List["ServicePart"]] = db.relationship(back_populates="job")

#The Mechanics table
class Mechanics(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(350), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(15), nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(db.Numeric(12, 2), nullable=False)
    tickets: Mapped[List["Service_Tickets"]] = db.relationship(secondary=service_mechanics, back_populates="mechanic_services")
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)

#The Inventory Table
class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(350), nullable=False)
    price: Mapped[float] = mapped_column(db.Numeric(12, 2), nullable=False)
    job_usage: Mapped[List["ServicePart"]] = db.relationship(back_populates="part")

#The Service Inventory Table
class ServicePart(Base):
    __tablename__ = "service_inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey("service_tickets.id"))
    inventory_id: Mapped[int] = mapped_column(db.ForeignKey("inventory.id"))
    quantity_used: Mapped[int] = mapped_column(db.Integer, nullable=False)
    job: Mapped["Service_Tickets"] = db.relationship(back_populates="parts_used") #creates relationship between the joint table and service ticket
    part: Mapped["Inventory"] = db.relationship(back_populates="job_usage")#This relationship has to be one-many when created in the joint table because it really is in the middle
