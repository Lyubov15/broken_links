from django.db import models

class Page(models.Model):
    url = models.URLField(max_length=500)
    check_date = models.DateTimeField(auto_now_add=True)
    is_valid_html = models.BooleanField(default=False)

    def __str__(self):
        return self.url

class Link(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='links')
    url = models.URLField(max_length=500)
    link_type = models.CharField(max_length=50)
    status_code = models.IntegerField()

    def __str__(self):
        return f"{self.url} ({self.status_code})"

class Error(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='errors')
    description = models.TextField()

    def __str__(self):
        return self.description

# Создавайте свои модели здесь.
