var Twit = require('twit')
var T = new Twit({
    consumer_key:         'S8gMgBFhScZ1PEQJqYmoDYcL9',
    consumer_secret:      'SupHG06pkr15zhXyFA9W66fRejODbc7bKNnRILcrQoouG2cgbh',
    access_token:         '433140581-y5EwvG001EVLQ3DLoabka7oHWINj5MX3DNAhb84O',
    access_token_secret:  'IC2ChWTcF3qKdq65xzwNvI8ICK34bTnmt6n1sljdfy81X',
})

var users = ["433140581","1035723202645909504"];

var stream = T.stream('statuses/filter', {follow: users});

stream.on('tweet', function (tweet) {
    if (users.indexOf(tweet.user.id_str) > -1) {
        console.log(tweet.user.name + ": " + tweet.text);
        T.post('statuses/retweet/:id', { id: tweet.id_str }, function (err, data, response) {
            console.log(data)
        })
    }
})