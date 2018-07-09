angular.module('customerModule')
.controller('dashboardCtrl', function($scope) {
    
    $scope.message = 'test';
   
    $scope.projects = [
        {
            name: 'Mining Project',
            price: 50,
            status:'Proposal Submitted'
        },
        {
            name: 'Lake Project',
            price: 10000,
            status:'Started'
        },
        {
            name: 'Parking Project',
            price: 20000,
            status:'Drone on site'
        }
    ];
    
});