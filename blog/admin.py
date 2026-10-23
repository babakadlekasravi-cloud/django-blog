from django.contrib import admin
from blog.models import Category,Post,Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['title','author','category','status']
    list_filter=['status']
    search_fields=['title','content']

class CommentAdmin(admin.ModelAdmin):
    list_display=['name','subject','email','approved','created_date']
    list_filter=['approved']
    search_fields=['name']


admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Comment,CommentAdmin)
