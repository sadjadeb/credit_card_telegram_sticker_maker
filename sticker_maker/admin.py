from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import BotUser

admin.site.unregister(Group)
admin.site.site_header = "Sticker Maker Admin"


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    ordering = ('-join_date',)
    list_display = ('id', 'user_id', 'username', 'first_name', 'last_name', 'sticker_set', 'join_date')
    search_fields = ('username', 'first_name', 'last_name')

    def sticker_set(self, obj):
        url = f'https://t.me/addstickers/cc_{obj.user_id}_by_credit_card_sticker_bot'
        return format_html('<a href="{}">sticker</a>', url)

    sticker_set.short_description = 'Sticker Set'
