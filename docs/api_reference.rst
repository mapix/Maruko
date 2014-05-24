API Documentation
=================

Basic Data Structure
--------------------

User::

    {
        "id": "52180037",
        "name": "颈椎君你不要疼",
        "email": "mapix.me@gmail.com",
        "avatar": "http://img3.douban.com/icon/u52180037-21.jpg",
        "create_time": "2014-05-04 08:44:15",
        "update_time": "2014-05-04 08:44:15",
    }


Flower::

    {
        "id": "10000",
        "owner_id": "52180037",
        "guardian_id": "52181137",
        "create_time": "2014-05-04 08:44:15",
        "update_time": "2014-05-04 08:44:15",
        "owner": <User Object>,
        "guardian": <User Object>,
    }


Message::

    {
        "id": "10000",
        "user_id": "52180037",
        "flower_id": "10000",
        "type": "watering" / "message",
        "text": "water me!",
        "create_time": "2014-05-04 08:44:15",
        "flower": <Flower Object>,
        "user": <User Object>,
    }


Song::

    {
        "id": "11100",
        "title": "世上只有妈妈好",
        "artist": "梁静茹",
        "play_count": 100,
        "create_time": "2014-05-04 08:44:15",
        "update_time": "2014-05-04 08:44:15",
    }


Statistics::

    {
        "flower": <Flower Object>,
        "wetness": 111,
        "temperature": 111,
        "lightness": 111,
    }


Task::

    {
        "id": "121231",
        "user_id": "1223423",
        "song_id": "1",
        "type": "music",
        "action": "play" / "stop",
        "done": true / false,
        "create_time": "2014-05-04 08:44:15",
        "update_time": "2014-05-04 08:44:15",
        "user": <User Object>,
        "song": <Song Object>,
    }



API Overview
------------

======  ==========================  ============
Method  URL                         Description
======  ==========================  ============
GET     /api/users/:id              获取用户信息
GET     /api/flowers/:id            获取花的信息
DELETE  /api/flowers/:id            删除花
POST    /api/flowers                增加花
GET     /api/songs                  获取播放列表
POST    /api/songs/:id              播放单曲
DELETE  /api/songs/:id              暂停单曲
POST    /api/registrations          设备注册
DELETE  /api/registrations          设备下线
GET     /api/messages               消息记录
POST    /api/statistics             信息收集
======  ==========================  ============


API Detail
----------

- 获取用户信息

  * 地址: GET /api/users/:id
  * 参数: 无
  * 返回::

     <User Ojbect>


- 获取花的信息

  * 地址: GET /api/flowers/:id
  * 参数: 无
  * 返回::

     <Flower Ojbect>


- 删除花

  * 地址: DELETE /api/flowers/:id
  * 参数: 无
  * 返回::

     <Common Return: success>


- 增加花

  * 地址: POST /api/flowers
  * 参数:
    + guardian_id: 看护人ID
  * 返回::

     <Flower Object>


- 获取播放列表

  * 地址: GET /api/songs
  * 参数: 无
  * 返回::

     [<Song Object> ...]


- 播放单曲

  * 地址: POST /api/songs/:id
  * 参数: 无
  * 返回::

     <Common Return: success>


- 设备上线

  * 地址: POST /api/registrations
  * 参数:
    + registration_id 来自GCM的注册ID
  * 返回::

     <Common Return: success>


- 设备下线

  * 地址: DELETE /api/registrations
  * 参数: 无
  * 返回::

     <Common Return: success>


- 消息记录

  * 地址: GET /api/messages
  * 参数: 无
  * 返回::

     [<Message Object> ...]


- 信息收集

  * 地址: POST /api/statistics
  * 参数:
    + wetness: 湿度
    + temperature: 温度
    + lightness: 光照
  * 返回::

     <Task Object>
     或
     <Common Return: success>



Api Common Return
-----------------
::

    {
        "status": <status>,
        "code": <code>,
        "message": <message>
    }

======  ======  =========================  ==========================
status  code    message                    Description
======  ======  =========================  ==========================
200     11000   success                    成功处理
403     11004   forbidden                  访问禁止(未登录或Token过期)
403     11005   need_permission            无权限访问
404     11006   user_not_exists            用户不存在
404     11007   flower_not_exists          花不存在
404     11008   song_not_exists            歌曲不存在
======  ======  =========================  ==========================



Async Push Message
------------------

- MESSAGE_TYPE

============  ===========    ===================
Data          Description    Payload 含义
============  ===========    ===================
message       新消息         message 结构体
statistics     数据更新       statistics 结构体
============  ===========    ===================

消息详细::

     {
         "type": <MESSAGE_TYPE>,
         "payload": <Message Object>/<Statistics Ojbect>
     }
