from django.contrib import admin
from .models import Complaint, ComplaintUpdate

class UpdateInline(admin.TabularInline):
    model = ComplaintUpdate
    extra = 0
    readonly_fields = ("author", "created_at")

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "status", "location", "created_by", "assigned_to", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description", "location")
    inlines = [UpdateInline]

admin.site.register(ComplaintUpdate)
