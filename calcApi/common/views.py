from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ApiRequest, ApiResponse
import csv
import io
from django.http import JsonResponse


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calculate(request) -> JsonResponse:

    if 'file' not in request.FILES:
        return JsonResponse({'error': 'File not found'}, status=404)

    get_file = request.FILES['file']
    decoded_file = get_file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    read_file = csv.reader(io_string, delimiter=',')

    sum_of_nums_in_file = float(0.0)

    for row in read_file:
        if len(row) != 3:
            continue
        a = row[0]
        o = row[1]
        b = row[2]
        try:
            a, b = float(a), float(b)
            if o == '+':
                sum_of_nums_in_file += a + b
            elif o == '-':
                sum_of_nums_in_file += a - b
            elif o == '*':
                sum_of_nums_in_file += a * b
            elif o == '/':
                sum_of_nums_in_file += a / b if b != 0 else 0
        except ValueError:
            continue

    request = ApiRequest.objects.create(user=request.user, request=get_file.name, file=get_file)
    ApiResponse.objects.create(request=request, response=sum_of_nums_in_file)

    return JsonResponse({
        'result':sum_of_nums_in_file
    })
