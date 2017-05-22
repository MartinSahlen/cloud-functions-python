//Handle Background events according to spec
function shimHandler(data) {
  return new Promise((resolve, reject) => {
    //Spawn the function and inject the env from the parent process.
    const p = require('child_process').execFile('./{{.FunctionName}}', [], {
      env: process.env,
    });
    var lastMessage;
    p.stdin.setEncoding('utf-8');
    //Log standard err messages to standard err
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
        reject();
      } else {
        // Resolve the promise with the latest output from stdout
        // In case of shimming http, this is the response object.
        resolve(lastMessage);
      }
    });
    //Write the object/message/request to the shim's stdin and signal
    //End of input.
    p.stdin.write(JSON.stringify(data));
    p.stdin.end();
  });
}

//Handle http request
function handleHttp(req, res) {
  var requestBody;

  switch (req.get('content-type')) {
    case 'application/json':
      requestBody = JSON.stringify(req.body);
      break;
    case 'application/x-www-form-urlencoded':
      //The body parser for cloud functions does this, so just play along
      //with it, sorry man! Maybe we should construct some kind of proper
      //form request body? or not. let's keep it this way for now, as
      //This is how cloud functions behaves.
      req.set('content-type', 'application/json')
      requestBody = JSON.stringify(req.body);
      break;
    case 'application/octet-stream':
      requestBody = req.body;
      break;
    case 'text/plain':
      requestBody = req.body;
      break;
  }

  var fullUrl = req.protocol + '://' + req.get('host') + req.originalUrl;

  var httpRequest = {
    'body': requestBody,
    'headers': req.headers,
    'method': req.method,
    'remote_addr': req.ip,
    'url': fullUrl
  };

  shimHandler(httpRequest)
  .then((result) => {
    data = JSON.parse(result);
    res.status(data.status_code);
    res.set(data.headers)
    res.send(data.body);
  })
  .catch(() => {
    res.status(500).end();
  })
}

//{{ if .TriggerHTTP }}
exports['{{.FunctionName}}'] = function(req, res) {
  return handleHttp(req, res);
}// {{ else }}
exports['{{.FunctionName}}'] = function(event, callback) {
  return shimHandler(event.data).then(function() {
    callback();
  }).catch(function() {
    callback(new Error("Function failed"));
  });
}// {{ end }}
