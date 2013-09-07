'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.

app.factory('TemplateIds', function () {
    return []
})
app.factory('VoiceIds', function () {
    return []
})

app.factory('PosVoiceIds', function () {
    return []
})

app.factory('FreVoiceIds', function () {
    return []
})

app.factory('StatVoiceIds', function () {
    return []
})

app.factory('PosStyleIds', function () {
    return []
})

app.factory('FreStyleIds', function () {
    return []
})

app.factory('StatStyleIds', function () {
    return []
})


app.factory('FormatIds', function () {
    return []
})



angular.module('myApp.services', []).
  value('version', '0.1');
