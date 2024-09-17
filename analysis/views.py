from django.http import JsonResponse
import pandas as pd
import plotly.express as px
from django.shortcuts import render
from .forms import FileUploadForm
from django.shortcuts import redirect
from django.urls import reverse

def analyze_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)

            # التأكد من وجود بيانات
            if df.empty:
                context = {'error': 'الملف فارغ.'}
                return render(request, 'analysis/upload.html', context)

            # Data Description
            describe = df.describe(include='all').to_html()

            # تأكد من وجود أعمدة لتحديد الرسوم البيانية
            if df.columns.size < 2:
                context = {'error': 'لا توجد بيانات كافية لإنشاء الرسوم البيانية.'}
                return render(request, 'analysis/upload.html', context)

            # Pie Chart
            fig_pie = px.pie(df, names=df.columns[0], values=df[df.columns[1]], title="Pie Chart")
            pie_chart = fig_pie.to_html(full_html=False)

            # Donut Chart
            fig_donut = px.pie(df, names=df.columns[0], values=df[df.columns[1]], hole=0.3, title="Donut Chart")
            donut_chart = fig_donut.to_html(full_html=False)

            # Line Chart
            time_column = 'Month'  # أو 'Date' بناءً على بياناتك
            if time_column not in df.columns:
                time_column = df.columns[0]  # افتراضيا استخدم أول عمود إذا لم يكن "Month" أو "Date"

            fig_line = px.line(df, x=time_column, y=df.columns[1], title="Line Chart")
            line_chart = fig_line.to_html(full_html=False)

            # Bar Chart
            fig_bar = px.bar(df, x=time_column, y=df.columns[1], title="Bar Chart")
            bar_chart = fig_bar.to_html(full_html=False)

            # استرداد القيم من الجلسة
            total1 = request.session.get('total1', '11096.623515 L.E')
            total2 = request.session.get('total2', '7096.000000 L.E')
            total3 = request.session.get('total3', '4000 L.E')

            context = {
                'describe': describe,
                'pie_chart': pie_chart,
                'donut_chart': donut_chart,
                'line_chart': line_chart,
                'bar_chart': bar_chart,
                'total1': total1,
                'total2': total2,
                'total3': total3,
            }
            return render(request, 'analysis/results.html', context)

    else:
        form = FileUploadForm()

    return render(request, 'analysis/upload.html', {'form': form})

def update_total(request):
    if request.method == 'POST':
        total = request.POST.get('total', '0')
        # حفظ القيم في الجلسة مع مفتاح مميز لكل بطاقة
        if 'total1' in request.POST:
            request.session['total1'] = total
        elif 'total2' in request.POST:
            request.session['total2'] = total
        elif 'total3' in request.POST:
            request.session['total3'] = total

        return JsonResponse({'status': 'success'})


def update_total(request):
    if request.method == 'POST':
        total = request.POST.get('total', '0')
        request.session['total'] = total
        return JsonResponse({'status': 'success'})