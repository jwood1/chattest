'use strict';

App.config(['$routeProvider', function($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: '/static/views/main.html',
        controller: 'MainCtrl'
      });
}]);

App.controller('MainCtrl', function($scope) {

});
