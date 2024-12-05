from django.contrib import admin

from .models import Invoice, RelationInvoice


class RelationInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "unit_number",
        "resident",
        "place",
        "company",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at", "company", "place")
    search_fields = ("unit_number", "resident__email", "company")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


admin.site.register(RelationInvoice, RelationInvoiceAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("relation", "value", "ticket_number", "is_active", "created_at")
    list_filter = ("is_active", "created_at", "relation__company")
    search_fields = (
        "ticket_number",
        "relation__unit_number",
        "relation__resident__email",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


admin.site.register(Invoice, InvoiceAdmin)
