# -*- coding: UTF-8 -*-
#! /usr/bin/env python

from mss.utils import Singleton
from tornado.web import HTTPError

import re, logging, pycurl, StringIO, simplejson

class CurlConnectionException(Exception):
    pass

class MSSCurl(Singleton):
    
    def __init__(self):
        pass
    
    def get(self, url):
        #caso ja haja uma conexao no barramento ele retornara uma mensagem de erro
        #testar se vem has_key('error_message'):
        try:
            # prepara para receber o content
            content_io = StringIO.StringIO()
                    
            # inicia o curl
            curl = pycurl.Curl()

            # url sem porta       
            curl.setopt(pycurl.URL, url)
                     
            # seta o header como list
            curl.setopt(pycurl.HTTPHEADER, ["Accept:application/json","Content-type:application/json"])
            
            # seta a resposta da conexao
            curl.setopt(pycurl.WRITEFUNCTION, content_io.write)
            
            logging.debug("[MSSCurl.get()] - get %s" % url)
            # abre a conexao
            curl.perform()
            
            logging.debug("[MSSCurl.get()] - Recuperando Dados" )
            
            # recupera o response como string
            data = content_io.getvalue()
            
            logging.debug("[MSSCurl.put()] - Response [%s]" % data)
            
            return simplejson.loads(data)
            
        except Exception, e:
            logging.exception(e)
            raise(CurlConnectionException("[MSSCurl.get() ERROR] - Problemas ao conectar com o SDE - url: %s" % url))
            
    
    def post(self, url, port, postfields):
        #caso ja haja uma conexao no barramento ele retornara uma mensagem de erro
        #testar se vem has_key('error_message'):
        
        try:
            # prepara para receber o content
            content_io = StringIO.StringIO()
                    
            # inicia o curl
            curl = pycurl.Curl()

            # url sem porta       
            curl.setopt(pycurl.URL, url)
            
            if port:       
                logging.debug("[MSSCurl.post()] - conectando na porta %s" % port)   
                # seta a porta da conexao
                curl.setopt(pycurl.PORT, port)
            
            # seta o header como list
            curl.setopt(pycurl.HTTPHEADER, ["Accept:application/json","Content-type:application/json"])
            
            # inicia um HTTP POST
            curl.setopt(pycurl.POST, 1)     
                        
            logging.debug("[MSSCurl.post()] - utilizando postfields (%s)" % postfields)
            curl.setopt(pycurl.POSTFIELDS, postfields)

            # seta a resposta da conexao
            curl.setopt(pycurl.WRITEFUNCTION, content_io.write)
            
            logging.debug("[MSSCurl.post()] - Tentando conexao" )
            # abre a conexao
            curl.perform()
            
            logging.debug("[MSSCurl.post()] - Conectado" )

            logging.debug("[MSSCurl.post()] - Recuperando Dados" )
            # recupera o response como string
            data = content_io.getvalue()

            logging.debug("[MSSCurl.post()] - Retornando json" )
            return simplejson.loads(data)
            
        except Exception, e:
            raise(CurlConnectionException("[MSSCurl.post() ERROR] - Problemas ao conectar com o SDE - url: %s" % url))
            
            
    def put(self, url):
        #caso ja haja uma conexao no barramento ele retornara uma mensagem de erro
        #testar se vem has_key('error_message'):
        try:
            # prepara para receber o content
            content_io = StringIO.StringIO()
                    
            # inicia o curl
            curl = pycurl.Curl()

            # url sem porta       
            curl.setopt(pycurl.URL, url)
            
            # seta o header como list
            curl.setopt(pycurl.HTTPHEADER, ["Accept:application/json","Content-type:application/json"])
            
            # inicia um HTTP PUT
            curl.setopt(pycurl.PUT, 1)        

            # seta a resposta da conexao
            curl.setopt(pycurl.WRITEFUNCTION, content_io.write)
            
            curl.setopt(pycurl.INFILESIZE, 0)
            
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.MAXREDIRS, 5)
            
            logging.debug("[MSSCurl.put()] - Tentando conexao" )
            # abre a conexao
            curl.perform()
            
            logging.debug("[MSSCurl.put()] - Conectado" )

            logging.debug("[MSSCurl.put()] - Recuperando Dados" )
            # recupera o response como string
            data = content_io.getvalue()
            
            logging.debug("[MSSCurl.put()] - Retornando json" )
            
            return simplejson.loads(data)
            
        except Exception, e:
            raise(CurlConnectionException("[MSSCurl.put() ERROR] - Problemas ao conectar com o SDE - url: %s" % url))
