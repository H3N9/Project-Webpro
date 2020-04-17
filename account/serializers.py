from rest_framework import serializers
from . import models

class Working_timeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Working_time
        exclude = ['employee']
    
class EmployeeSerializer(serializers.ModelSerializer):
    working_times = Working_timeSerializer(many=True, read_only=True)
    class Meta:
        model = models.Employee
        fields = ['fname','lname','birthdate','age','hire_date','working_age','rating_wage_per_hour','working_times']


    def create(self,  validated_data):
        working_times_data = validated_data.pop('working_times')
        employee = models.Employee.objects.create(**validated_data)
        for working_time_data in working_times_data:
            models.Working_time.objects.create(employee=employee, **working_time_data)
        return employee