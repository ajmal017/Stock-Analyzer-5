from django.shortcuts import render
from Analyze.cmd_driver import driver


def indexView(request):
    if "GET" == request.method:
        return render(request, 'index.html', {"data":"hide"})
    else:
        excel_file = request.FILES["excel_file"]
        iex_key = request.POST['iex-key']
        excel_data_df, excel_data_dict, web_charts = driver.run_analytics(excel_file, iex_key)
        
        # need to pass through matpoltlib charts
        return render(request, 'index.html', {"excel_data":excel_data_df, "excel_data_dict":excel_data_dict, "web_charts":web_charts, "data":"show"})
    