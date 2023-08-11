from ossapi import Ossapi, UserLookupKey, GameMode, RankingType

client_id = 22250
client_secret = 'EFa2u6qrI8nD6LpHOmtYKnaUVjTEFvrk2GVvZs4u'
api = Ossapi(client_id, client_secret)

user_list = api.user(10652591)
print(user_list)
print(user_list[0].country.name)
