var customerModule =  angular.module('customerModule');

customerModule.config(function($stateProvider, $urlRouterProvider) {
    
    
    $stateProvider
        
        .state('customerDashboard', {
            url: '/customer/dashboard',
            templateUrl: '/js/customer/proposal/dashboard.html',
            'controller' : 'dashboardCtrl'
        })
        
        .state('customerProposal', {
            url: '/customer/proposal',
            templateUrl: '/js/customer/proposal/get-proposal.html'
        })
        .state('customerEstimate', {
            url: '/customer/estimate',
            template: '<h1>Get Estimate</h1>'
        })

        .state('customerReports', {
            url: '/customer/reports',
            template: '<h1>Reports</h1>'
        })

        .state('customerActivity', {
            url: '/customer/activity',
            template: '<h1>Activity</h1>'
        })
        
})
