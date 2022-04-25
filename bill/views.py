from uuid import uuid4
from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view

from storage.models import Goods
from storage.serializers import GoodsSerializer
from .models import Bill, BillDetail
from .serializers import BillDetailSerializer, BillSerializer, NewBillDetailSerializer, NewBillSerializer
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

create_bill_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'data': openapi.Schema(type=openapi.TYPE_ARRAY,
                               items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                    properties={
                                                        'codegood': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                                                        'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='number'),
                                                    })
                               )

    },
    required=['name', 'phone', 'address', 'data']
)


def create_code_bill():
    return str(uuid4()).replace("-", "")


@api_view(["GET"])
def get_bill_by_code(request, code):
    bill = Bill.objects.get(code=code)
    serializer = BillSerializer(bill)
    return Response(serializer.data)


@swagger_auto_schema(method='POST', request_body=create_bill_schema)
@api_view(["POST"])
def create_bill(request):
    try:
        code = create_code_bill()
        dataBill = {
            "name": request.data.get("name"),
            "address": request.data.get("address"),
            "phone": request.data.get("phone"),
            "code": code
        }
        dataDetail = request.data.get("data")
    except:
        return Response({"message": "Tham số truyền về sai", "error": True})
    with transaction.atomic():
        try:
            bill = NewBillSerializer(data=dataBill)
            try:
                if bill.is_valid():
                    bill.save()
                    mybill = Bill.objects.get(code=code)
            except:
                return Response({"message": "Không thể tạo hóa đơn", "error": True})
            for data in dataDetail:
                try:
                    good = Goods.objects.get(
                        code=str(data.get("codegood")))
                    detail = {
                        "amount": int(data.get("amount")),
                        "price": good.getPrice(),
                        "billCode": mybill.pk,
                        "codeGood": good.pk
                    }
                except:
                    mybill.delete()
                    return Response({"message": "Mã mặt hàng {} có vấn đề".format(
                        data.get("codegood")), "error": True})
                billDetail = NewBillDetailSerializer(data=detail)
                try:
                    if billDetail.is_valid():
                        billDetail.save()
                        serializer = GoodsSerializer(
                            good, data={'quantity': good.getQuantity() - int(data.get("amount"))}, partial=True)
                        try:
                            if serializer.is_valid():
                                serializer.save()
                        except:
                            mybill.delete()
                            return Response({"message": "Số lượng hàng {} không đủ".format(
                                good.name), "error": True})
                except:
                    mybill.delete()
                    return Response({"message": "Thông tin mặt hàng {} có vấn đề".format(
                        good.name), "error": True})
        except:
            mybill.delete()
            return Response({"message": "Đã xảy ra lỗi khi thêm đơn hàng", "error": True})

    return Response({"message": "Đặt hàng thành công", "error": False})
