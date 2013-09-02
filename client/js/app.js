'use strict';



var app = angular.module('myApp', [])


app.run(function ($rootScope, $location, $anchorScroll, $routeParams) {

    $rootScope.$on('$routeChangeSuccess', function (newRoute, oldRoute) {
            $location.hash($routeParams.scrollTo);
            $anchorScroll();
        },
        $rootScope.location = $location
    );
})
;


/*
 For adding remove method to arrays
 */

app.config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
    }
]);


 Array.prototype.remove = function () {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};

// Declare app level module which depends on filters, and services

 app.config(['$routeProvider', function($routeProvider) {
  	$routeProvider.when('/', {'templateUrl': 'partials/home.html', controller: 'HomeCtrl'});
    $routeProvider.when('/add/billm', {templateUrl: 'partials/billm.html', controller: 'BillmCtrl'});
   	$routeProvider.when('/add/coupons', {templateUrl: 'partials/coupons.html', controller: 'CouponsCtrl'});
   	$routeProvider.when('/add/delivery', {templateUrl: 'partials/delivery.html', controller: 'DeliveryCtrl'});
   	$routeProvider.when('/add/format', {templateUrl: 'partials/format.html', controller: 'FormatCtrl'});
   	$routeProvider.when('/add/frequency', {templateUrl: 'partials/frequency.html', controller: 'FrequencyCtrl'});
   	$routeProvider.when('/add/hook', {templateUrl: 'partials/hook.html', controller: 'HookCtrl'});
   	$routeProvider.when('/add/hooktemp', {templateUrl: 'partials/hooktemp.html', controller: 'HooktempCtrl'});
   	$routeProvider.when('/add/pos_stmt', {templateUrl: 'partials/pos_stmt.html', controller: 'PositionCtrl'});
   	$routeProvider.when('/add/sfp', {templateUrl: 'partials/sfp.html', controller: 'SfpCtrl'});
    $routeProvider.when('/add/slogen', {templateUrl: 'partials/slogen.html', controller: 'SlogenCtrl'});
    $routeProvider.when('/add/station', {templateUrl: 'partials/station.html', controller: 'StationCtrl'});
    $routeProvider.when('/add/template', {templateUrl: 'partials/template.html', controller: 'TemplateCtrl'});
    $routeProvider.when('/add/voice', {templateUrl: 'partials/voice.html', controller: 'VoiceCtrl'});


    $routeProvider.otherwise({redirectTo: '/'});
  }]);