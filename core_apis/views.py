from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer

class InvoiceListCreateView(APIView):
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            invoice_details_data = request.data.get('invoice_details', [])
            for item in invoice_details_data:
                item['invoice'] = serializer.instance.id

                serializer = InvoiceDetailSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvoiceDetailView(APIView):
    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Update existing invoice details and create new ones
            existing_details = set(invoice.invoicedetail_set.all().values_list('id', flat=True))
   
            for item in request.data.get('invoice_details', []):
                if item.get('id') in existing_details:

                    item['invoice'] = serializer.instance.id
                    detail = InvoiceDetail.objects.get(pk=item['id'])
                    serializer = InvoiceDetailSerializer(detail, data=item)
                    if serializer.is_valid():
                        
                        serializer.save()
                    else: 

                        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
                else:
                    item['invoice'] = serializer.instance.id
                    serializer = InvoiceDetailSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else: return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)