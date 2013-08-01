# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def tester():
    return dict()

@auth.requires_login()
def list_songs():
    songs=db().select(db.song.ALL,orderby=db.song.title)
    return dict(songs=songs)

def filter_artist(artists):
    a = []
    for artist in artists:
        a.append(str(artist))
    return a

def static_rabbithole(band):
    import pyechonest
    artist = artist.Artist('Motherjane')#Replace with band
    similars = a.similar[:5]
    similar_artists = filter_artist(similars)
    recommended_songs = []
    for artist in similar_artists:
        bands = db(db.band.name == artist).select(db.band.ALL,orderby=db.band.title)
        for band in bands:
            albums = db(db.album.band == band.id).select(db.album.ALL)
            for album in albums:
                songs = db(db.song.album == album.id).select(db.song.ALL)
                recommended_songs.append(songs)
    #Add a loop to check if user has already heard the song
    return recommended_songs

def dynamic_rabbithole(band):
    import pyechonest
    artist = artist.Artist('Motherjane')#Replace with band
    similars = a.similar[:5]
    similar_artists = filter_artist(similars)
    recommended_songs = []
    for artist in similar_artists:
        bands = db(db.band.name == artist).select(db.band.ALL,orderby=db.band.title)
        for band in bands:
            albums = db(db.album.band == band.id).select(db.album.ALL)
            for album in albums:
                songs = db(db.song.album == album.id).select(db.song.ALL)
                recommended_songs.append(songs)
    #Add a loop to check if user has already heard the song
    return recommended_songs

def show_similar_songs():
    #Add a check/preference for songs of band are liked by the user
    return dict()