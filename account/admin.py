from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserModelAdmin(BaseUserAdmin):
 

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','roll_no','email', 'full_name','isverified', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('roll_no','email', 'password')}),
        ('Personal info', {'fields': ('full_name','isverified','gender','branch','mobile_number','year')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('roll_no','email', 'full_name','gender','branch','mobile_number','year','isverified', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','id','roll_no')
    ordering = ('roll_no',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
# Register your models here.
