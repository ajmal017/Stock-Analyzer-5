#import urllib

#from django.shortcuts import render, redirect
#from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
#from django.conf import settings

from django.shortcuts import render
from Analyze.cmd_driver import driver


def indexView(request):
    if "GET" == request.method:
        return render(request, 'index.html', {"data":"hide"})
    else:
        excel_file = request.FILES["excel_file"]
        iex_key = request.POST['iex-key']
        excel_data_df, excel_data_dict = driver.run_analytics(excel_file, iex_key)
        
        return render(request, 'index.html', {"excel_data":excel_data_df, "excel_data_dict":excel_data_dict, "data":"show"})
    