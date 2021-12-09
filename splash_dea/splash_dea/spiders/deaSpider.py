import scrapy
import json
import base64
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class DEASpider(scrapy.Spider):
    name = 'dea'

    def start_requests(self):
        splash_args = {
            'html': 1,
            'png': 1,
            'width': 600,
            'timeout':50,
            'wait': 0.,
        }
        request = SplashRequest(url='https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin',
                                callback=self.login_1,
                                method='GET',
                                endpoint='render.json',
                                magic_response=True,
                                args=splash_args,
                                dont_filter=True,
                                )
        request.meta['splash']['session_id'] = 1
        self.logger.info(f'INITIAL REQUEST at {request.url}')
    
        return [request]


    def login_1(self, response):
        #open_in_browser(response)
        self.logger.info(f'GENERATING login_1 response pnG.')
        imgdata = base64.b64decode(response.data['png'])
        filename = './img/dea_01.png'

        with open(filename, 'wb') as f:
            f.write(imgdata)


        self.logger.info(f'SAVED login_1 response png to {filename}')

        splash_args = {
            'html': 1,
            'png': 1,
            'width': 600,
            'timeout':50,
            'wait': 0,
        }

        formdata = {'pform:deaNumber':'FE9093028'}
        formRequest = SplashFormRequest.from_response(
            response=response,
            formdata=formdata,
            callback=self.login_2,
            endpoint='render.json',
            args=splash_args,
            dont_filter=True,
        )
        formRequest.meta['splash']['session_id'] = 1
        self.logger.info(f'SENDING FIRST LOGIN REQUEST with {formdata} \n to {formRequest.url}')

        yield formRequest



    def login_2(self, response):
        self.logger.info(f'RECEIVED FIRST LOGIN RESPONSE')
        self.logger.info(f'GENERATING login_2 response png.')
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
        

