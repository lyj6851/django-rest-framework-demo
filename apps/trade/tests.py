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
    out_trade_no="20161223818",
    total_amount=8888,
    subject="wxw",
    return_url="https://www.baidu.com",
    notify_url="https://example.com/notify"  # this is optional
)
re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
print(re_url)
