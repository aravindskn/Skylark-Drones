var bcrypt = require('bcrypt-nodejs');


function hashPassword (passport, next) {
  var salt = 8
  if (passport.password) {
    bcrypt.hash(passport.password, null,null, function (err, hash) {
      if (err) {
        delete passport.password;
        sails.log.error(err);
        throw err;
      }
      passport.password = hash;
      next(null, passport);
    });
  }
  else {
    next(null, passport);
  }
}


module.exports = {

  attributes: {
	    provider: 'STRING',
	    uid: 'STRING',
	    name: 'STRING',
	    email: 'STRING',
	    firstname: 'STRING',
	    lastname: 'STRING',
	    password: { type: 'string', minLength: 5 },
	    validatePassword: function (password, next) {
	      	bcrypt.compare(password, this.password, next);
	    }
	},
	beforeCreate: function (passport, next) {	
    	hashPassword(passport, next);
	},

	beforeUpdate: function (passport, next) {
    	hashPassword(passport, next);
	}
}

