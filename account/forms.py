from django import forms
from . import models
from django.core.exceptions import ValidationError
from datetime import date
from cloth.models import Cloth_in_stock


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
            'rating_wage_per_hour': forms.DateInput(attrs={'class': 'form-control','oninput':"positive(document.getElementById(\'id_rating_wage_per_hour\'))"})
        }

    def clean(self):
        cleaned_data = super().clean()
        hire_date = cleaned_data.get("hire_date")
        birthdate = cleaned_data.get("birthdate")

        if hire_date > date.today():            
            msg = "กรุณากรอกวันที่ตามจริง"
            self.add_error('hire_date', msg)
        if birthdate > date.today():
            msg = "กรุณากรอกวันที่ตามจริง"
            self.add_error('birthdate', msg)


class Working_timeForm(forms.ModelForm):
    from_afternoon = forms.TimeField(required=False, 
        widget=forms.TimeInput(attrs={'type':'time', 'oninput':'setRequired(2)', 'class': 'form-control'}), 
        label='เวลาเริ่มงานบ่าย')

    to_afternoon = forms.TimeField(required=False, 
        widget=forms.TimeInput(attrs={'type':'time', 'oninput':'setRequired(2)', 'class': 'form-control'}), 
        label='เวลาเลิกงานบ่าย')

    from_beforenoon = forms.TimeField(required=False, 
        widget=forms.TimeInput(attrs={'type':'time', 'oninput':'setRequired(1)', 'class': 'form-control'}), 
        label='เวลาเริ่มงานเช้า')
    to_beforenoon = forms.TimeField(required=False, 
        widget=forms.TimeInput(attrs={'type':'time', 'oninput':'setRequired(1)', 'class': 'form-control'}), 
        label='เวลาเลิกงานเช้า')
    class Meta:
        model = models.Working_time
        exclude = ['employee', 'total_wage', 'normal_wage','ot_wage']
        labels = {
            'date': 'วันที่'
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
    
    def clean(self):
        clean_data = super().clean()
        date = clean_data.get("date")
        fbn = clean_data.get('from_beforenoon')
        tbn = clean_data.get('to_beforenoon')
        fan = clean_data.get('from_afternoon')
        tan = clean_data.get('to_afternoon')
        if date > date.today():            
            msg = "กรุณากรอกวันที่ตามจริง"
            self.add_error('date', msg)
        if fbn or tbn:
            if tbn < fbn:
                raise ValidationError(
                    'ข้อมูลเวลาผิดพลาด'
                )
        if fan or tan:
            if tan < tbn:
                print('hello')
                msg = "ข้อมูลเวลาผิดพลาด"
                raise ValidationError(
                    'ข้อมูลเวลาผิดพลาด'
                )
        if fbn and tbn and fan and tan:
            if fan < tbn:
                raise ValidationError(
                    'ข้อมูลเวลาผิดพลาด'
                )

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = models.Expense
        exclude = ['type_expense']
        labels = {
            'amount':'จำนวนเงิน',
            'description':'รายละเอียด',
        }
        widgets = {
            'amount':forms.NumberInput(attrs={ 'class':'form-control','oninput':"positive(document.getElementById(\'id_amount\'))"}),
            'description':forms.Textarea(attrs={ 'class':'form-control', 'rows':'3'})
        }

class RevenueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RevenueForm, self).__init__(*args, **kwargs)
        self.fields['customer'].required = False
        self.fields['amount'].widget.attrs['readonly'] = True 
    class Meta:
        model = models.Revenue
        fields = '__all__'        
        labels = {
            'amount':'จำนวนเงินทั้งหมด',
            'description':'รายละเอียด',
            'customer':'ลูกค้า',
            'type_revenue':'ประเภทรายรับ',
        }
        widgets = {            
            'amount':forms.NumberInput(attrs={ 'class':'form-control','oninput':"positive(document.getElementById(\'id_amount\'))"}),
            'description':forms.Textarea(attrs={ 'class':'form-control', 'rows':'3'}),
            'customer':forms.Select(attrs={ 'class':'form-control'}),
            'type_revenue':forms.Select(attrs={ 'class':'form-control','onchange':"chooseForm(document.getElementById(\'id_type_revenue\').value)"})
        }


class Paid_salaryForm(forms.ModelForm):
    class Meta:
        model = models.Paid_salary
        exclude = ['expense', 'employee']
        labels = {
            'start_date':'วันเริ่ม',
            'end_date':'จนถึง',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        }
    def clean(self):
        clean_data = super().clean()
        date_data1 = clean_data.get('start_date')
        date_data2 = clean_data.get('end_date')
        if date_data1 > date_data2:
            raise ValidationError('ข้อมูลเวลาผิดพลาด')

class CustomerForm(forms.ModelForm):    
    class Meta:
        model = models.Customer
        fields = '__all__'
        labels = {
            'name':'ชื่อลูกค้า',
            'contact':'เบอร์ติดต่อ',
            'address':'ที่อยู่',
        }
        widgets = {
            'name': forms.DateInput(attrs={'class':'form-control'}),
            'contact': forms.DateInput(attrs={'class':'form-control'}),
            'address': forms.DateInput(attrs={'class':'form-control'}),
        }

class Sell_listForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sell_listForm, self).__init__(*args, **kwargs)
        self.fields['unit_price'].widget.attrs['readonly'] = True 
    class Meta:
        model = models.Sell_list
        exclude = ['selling_revenue','list_no']
        labels = {
            'quantity':'จำนวน',
            'unit_price':'ราคาต่อหน่วย',
            'cloth_in_stock':'ผ้าจากในคลัง',
        }
        widgets = {
            'quantity':forms.NumberInput(attrs={'oninput':"assign(this)", 'class':'form-control'}),
            'unit_price': forms.NumberInput(attrs={'oninput':"positive(this)", 'class':'form-control'}),
            'cloth_in_stock': forms.Select(attrs={ 'class':'form-control', 'oninput':"addOption(this)"})
        }

    def clean(self):
        quantity = self.cleaned_data.get('quantity')
        cloth_in_stock = self.cleaned_data.get('cloth_in_stock')
        if quantity > cloth_in_stock.quantity:
            raise ValidationError('มีจำนวนไม่พอ')

class Engage_listForm(forms.ModelForm):
    class Meta:
        model = models.Engage_list
        exclude = ['engaging_revenue', 'list_no']
        labels = {
            'quantity':'จำนวน',
            'unit_price':'ราคาทั้งหมด',
            'cloth_type':'ประเภทผ้า',
            'color':'สี',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'oninput':"positive(this)", 'class':'form-control'}),
            'unit_price': forms.NumberInput(attrs={'oninput':"assign2(this)", 'class':'form-control'}),
            'cloth_type': forms.Select(attrs={ 'class':'form-control'}),
            'color': forms.Select(attrs={ 'class':'form-control'})
        }
