import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.environ["OPENAI_ORGANIZATION"]
openai.api_key = os.environ["OPENAI_KEY"]

BASE_URL = "https://api.openai.com/v1/engines"
SEARCH_URL = "https://api.openai.com/v1/engines/davinci/search"
COMPLETION_URL = "https://api.openai.com/v1/engines/davinci/completions"


# import requests

# headers = {
#     'Authorization' : f"Bearer {os.environ['OPENAI_KEY']}"
# }

## semantic serach
# print(openai.Engine('davinci').search(
#     documents=['White House', 'hospital', 'school'],
#     query='the president'
# ))

promp = """
Harley Finkelstein: � I get to McGill in September 2001 and 11 days later September 11th happens, stock market crashes, things get really, really bad and my parents 
lose everything.  I mean, we lost our house, we lost everything.  We didn�t have a penny to our name. 
Tim Ferriss: Why is that? That�s because of the equity markets?
Harley Finkelstein: My dad was just over-leveraged for the most part.  He was doing things he probably
 shouldn�t have been doing.  And he just did stuff that was just 
highly correlated to the equity markets doing well, and when the equity markets fell apart things fell apart for us. 
 And my mom called me and said, �Hey, you�ve got to
 move back down to Florida because there�s no way you can stay in Montreal.  We can�t give you money.  
 Just come back down here and we�ll figure it all out. � And I was 17 years old when I started McGill, I was a bit younger than my peers. 
I loved Montreal, I love being on my own.  And so I basically told my parents, �Hey, I�m going to stay here.
 I�m going to figure this out on my own, and I�m actually
 going to also try if I can to help the family out as well. � I have two much older sisters, so I thought, 
 �Okay, I�ll figure this out on my own. � And I tried my hand
  at a bunch of stuff.  I worked at a travel agency.  I�ve been a DJ since I was a kid, so I deejayed parties
   and events and weddings and anything that � 
Tim Ferriss: And bar mitzvahs. 
Harley Finkelstein: And lots and lots of bar mitzvahs, like 300 bar mitzvahs as you know, we�ve talked about that
 a lot.  And so, I deejayed, I was working at a travel agency trying to go to McGill and it just wasn�t working.
"""


## Try completion with one of the prompts
print(
    openai.Completion.create(engine="davinci", prompt=promp, max_tokens=30, top_p=0.4)
)
