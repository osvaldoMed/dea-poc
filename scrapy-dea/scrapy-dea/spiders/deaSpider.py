import scrapy
import json
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class DEASpider(scrapy.Spider):
    name = 'dea'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'



    def start_requests(self):
        url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin'

        request = scrapy.Request(url='https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin',
                                    callback=self.login_1,
                                    dont_filter=True)
        request.meta['cookiejar'] = 1

        self.logger.info(f'INITIAL REQUEST to {request.url}')
        self.logger.info(f'INITIAL REQUEST HEADERS:  {request.headers}')
    
        return [request]


    def login_1(self, response):
        #open_in_browser(response)
        self.logger.info(f'RECEIVED start_request response')
        self.logger.info(f'HEADERS in start_request response: {response.headers}')
        formdata = {
            'pform': 'pform',
            'pform:deaNumber':'FE9093028',
            'pform:validateDeaNumber': '',
            'javax.faces.ViewState': 'e2s1',
        }
        formRequest = FormRequest.from_response(response=response,
                                        formdata=formdata,
                                        callback=self.login_2,
                                        meta={'cookiejar':response.meta['cookiejar']},
                                        dont_filter=True)

        self.logger.info(f'SENDING login_1 REQUEST with \n formdata:{formdata} \n to {formRequest.url} \n and headers:{formRequest.headers}')

        yield formRequest



    def login_2(self, response):
        open_in_browser(response)
        self.logger.info(f'RECEIVED login_1 response')
        self.logger.info(f'HEADERS in login response: {response.headers}')

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
        self.logger.info(f'SENDING login_2 REQUEST with \n formdata:{formdata} \n to {formRequest.url} \n and headers:{formRequest.headers}')

        yield formRequest
        
    def login_3(self, response):
        open_in_browser(response)
        self.logger.info(f'RECEIVED LAST LOGIN REQUEST FROM {response.url}')
        #open_in_browser(response)



