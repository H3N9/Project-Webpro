from django.db import models

# Create your models here.
class Employee(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    birthdate = models.DateField()
    age = models.IntegerField()
    hire_date = models.DateField()
    working_age = models.IntegerField()
    rating_wage_per_hour = models.FloatField()

class Working_time(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="working_times")
    from_beforenoon = models.TimeField(null=True, blank=True)
    to_beforenoon = models.TimeField(null=True,blank=True)
    from_afternoon = models.TimeField(null=True,blank=True)
    to_afternoon = models.TimeField(null=True,blank=True)
    normal_wage = models.FloatField()
    ot_wage = models.FloatField()
    total_wage = models.FloatField()
    class Meta:
        unique_together = ['date', 'employee']
    

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(auto_now=True)
    description = models.TextField(null=True)
    type_expense = models.CharField(max_length=1,choices=[('1','paid_salary'),('2','others')])

class Paid_salary(models.Model):
    expense = models.OneToOneField(Expense, primary_key=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=10, null=True)
    address = models.TextField(null=True)

    def __str__(self):
        return self.name
    

class Revenue(models.Model):
    amount = models.FloatField()
    types = [('1','ขายผ้าจากคลัง'),('2','รับจ้างย้อม')]
    type_revenue = models.CharField(
        choices=types,max_length=1)
    date = models.DateField(auto_now=True)
    description = models.TextField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

class Selling(models.Model):
    revenue = models.OneToOneField(Revenue, primary_key=True, on_delete=models.CASCADE)

class Sell_list(models.Model):
    selling_revenue = models.ForeignKey(Selling, on_delete=models.CASCADE)
    list_no = models.AutoField(primary_key=True)
    quantity = models.FloatField()
    unit_price = models.FloatField()
    cloth_in_stock = models.ForeignKey('cloth.Cloth_in_stock', on_delete=models.CASCADE, related_name='cloth_sell')

class Engaging(models.Model):
    revenue = models.OneToOneField(Revenue, primary_key=True, on_delete=models.CASCADE)

class Engage_list(models.Model):
    engaging_revenue = models.ForeignKey(Engaging, on_delete=models.CASCADE)
    list_no = models.AutoField(primary_key=True)
    quantity = models.FloatField()
    unit_price = models.FloatField()
    cloth_type = models.ForeignKey('cloth.Cloth_type', on_delete=models.DO_NOTHING, null=True, related_name='cloth_engage')
    color = models.ForeignKey('cloth.Color', on_delete=models.DO_NOTHING, null=True, related_name='color_engage')
