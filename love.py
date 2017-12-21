import rpyc


conn=rpyc.connect("10.142.0.2",1234,config={"allow_all_attrs":True})
obj=conn.root.DBConnection()
man=obj.getClients()
etc

