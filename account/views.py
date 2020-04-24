from django.shortcuts import render, redirect
from .forms import EmployeeForm, Working_timeForm, ExpenseForm, RevenueForm, Paid_salaryForm, CustomerForm, Sell_listForm, Engage_listForm
from .models import Employee, Working_time, Expense, Paid_salary, Customer, Revenue, Sell_list, Engage_list, Selling, Engaging
from datetime import datetime
from dateutil.parser import parse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.db.models import Max, Min #Models.objects.all().aggregate(Avg('price'))
from rest_framework.renderers import JSONRenderer
from .serializers import EmployeeSerializer, Working_timeSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms import formset_factory


# Create your views here.
@login_required
def showEmployee(request):
    context = {}
    employees = Employee.objects.all().order_by('id')
    if request.method == 'GET':
        fname = request.GET.get('fname', '')
        lname = request.GET.get('lname', '')
        if fname:
            employees = Employee.objects.filter(fname__icontains=fname)
        elif lname:
            employees = Employee.objects.filter(lname__icontains=lname)
        elif fname and lname:
            employees = Employee.objects.filter(fname__icontains=fname,lname__icontains=lname)
    context['employees'] = employees
    return render(request, 'account/employee.html', context=context)

@login_required
def addEmployee(request):
    context = {}
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            add = Employee.objects.create(
                fname=data['fname'],
                lname=data['lname'],
                birthdate=data['birthdate'],
                age=(datetime.now().year-data['birthdate'].year),
                hire_date=data['hire_date'],
                working_age=(datetime.now().year-data['hire_date'].year),
                rating_wage_per_hour=data['rating_wage_per_hour'],
            )
            return redirect('showEmployee')
    context['form'] = form
    return render(request, 'account/addEmployee.html', context=context)

@login_required
def detail(request, eid):
    context = {}
    total = 0
    paid = 0
    employee = Employee.objects.get(pk=eid)
    employee.age = datetime.now().year-employee.birthdate.year
    employee.save()
    date_payment = Working_time.objects.filter(employee=eid)
    paid_salarys = Paid_salary.objects.filter(employee=eid)
    paidList = checkTimeMath(paid_salarys, date_payment)
    form = Paid_salaryForm()
    if request.method == "POST":
        form = Paid_salaryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            date_payment = Working_time.objects.filter(date__range=[data['start_date'], data['end_date']], employee=eid)
            for each in date_payment:
                has = 0
                for paid_salary in paid_salarys:
                    if each.date >= paid_salary.start_date and each.date <= paid_salary.end_date:
                        has = 1
                        break
                if not has:
                    total += each.total_wage
            paid = 1
            context['st'] = data['start_date']
            context['ed'] = data['end_date']
    context['paidList'] = paidList 
    context['paid_salarys'] = paid_salarys
    context['paid'] = paid
    context['total'] = total
    context['form'] = form
    context['employee'] = employee
    context['date_payment'] = date_payment
    context['eid'] = eid
    return render(request, 'account/detail.html', context=context)

def checkTimeMath(payment, date):
    paidList = []
    for each in date:
        has = 0
        for paid in payment:
            if each.date >= paid.start_date and each.date <= paid.end_date:
                paidList.append(1)
                has = 1
                break 
        if not has:
            paidList.append(0)
                
    return paidList

"""@csrf_exempt
def sendDataAPI(request, eid):
    
    if request.method == 'GET':
        employee = Employee.objects.get(pk=eid)
        serializer = EmployeeSerializer(instance=employee)
        return JsonResponse(serializer.data, status=200, safe=False)"""

@login_required
def deleteEmployee(request, eid):
    employee = Employee.objects.get(pk=eid)
    employee.delete()
    return redirect('showEmployee')

