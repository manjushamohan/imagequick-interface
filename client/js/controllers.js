'use strict';
var SERVER_DOMAIN = 'http://localhost:5000'
//Add no ending slashes.
/* Controllers */


function HomeCtrl($scope) {
  $scope.name = 'ImageQuick';
}
function BillmCtrl($scope) {
  $scope.name = 'BillmCtrl';
}
function CouponsCtrl($scope) {
  $scope.name = 'Coupons';
}
function DeliveryCtrl($scope) {
  $scope.name = 'Delivery';
}
function FormatCtrl($scope,$http) {
  $scope.name = 'Format';
  $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
   $scope.voices = response.data.voices
 })
}
function FrequencyCtrl($scope) {
  $scope.name = 'Frequency';
}
function HookCtrl($scope) {
  $scope.name = 'Hook';
}
function HooktempCtrl($scope) {
  $scope.name = 'Hooktemp';
}
function PositionCtrl($scope) {
  $scope.name = 'Position';
}
function SfpCtrl($scope) {
  $scope.name = 'Sfp';
}
function SlogenCtrl($scope) {
  $scope.name = 'Slogan';
}
function StationCtrl($scope) {
  $scope.name = 'Station';
}
function TemplateCtrl($scope) {
  $scope.name = 'Template';
}
function VoiceCtrl($scope,$http) {
  $scope.name = 'Voice';
  $scope.add = function(voice){
    $http.post( SERVER_DOMAIN + "/add/voice",voice).then(function(data){
      if(data.data.status == 'success'){
        $.notify("Added "+data.data.data.name,'success')
        $scope.voice = {}
      }
      else{
        $.notify("Error adding "+voice.name,'error')
      }
    });
  }
}

function Analt_HomeCtrl($scope,$http){
  $http.get(SERVER_DOMAIN+'/analytics/voice/').then(function(response){
    $scope.chart = response.data.chart
    var chart = response.data.chart
    var ctx = $("#myChart").get(0).getContext("2d");
    //This will get the first returned node in the jQuery collection.
    var data = {
      labels : chart.labels,
      datasets : [
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "#d30000",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#d30000",
        data : chart.play
      },
      ]
    }
    new Chart(ctx).Bar(data);

    //Buy Ratio Chart
    var ctx2 = $("#buyChart").get(0).getContext("2d");
    //This will get the first returned node in the jQuery collection.
    var data = {
      labels : chart.labels,
      datasets : [
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "#689512",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#689512",
        data : chart.buy
      },
      ]
    }
    new Chart(ctx2).Bar(data);
})

  //Get Month Info
  $http.get(SERVER_DOMAIN+'/analytics/voice/monthly/2/').then(function(response){
    var charts = response.data.charts
    var ctxPlayMonth = $("#playChartMonth").get(0).getContext("2d");
    //This will get the first returned node in the jQuery collection.
    $scope.months = [charts[0].month,charts[1].month]
    var data = {
      labels : charts[1].labels,
      datasets : [
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "#d30000",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#d30000",
        data : charts[0].play
      },
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "rgba(220,220,220,0.5)",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#000000",
        data : charts[1].play
      },
      ]
    }
    new Chart(ctxPlayMonth).Bar(data);

    //Buy
    var ctxBuyMonth = $("#buyChartMonth").get(0).getContext("2d");
    //This will get the first returned node in the jQuery collection.
    $scope.months = [charts[0].month,charts[1].month]
    var data = {
      labels : charts[1].labels,
      datasets : [
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "#689512",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#689512",
        data : charts[0].buy
      },
      {
        fillColor : "rgba(220,220,220,0.5)",
        strokeColor : "rgba(220,220,220,0.5)",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#000000",
        data : charts[1].buy
      },
      ]
    }
    new Chart(ctxBuyMonth).Bar(data);
  })
}

function TemplateImagingViewCtrl($http,$scope){
  $http.get(SERVER_DOMAIN+'/view/templates/imaging').then(function(response){
    $scope.templates = response.data.templates;

  })

  $scope.edit = function(template){
    $scope.textarea = template;
    $('#json').foundation('reveal', 'open');
    var a = angular.copy(template)
    var session = ace.EditSession(a)
    var editor = ace.edit("editor",session);
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/javascript");
    
  }
}