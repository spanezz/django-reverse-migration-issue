from django.db import models


class Grandparent(models.Model):
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=255, default="hey, you!")


class Parent(models.Model):
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=255, default="hey, you!")
    parent = models.ForeignKey(Grandparent, on_delete=models.CASCADE)


class Child(models.Model):
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=255, default="hey, you!")
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)


class Grandchild(models.Model):
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=255, default="hey, you!")
    parent = models.ForeignKey(Child, on_delete=models.CASCADE)