@login_required
def addTime(request, eid):
    context = {}
    formTime = Working_timeForm()
    employee = Employee.objects.get(pk=eid)
    if request.method == 'POST':
        formTime = Working_timeForm(request.POST)
        if formTime.is_valid():
            data = formTime.cleaned_data
            amount = checkTime(
                data['from_beforenoon'],
                data['to_beforenoon'],
                data['from_afternoon'],
                data['to_afternoon'],
                employee.rating_wage_per_hour,
                )
            add = Working_time.objects.create(
                date=data['date'],
                employee=Employee.objects.get(pk=eid),
                from_beforenoon=data['from_beforenoon'],
                to_beforenoon=data['to_beforenoon'],
                from_afternoon=data['from_afternoon'],
                to_afternoon=data['to_afternoon'],
                normal_wage=amount[0],
                ot_wage=amount[1],
                total_wage=(amount[0]+amount[1]),
            )
            
            return redirect('/employee/detail/%d'%eid)
    context['formTime'] = formTime
    context['eid'] = eid
    return render(request, 'account/addTime.html', context=context)


def checkTime(start_bn, end_bn, start_an,end_an, rate):
    if start_bn and end_bn and start_an and end_an:
        bn = (end_bn.hour*60+end_bn.minute)-(start_bn.hour*60+start_bn.minute)
        an = (end_an.hour*60+end_an.minute)-(start_an.hour*60+start_an.minute)
        hour = bn//60+an//60
    elif start_bn and end_bn:
        bn = (end_bn.hour*60+end_bn.minute)-(start_bn.hour*60+start_bn.minute)
        hour = bn//60
    elif start_an and end_an:
        an = (end_an.hour*60+end_an.minute)-(start_an.hour*60+start_an.minute)
        hour = an//60
    
    if hour > 8:
        extra = (hour-8)*rate*1.5
        normal = 8*rate
        return [normal,extra]
    elif hour <= 8 and hour >= 1:
        normal = hour*rate
        return [normal,0]


@login_required
def account(request):
    context = {}
    expenses = Expense.objects.all()
    revenues = Revenue.objects.all()
    paid = Paid_salaryForm()
    if request.method == 'POST':
       paid = Paid_salaryForm(request.POST)
       if paid.is_valid():
            data = paid.cleaned_data
            expenses = Expense.objects.filter(date__range=[data['start_date'], data['end_date']])
            revenues = Revenue.objects.filter(date__range=[data['start_date'], data['end_date']])
    context['paid'] = paid
    context['revenues'] = revenues
    context['expenses'] = expenses
    return render(request, 'account/account.html', context=context)

@login_required
def expense(request):
    context = {}
    form = ExpenseForm()
    if request.method=='POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            add = Expense.objects.create(
                amount=data['amount'],
                date=datetime.now(),
                description=data['description'],
                type_expense='2',
            )
            return redirect('account')
    context['form'] = form
    return render(request, 'account/expense.html', context=context)


