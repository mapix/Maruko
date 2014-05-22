API Documentation
=================

Basic Data Structure
--------------------

User::

    {
        "id": "52180037",
        "name": "颈椎君你不要疼",
        "avatar": "http://img3.douban.com/icon/u52180037-21.jpg",
        "create_time": "2014-05-04 08:44:15",
        "update_time": "2014-05-04 08:44:15",
    }


API Overview
------------

======  ==========================  ============
Method  URL                         Description
======  ==========================  ============
GET     /api/users/:id              获取用户信息
======  ==========================  ============


API Detail
----------

- 获取用户信息

  * 地址: GET /api/users/:id
  * 参数:
  * 返回::

     <User Ojbect>

