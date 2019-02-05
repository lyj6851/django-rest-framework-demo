from alipay import AliPay

alipay = AliPay(
    appid="2016092300578435",
    app_notify_url="http://projectsedus.com/",
    app_private_key_path="../trade/keys/private_2048.txt",
    alipay_public_key_path="../trade/keys/alipay_key_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    debug=True,  # 默认False,
    sign_type="RSA2",  # RSA 或者 RSA2

)

url = alipay.api_alipay_trade_page_pay(
    out_trade_no="201612238181",
    total_amount=8888,
    subject="wxw",
    return_url="https://www.baidu.com",
    notify_url="https://example.com/notify"  # this is optional
)
re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
print(re_url)

'''
验证过程
signature = data.pop("sign")
success = alipay.verify(data, signature)
if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
    print("trade succeed")
'''

'''

检验支付完成？
alipay = AliPay(appid="", ...)

result = alipay.api_alipay_trade_pay(
    out_trade_no="out_trade_no",
    scene="bar_code/wave_code",
    auth_code="auth_code",
    subject="subject",
    discountable_amount=10,
    total_amount=20,
    notify_url="https://example.com/notify" # this is optional
)

if  result["code"] == "10000":
    print("Order is paid")
'''
