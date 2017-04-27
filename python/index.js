const os = require('child_process');

exports.serve = function(req, res) {
  const p = os.execFile('./dist/func/func');
  var lastMessage = ""
  p.stderr.on('data', (err) => {
    console.error(err.toString());
  })
  p.stdout.on('data', (out) => {
    console.log(out.toString());
    lastMessage = out;
  })
  p.on('close', (code) => {
    if (code !== 0) {
      //This means the shim failed / panicked. So we reject hard.
      res.end('err')
    } else {
      // Resolve the promise with the latest output from stdout
      // In case of shimming http, this is the response object.
      res.end(lastMessage)
    }
  });
}
