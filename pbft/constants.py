# 定义一些常量和变量

N = 3  # 节点总数
f = 1  # 故障节点数
T = 2 * f + 1  # 共识阈值

# 定义一些消息类型

MessageType = enum("MessageType", ("PRE_PREPARE", "PREPARE", "COMMIT"))

# 定义一些错误码

ErrorCode = enum("ErrorCode", ("OK", "INVALID_PARAMETER", "DUPLICATE_MESSAGE", "MALFORMED_MESSAGE"))
