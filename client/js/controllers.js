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







/*
angular.module('myApp.controllers', []).
  controller('BillmCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('CouponsCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('DeliveryCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('FormatCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('FrequencyCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('HookCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('HooktempCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('PositionCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('SfpCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('SlogenCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  controller('StationCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
   controller('TemplateCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
    controller('VoiceCtrl', [function($scope) {
  	$scope.home="ImageQuick";

  }]).
  
  controller('HomeCtrl',[function($scope) {
    $scope.name = 'Campsia';
}]);*/