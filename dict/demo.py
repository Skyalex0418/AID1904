while True:
  print("一级界面")
  cmd = input()
  if cmd == 'in':
    while True:
      print("二级界面")
      cmd = input()
      if cmd == 'out':
        break