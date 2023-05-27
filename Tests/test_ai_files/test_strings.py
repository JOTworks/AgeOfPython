string_variable_asign ="""
(defrule   (true)
=>  (up-modify-goal 1 c:= 3)
  (up-modify-goal 1 c:+ 1)
)
"""