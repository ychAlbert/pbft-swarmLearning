# 导入一些必要的库和模块
import torch # 用于处理模型参数
import hashlib # 用于生成参数摘要
import utils # 用于定义一些辅助函数

# 定义一个函数来执行PBFT协议
def execute_PBFT(model, received_parameters):
    # 初始化一些变量
    leader = None # 领导者节点
    view = 0 # 视图编号，用于记录协议的轮数
    pre_prepare = None # 预准备消息，由领导者发送，包含视图编号和参数摘要
    prepare = {} # 准备消息，由其他节点发送，包含视图编号和参数摘要，用于表达对领导者的认可
    commit = {} # 提交消息，由其他节点发送，包含视图编号和参数摘要，用于表达对参数的认可
    committed = False # 是否已经提交参数
    parameters = None # 合并后的参数

    # 选择一个领导者
    leader = (utils.generate_random_number() % N) + 1 # 从1到N中随机选择一个节点作为领导者

    # 如果自己是领导者，执行以下步骤
    if self == leader:
        # 增加视图编号
        view += 1
        # 使用聚合函数合并收到的参数，并生成一个参数摘要
        parameters = aggregate_function(received_parameters)
        digest = hashlib.sha256(parameters).hexdigest()
        # 创建并发送预准备消息给其他节点
        pre_prepare = (view, digest)
        utils.send_message(pre_prepare, "all nodes except self")

    # 如果自己不是领导者，执行以下步骤
    else:
        # 接收预准备消息，并验证其有效性
        pre_prepare, leader = utils.receive_message()
        if utils.verify_parameters(pre_prepare):
            # 创建并发送准备消息给其他节点
            prepare[self] = (view, digest)
            utils.send_message(prepare[self], "all nodes except self and leader")

    # 接收准备消息，并验证其有效性
    while len(prepare) < T:
        message, sender = utils.receive_message()
        if utils.verify_parameters(message):
            prepare[sender] = message

    # 如果收到了足够多的（超过T个）有效的准备消息，且与预准备消息一致，创建并发送提交消息给其他节点
    if len(prepare) >= T and prepare[sender] == pre_prepare:
        commit[self] = (view, digest)
        utils.send_message(commit[self], "all nodes except self")

    # 接收提交消息，并验证其有效性
    while len(commit) < T:
        message, sender = utils.receive_message()
        if utils.verify_parameters(message):
            commit[sender] = message

    # 如果收到了足够多的（超过T个）有效的提交消息，且与预准备消息一致，更新自己的模型参数，并将提交标志设为真
    if len(commit) >= T and commit[sender] == pre_prepare:
        model.load_state_dict(parameters)
        committed = True

