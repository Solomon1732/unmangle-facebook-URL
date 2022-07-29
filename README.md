# UnmangleFacebookURL

A small program for decrypting (unmangling) links shared on Facebook. It's simple to use. Open a terminal (or command line), enter the desired URL when prompted, copy the result.

A mangled URL generally has the following form:
> https://l.facebook.com/l.php?u=https%3A%2F%2Fexample.com%3Ffbclid%3DIwAR02DxZKKFYZbmeWTolyTCxEPYEeaoA3Zexhc3UwZysKOIG1Yhp_lC36OT8&h=AT3Nx6gLcU9KeX1tx2FWJvJX_OhCwzh14wJTJJxJv3e4f95A9RbAprCMRCGccCVJuu4RYELwg3Haxw007ZeM_Eei9NL4Qssw-tAC8Yz8xYsRQSBhLIv_4oqp8YyCH1JaeO4JR8w8wBmy1pxmAim5FwDI_dY5iMeo2Pd3EfS35o03TYm-OFPlAB-kiM2Maam1GQZFlJLvb4xtUKz15fd6kUg7RkyeyThCyfqYUmasybsFTruHJUwhu2jQRx68gDkJatxUBzSoRewpWjw_4hv0NCQ51sw3gEBvjq32dtzsJDS1DinY__clbShirpLPuDUJnBr6rt0i4edmmNT1AvanOl3WohooGlduZNmzODymuKOGRbV_qgm0x5JIAcMTZkfkqbgnUr4OSIazSnbfqtfFct_9WI_OKQ9wBvFWR4sXhgT6BvBuspMsQU_wUcUb3v08qfNL9VbHPpeT6oYrqkXkH1jPanDk5Vly403TUBBGAobwObNYjcbDYDBT-EWTw03qGNBtNZxcDKHorvmKLMNmjCKiaEP69s7LGhcasHBjTDlWtt51Uq1CI5lubWiSE_Li8qFQu-MuBbNzMGzaDSGiFEJKmL6R1SL5fyKcIVP9tQ34-bCwUQE

The resulting URL will look something like this:
> https://example.com

This program preservs the original URL parameters, such as fragments or query. The only change it does is to remove Facebook's added `fbclid` query parameter. Facebook uses it to track the URL's usage.