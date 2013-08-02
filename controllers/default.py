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

@auth.requires_login()
def static_rabbithole():
    from pyechonest import config
    from pyechonest import artist
    config.ECHO_NEST_API_KEY = "Q1EZUHKJSNE7GZWMT"
    
    listens = db(auth.user_id == db.listens.user_id).select(db.listens.ALL,orderby=~db.listens.count)
    recommended_songs = []
    similar_artists = []
    
    for listen in listens:
        songs = db(listen.song_id == db.song.id).select(db.song.ALL)
        for song in songs:
            albums = db(song.album == db.album.id).select(db.album.ALL)
            for album in albums:
                bands = db(album.band == db.band.id).select(db.band.ALL)
                for band in bands:
                    a = artist.Artist(band.name)
                    #Search for duplicacy
                    artists = filter_artist(a.similar[:5])
                    for artist in artists:
                        similar_artists.append(artist)
                    
    for artist in similar_artists:
        bands = db(db.band.name == artist).select(db.band.ALL)
        for band in bands:
            albums = db(db.album.band == band.id).select(db.album.ALL)
            for album in albums:
                songs = db(db.song.album == album.id).select(db.song.ALL)
                for song in songs:
                    recommended_songs.append(song.id)
    #Add a loop to check if user has already heard the song
    return dict(songs=recommended_songs)

@auth.requires_login()
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

def listen():
    vars = request.get_vars.copy()
    uid = int(str(vars['uid']))
    if db((db.listens.song_id== uid) and (db.listens.user_id==auth.user_id)).isempty():
        db.listens.insert(user_id=auth.user_id,song_id=uid,count=1)
    else:
        listens = db(db.listens.song_id==uid and db.listens.user_id==auth.user_id).select(db.listens.ALL)
        for i in listens:
            c = i.count
            db(i.id==db.listens.id).update(count=c+1)
    return dict()