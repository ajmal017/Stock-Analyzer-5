#import urllib

#from django.shortcuts import render, redirect
#from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
#from django.conf import settings

from django.shortcuts import render
import django_excel as excel
#from django.http import HttpResponse
#import openpyxl


from Analyze.cmd_driver import driver



def indexView(request):
    if "GET" == request.method:
        return render(request, 'index.html')
    else:
        excel_file = request.FILES["excel_file"]

        excel_data_df, excel_data_dict = driver.run_analytics(excel_file)
        
        #headers = list(excel_data_dict.keys())

        
        
        
        
        '''
        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["tfsa"]
        print(worksheet)
        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        '''
        
        return render(request, 'index.html', {"excel_data":excel_data_df, "excel_data_dict":excel_data_dict})

"""
https://github.com/pyexcel-webwares/django-excel
http://django.pyexcel.org/en/latest/
https://www.pythoncircle.com/post/591/how-to-upload-and-process-the-excel-file-in-django/
https://assist-software.net/blog/how-export-excel-files-python-django-application
"""


    