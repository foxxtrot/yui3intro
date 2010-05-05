from django.db import models

class Registration(models.Model):
	full_name = models.CharField(max_length=60)
	email = models.EmailField(max_length=255)
	checkedin = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s <%s>" % (self.full_name, self.email)
