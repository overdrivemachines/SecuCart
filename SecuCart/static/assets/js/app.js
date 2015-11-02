var app = angular.module('app',[]);


app.controller('main',['$scope', function($scope){
	$scope.shopping_cart = [];
	$scope.inventory = false;
	$scope.setInv = function(arg){
		$scope.inventory = arg;
	};
}])