@login_required
def revenue(request):
    context = {}
    amountForm = 1
    revenue_form = RevenueForm()
    sell_form = formset_factory(Sell_listForm, extra=10)
    engage_form = formset_factory(Engage_listForm, extra=10)
    sell_formSet = sell_form()
    engage_formSet = engage_form()
    if request.method=='POST':
        revenue_form = RevenueForm(request.POST)
        if revenue_form.is_valid():
            revenue_form = revenue_form.cleaned_data
            if revenue_form['type_revenue'] == '1':
                sell_data = sell_form(request.POST)
                if sell_data.is_valid():
                    revenue = Revenue.objects.create(
                        amount=revenue_form['amount'],
                        date=datetime.now(),
                        type_revenue=revenue_form['type_revenue'],
                        description=revenue_form['description'],
                        customer=revenue_form['customer']
                    )
                    selling = Selling.objects.create(revenue=revenue)
                    for sell_form in sell_data:
                        if sell_form.cleaned_data.get('quantity'):
                            if sell_form.is_valid():
                                sell_list = Sell_list.objects.create(
                                    selling_revenue=selling,
                                    quantity=sell_form.cleaned_data['quantity'],
                                    unit_price=sell_form.cleaned_data['unit_price'],
                                    cloth_in_stock=sell_form.cleaned_data['cloth_in_stock']
                                )
                                cloth = sell_form.cleaned_data['cloth_in_stock']
                                cloth.quantity = cloth.quantity-sell_form.cleaned_data['quantity']
                                cloth.save()
                    return redirect('account')
                else:
                    revenue_form = RevenueForm(request.POST)
                    sell_formSet = sell_form(request.POST)
                    amountForm = request.POST.get('amountForm')
            elif revenue_form['type_revenue'] == '2':
                engage_data = engage_form(request.POST)
                if engage_data.is_valid():
                    revenue = Revenue.objects.create(
                        amount=revenue_form['amount'],
                        date=datetime.now(),
                        type_revenue=revenue_form['type_revenue'],
                        description=revenue_form['description'],
                        customer=revenue_form['customer']
                    )
                    engaging = Engaging.objects.create(revenue=revenue)
                    for engage_form in engage_data:
                         if engage_form.cleaned_data.get('quantity'):
                            engage_form = engage_form.cleaned_data
                            engage_list = Engage_list.objects.create(
                                engaging_revenue=engaging,
                                quantity=engage_form['quantity'],
                                unit_price=engage_form['unit_price'],
                                cloth_type=engage_form['cloth_type'],
                                color=engage_form['color']
                            )
                    return redirect('account')
                else:
                    revenue_form = RevenueForm(request.POST)
                    amountForm = request.POST.get('amountForm')
    context['revenue'] = revenue_form
    context['sells'] = sell_formSet
    context['engages'] = engage_formSet
    context['amountForm'] = amountForm
    return render(request, 'account/revenue.html', context=context)

@login_required
def paidSalary(request, eid):
    employee = Employee.objects.get(pk=eid)
    if request.method == "POST":
        st = parse(request.POST.get('st'))
        ed = parse(request.POST.get('ed'))
        total = request.POST.get('total')
        date_payment = Working_time.objects.filter(date__range=[st, ed], employee=eid)
        expense = Expense.objects.create(
            amount=total,
            date=datetime.now(),
            description='จ่ายเงินลูกจ้าง %s %s ของวันที่ %s-%s'%(employee.fname, employee.lname,st,ed),
            type_expense='1',
        )
        paid = Paid_salary.objects.create(
            expense=expense,
            start_date=st,
            end_date=ed,
            employee=Employee.objects.get(pk=eid),
        )
    return redirect('/employee/detail/%d'%eid)


def customer(request):
    context = {}
    return render(request, 'account/customer.html', context=context)

def addCustomer(request):
    context = {}
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            customer = Customer.objects.create(
                name=data['name'],
                contact=data['contact'],
                address=data['address'],
            )
            return redirect('customer')
    context['form'] = form
    return render(request, 'account/addCustomer.html', context=context)

def editEmployee(request, eid):
    context = {}
    employee = Employee.objects.get(pk=eid)
    form = EmployeeForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            employee.fname = data['fname']
            employee.lname = data['lname']
            employee.birthdate = data['birthdate']
            employee.hire_date = data['hire_date']
            employee.rating_wage_per_hour = data['rating_wage_per_hour']
            employee.save()
            return redirect('/employee/detail/%d'%eid)
    context['form'] = form
    context['employee'] = employee
    return render(request, 'account/editEmployee.html', context=context)

def revenueDetail(request, aid):
    context = {}
    revenue = Revenue.objects.get(pk=aid)
    if Selling.objects.get(pk=revenue):
        sell = Selling.objects.get(pk=revenue)
        sell_list = Sell_list.objects.filter(selling_revenue=sell)
        context['sell'] = sell_list
    elif Engaging.objects.get(pk=revenue):
        engage = Engaging.objects.get(pk=revenue)
        engage_list = Engage_list.objects.filter(engaging_revenue=engage)
        context['engage'] = engage_list
    context['revenue'] = revenue
    return render(request, 'account/revenueDetail.html', context=context)
