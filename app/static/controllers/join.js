'use strict';


App.controller('JoinCtrl', function($rootScope, $scope, $location, PubNub) {
    $scope.data = {
      username: $scope.user.username
    };
    $scope.join = function() {
      var _ref, _ref1, _ref2;
      $rootScope.data || ($rootScope.data = {});
      $rootScope.data.username = (_ref = $scope.data) != null ? _ref.username : void 0;
      $rootScope.data.city = (_ref1 = $scope.data) != null ? _ref1.city : void 0;
      $rootScope.data["super"] = (_ref2 = $scope.data) != null ? _ref2["super"] : void 0;
      $rootScope.data.uuid = Math.floor(Math.random() * 1000000) + '__' + $scope.data.username;
      $rootScope.secretKey = $scope.data["super"] ? 'sec-c-MmZjODVmNzgtMGIzYS00NDJjLThhOWYtYmNmYmM5MTAwMmRl' : null;
      $rootScope.authKey = $scope.data["super"] ? 'ChooseABetterSecret' : null;
      PubNub.init({
        subscribe_key: 'sub-c-69c27836-95e6-11e3-8d39-02ee2ddab7fe',
        publish_key: 'pub-c-7e40ae90-8c72-4a82-a933-bc05008777cc',
        secret_key: $rootScope.secretKey,
        auth_key: $rootScope.authKey,
        uuid: $rootScope.data.uuid,
        ssl: true
      });
      if ($scope.data["super"]) {
        /* Grant access to the SuperUsers room for supers only!*/

        PubNub.ngGrant({
          channel: 'SuperUsers',
          auth_key: $rootScope.authKey,
          read: true,
          write: true,
          callback: function() {
            return console.log('SuperUsers! all set', arguments);
          }
        });
        PubNub.ngGrant({
          channel: "SuperUsers-pnpres",
          auth_key: $rootScope.authKey,
          read: true,
          write: false,
          callback: function() {
            return console.log('SuperUsers! presence all set', arguments);
          }
        });
        PubNub.ngGrant({
          channel: '__controlchannel',
          read: true,
          write: true,
          callback: function() {
            return console.log('control channel all set', arguments);
          }
        });
        PubNub.ngGrant({
          channel: '__controlchannel-pnpres',
          read: true,
          write: false,
          callback: function() {
            return console.log('control channel presence all set', arguments);
          }
        });
      }
      return $location.path('/chat');
    };
    return $(".prettyprint");
  });