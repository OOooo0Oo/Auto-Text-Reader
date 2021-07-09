from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 濉叆 httpapi 鏈嶅姟杩愯鐨勫湴鍧�
        verifyKey="TextToSpeech", # 濉叆 authKey
        account=3558994956, # 浣犵殑鏈哄櫒浜虹殑 qq 鍙�
        websocket=True # Graia 宸茬粡鍙互鏍规嵁鎵�閰嶇疆鐨勬秷鎭帴鏀剁殑鏂瑰紡鏉ヤ繚璇佹秷鎭帴鏀堕儴鍒嗙殑姝ｅ父杩愪綔.
    )
)
@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    await app.sendFriendMessage(friend, MessageChain.create([
        Plain("Hello, World!")
    ]))
app.launch_blocking()