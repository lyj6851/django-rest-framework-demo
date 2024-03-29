# encoding: utf-8
import time

from VueDjangoFrameWorkShop.settings import private_key_path, ali_pub_key_path
from goods.models import Goods
from goods.serializers import GoodsSerializer
from rest_framework import serializers
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from utils.alipay import alipay

__author__ = 'mtianyan'
__date__ = '2018/3/11 0011 16:19'


class ShopCartDetailSerializer(serializers.ModelSerializer):
    # 一条购物车关系记录对应的只有一个goods。
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")


class ShopCartSerializer(serializers.Serializer):
    # 因为用户和商品组合唯一，修改数量时，默认会报错，所以不用modelserializer
    # 使用Serializer本身最好, 因为它是灵活性最高的。
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())
    # 这里many=flase 商品数量一对一

    # 重写baseserializer
    # 对于字段的具体验证放在serializer中
    # 默认情况下，此字段是读写的，但您可以使用该read_only标志更改此行为。
    # queryset - 验证字段输入时用于模型实例查找的查询集。
    '''
    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')
    '''

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        # 相当于在fields中添加字段

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)
    singer_mobile = serializers.CharField(required=True, max_length=11, min_length=11, label='联系方式')
    nonce_str = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    # 注意名称和model的字段名一致

    # 可以对field中的重新定义，但不会引用之前的verbose_name，需要添加label

    # 支付宝
    def get_alipay_url(self, obj):
        # alipay = AliPay(
        #     appid="2016092300578435",
        #     app_notify_url="http://127.0.0.1:8000/alipay/return/",
        #     app_private_key_path=private_key_path,
        #     alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     debug=True,  # 默认False,
        #     return_url="http://127.0.0.1:8000/alipay/return/"
        # )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    # 订单号
    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    # 订单号添加到数据库
    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    # 一个订单有多个订单商品项
    goods = OrderGoodsSerialzier(many=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        # alipay = AliPay(
        #     appid="2016091200490210",
        #     app_notify_url="http://115.159.122.64:8000/alipay/return/",
        #     app_private_key_path=private_key_path,
        #     alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     debug=True,  # 默认False,
        #     return_url="http://115.159.122.64:8000/alipay/return/"
        # )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"
