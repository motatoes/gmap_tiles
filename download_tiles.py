#!/usr/bin/python

import urllib2
import os, sys, argparse
from gmap_utils import *

import time
import random

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True):

    start_x, start_y = latlon2xy(zoom, lat_start, lon_start)
    stop_x, stop_y = latlon2xy(zoom, lat_stop, lon_stop)
    
    print "x range", start_x, stop_x
    print "y range", start_y, stop_y
    
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
    headers = { 'User-Agent' : user_agent }
    
    for x in xrange(start_x, stop_x):
        for y in xrange(start_y, stop_y):
            
            url = None
            filename = None
            
            if satellite:        
                url = "http://khm1.google.com/kh?v=87&hl=en&x=%d&y=%d&z=%d" % (x, y, zoom)
                filename = "%d_%d_%d_s.jpg" % (zoom, x, y)
            else:
                url = "http://mt1.google.com/vt/lyrs=h@162000000&hl=en&x=%d&s=&y=%d&z=%d" % (x, y, zoom)
                filename = "%d_%d_%d_r.png" % (zoom, x, y)    
    
            if not os.path.exists(filename):
                
                bytes = None
                
                try:
		    print(url)
                    req = urllib2.Request(url, data=None, headers=headers)
                    response = urllib2.urlopen(req)
                    bytes = response.read()
                except Exception, e:
                    print "--", filename, "->", e
                    sys.exit(1)
                
                if bytes.startswith("<html>"):
                    print "-- forbidden", filename
                    sys.exit(1)
                
                print "-- saving", filename
                
                f = open(filename,'wb')
                f.write(bytes)
                f.close()
                
                time.sleep(1 + random.random())

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Prossess our agruments')
    parser.add_argument('--lat_start', type=float, nargs=1, help='The starting latitude point')
    parser.add_argument('--lat_stop', type=float, nargs=1, help='The ending latitude point')
    parser.add_argument('--lon_start', type=float, nargs=1, help='The starting longitude point')
    parser.add_argument('--lon_stop', type=float, nargs=1, help='The ending longitude point')
    parser.add_argument('--zoom', type=int, nargs=1, help='The zoom level to download')
    parser.add_argument('--satellite', type=bool, nargs=1, help='Download satellite imagery or maps?')

    args = parser.parse_args()
    
    if args.lat_start is None \
         or args.lat_stop is None \
	 or args.lon_start is None \
	 or args.lon_stop is None:

        print('NOTICE: one of the latitude or longitude arguments was not found') 
        print('using the default arguments')

	lat_start, lon_start = 46.53, 6.6
	lat_stop, lon_stop = 46.49, 6.7
    else:
	lat_start = args.lat_start[0]
        lat_stop = args.lat_stop[0]
        lon_start = args.lon_start[0]
        lon_stop = args.lon_stop[0]

    if args.zoom is None:
        print('NOTICE: zoom was not found, using the default zoom value of 13')
	zoom = 13
    else:

        zoom = args.zoom[0]

    print(lat_start)
    download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True)
