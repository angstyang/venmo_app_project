from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction
from transactions.serializers import transactionSerializer
from rest_framework.decorators import api_view

# Create your views here.
# def index(request):
#     return render(request, "transactions/index.html")


def index(request):
    print("------------------------- I AM HERE")
    queryset = Transaction.objects.all()
    return render(request, "transactions/index.html", {'transactions': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'transactions/index.html'

    def get(self, request):
        queryset = Transaction.objects.all()
        return Response({'transactions': queryset})


class list_all_transactions(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'transactions/transaction_list.html'

    def get(self, request):
        queryset = Transaction.objects.all()
        return Response({'transactions': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def transaction_list(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            transactions = transactions.filter(title__icontains=title)

        transactions_serializer = transactionSerializer(
            transactions, many=True)
        return JsonResponse(transactions_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        transaction_data = JSONParser().parse(request)
        transaction_serializer = transactionSerializer(data=transaction_data)
        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return JsonResponse(transaction_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(transaction_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Transaction.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Transactions were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return JsonResponse({'message': 'The transaction does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        transaction_serializer = transactionSerializer(transaction)
        return JsonResponse(transaction_serializer.data)

    elif request.method == 'PUT':
        transaction_data = JSONParser().parse(request)
        transaction_serializer = transactionSerializer(
            transaction, data=transaction_data)
        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return JsonResponse(transaction_serializer.data)
        return JsonResponse(transaction_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        transaction.delete()
        return JsonResponse({'message': 'Transaction was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def transaction_list_published(request):
    transactions = Transaction.objects.filter(published=True)

    if request.method == 'GET':
        transactions_serializer = transactionSerializer(
            transactions, many=True)
        return JsonResponse(transactions_serializer.data, safe=False)
