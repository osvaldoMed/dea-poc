import scrapy
import json
import base64
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class DEASpider(scrapy.Spider):
    name = 'dea'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'

    def start_requests(self):
        script = """
            function main(splash, args)
            splash:go(args.url)

            local entries = splash:history()
            local last_response = entries[#entries].response

            return {
                html = splash:html(),
                png = splash:png(),
                cookies = splash:get_cookies(),
                headers = last_response.headers,
                }
            end"""

        url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin'
        headers_0 = {
            'Host': 'apps.deadiversion.usdoj.gov',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Linux",
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        request = SplashRequest(
            url=url,
            callback=self.login_1,
            endpoint='execute',
            session_id=1,
            args={'lua_source': script, 'wait':20.},
        )
        self.logger.info(f'INITIAL REQUEST to {request.url}')
        self.logger.info(f'INITIAL REQUEST HEADERS:  {request.headers}')
        self.logger.info(f'INITIAL REQUEST splash args: {request.meta["splash"]}')
    
        return [request]

    def login_1(self, response):
        cookies = response.data['cookies']
        headers = response.data['headers']
        html = response.data['html']
        self.logger.info(f'RECEIVED start_request response')
        self.logger.info(f'COOKIES in start_request response: {cookies}')
        self.logger.info(f'HEADERS in start_request response: {headers}')
        self.logger.info(f'HTML in start_request response: {html}')


        self.logger.info(f'GENERATING start_request response png.')
        imgdata = base64.b64decode(response.data['png'])
        filename = './img/dea_01.png'

        with open(filename, 'wb') as f:
            f.write(imgdata)

    #     self.logger.info(f'SAVED start_request response png to {filename}')

        script = """
            function main(splash, args)
            splash:init_cookies(splash.args.cookies)
            splash:go(splash.args.url)

            local entries = splash:history()
            local last_response = entries[#entries].response

            return {
                html = splash:html(),
                png = splash:png(),
                cookies = splash:get_cookies(),
                headers = last_response.headers,
                }
            end"""

        url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin?execution=e2s1'
        formdata = {
            'pform': 'pform',
            'pform:deaNumber':'FE9093028',
            'pform:validateDeaNumber': '',
            'javax.faces.ViewState': 'e2s1',
        }

        request = SplashFormRequest(
            url=url,
            callback=self.login_2,
            formdata=formdata,
            endpoint='execute',
            session_id=1,
            args={'lua_source': script, 'cookies': cookies, 'wait':20.},
        )


        self.logger.info(f'login_1 REQUEST to {request.url}')
        self.logger.info(f'login_1 REQUEST HEADERS:  {request.headers}')
        self.logger.info(f'login_1 REQUEST splash args: {request.meta["splash"]}')

        return request

    #     self.logger.info(f'GENERATING start_request response png.')
    #     imgdata = base64.b64decode(response.data['png'])
    #     filename = './img/dea_01.png'

    #     with open(filename, 'wb') as f:
    #         f.write(imgdata)

    #     self.logger.info(f'SAVED start_request response png to {filename}')


    #     script = """
    #         function main(splash, args)
    #         splash:init_cookies(splash.args.cookies)
    #         splash:go(splash.args.url)

    #         return {
    #             html = splash:html(),
    #             png = splash:png(),
    #             cookies = splash:get_cookies(),
    #             }
    #         end"""

    #     formdata = {'pform:deaNumber':'FE9093028'}
    #     formRequest = SplashFormRequest(
    #         url=response.url,
    #         formdata=formdata,
    #         callback=self.login_2,
    #         endpoint='execute',
    #         session_id=1,
    #         args={'lua_source': script, 'cookies': response.data['cookies'], 'wait': 10.},
    #         dont_filter=True,
    #     )
    # #

    #     self.logger.info(f'SENDING login_1 REQUEST with \n formdata:{formdata} \n to {formRequest.url} \n and args:{formRequest.meta["splash"]["args"]}')

    #     yield formRequest



    def login_2(self, response):
        cookies = response.data['cookies']
        headers = response.data['headers']
        html = response.data['html']
        self.logger.info(f'RECEIVED login_1 response')
        self.logger.info(f'COOKIES in login_1 response: {cookies}')
        self.logger.info(f'HEADERS in login_1 response: {headers}')
        self.logger.info(f'HTML in login_1 response: {html}')
    #     self.logger.info(f'RECEIVED login_1 response')
    #     self.logger.info(f'COOKIES in login_1 response: {response.data["cookies"]}')

        self.logger.info(f'GENERATING login_1 response png.')
        imgdata = base64.b64decode(response.data['png'])
        filename = './img/dea_02.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)

        self.logger.info(f'SAVED login_2 response png to {filename}')
        
    #     open_in_browser(response)\n to {formRequest.url}

    #     formdata = {
    #         'csa_lastName': 'Estler', 
    #         'csa_ssn': '628225151', 
    #         'csa_zip': '78749', 
    #         'csa_expMonth': '08', 
    #         'csa_expYear': '2022',
    #         'csa_loginTarget': 'validationLogin',
    #         'submit': 'Login',
    #     }
    #     formRequest = FormRequest(url='https://apps.deadiversion.usdoj.gov/webforms2/spring/loginProcess',
    #                                     formdata=formdata,
    #                                     callback=self.login_3,
    #                                     meta={'cookiejar':response.meta['cookiejar']},
    #                                     dont_filter=True)
    #     self.logger.info(f'SECOND LOGIN REQUEST with {formdata} \n to {formRequest.url}')
    #     yield formRequest
        

