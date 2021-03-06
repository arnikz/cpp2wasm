# this Python snippet is stored as src/py/api.py
def calculate(body):
  epsilon = body['epsilon']
  guess = body['guess']
  from newtonraphsonpy import NewtonRaphson
  finder = NewtonRaphson(epsilon)
  root = finder.find(guess)
  return {'root': root}