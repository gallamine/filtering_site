import shelve




def writeKey(key,value):

    try:
        d = shelve.open('filter_site_krufty.db')
        d[key] = value
        d.close()
        return True
    except:
        return False

def readKey(key):
    try:
        d = shelve.open('filter_site_krufty.db')
        ret_val = d[key]
        d.close()
        return ret_val
    except Exception as e:
        print e
        return False


def removeKey(key):
    del d[key]