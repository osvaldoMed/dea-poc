import scrapy
import json
import base64
from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class AllDEASpider(scrapy.Spider):
    name = 'all'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'


    def start_requests(self):
        script_val = """
            function main(splash, args)
                --------------------------------------------------------------------------
                ------------------------ helper functions --------------------------------
                --------------------------------------------------------------------------
                function send_text(sel, text)
                    splash:select(sel):focus()
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
                --------------------------------------------------------------------------

                pngTable = {}  -- <==== Array to save png screenshots
                htmlTable = {} -- <==== Array to save HTML screenshots

                --------------------------------------------------------------------------
                ------------------------ GO to DEA website -------------------------------
                --------------------------------------------------------------------------
                assert(splash:go(args.url))

                --------------------------------------------------------------------------
                ------------------------ login_0 -- DEA NUMBER----------------------------
                --------------------------------------------------------------------------
                wait_for_element('#pform\\\\:deaNumber') 
                send_text('#pform\\\\:deaNumber', 'FE9093028')

                pngTable['0'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['0'] = splash:html()   -- <=================== HTML SCREENSHOT
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

                pngTable['1'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['1'] = splash:html()   -- <=================== HTML SCREENSHOT
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

                pngTable['2'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['2'] = splash:html()   -- <=================== HTML SCREENSHOT
                -- ==CLICK validate dob button
                splash:select('#checkDob\\\\:validateDob'):mouse_click()

                --------------------------------------------------------------------------
                ------------------------ login_3 -- CHECKBOX -----------------------------
                --------------------------------------------------------------------------
                wait_for_element('#ackForm\\\\:acknowledgementCheckbox_input')
                -- CLICK checkmark box
                assert(splash:select('#ackForm\\\\:acknowledgementCheckbox_input'))
                splash:select('span.ui-c'):mouse_click()
                assert(splash:wait(0.5))
                -- intermedian click to make next possible
                assert(splash:select('table'))
                splash:select('table'):mouse_click()
                assert(splash:wait(0))
                pngTable['3'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['3'] = splash:html()   -- <=================== HTML SCREENSHOT
                -- CLICK next button
                splash:select('button[type=submit]'):mouse_click()

                --------------------------------------------------------------------------
                ------------------------ login_4 -- DEA NUMBER AGAIN ---------------------
                --------------------------------------------------------------------------
                wait_for_element('#validationForm\\\\:deaNumber')
                wait_for_element('#validationForm\\\\:proceed')

                send_text('#validationForm\\\\:deaNumber', 'FE9093028')

                pngTable['4'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['4'] = splash:html()   -- <=================== HTML SCREENSHOT

                -- Click next 
                splash:select('#validationForm\\\\:proceed'):mouse_click()
                assert(splash:wait(10))

                --------------------------------------------------------------------------
                ------------------- PROVIDERS DEA INFORMATION PAGE -----------------------
                --------------------------------------------------------------------------
                wait_for_element('#validationForm\\\\:j_idt26')
                pngTable['5'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['5'] = splash:html()   -- <=================== HTML SCREENSHOT

                local entries = splash:history()
                local last_response = entries[#entries].response

                return {
                    html = splash:html(),
                    cookies = splash:get_cookies(),
                    headers = last_response.headers,
                    png_dict = pngTable,
                    html_dict = htmlTable,
                    }
            end"""
        
        script_lic = """
            function main(splash, args)
                --------------------------------------------------------------------------
                ------------------------ helper functions --------------------------------
                --------------------------------------------------------------------------
                function send_text(sel, text)
                    splash:select(sel):focus()
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
                --------------------------------------------------------------------------

                pngTable = {}  -- <==== Array to save png screenshots
                htmlTable = {} -- <==== Array to save HTML screenshots

                --------------------------------------------------------------------------
                ------------------------ GO to DEA website -------------------------------
                --------------------------------------------------------------------------
                assert(splash:go(args.url))

                --------------------------------------------------------------------------
                ------------------------ login_0 -- DEA NUMBER----------------------------
                --------------------------------------------------------------------------
                wait_for_element('#pform\\\\:deaNumber') 
                send_text('#pform\\\\:deaNumber', 'FE9093028')

                pngTable['0'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['0'] = splash:html()   -- <=================== HTML SCREENSHOT
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

                pngTable['1'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['1'] = splash:html()   -- <=================== HTML SCREENSHOT
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

                pngTable['2'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['2'] = splash:html()   -- <=================== HTML SCREENSHOT
                -- ==CLICK validate dob button
                splash:select('#checkDob\\\\:validateDob'):mouse_click()

                --------------------------------------------------------------------------
                ------------------------ Arrived to Print Certificate Page ---------------
                --------------------------------------------------------------------------
                wait_for_element('#printCertForm\\\\:printCertButton')
                pngTable['3'] = splash:png()   -- <===================== PNG SCREENSHOT
                htmlTable['3'] = splash:html()   -- <=================== HTML SCREENSHOT


                local entries = splash:history()
                local last_response = entries[#entries].response

                return {
                    html = splash:html(),
                    cookies = splash:get_cookies(),
                    headers = last_response.headers,
                    png_dict = pngTable,
                    html_dict = htmlTable,
                    }
            end"""

        init_url_val = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/validationLogin'
        init_url_lic = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/dupeCertLogin'

        request_val = SplashRequest(
            url=init_url_val,
            callback=self.login_1_val,
            endpoint='execute',
            session_id=1,
            args={'lua_source': script_val, 'timeout': 3600},
        )        
        request_lic = SplashRequest(
            url=init_url_lic,
            callback=self.login_1_lic,
            endpoint='execute',
            session_id=2,
            args={'lua_source': script_lic, 'timeout': 3600},
        )
    
        return [request_val, request_lic]

    def login_1_val(self, response):
        self.logger.info(f'RECEIVED SPLASH RESPONSE VAL')
        save_dir = 'validation_results'
        save_name = 'validation'

        #### save png screenshots
        png_dict = response.data['png_dict']
        for i, png in png_dict.items():
            i = int(i)
            imgdata = base64.b64decode(png)
            filename = f'./{save_dir}/img/{save_name}_{i:02d}.png'

            with open(filename, 'wb') as f:
                f.write(imgdata)
            self.logger.info(f'SAVED screenshot {i:02d} to: {filename}')

        #### save HTML screenshots
        html_dict = response.data['html_dict']
        for i, html in html_dict.items():
            i = int(i)
            filename = f'./{save_dir}/html/{save_name}_{i:02d}.html'

            with open(filename, 'wt') as f:
                f.write(html)
            self.logger.info(f'SAVED HTML {i:02d} to: {filename}')

        #### BUILD last post request to get PDF file
        download_url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/main?execution=e1s4'
        cookie_list = response.data['cookies']
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

        request = FormRequest(
            url=download_url,
            callback= self.save_pdf_val,
            formdata=formdata,
            method='POST',
            headers=headers,
            cookies=cookie_list,
        )

        return request


    def save_pdf_val(self, response):
        self.logger.info(f'<<<<<<<<<< RECEIVED PDF RESPONSE VAL >>>>>>>>>')
        save_dir = 'validation_results'
        save_name = 'validation'

        # Save PDF to local Storage
        pdf_filename = f'./{save_dir}/files/{save_name}_file.pdf'
        pdf_data = response.body
        with open(pdf_filename, 'wb') as f:
            f.write(pdf_data)
        self.logger.info(f'SAVED DEA VERIFICATION PDF {pdf_filename}')
        
        return

    
    def login_1_lic(self, response):
        self.logger.info(f'RECEIVED SPLASH RESPONSE LIC')
        save_dir = 'license_results'
        save_name = 'license'

        #### save png screenshots
        png_dict = response.data['png_dict']
        for i, png in png_dict.items():
            i = int(i)
            imgdata = base64.b64decode(png)
            filename = f'./{save_dir}/img/{save_name}_{i:02d}.png'

            with open(filename, 'wb') as f:
                f.write(imgdata)
            self.logger.info(f'SAVED screenshot {i:02d} to: {filename}')

        #### save HTML screenshots
        html_dict = response.data['html_dict']
        for i, html in html_dict.items():
            i = int(i)
            filename = f'./{save_dir}/html/{save_name}_{i:02d}.html'

            with open(filename, 'wt') as f:
                f.write(html)
            self.logger.info(f'SAVED HTML {i:02d} to: {filename}')

        #### BUILD last post request to get PDF file
        download_url = 'https://apps.deadiversion.usdoj.gov/webforms2/spring/main?execution=e1s2'
        cookie_list = response.data['cookies']
        formdata = {
            'printCertForm': 'printCertForm',
            'printCertForm:printCertButton': '',
            'javax.faces.ViewState': 'e1s2',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Referer': 'https://apps.deadiversion.usdoj.gov/webforms2/spring/main?execution=e1s2',
        }

        request = FormRequest(
            url=download_url,
            callback= self.save_pdf_lic,
            formdata=formdata,
            method='POST',
            headers=headers,
            cookies=cookie_list,
        )

        return request

    def save_pdf_lic(self, response):
        self.logger.info(f'<<<<<<<<<< RECEIVED PDF RESPONSE LIC >>>>>>>>>')
        save_dir = 'license_results'
        save_name = 'license'

        # Save PDF to local Storage
        pdf_filename = f'./{save_dir}/files/{save_name}_file.pdf'
        pdf_data = response.body
        with open(pdf_filename, 'wb') as f:
            f.write(pdf_data)
        self.logger.info(f'SAVED DEA Certificate PDF {pdf_filename}')
        
        return




