var passport = require('passport');
var successUrl = '/app'
module.exports = {

  login: function (req, res) {
    if (req.isAuthenticated()) {
      res.redirect(successUrl)
      res.end();
    }else{
      res.view({layout:'guest-layout',view:'login'});
    }
  },

  logout: function (req, res){
    req.logout()
    res.redirect('/login');
  },


  validateRegister : function(req,res,create){

    //var errors = anchor(req.body).to({type :{name:'string'}})
    /*if(!req.body.name) {
      throw ValidationException('Invalid data')
    }*/
    
    //https://github.com/ctavan/express-validator

    req.checkBody({
     'email': {
        notEmpty: true,
        isEmail: {
          errorMessage: 'Invalid Email'
        },
        isLength: {
          options: [{max: 100 }],
          errorMessage: 'Must be less than 100 chars' 
        },
      },
      'password': {
        notEmpty: true,
        isLength: {
          options: [{min:5, max: 100 }],
          errorMessage: 'Must be between 8 - 100 chars' 
        },
        errorMessage: 'Invalid Password'
      },
      'name': { //
        notEmpty: true,
        isLength: {
          options: [{ min: 3, max: 100 }],
          errorMessage: 'Must be between 3 and 100 chars long' 
        },
        errorMessage: 'Invalid Name'
      }
    })
    
    var errors = req.validationErrors(true);
    if(errors) {
      throw ValidationException('Validation failed',errors)
    }
  },

  register : function(req,res){

    this.validateRegister(req,res)

    User.create({
      email:req.body.email,
      password:req.body.password,
      name:req.body.name
    },function(err,user){
      res.send(200,{url:'/login'});  
    })
    
  },

  localLogin: function (req, res,next) {
     passport.authenticate('local', function(err,user){

      if (err) { 
        return res.send(400,{msg:'Invalid Username or Password'})
      }
        
      req.logIn(user, function(err) {
        if (err) { 
            return next(err); 
        }
        return res.send(200,{url:successUrl})
        });
     })(req, res, next); 
  },

  facebook: function (req, res, next) {
     passport.authenticate('facebook', { scope: ['email', 'public_profile']},
        function (err, user) {
            req.logIn(user, function (err) {
            if(err) {
                req.session.flash = 'There was an error';
                res.redirect('/login');
            } else {
                req.session.user = user;
                res.redirect('/home');
            }
        });
    })(req, res, next);
  },

  facebookCallback: function (req, res, next) {
  	console.log ('callback');
    passport.authenticate('facebook', {
        successRedirect: '/app',
        failureRedirect: '/login' }
    )(req, res, next); 
  },

  google: function (req, res, next) {
    passport.authenticate('google', { scope: ['https://www.googleapis.com/auth/plus.login'] } ,
      function (err, user) {
          req.logIn(user, function (err) {
          if(err) {
              req.session.flash = 'There was an error';
              res.redirect('/login');
          } else {
              req.session.user = user;
              res.redirect('/home');
          }
      });
    })(req, res, next);
  },

  googleCallback: function (req, res, next) {
    console.log ('callback');
    passport.authenticate('google', {
        successRedirect: '/app',
        failureRedirect: '/login' }
    )(req, res, next); 
  },

  linkedin: function (req, res, next) {
    passport.authenticate('linkedin', { scope: ['r_emailaddress', 'r_basicprofile']},
      function (err, user) {
          req.logIn(user, function (err) {
          if(err) {
              req.session.flash = 'There was an error';
              res.redirect('/login');
          } else {
              req.session.user = user;
              res.redirect('/home');
          }
      });
    })(req, res, next);
  },

  linkedinCallback: function (req, res, next) {
    passport.authenticate('linkedin', {
        successRedirect: '/app',
        failureRedirect: '/login' }
    )(req, res, next); 
  }



};

