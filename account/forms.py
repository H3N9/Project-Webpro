from django import forms
from . import models

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        exclude = ['age', 'working_age']
        labels = {
            'fname': 'ชื่อพนักงาน',
            'lname': 'นามสกุลพนักงาน',
            'birthdate': 'วันเกิด',
            'hire_date': 'วันเริ่มทำงาน',
            'rating_wage_per_hour': 'ค่าจ้างต่อชั่วโมง',
        }
        widgets = {
            'fname': forms.DateInput(attrs={'class':'form-control'}),
            'lname': forms.DateInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'birthdate': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'rating_wage_per_hour': forms.DateInput(attrs={'class': 'form-control'})
        }

class Working_timeForm(forms.ModelForm):
    from_afternoon = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type':'time'}), label='เวลาเริ่มงานบ่าย')
    to_afternoon = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type':'time'}), label='เวลาเลิกงานบ่าย')
    from_beforenoon = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type':'time'}), label='เวลาเริ่มงานเช้า')
    to_beforenoon = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type':'time'}), label='เวลาเลิกงานเช้า')
    class Meta:
        model = models.Working_time
        exclude = ['employee', 'total_wage', 'normal_wage','ot_wage']
        labels = {
            'date': 'วันที่'
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = models.Expense
        exclude = ['type_expense']
        labels = {
            'date': 'วันที่',
            'amount':'จำนวนเงิน',
            'description':'รายละเอียด',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'amount':forms.DateInput(attrs={ 'class':'form-control'}),
            'description':forms.Textarea(attrs={ 'class':'form-control', 'rows':'3'})
        }

class RevenueForm(forms.ModelForm):
    class Meta:
        model = models.Revenue
        fields = '__all__'
        labels = {
            'date': 'วันที่',
            'amount':'จำนวนเงิน',
            'description':'รายละเอียด',
            'customer':'ลูกค้า',
            'type_revenue':'ประเภทรายรับ',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'amount':forms.NumberInput(attrs={ 'class':'form-control'}),
            'description':forms.Textarea(attrs={ 'class':'form-control', 'rows':'3'}),
            'customer':forms.Select(attrs={ 'class':'form-control'}),
            'type_revenue':forms.Select(attrs={ 'class':'form-control'})
        }