# -*- coding: utf8 -*-
import urllib
import urllib2
import urlparse
import json

class Scrive(object):
    """
    This module helps you to integrate Scrive.com into your python application.

    naming:
    OAUTH_CONSUMER_KEY: Client credentials identifier
    OAUTH_TOKEN:        Token credientials identifier: oauth_token
    OAUTH_SIGNATURE:    Client credentials secret&Token credentials secret
    """
    OAUTH_CONSUMER_KEY          = ''  # Client credentials identifier
    OAUTH_TOKEN                 = ''  # Token credentials identifier
    OAUTH_SIGNATURE             = "&" # Client credentials secret&Token credentials secret

    # Callback url to your website. (optional)
    CALLBACK_URL_TEMPLATE = 'http://example.com/api/scrive_callback/%s/'

    BASE_URL = 'https://scrive.com/'

    def __init__(self, oauth_consumer_key, oauth_token, oauth_signature, callback_url_template):
        self.OAUTH_CONSUMER_KEY = oauth_consumer_key
        self.OAUTH_TOKEN = oauth_token
        self.OAUTH_SIGNATURE = oauth_signature
        self.CALLBACK_URL_TEMPLATE = callback_url_template

    def get_oauth_temporary_credentials(self):
        """
        This method can request temporary credentials that you generally don't need.
        Credentials specified in OAUTH_CONSUMER_KEY, OAUTH_TOKEN and OAUTH_SIGNATURE are enough.
        """
        URL = urlparse.urljoin(self.BASE_URL, '/oauth/temporarycredentials?privileges=DOC_CREATE+DOC_SEND+DOC_CHECK')

        headers = '''
        OAuth realm="Scrive",
        oauth_consumer_key="%s",
        oauth_signature_method="PLAINTEXT",
        oauth_callback="%s",
        oauth_signature="%s",
        privileges="DOC_CREATE"
        ''' % (
            self.OAUTH_CONSUMER_KEY,
            '',
            self.OAUTH_SIGNATURE,
        )
        headers = headers.strip().replace('\n', '').replace(' ', '').replace(',', ', ')

        headers = {'Authorization': headers}
        request = urllib2.Request(URL, headers=headers)

        try:
            response = urllib2.urlopen(request)
            credentials = response.read()

        except urllib2.HTTPError, error:
            html = error.read()
            print html
            raise error
        else:
            return dict(urlparse.parse_qsl(credentials))

    def create_document(self, template_id):
        """
        Create new document from template.
        """
        URL = urlparse.urljoin(self.BASE_URL, '/api/createfromtemplate/%s' % template_id)
        headers = '''
            oauth_consumer_key="%s",
            oauth_signature_method="PLAINTEXT",
            oauth_token="%s",
            oauth_signature="%s"
            '''%(self.OAUTH_CONSUMER_KEY, self.OAUTH_TOKEN, self.OAUTH_SIGNATURE)
        headers = headers.strip().replace('\n', '').replace(' ', '').replace(',', ', ')
        headers = {'Authorization': headers}

        data = urllib.urlencode({})
        request = urllib2.Request(URL, data, headers=headers)

        try:
            response = urllib2.urlopen(request)
            html = response.read()
        except urllib2.HTTPError, error:
            html = error.read()
            print html
            raise error

        resp_json = json.loads(html)

        return resp_json

    def check_state(self, document_id):
        """
        Just print the document's json
        """
        URL = urlparse.urljoin(self.BASE_URL, '/api/get/%s' % document_id)
        headers = '''
            oauth_consumer_key="%s",
            oauth_signature_method="PLAINTEXT",
            oauth_token="%s",
            oauth_signature="%s"
            '''%(self.OAUTH_CONSUMER_KEY, self.OAUTH_TOKEN, self.OAUTH_SIGNATURE)
        headers = headers.strip().replace('\n', '').replace(' ', '').replace(',', ', ')
        headers = {'Authorization': headers}

        request = urllib2.Request(URL, headers=headers)

        try:
            response = urllib2.urlopen(request)
            html = response.read()
        except urllib2.HTTPError, error:
            html = error.read()
            print html
            raise error

        resp_json = json.loads(html)

        return resp_json

    def send_reminder(self, document_id):
        """
        remind customer that document is awaiting his/her signature.
        """
        URL = urlparse.urljoin(self.BASE_URL, '/api/remind/%s/' % document_id)
        headers = '''
            oauth_consumer_key="%s",
            oauth_signature_method="PLAINTEXT",
            oauth_token="%s",
            oauth_signature="%s"
            '''%(self.OAUTH_CONSUMER_KEY, self.OAUTH_TOKEN, self.OAUTH_SIGNATURE)
        headers = headers.strip().replace('\n', '').replace(' ', '').replace(',', ', ')
        headers = {'Authorization': headers}

        data = urllib.urlencode({})
        request = urllib2.Request(URL, data, headers=headers)

        try:
            response = urllib2.urlopen(request)
            html = response.read()
        except urllib2.HTTPError, error:
            html = error.read()
            print html
            raise error

        resp_json = json.loads(html)

        return resp_json

    def update_document(self, resp_json, customer_data, delivery_method='mail', authentication='mail', lang='en'):
        """
        modify signatories to include customer data and other settings.
        WARNING: we assume that you are first signatory and customer is second.
        """

        CALLBACK_URL = self.CALLBACK_URL_TEMPLATE % resp_json['id']

        for k, v in customer_data.iteritems():
            self._set_field(k, v, resp_json['signatories'][1])

        resp_json['delivery']       = delivery_method
        resp_json['authentication'] = authentication

        resp_json['lang'] = lang
        resp_json['apicallbackurl'] = CALLBACK_URL

        URL = urlparse.urljoin(self.BASE_URL, '/api/update/%s' % resp_json['id'])

        headers = '''
            oauth_consumer_key="%s",
            oauth_signature_method="PLAINTEXT",
            oauth_token="%s",
            oauth_signature="%s"
            '''%(self.OAUTH_CONSUMER_KEY, self.OAUTH_TOKEN, self.OAUTH_SIGNATURE)

        headers = headers.strip().replace('\n', '')
        headers = {'Authorization': headers}

        data = urllib.urlencode({'json': json.dumps(resp_json)})
        request = urllib2.Request(URL, data, headers=headers)
        response = urllib2.urlopen(request)

        try:
            response = urllib2.urlopen(request)
            html = response.read()
        except urllib2.HTTPError, error:
            html = error.read()
            print html
            raise error

        resp_json = json.loads(html)

        return resp_json


    def download_document(self, document_id):
        """
        save pdf to disk.
        """

        filename = 'document_{0}.pdf'.format(document_id)

        URL = urlparse.urljoin(self.BASE_URL, '/api/downloadmainfile/{0}/document_{0}.pdf'.format(document_id) )
        # print URL

        headers = '''
            oauth_consumer_key="%s",
            oauth_signature_method="PLAINTEXT",
            oauth_token="%s",
            oauth_signature="%s"
            '''%(self.OAUTH_CONSUMER_KEY, self.OAUTH_TOKEN, self.OAUTH_SIGNATURE)

        headers = headers.strip().replace('\n', '')
        headers = {'Authorization': headers}
        data = urllib.urlencode({})
        request = urllib2.Request(URL, headers=headers)

        try:
            response = urllib2.urlopen(request)
            file_content = response.read()
        except urllib2.HTTPError, error:
            html = error.read()
            # print html
            raise error
        else:
            with open(filename, 'wb') as f:
                f.write(file_content)


    def sign_document(self, resp_json):
        """
        Sign your document automatically.
        """
        URL = urlparse.urljoin(self.BASE_URL, '/api/sign/{0}/{1}'.format(resp_json['id'], resp_json['signatories'][0]['id']) )

        headers = '''
            oauth_consumer_key="%s",
            oauth_signature_method="PLAINTEXT",
            oauth_token="%s",
            oauth_signature="%s"
            '''%(self.OAUTH_CONSUMER_KEY,
                 self.OAUTH_TOKEN,
                 self.OAUTH_SIGNATURE)

        headers = headers.strip().replace('\n', '')
        headers = {'Authorization': headers}

        data = urllib.urlencode( {'fields': json.dumps([])} )

        request = urllib2.Request(URL, data, headers=headers)

        try:
            response = urllib2.urlopen(request)
            html = response.read()
        except urllib2.HTTPError, error:
            html = error.read()
            print html
            raise error

        return html


    def ready_document(self, resp_json):
        """
        Prepare for signing.
        """

        URL = urlparse.urljoin(self.BASE_URL, '/api/ready/%s' % resp_json['id'])

        headers = '''
            oauth_consumer_key="%s",
            oauth_signature_method="PLAINTEXT",
            oauth_token="%s",
            oauth_signature="%s"
            '''%(self.OAUTH_CONSUMER_KEY, self.OAUTH_TOKEN, self.OAUTH_SIGNATURE)

        headers = headers.strip().replace('\n', '')
        headers = {'Authorization': headers}
        data = urllib.urlencode({})
        request = urllib2.Request(URL, data, headers=headers)

        try:
            response = urllib2.urlopen(request)
            html = response.read()
        except urllib2.HTTPError, error:
            html = error.read()
            # print html
            raise error

        return html

    def _set_field(self, name, value, obj):
        '''
        helper function for setting value of a field
        '''
        for i, x in enumerate(obj['fields']):
            if x['name'] == name:
                x['value'] = value
                # print 'Updated', name, value
                break
        else:
            print 'Field', name, 'not found'

        return obj
