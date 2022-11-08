from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Coupon(models.Model):
    # Field name made lowercase.
    coupon_id = models.IntegerField(db_column='Coupon_ID', primary_key=True)
    # Field name made lowercase.
    platform = models.ForeignKey(
        'Platforms', models.DO_NOTHING, db_column='Platform_ID', blank=True, null=True)
    # Field name made lowercase.
    discount = models.DecimalField(
        db_column='Discount', max_digits=3, decimal_places=2, blank=True, null=True)
    # Field name made lowercase.
    expiry = models.DateField(db_column='Expiry', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Coupon'


class Customers(models.Model):
    # Field name made lowercase.
    customer_id = models.IntegerField(
        db_column='Customer_ID', primary_key=True)
    # Field name made lowercase.
    last_name = models.CharField(
        db_column='Last_Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    first_name = models.CharField(
        db_column='First_Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    address = models.CharField(
        db_column='Address', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    phone = models.FloatField(db_column='Phone', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customers'


class Foods(models.Model):
    # Field name made lowercase.
    item_id = models.IntegerField(db_column='Item_ID', primary_key=True)
    # Field name made lowercase.
    restaurant = models.ForeignKey(
        'Restaurants', models.DO_NOTHING, db_column='Restaurant_ID', blank=True, null=True)
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Foods'


class Login(models.Model):
    # Field name made lowercase.
    login_id = models.CharField(
        db_column='Login_ID', primary_key=True, max_length=30)
    # Field name made lowercase.
    customer = models.ForeignKey(
        Customers, models.DO_NOTHING, db_column='Customer_ID', blank=True, null=True)
    # Field name made lowercase.
    password = models.CharField(
        db_column='Password', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Login'


class Orders(models.Model):
    # Field name made lowercase.
    order_id = models.IntegerField(db_column='Order_ID', primary_key=True)
    # Field name made lowercase.
    coupon = models.ForeignKey(
        Coupon, models.DO_NOTHING, db_column='Coupon_ID', blank=True, null=True)
    # Field name made lowercase.
    customer = models.ForeignKey(
        Customers, models.DO_NOTHING, db_column='Customer_ID', blank=True, null=True)
    # Field name made lowercase.
    item_id_list = models.CharField(
        db_column='Item_ID_List', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)
    # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Orders'


class Platforms(models.Model):
    # Field name made lowercase.
    platform_id = models.CharField(
        db_column='Platform_ID', primary_key=True, max_length=255)
    # Field name made lowercase.
    platform_name = models.CharField(
        db_column='Platform_Name', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Platforms'


class Restaurants(models.Model):
    # Field name made lowercase.
    restaurant_id = models.IntegerField(
        db_column='Restaurant_ID', primary_key=True)
    # Field name made lowercase.
    platform_id = models.CharField(
        db_column='Platform_ID', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    cuisine_type = models.CharField(
        db_column='Cuisine_Type', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    location = models.CharField(
        db_column='Location', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    name = models.CharField(
        db_column='Name', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Restaurants'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
