from django.db import models

class Cloth_in_stock(models.Model):
    quantity = models.FloatField()
    cloth_type = models.ForeignKey('Cloth_type', on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE)
    price = models.FloatField()
    def __str__(self):
        return "%s %s"%(self.cloth_type,self.color)
    

class Cloth_type(models.Model):
    name = models.CharField(max_length=255)
    cloth_desc = models.TextField(null=True)

    def __str__(self):
        return self.name
    

class Color(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to='decoration/image')

    def __str__(self):
        return self.name
    
