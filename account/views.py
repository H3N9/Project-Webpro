from django.shortcuts import render, redirect
from .forms import EmployeeForm, Working_timeForm, ExpenseForm, RevenueForm, Paid_salaryForm, CustomerForm
from .models import Employee, Working_time, Expense, Paid_salary, Customer
from datetime import datetime
from dateutil.parser import parse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def showEmployee(request):
    context = {}
    employees = Employee.objects.all()
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
    date_payment = Working_time.objects.filter(employee=eid)
    form = Paid_salaryForm()
    if request.method == "POST":
        form = Paid_salaryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            date_payment = Working_time.objects.filter(date__range=[data['start_date'], data['end_date']], employee=eid)
            for each in date_payment:
                total += each.total_wage
            paid = 1
            context['st'] = data['start_date']
            context['ed'] = data['end_date']
    context['paid'] = paid
    context['total'] = total
    context['form'] = form
    context['employee'] = employee
    context['date_payment'] = date_payment
    context['eid'] = eid
    return render(request, 'account/detail.html', context=context)

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
                date=data['date'],
                description=data['description'],
                type_expense='2',
            )
            return redirect('expense')
    context['form'] = form
    return render(request, 'account/expense.html', context=context)


@login_required
def revenue(request):
    context = {}
    form = RevenueForm()
    if request.method=='POST':
        form = RevenueForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return redirect('revenue')
    context['form'] = form
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
            description='จ่ายเงินลูกจ้าง',
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
