  var passport = require('passport'),
      FacebookStrategy = require('passport-facebook').Strategy,
      LocalStrategy = require('passport-local').Strategy;
      GoogleStrategy = require('passport-google-oauth').OAuth2Strategy;
      LinkedInStrategy = require('passport-linkedin-oauth2').Strategy;;
   
   
  var verifyHandler = function(token, tokenSecret, profile, done) {
    process.nextTick(function() {
   
      User.findOne({uid: profile.id}, function(err, user) {
        if (user) {
          return done(null, user);
        } else {
   
          var data = {
            provider: profile.provider,
            uid: profile.id,
            name: profile.displayName
          };
   
          if (profile.emails && profile.emails[0] && profile.emails[0].value) {
            data.email = profile.emails[0].value;
          }
          if (profile.name && profile.name.givenName) {
            data.firstname = profile.name.givenName;
          }
          if (profile.name && profile.name.familyName) {
            data.lastname = profile.name.familyName;
          }
   
          User.create(data, function(err, user) {
            return done(err, user);
          });
        }
      });
    });
  };


  function localAuth(username, password, done) {
      User.findOne().where({
        'email': username, 
      }).exec(function(err, user) {
        if (err) {
          return done(err);
        }

        if (!user) {
          return done(null, false);
        }

        user.validatePassword(password,function(err,verified){
           if(err || !verified){ 
              done('auth failed')
            }
            else{
              done(err,user)
            }
        })
      });
  }

  var googleHandler =  function(accessToken, refreshToken, profile, done) {

         User.findOrCreate({ googleId: profile.id }, function (err, user) {
           return done(err, user);
         });
  }

  var linkedinHandler =  function(accessToken, refreshToken, profile, done) {

    process.nextTick(function() {

      console.log(profile);
   
      User.findOne({uid: profile.id}, function(err, user) {
        if (user) {
          return done(null, user);
        }else {
          var data = {
            provider: profile.provider,
            uid: profile.id,
            name: profile.displayName
          };
   
          if (profile.emails && profile.emails[0] && profile.emails[0].value) {
            data.email = profile.emails[0].value;
          }
          if (profile.name && profile.name.givenName) {
            data.firstname = profile.name.givenName;
          }
          if (profile.name && profile.name.familyName) {
            data.lastname = profile.name.familyName;
          }
   
          User.create(data, function(err, user) {
            return done(err, user);
          });
        }
      });
    });
   }

   
  passport.serializeUser(function(user, done) {
    console.log('serializing user')
    console.log(user)
    done(null, user.id);
  });
   
  passport.deserializeUser(function(uid, done) {
    User.findOne({id: uid}, function(err, user) {
      done(err, {name:user.name,roles : user.roles});
    });
  });
   
  module.exports.http = {
   
    customMiddleware: function(app) {
   
      passport.use(new FacebookStrategy({
        clientID: "225505704490313",
        clientSecret: "154c1d839a24c849439b3e6ad9156feb",
        callbackURL: "http://localhost:1337/auth/facebook/callback"
      }, verifyHandler));


      passport.use(new LocalStrategy({usernameField:'email'},localAuth));

      passport.use(new GoogleStrategy({
        clientID: "338101191947-9kgi11upi03jggb1lf4e4divenb5hkbg.apps.googleusercontent.com",
        clientSecret: "jn5jfQ8U_WIe6ebtafoeaROq",
        callbackURL: "http://localhost:1337/auth/google/callback"
      }, googleHandler ));

      /*passport.use(new LinkedInStrategy({
        clientID:"",
        clientSecret: "",
        callbackURL: "http://localhost:1337/auth/linkedin/callback",
        scope: ['r_emailaddress', 'r_basicprofile'],
        state: true
      }, linkedinHandler )); */

      app.use(passport.initialize());
      app.use(passport.session());
    }
  };