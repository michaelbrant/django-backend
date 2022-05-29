names = [
    "create instant invite",  # 1
    "kick members",  # 2
    "ban members",  # 4
    "administrator",  # 8
    "manage channels",  # 16
    "manage server",  # 32
    "add reactions",  # 64
    "view audit log",  # 128
    "priority speaker",  # 256
    "stream video",  # 512
    "view channels",  # 1024
    "send messages",  # 2048
    "send tts messages",  # 4096
    "manage messages",  # 8192
    "embed links",  # 16384
    "attach files",  # 32768
    "read message history",  # 65536
    "mention all roles",  # 131072
    "use external emojis",  # 262144
    "view server insights",  # 524288
    "connect voice",  # 1048576
    "speak",  # 2097152
    "mute members",  # 4194304
    "deafen members",  # 8388608
    "move members",  # 16777216
    "use voice activity",  # 33554432
    "change nickname",  # 67108864
    "manage nicknames",  # 134217728
    "manage roles",  # 268435456
    "manage webhooks",  # 536870912
    "manage emojis and stickers",  # 1073741824
    "use application commands",  # 2147483648
    "request to speak",  # 4294967296
    "manage events",  # 8589934592
    "manage threads",  # 17179869184
    "public threads",  # 34359738368
    "private threads",  # 68719476736
    "use external stickers",  # 137438953472
    "send messages in threads",  # 274877906944
    "start activities"  # 549755813888
]
names.reverse()


def get_perms_list(perm_integer):
  all_perms = []
  for i in range(len(names)):
      permission = 2**((len(names)-1)-i)
      if not perm_integer - permission < 0:
          all_perms.append(names[i])
          perm_integer -= permission
  return all_perms
