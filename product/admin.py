from django.contrib import admin
from product.models import Product
from apitest.models import Apitest, Apis
from apptest.models import Appcase
from webtest.models import Webcase
# Register your models here.


class ApisAdmin(admin.TabularInline):
    list_display = ['apiname', 'apiurl', 'apiparamvalue', 'apimethod', 'apiresult',
                    'apistatus', 'create_time', 'id', 'product']
    model = Apis
    extra = 1


class AppcaseAdmin(admin.TabularInline):
    # 将app测试用例关联到产品页面，可以在产品页面编辑app测试用例
    list_play = ['appcasename', 'apptestresult', 'create_time', 'id', 'product']
    model = Appcase
    extra = 1


class WebcaseAdmin(admin.TabularInline):
    # 将app测试用例关联到产品页面，可以在产品页面编辑app测试用例
    list_play = ['webcasename', 'webtestresult', 'create_time', 'id', 'product']
    model = Webcase
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc', 'producter', 'create_time', 'id']
    inlines = [ApisAdmin, AppcaseAdmin, WebcaseAdmin]

# 注册的时候，将原模型和ModelAdmin耦合起来
admin.site.register(Product, ProductAdmin)