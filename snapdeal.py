import requests
from bs4 import BeautifulSoup
import json
import sys


def snapdeal(username, password, item_id):
    try:
        '''
        please select the product with no choices: 647509656596, 672053439838
        '''
        # creating the request session
        request = requests.session()
        url = "https://www.snapdeal.com/login_security_check"
        data = {'_spring_security_remember_me': 'on',
                'ajax': 'true',
                'j_mobile': 'false',
                'j_otp': '',
                'j_otpId': '',
                'j_password': password,
                'j_username': username,
                'keepLoggedIn': 'true',
                'webTargetUrl': ''}
        headers = {'accept': "application/json, text/javascript, */*; q=0.02",
                   'origin': "https://www.snapdeal.com",
                   'x-requested-with': "XMLHttpRequest",
                   'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                   'cntent-type': "application/x-www-form-urlencoded",
                   'referer': "https://www.snapdeal.com//login",
                   'accept-encoding': "gzip, deflate, br",
                   'accept-language': "en-US,en;q=0.8",
                   'cache-control': "no-cache",
                   'content-type': "application/x-www-form-urlencoded"}
        response = request.post(url, data=data, headers=headers)

        # checking username and password is correct?
        if json.loads(response.text)['status'] == "fail":
            return "Invalid username and password"
        url = "https://www.snapdeal.com/wishlist/add"
        payload = {"pog": item_id}
        response = request.get(url, params=payload)
        url = "https://www.snapdeal.com/mywishlist"
        response = request.get(url)
        soup = BeautifulSoup(response.text, 'html5lib')
        catalogId = soup.find("a", {"class": "wishBuy"}).get("catalog")
        supc = soup.find("a", {"class": "wishBuy"}).get("supc")
        tknbta = json.loads(soup.find("input", {"id": "alpha"}).get("value"))['items']['tknbta']
        tkndlta = json.loads((soup.find("input", {"id": "alpha"})).get("value"))['items']['tkndlta']
        tkngma = json.loads((soup.find("input", {"id": "alpha"})).get("value"))['items']['tkngma']
        tknlfa = json.loads((soup.find("input", {"id": "alpha"})).get("value"))['items']['tknlfa']
        tknmga = json.loads((soup.find("input", {"id": "alpha"})).get("value"))['items']['tknmga']
        vendorcode = soup.find("a", {"class": "wishBuy"}).get("vendorcode")
        if vendorcode == "undefined":
            return "Product have the choices"
        payload = {
            'buyBackQuoteId': '',
            'buyBackQuoteName': '',
            'buyBackQuoteValue': '',
            'catalogId': catalogId,
            'qty': '1',
            'stsQuoteId': '',
            'supc': supc,
            'tknbta': tknbta,
            'tkndlta': tkndlta,
            'tkngma': tkngma,
            'tknlfa': tknlfa,
            'tknmga': tknmga,
            'vendorCode': vendorcode
        }
        url = "https://www.snapdeal.com/json/cart/operation/addToCart"
        request.headers.update({'Origin': 'https://www.snapdeal.com',
                                'tknlfa': tknlfa,
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'tkndlta': tkndlta,
                                'Accept': '*/*',
                                'tknmga': tknmga,
                                'tknbta': tknbta,
                                'X-Requested-With': 'XMLHttpRequest',
                                'tkngma': tkngma,
                                'Referer': 'https://www.snapdeal.com/mywishlist',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Accept-Language': 'en-US,en;q=0.8'})
        request.post(url, data=(payload), headers=headers)
        return "Successfully added to cart"
    except Exception, e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print "Please run the command: python snapdeal.py email password item_id"
        sys.exit(0)
    username, password, item_id = sys.argv[1], sys.argv[2], sys.argv[3]
    print snapdeal(username, password, item_id)
