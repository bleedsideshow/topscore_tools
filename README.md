# topscore_tools

This module will help you pull data from your site's TopScore database via their API.

# API documentation

The TopScore API Spec can be found [here](https://docs.google.com/document/d/148SFmTpsdon5xoGpAeNCokrpaPKKOSDtrLNBHOIq5c4/edit).  It's somewhat bare bones but was useful enough to get this package up and running.

The main thing you'll need is to get your client id and client secret, which can be found at yoursite.com/u/oauth-key.

# topscore_api.sh

Once you have the client id and client secret, you can run the topscore_api.sh script:
  ./tools/topscore_api.sh [site name] [client id] [client secret] [username] [password] [query]
  
Where `site name` is the prefix for your organization's website (e.g. pada, wafc).
