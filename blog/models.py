from django.db import models
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=220,unique=True,blank=True)
    content=models.TextField()
    author=models.CharField(max_length=100,default='anonymous')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_at']
        indexes=[
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base=slugify(self.title)[:200]
            slug=base
            i=1
            while Post.objects.filter(slug=slug).exists():
                i+=1
                slug=f"{base}-{i}"
            self.slug=slug

        super().save(*args, **kwargs)