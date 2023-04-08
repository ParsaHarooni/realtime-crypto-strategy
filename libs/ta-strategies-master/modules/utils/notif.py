def set_notif(name:str,configs:dict,is_init=True):
    msg =  "Initial" if is_init else "End"
    msg = "*** "+msg + " of (" + name + ") via " + configs["symbol"] + " in the (" + configs["tf"] + ") duration ***"
    print(msg)
