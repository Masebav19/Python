
def str2array(string=""):
    if len(string)>0:
        array = [int(x) for x in string.split(',')]
        return array
    else:
        return False


