from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = serializers.SerializerMethodField()

    def get_invoice_details(self, obj):
        return InvoiceDetailSerializer(obj.invoicedetail_set.all(), many=True).data

    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceDetail
        fields = '__all__'