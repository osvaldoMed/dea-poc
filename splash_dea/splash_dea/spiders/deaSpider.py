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
                --------------------------------------------------------------------------
                ------------------------ helper functions --------------------------------
                --------------------------------------------------------------------------
                -- function to select given element and focus it. accepts css selector
                function focus(sel)
                    splash:select(sel):focus()
                end

                function send_text(sel, text)
                    focus(sel)
                    splash:send_text(text)
                    assert(splash:wait(1))
                end

                -- function to wait for element to be rendered and selectable on the page.
                function wait_for_element(sel)
                    while not splash:select(sel) do
                        splash:wait(0.1)
                    end
                end
                --------------------------------------------------------------------------

                pngTable = {}
                htmlTable = {}

                --------------------------------------------------------------------------
                ------------------------ GO to DEA website -------------------------------
                --------------------------------------------------------------------------
                assert(splash:go(args.url))

                --------------------------------------------------------------------------
                ------------------------ login_0 -- DEA NUMBER----------------------------
                --------------------------------------------------------------------------

                wait_for_element('#pform\\\\:deaNumber') -- <=========== Wait for (deaNumber input element)

                send_text('#pform\\\\:deaNumber', 'FE9093028')

                pngTable['0'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['0'] = splash:html()   -- <=================== html SCREENSHOT
                -- Click next 
                splash:select('#pform\\\\:validateDeaNumberButton'):mouse_click()

                --------------------------------------------------------------------------
                ------------------------ login_1 -- PERSONAL DATA ------------------------
                --------------------------------------------------------------------------
                wait_for_element('#csa_lastName') -- <=========== Wait for (lastName input element)
                wait_for_element('input[type=submit]') -- <====== Wait for LOGIN button to appear
                send_text('#csa_lastName', 'Estler')-- <========== LAST NAME
                send_text('#csa_ssn', '628225151')-- <========== SSN
                send_text('#csa_zip', '78749')-- <========== ZIP
                send_text('#csa_expMonth', '08')-- <========== EXP MONTH
                send_text('#csa_expYear', '2022')-- <========== EXP YEAR

                pngTable['1'] = splash:png()   -- <=================== SCREENSHOT
                -- Select LOGIN button and click it
                splash:select('input[type=submit]'):mouse_click()

                --------------------------------------------------------------------------
                ------------------------ login_2 -- DATE OF BIRTH ------------------------
                --------------------------------------------------------------------------
                wait_for_element('#checkDob\\\\:dobCal_input') -- <== wait for DOB field
                wait_for_element('table') -- <== wait for table element
                wait_for_element('#checkDob\\\\:validateDob') --<==== wait for DOB button

                send_text('#checkDob\\\\:dobCal_input','04/27/1988')
                
                splash:select('table'):mouse_click() -- <==== Intermedian click
                splash:select('table'):mouse_click() -- <==== Second intermedian click

                pngTable['2'] = splash:png()   -- <=================== SCREENSHOT
                -- ==CLICK validate dob button
                splash:select('#checkDob\\\\:validateDob'):mouse_click()
                assert(splash:wait(10))

                --------------------------
                -- login_3 -- checkmark---
                --------------------------
                -- CLICK checkmark box
                assert(splash:select('span.ui-c'))
                splash:select('span.ui-c'):mouse_click()
                assert(splash:wait(0.5))
                -- intermedian click to make next possible
                assert(splash:select('legend'))
                splash:select('table'):mouse_click()
                assert(splash:wait(0.2))
                pngTable['3'] = splash:png()   -- <=================== SCREENSHOT
                -- CLICK next button
                splash:select('button[type=submit]'):mouse_click()
                assert(splash:wait(10))

                ----------------------------------
                -- login_4 -- DEA NUMBER AGAIN----
                ----------------------------------
                assert(splash:select('#validationForm\\\\:deaNumber'))
                focus('#validationForm\\\\:deaNumber')
                splash:send_text('FE9093028')   -- <========== DEA NUMBER
                assert(splash:wait(0))
                pngTable['4'] = splash:png()   -- <=================== SCREENSHOT
                -- Click next 
                assert(splash:select('#validationForm\\\\:proceed'))
                splash:select('#validationForm\\\\:proceed'):mouse_click()
                assert(splash:wait(10))

                ------------------------------------------
                -- PROVIDERS DEA INFORMATION PAGE---------
                ------------------------------------------
                -- ==HOVER validate dob button
                assert(splash:select('button[type=submit]'))
                splash:select('button[type=submit]'):mouse_hover()
                assert(splash:wait(1))
                pngTable['5'] = splash:png()   -- <=================== SCREENSHOT

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
    
        return [request]

    def login_1(self, response):
        self.logger.info(f'RECEIVED start_request response')
        self.logger.info(f'RESPONSE URL = {response.url}')

        #### HANDLE cookies, headers and screenshots
        cookie_list = response.data['cookies']

        #### save screenshots
        png_dict = response.data['png_dict']
        for i, png in png_dict.items():
            i = int(i)
            imgdata = base64.b64decode(png)
            filename = f'./img/dea_{i:02d}.png'

            with open(filename, 'wb') as f:
                f.write(imgdata)
            self.logger.info(f'SAVED screenshot {filename}')

        formdata = {
            'validationForm': 'validationForm',
            'validationForm:deaNumber': 'FE9093028',
            'validationForm:j_idt95': '',
            'javax.faces.ViewState': 'e1s4',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Referer': 'https://apps.deadiversion.usdoj.gov/webforms2/spring/main?execution=e1s4',
        }

        download_url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/main?execution=e1s4'
        request = FormRequest(
            url=download_url,
            callback= self.save_pdf,
            formdata=formdata,
            method='POST',
            headers=headers,
            cookies=cookie_list,
        )

        return request

    def save_pdf(self, response):
        self.logger.info(f'<<<<<<<<<< RECEIVED PDF RESPONSE >>>>>>>>>')

        pdf_filename = 'files/dea_verification.pdf'
        with open(pdf_filename, 'wb') as f:
            f.write(response.body)
        self.logger.info(f'SAVED DEA VERIFICATION PDF {pdf_filename}')

        return




