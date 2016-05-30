__author__ = 'ronsneh'

from flask import Flask, render_template

import threading
import urllib2
import json

app = Flask(__name__)
items = []
threadLock = threading.Lock()
threads = []
searchLink = "https://www.googleapis.com/customsearch/v1" \
             "?q=%(q)s" \
             "&num=%(num)" \
             "d&key=AIzaSyDfM13UigJxr9AHsV15y37lhfEMS66zvS8" \
             "&cx=010864854750275129855:bq0gjrtykuk&alt=json"

with open('links.txt', 'r') as readfile:
    data_file = readfile.read()
    dataLines = data_file.splitlines()


@app.route('/')
def dash():
    for line in dataLines:
        thread = SearchThread(line)
        thread.start()
        threads.append(thread)

    for _thread in threads:
        _thread.join()

    return render_template('index.html', items=items)


class SearchThread(threading.Thread):
    def __init__(self, term):
        threading.Thread.__init__(self)
        self.term = term

    def run(self):
        threadLock.acquire()
        link = searchLink % {
            "start": 0,
            "num": 1,
            "q": self.term,
        }
        print "Start Thread name %s. open url for %s" % (self.getName(), self.term)

        try:
            response = urllib2.urlopen(link)
            response_json = json.loads(response.read())
            if 'items' in response_json:
                response_items = response_json['items']
                first_item = response_items[0]
                items.append({
                    "link": first_item['link'],
                    "title": first_item['title'],
                    "snippet": first_item['snippet']
                })
            else:
                print "Could not fetch item for %s" % self.term
        except urllib2.HTTPError as e:
            print "Thread name %s, could not fetch %s. (%s)" % (self.getName(), self.term, e)

        threadLock.release()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')