# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Museek'),XML('&trade;&nbsp;'),
                  _class="brand",_href="#")
response.title = request.application.replace('_',' ').title()
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'list_songs'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (SPAN('Navigate', _class='highlighted'), False, 'http://web2py.com', [
        (T('Bands'), False, URL('default', 'list_bands')),
        (T('Songs'), False, URL('default', 'list_songs'), ),
            ('Dig Deeper', False, URL('default', 'static_rabbithole'),),
            (T('About Us'), False, 'http://www.web2py.com/book'),
            (T('Community'), False, None, [
                        (T('Twitter'), False, 'http://twitter.com/museek'),
                        (T('Facebook'), False, 'http://facebook.com/museek'),
                        (T('Live Chat'), False,'http://webchat.freenode.net/?channels=museek'),
                        ]),
                
                ]
         )]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
