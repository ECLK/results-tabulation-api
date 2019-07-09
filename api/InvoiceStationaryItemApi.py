from flask import abort
from schemas import Invoice_StationaryItem_Schema as Schema
from domain import InvoiceStationaryItemDomain
from util import RequestBody


def get_all(invoiceId):
    result = InvoiceStationaryItemDomain.get_all(invoiceId)

    return Schema(many=True).dump(result).data


def get_by_id(invoiceId, stationaryItemId, body):
    result = InvoiceStationaryItemDomain.create(body)

    return Schema().dump(result).data, 201


def create(invoiceId, body):
    request_body = RequestBody(body)
    result = InvoiceStationaryItemDomain.create(
        invoiceId=invoiceId,
        stationaryItemId=request_body.get("stationaryItemId")
    )

    return Schema().dump(result).data, 201


def update(invoiceId, stationaryItemId, body):
    result = InvoiceStationaryItemDomain.create(body)

    return Schema().dump(result).data, 201