import scrapy
import json
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class DEASpider(scrapy.Spider):
    name = 'dea'


    def start_requests(self):
        i = 1

        request = scrapy.Request(url='https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin',
                                    callback=self.login_1,
                                    dont_filter=True)
        request.meta['cookiejar'] = i
        self.logger.info(f'INITIAL REQUEST at {request.url}')
    
        return [request]


    def login_1(self, response):
        open_in_browser(response)

        formdata = {'pform:deaNumber':'FE9093028'}
        formRequest = FormRequest.from_response(response=response,
                                        formdata=formdata,
                                        callback=self.login_2,
                                        meta={'cookiejar':response.meta['cookiejar']},
                                        dont_filter=True)
        self.logger.info(f'FIRST LOGIN REQUEST with {formdata} \n to {formRequest.url}')
        self.logger.info(f'FIRST LOGIN REQUEST COOKIES with {formRequest.headers}')

        yield formRequest



    def login_2(self, response):
        open_in_browser(response)

        formdata = {
            'csa_lastName': 'Estler', 
            'csa_ssn': '628225151', 
            'csa_zip': '78749', 
            'csa_expMonth': '08', 
            'csa_expYear': '2022',
            'csa_loginTarget': 'validationLogin',
            'submit': 'Login',
        }
        formRequest = FormRequest(url='https://apps.deadiversion.usdoj.gov/webforms2/spring/loginProcess',
                                        formdata=formdata,
                                        callback=self.login_3,
                                        meta={'cookiejar':response.meta['cookiejar']},
                                        dont_filter=True)
        self.logger.info(f'SECOND LOGIN REQUEST with {formdata} \n to {formRequest.url}')
        yield formRequest
        
    def login_3(self, response):

        self.logger.info(f'RECEIVED LAST LOGIN REQUEST FROM {response.url}')
        open_in_browser(response)



