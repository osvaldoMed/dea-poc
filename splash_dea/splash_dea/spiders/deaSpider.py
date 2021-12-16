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

                pngTable = {}

                -- Go to DEA website and wait to load
                assert(splash:go(args.url))
                assert(splash:wait(1))

                --
                -- login_0 -- DEA NUMBER
                --
                focus('#pform\\\\:deaNumber')
                splash:send_text('FE9093028')   -- <========== DEA NUMBER
                assert(splash:wait(0))
                pngTable['0'] = splash:png()
                -- Click next 
                splash:select('#pform\\\\:validateDeaNumberButton'):mouse_click()
                assert(splash:wait(5))


                --
                -- login_1 -- PERSONAL DATA
                --
                -- Focus input field and fill it with dea number
                focus('#csa_lastName')
                splash:send_text('Estler')   -- <========== LAST NAME
                assert(splash:wait(1))
                focus('#csa_ssn')
                splash:send_text('628225151')   -- <========== SSN
                assert(splash:wait(1))
                focus('#csa_zip')
                splash:send_text('78749')   -- <========== ZIP CODE
                assert(splash:wait(1))
                focus('#csa_expMonth')
                splash:send_text('08')   -- <========== EXP MONTH
                assert(splash:wait(1))
                focus('#csa_expYear')
                splash:send_text('2022')   -- <========== EXP YEAR
                assert(splash:wait(1))
                pngTable['1'] = splash:png()

                -- Select LOGIN button and click it
                assert(splash:select('input[type=submit]'))
                splash:select('input[type=submit]'):mouse_click()
                assert(splash:wait(10))

                --
                -- login_2 -- DATE OF BIRTH
                --
                -- HOVER validate dob button
                assert(splash:select('button[type=submit]'))
                splash:select('button[type=submit]'):mouse_hover()
                assert(splash:wait(0.5))
                pngTable['2'] = splash:png()
                -- Focus input field and fill it with dea number
                assert(splash:select('input[type=text]'))
                focus('input[type=text]')
                splash:send_text('04/27/1988')   -- <========== DATE OF BIRTH
                assert(splash:wait(1))
                pngTable['3'] = splash:png()
                -- intermedian click to make calendar dissapear
                assert(splash:select('table'))
                splash:select('table'):mouse_click()
                assert(splash:wait(0.2))
                pngTable['4'] = splash:png()
                -- SECOND intermedian click to make validate button clickable
                splash:select('table'):mouse_click()
                assert(splash:wait(0.2))
                pngTable['4'] = splash:png()
                -- HOVER validate dob button
                assert(splash:select('button[type=submit]'))
                splash:select('button[type=submit]'):mouse_hover()
                assert(splash:wait(1))
                pngTable['5'] = splash:png()

                splash:select('button[type=submit]'):mouse_click()
                assert(splash:wait(5))
                pngTable['6'] = splash:png()


                


                local entries = splash:history()
                local last_response = entries[#entries].response

                return {
                    html = splash:html(),
                    cookies = splash:get_cookies(),
                    headers = last_response.headers,
                    png_dict = pngTable,
                    }
            end"""

        url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin'

        request = SplashRequest(
            url=url,
            callback=self.login_1,
            endpoint='execute',
            session_id=1,
            args={'lua_source': script, 'timeout': 3600},
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

        png_dict = response.data['png_dict']

        for i, png in png_dict.items():
            i = int(i)
            self.logger.info(f'GENERATING start_request response png_{i:02d}')
            imgdata = base64.b64decode(png)
            filename = f'./img/dea_{i:02d}.png'

            with open(filename, 'wb') as f:
                f.write(imgdata)


