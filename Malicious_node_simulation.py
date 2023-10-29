import torch
import flcore.clients.clientavg as clients
import flcore.servers.serveravg as servers
import random

# 模拟10个客户端
clients = [clients.ClientAvg(cid=i) for i in range(10)]
server = servers.ServerAvg(clients)

# 正常训练1轮
server.train(1) 

# 选择客户端2作为投毒节点
poison_client = clients[2] 

# 在投毒客户端中添加对模型的干扰
poison_model = torch.rand_like(poison_client.model) * 1000
poison_client.model -= poison_model

# 继续训练1轮,包含投毒参数  
server.train(1)

# 投毒后模型参数发生明显变化
print('Model diff:', torch.norm(server.model - poison_client.model))

# ...初始化代码省略

# 模拟随机宕机  
offline_client = random.choice(clients)
offline_client.offline = True

print(f'Client {offline_client.cid} is offline')

# 训练时排除宕机客户端
server.selected_clients = [c for c in server.selected_clients if not c.offline]
server.train(1)

# 宕机客户端的模型参数不会更新
print('Model diff:', torch.norm(offline_client.model - server.model))
