kinvey_speed_test
=================

Simple Python module to automate testing of storage/aggregation time using the REST API on Kinvey (www.kinvey.com).

You will need to create two text files: one for holding your endpoint info
(mine is called endpoints.json) and one for your authentication info
(mine is called account_sunspritedev.json).

They look like this (with actual username, password, and endpoint URLs 
replaced with dummy info):

account_sunspritedev.json:
```
{
  "username": "example@username.com",
  "password": "examplePassword"
}
```
endpoints.json:
```
{
    "endpoints": [
        "http://baas.kinvey.com/appdata/xxxx/yyy", 
        "http://baas.kinvey.com/rpc/xxx/custom/yyy"
    ],

    "linecolors": [
        "black",
        "red"
    ]
} 
```