
angular.module('autModule',['ngMessages'])
  .controller('loginCtrl', function($scope,$http) {

    $scope.isRegister = false;

    $scope.data = {email : '', password:''};

    $scope.register = {name:'',email : '', password:''};


    $scope.login = function(isValid){
        /*if(!validator.isEmail($scope.data.email)){
          alert('Please enter valid email');
          e.preventDefault()
          return false;
        }else if(!validator.isByteLength($scope.data.password,{min:8,max:50})){
          alert('Password should be 8- 50 character');
          e.preventDefault()
          return false;
        }else{
          return true;
        }*/
        if(isValid){
            $http.post('/login',$scope.data)
              .success(function(resp){
                window.location = resp.url
              })
              .error(function(){
                alert('failed')
              })
        }else{

        }
    }


    $scope.doRegister = function(isValid){
      if(isValid){
            $http.post('/register',$scope.register)
              .success(function(resp){
                window.location = resp.url
              })
              .error(function(){
                alert('failed')
              })
        }else{

        }
    }

    $scope.showRegister = function(e){/* e.preventDefault(); */$scope.isRegister = true}

    $scope.showLogin = function(e){/*e.preventDefault();*/$scope.isRegister = false}





  })



 
 