/**
 * This is an example of a basic node.js script that performs
 * the Authorization Code oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/web-api/authorization-guide/#authorization_code_flow
 */

var express = require('express'); // Express web server framework
var request = require('request'); // "Request" library
var querystring = require('querystring');
var cookieParser = require('cookie-parser');

var client_id = 'a3dc7add85b7450eb59b7507049517fd'; // Your client id
var client_secret = 'fdc098985dc24a03a3a67870ca5240f5'; // Your secret
var redirect_uri = 'http://localhost:8888/callback'; // Your redirect uri
var app = express();
app.use("/", express.static(__dirname));
app.use('/', express.static(__dirname + '/view'));
app.use('/', express.static(__dirname + '/scripts'));
app.use('/', express.static(__dirname + '/css'));


app.get("/", function(req, res){
  res.sendfile("index")
})

console.log('Listening on 8888');
app.listen(8888);
