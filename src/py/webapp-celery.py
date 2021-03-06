# this Python snippet is stored as src/py/webapp-celery.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# this Python code snippet is later referred to as <<py-form>>
@app.route('/', methods=['GET'])
def form():
  return '''<!doctype html>
    <form method="POST">
      <label for="epsilon">Epsilon</label>
      <input type="number" name="epsilon" value="0.001">
      <label for="guess">Guess</label>
      <input type="number" name="guess" value="-20">
      <button type="submit">Submit</button>
    </form>'''

# this Python code snippet is later referred to as <<py-submit>>
@app.route('/', methods=['POST'])
def submit():
  epsilon = float(request.form['epsilon'])
  guess = float(request.form['guess'])
  from tasks import calculate
  job = calculate.delay(epsilon, guess)
  return redirect(url_for('result', jobid=job.id))

# this Python code snippet is later referred to as <<py-result>>
@app.route('/result/<jobid>')
def result(jobid):
  from tasks import capp
  job = capp.AsyncResult(jobid)
  job.maybe_throw()
  if job.successful():
    result = job.get()
    epsilon = result['epsilon']
    guess = result['guess']
    root = result['root']
    return f'''<!doctype html>
      <p>With epsilon of {epsilon} and a guess of {guess} the found root is {root}.</p>'''
  else:
    return f'''<!doctype html>
      <p>{job.status}<p>'''

if __name__ == '__main__':
  app.run(port=5000)