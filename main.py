import sys, requests, telnetlib, threading, os
from tcping import Ping
sys.path.append('../..')
import go, tools

def disconnectQG(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    uuid = meta_data.get('uuid')
    
    go.commonx('DELETE FROM `botConnectqg` WHERE `uuid`="{0}" and `uid`={1} and `gid`={2}'.format(uuid, uid, gid))
    go.send(meta_data, '[CQ:face,id=161] 解绑成功！')

def connectQG(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    uuid = meta_data.get('uuid')
    
    if not go.selectx('SELECT * FROM `botConnectqg` WHERE `uuid`="{0}" and `uid`={1} and `gid`={2}'.format(uuid, uid, gid)):
        go.commonx('INSERT INTO `botConnectqg` (`uuid`,`uid`,`gid`) VALUES ("{0}",{1},{2});'.format(uuid, message, gid))
        go.send(meta_data, '[CQ:face,id=161] 绑定成功！')
    else:
        go.send(meta_data, '[CQ:face,id=151] 该用户已经绑定过本群了！')

def connectQQ(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    message1 = message.split(' ')
    userid = message1[0]
    pswd = message1[1]
    listtt = go.selectx("SELECT * FROM `into` WHERE `id` = "+str(userid), database='php10')
    listt = listtt[0]
    if listt.get('qqpswd') == pswd and listt.get('qqpswd') != '':
        go.commonx('UPDATE `into` SET `qqstate`='+str(uid)+', `qqpswd`="" WHERE `id`='+str(userid), database='php10')
        go.send(meta_data, '[CQ:face,id=161] 绑定成功！')
    else:
        go.send(meta_data, '[CQ:face,id=151] 参数二（密钥）不正确，禁止冒充他人绑定！')
        
        
# ---站长工具---
def get_ip_status(meta_data, ip, port):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    server = telnetlib.Telnet()
    try:
        server.open(ip,port)
        go.send(meta_data, '{0} port {1} is open'.format(ip, port))
    finally:
        server.close()
        
def telnetport(meta_data, minport=20, maxport=36500):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    if '127.0.0.1' in message:
        go.send(meta_data, '禁止扫描我的服务器！')
        return 
    
    host = message
    threads = []
    for port in range(minport, maxport):
        t = threading.Thread(target=get_ip_status,args=(meta_data, host, port))
        t.start()
        threads.append(t)
 
    for t in threads:
        t.join()

def whois(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    con = os.popen('whois '+str(message))
    go.send(meta_data, con.read())

def ping_check(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    message1 = message.split(' ')
    ip = message1[0]
    port = message1[1]
    
    go.send(meta_data, '正在努力ping中...')
    ping = Ping(ip, port, 60)
    ping.ping(10)

    ret = ping.result.rows
    for r in ret:
        go.send(meta_data, r)
    ret = ping.result.raw
    ret = ping.result.table
