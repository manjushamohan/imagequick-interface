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


function CouponsCtrl($scope,$http) {
    $scope.name = 'Coupons';

    $scope.add = function(coupon){
      $http.post( SERVER_DOMAIN + "/add/coupon",coupon).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.code,'success')
          $scope.coupon = {}
        }
        else{
          $.notify("Error adding "+coupon.code,'error')
        }
      });
    }
}


function DeliveryCtrl($scope) {
    $scope.name = 'Delivery';
}


function FormatCtrl($scope,$http,VoiceIds) {
    $scope.name = 'Format';
    console.log(VoiceIds)
   
    $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })

    $scope.select_voice=function(voice,value){
     if(value==true){
      console.log(voice)
     }
    }

    $scope.add = function(format,voice){
      console.log(format)
      $http.post( SERVER_DOMAIN + "/add/format",format).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.format = {}
        }
        else{
          $.notify("Error adding "+format.name,'error')
        }
      });
    }

}


function FrequencyCtrl($scope,$http) {
    $scope.name = 'Frequency';


    $scope.add = function(frequency){
     
      $http.post( SERVER_DOMAIN + "/add/frequency",frequency).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.frequency,'success')
          $scope.frequency = {}
        }
        else{
          $.notify("Error adding "+frequency.frequency,'error')
        }
      });
    }
}


function HookCtrl($scope,$http) {
    $scope.name = 'Hook';

    $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
      console.log(response.data.formats)
     $scope.formats = response.data.formats
    })
    $scope.add = function(hook){
      console.log(hook)
      $http.post( SERVER_DOMAIN + "/add/hook",hook).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.hook,'success')
          $scope.hook = {}
        }
        else{
          $.notify("Error adding "+hook.hook,'error')
        }
      });
    }
    
}


function HooktempCtrl($scope,$http) {
    $scope.name = 'Hooktemp';

    $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })

    $http.get(SERVER_DOMAIN+'/get/voices/').then(function(response){
     $scope.voices = response.data.voices
    })
}


function PositionCtrl($scope) {
    $scope.name = 'Position';
}


function SfpCtrl($scope) {
    $scope.name = 'Sfp';
}


function SloganCtrl($scope,$http) {
    $scope.name = 'Slogan';
    $scope.add = function(slogan){
      $http.post( SERVER_DOMAIN + "/add/slogan_length",slogan).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.slogan,'success')
          $scope.slogan = {}
        }
        else{
          $.notify("Error adding "+slogan.slogan,'error')
        }
      });
    }


}


function StationCtrl($scope,$http) {
    $scope.name = 'Station';
    $http.get(SERVER_DOMAIN+'/get/formats/').then(function(response){
     $scope.formats = response.data.formats
    })
    $scope.add = function(station){
      $http.post( SERVER_DOMAIN + "/add/station",station).then(function(data){
        if(data.data.status == 'success'){
          $.notify("Added "+data.data.data.name,'success')
          $scope.station = {}
        }
        else{
          $.notify("Error adding "+station.name,'error')
        }
      });
    }

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