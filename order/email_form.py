css = """    * {
      margin: 0;
    }

    body {
      width: 100%;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;
      flex-direction: column;
      align-items: center;
      font-family: 'RockStar', Helvetica, sans-serif;
    }

    h1,
    h2,
    h3 {
      font-weight: 500;
    }

    p {
      font-size: 18px;
      color: #A0A0A0;
    }

    .container {
      width: 600px;
      height: 1200px;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;      
      flex-direction: column;
      align-items: center;
      gap: 20px;
    }

    header {
      width: 100%;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      flex-direction: column;
      align-items: center;
      padding: 30px 0;
      border-bottom: 1px solid #FFCBCC;
    }

    .products {
      width: 100%;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      flex-direction: column;
      gap: 5px;
      padding: 0 0 30px 0;
      border-bottom: 1px solid #FFCBCC;
    }

    .products__title {
      margin-bottom: 10px;
    }

    .products__list {
      width: 100%;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      flex-direction: column;
      gap: 10px;
      margin-bottom: 20px;
    }

    .products__list__item {
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      justify-content: space-between;
      width: 100%;
    }

    .products__list__item__name {
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      align-items: center;
      gap: 5px;
    }

    .products__price {
      width: 100%;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      flex-direction: column;
      margin-bottom: 10px;
    }

    .products__price__discount {
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      justify-content: space-between;
      width: 100%;
    }

    .products__price__total {
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      justify-content: space-between;
      width: 100%;
    }

    .products__price__total p {
      color: #A0A0A0;
    }

    .info {
      width: 100%;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      flex-direction: column;
      gap: 5px;
      padding: 0 0 30px 0;
      border-bottom: 1px solid #FFCBCC;
    }

    .info__title {
      margin-bottom: 10px;
    }

    .info__list {
      width: 100%;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      flex-direction: column;
      gap: 10px;
      margin-bottom: 20px;
    }

    .info__list__item {
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      gap: 10px;
      width: 100%;
    }

    .info__list__item span {
      font-size: 18px;
      font-weight: 500;
    }

    a {
      width: 100%;
      padding: 20px 0;
      font-size: 18px;
      border: none;
      color: white;
      background-color: black;
      cursor: pointer;
      display: flex;
      display:-webkit-flex;
      display:-ms-flexbox;  
      align-items: center;
      justify-content: center;
      text-decoration: none;
    }"""


def oplata(items, order, user_u, to_pay=False):
    from sberbank.models import Payment
    items_str = ""
    for i in items:
        items_str += f"""<tr>
            <td style="display: flex;color: #A0A0A0;">{i["name"]}
                <span style="color: #000;margin: 0 20px;">x{i["count"]}</span>
            </td>
            <td style="color: #000;padding-bottom: 20px;font-weight: 500;text-align: end;">{i["money"]} &#8381;</td>
        </tr>"""
    button_pay_online = ""
    if order.pay_online:
        if to_pay:
            row = Payment.objects.filter(order=order.id).last()
            print(row)
            button_pay_online = f"""
                                <tr>
                            <td colspan="3" style="padding-top: 20px;">
                                <a style="width: 100%;
                                              padding: 20px 0;
                                              font-size: 18px;
                                              border: none;
                                              color: white;
                                              background-color: black;
                                              cursor: pointer;
                                              display: flex;
                                              align-items: center;
                                              justify-content: center;
                                              text-align: center;
                                              text-decoration: none;" href="{f"https://api.tm-she.com/ru/order/pay_order/?order={order.id}"}">
                                    <span style="margin: auto;">
                                        Оплатить заказ
                                    </span>
                                </a>
                            </td>
                        </tr>"""
    sale = ""
    if user_u.distribution:
        sale = """<tr>
                        <td style="display: flex;color: #A0A0A0;">Скидка:</td>
                        <td style="color: #000;padding-bottom: 5px;font-weight: 500;font-size:22px;text-align: end;">0%</td>
                  </tr>"""
    code = f"""
        <html>
            <head>
            </head>
            <body style="width: 100%;background:white;font-family: RockStar;margin: 0;">
                <table cellspacing="0" cellpadding="0"
                    style="border:none;border-collapse:collapse;width: 90%;max-width:700px;margin: auto;">
                    <tr>
                        <td style="width: 100%;padding: 26px;justify-content: center;
                        display: flex;">
                            <img style="margin: auto;"
                                src="https://api.tm-she.com/staticfiles/img/email.png"
                                alt="SHE" width="200px" />
                        </td>
                    </tr>
                    <tr style="border-bottom: 1px solid #FFCBCC;">
                    <tr>
                        <td style="color: #000;width: 90%;padding: 20px 0;">Товары</td>
                        <td style="width: 5%;"></td>
                    </tr>
                        {items_str}
                        {sale}
                    <tr>
                        <td style="display: flex;color: #A0A0A0;">Итог:</td>
                        <td style="color: #000;padding-bottom: 20px;font-weight: 500;font-size:20px;text-align: end;">{order.sum}&#8381;</td>
                    </tr>
                    </tr>
                    <tr style="border-bottom: 1px solid #FFCBCC;">
                    <tr>
                        <td style="color: #000;padding: 20px 0;">Информация</td>
                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 20px;">
                            <p style="margin: 0;color: #A0A0A0; display: flex;">Получатель: <span
                                    style="color: #000;font-weight: 500; margin-left: 10px;">{user_u.get_full_name()}</span></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 20px;">
                            <p style="margin: 0;color: #A0A0A0; display: flex;">Телефон: <span
                                    style="color: #000;font-weight: 500; margin-left: 10px;">{user_u.phone}</span>
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 20px;">
                            <p style="margin: 0;color: #A0A0A0; display: flex;">Email: <span
                                    style="color: #000;font-weight: 500; margin-left: 10px;">{user_u.email}</span></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 20px;">
                            <p style="margin: 0;color: #A0A0A0; display: flex;">Адрес: <span
                                    style="color: #000;font-weight: 500; margin-left: 10px;">{order.address}</span></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 20px;">
                            <p style="margin: 0;color: #A0A0A0; display: flex;">Способ доставки: <span
                                    style="color: #000;font-weight: 500;margin-left: 10px;">{order.delivery}</span></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 20px;">
                            <p style="margin: 0;color: #A0A0A0; display: flex;">Номер заказа: <span
                                    style="color: #000;font-weight: 500; margin-left: 10px;">{order.order_id}</span></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 20px;">
                            <p style="margin: 0;color: #A0A0A0; display: flex;">Дата: <span
                                    style="color: #000;font-weight: 500; margin-left: 10px;">{order.data_order}</span></p>
                        </td>
                    </tr>
                    </tr>
                    <tr>
                    {button_pay_online}
                    </tr>
                </table>
            </body>
        </html>
    """
    return code
