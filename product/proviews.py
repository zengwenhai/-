from django.shortcuts import render
from product.models import Product
# Create your views here.


# 产品管理
def product_manage(request):
    username = request.session.get('user', '')  # 从session中获取用户名
    product_list = Product.objects.all()  # 获取全部数据
    return render(request, 'product_manage.html', {'user': username, 'products': product_list})