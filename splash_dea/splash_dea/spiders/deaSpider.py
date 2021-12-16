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
                -- function to select given element and focus it. accepts css selector
                function focus(sel)
                    splash:select(sel):focus()
                end

                -- Go to DEA website and wait to load
                assert(splash:go(args.url))
                assert(splash:wait(1))

                -- Focus input field and fill it with dea number
                focus('#pform\\\\:deaNumber')
                splash:send_text('FE9093028')   -- <========== DEA NUMBER
                assert(splash:wait(0.5))
                local png_0 = splash:png()

                -- Select NEXT button and click it with
                splash:select('#pform\\\\:validateDeaNumberButton'):mouse_click()
                assert(splash:wait(5))
                local png_1 = splash:png()

                -- Focus input field and fill it with dea number
                focus('#csa_lastName')
                splash:send_text('Estler')   -- <========== DEA NUMBER
                assert(splash:wait(1))
                focus('#csa_ssn')
                splash:send_text('628225151')   -- <========== DEA NUMBER
                assert(splash:wait(1))
                focus('#csa_zip')
                splash:send_text('78749')   -- <========== DEA NUMBER
                assert(splash:wait(1))
                focus('#csa_expMonth')
                splash:send_text('08')   -- <========== DEA NUMBER
                assert(splash:wait(1))
                focus('#csa_expYear')
                splash:send_text('2022')   -- <========== DEA NUMBER
                assert(splash:wait(1))
                

                assert(splash:wait(5))
                local png_2 = splash:png()


                local entries = splash:history()
                local last_response = entries[#entries].response

                return {
                    html = splash:html(),
                    cookies = splash:get_cookies(),
                    headers = last_response.headers,
                    png_0 = png_0,
                    png_1 = png_1,
                    png_2 = png_2,
                    }
            end"""

        url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin'

        request = SplashRequest(
            url=url,
            callback=self.login_1,
            endpoint='execute',
            session_id=1,
            args={'lua_source': script, 'deaNumber': 'FE9093028'},
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

        png_list = [
            response.data['png_0'],
            response.data['png_1'],
            response.data['png_2'],
        ]

        for i, png in enumerate(png_list):
            self.logger.info(f'GENERATING start_request response png_{i:02d}')
            imgdata = base64.b64decode(png)
            filename = f'./img/dea_{i:02d}.png'

            with open(filename, 'wb') as f:
                f.write(imgdata)



    #     self.logger.info(f'SAVED start_request response png to {filename}')

        # script = """
        #     function main(splash, args)
        #     splash:init_cookies(splash.args.cookies)
        #     splash:go(splash.args.url)

        #     local entries = splash:history()
        #     local last_response = entries[#entries].response

        #     return {
        #         html = splash:html(),
        #         png = splash:png(),
        #         cookies = splash:get_cookies(),
        #         headers = last_response.headers,
        #         }
        #     end"""

        # url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin?execution=e2s1'
        # formdata = {
        #     'pform': 'pform',
        #     'pform:deaNumber':'FE9093028',
        #     'pform:validateDeaNumber': '',
        #     'javax.faces.ViewState': 'e2s1',
        # }

        # request = SplashFormRequest(
        #     url=url,
        #     callback=self.login_2,
        #     formdata=formdata,
        #     endpoint='execute',
        #     session_id=1,
        #     args={'lua_source': script, 'cookies': cookies, 'wait':20.},
        # )


        # self.logger.info(f'login_1 REQUEST to {request.url}')
        # self.logger.info(f'login_1 REQUEST HEADERS:  {request.headers}')
        # self.logger.info(f'login_1 REQUEST splash args: {request.meta["splash"]}')

        # return request

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



    # def login_2(self, response):
    #     cookies = response.data['cookies']
    #     headers = response.data['headers']
    #     html = response.data['html']
    #     self.logger.info(f'RECEIVED login_1 response')
    #     self.logger.info(f'COOKIES in login_1 response: {cookies}')
    #     self.logger.info(f'HEADERS in login_1 response: {headers}')
    #     self.logger.info(f'HTML in login_1 response: {html}')
    # #     self.logger.info(f'RECEIVED login_1 response')
    # #     self.logger.info(f'COOKIES in login_1 response: {response.data["cookies"]}')

    #     self.logger.info(f'GENERATING login_1 response png.')
    #     imgdata = base64.b64decode(response.data['png'])
    #     filename = './img/dea_02.png'
    #     with open(filename, 'wb') as f:
    #         f.write(imgdata)

    #     self.logger.info(f'SAVED login_2 response png to {filename}')
        
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
        

