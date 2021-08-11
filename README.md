# WordPress Advanced Video Embed v1.0 LFI PoC Rewrite

- Original exploit: [https://www.exploit-db.com/exploits/39646](https://www.exploit-db.com/exploits/39646)

This is a rewrite of an original exploit by evait security GmbH. I have updated the script to Python 3 and added arguments in order to avoid hard-coding the target URL and LFI path. I've modified the exploit to pull down the "image" URL from the front page of the blog instead of the post itself. This was done to get the exploit working properly on a certain VulnHub box.


 `./advanced-video-lfi.py -h` for usage.

