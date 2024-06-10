from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .forms import ReportForm
from .models import SemiAnnual2024Report, SemiAnnual2024CreatorsSummaryReport, SemiAnnual2024UserCompany


@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user  # Установите поле user
            report.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'sixmonths2024/report_form.html', {'form': form})


@login_required
def update_report(request, pk):
    report = get_object_or_404(SemiAnnual2024Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')  # Замените 'report_list' на имя вашего URL-шаблона
    else:
        form = ReportForm(instance=report)
    return render(request, 'sixmonths2024/report_form.html', {'form': form})


@login_required
def report_list(request):
    user = request.user

    creators_summary_report = SemiAnnual2024CreatorsSummaryReport.objects.first()
    if creators_summary_report and user in creators_summary_report.creators.all():
        reports = SemiAnnual2024Report.objects.all()
        return render(request, 'sixmonths2024/report_list.html', {'reports': reports})
    else:
        user_company = SemiAnnual2024UserCompany.objects.get(user=user)
        company = user_company.companies.first()

        # Если для этой компании уже есть отчет, получаем его
        report = SemiAnnual2024Report.objects.filter(company=company).first()

        if request.method == 'POST':
            form = ReportForm(request.POST, instance=report)
            if form.is_valid():
                report = form.save(commit=False)
                report.user = request.user  # Устанавливаем текущего пользователя
                report.save()
                return redirect('report_list')
        else:
            form = ReportForm(instance=report, initial={'company': company})
            user_company = SemiAnnual2024UserCompany.objects.filter(user=user).first()
            available_companies = user_company.companies.all()  # Компании, доступные пользователю
            form.fields['company'].queryset = available_companies  # Ограничиваем доступные компании
        return render(request, 'sixmonths2024/report_form.html', {'form': form})
