/**
 * Route Mappings
 * (sails.config.routes)
 *
 * Your routes map URLs to views and controllers.
 *
 * If Sails receives a URL that doesn't match any of the routes below,
 * it will check for matching files (images, scripts, stylesheets, etc.)
 * in your assets directory.  e.g. `http://localhost:1337/images/foo.jpg`
 * might match an image file: `/assets/images/foo.jpg`
 *
 * Finally, if those don't match either, the default 404 handler is triggered.
 * See `api/responses/notFound.js` to adjust your app's 404 logic.
 *
 * Note: Sails doesn't ACTUALLY serve stuff from `assets`-- the default Gruntfile in Sails copies
 * flat files from `assets` to `.tmp/public`.  This allows you to do things like compile LESS or
 * CoffeeScript for the front-end.
 *
 * For more information on configuring custom routes, check out:
 * http://sailsjs.org/#!/documentation/concepts/Routes/RouteTargetSyntax.html
 */

module.exports.routes = {

  /***************************************************************************
  *                                                                          *
  * Make the view located at `views/homepage.ejs` (or `views/homepage.jade`, *
  * etc. depending on your default view engine) your home page.              *
  *                                                                          *
  * (Alternatively, remove this and add an `index.html` file in your         *
  * `assets` directory)                                                      *
  *                                                                          *
  ***************************************************************************/

  'GET  /' : 'AuthController.login',

  'GET /login' : 'AuthController.login',
  'POST /login' : 'AuthController.localLogin',
 
  
  'GET /logout' : 'AuthController.logout',
  'GET /register' : {
                      locals: {
                          layout: 'guest-layout'
                      },
                      view:'auth/register'
                    },
  
  'POST /register' : 'AuthController.register',  
  'GET /auth/facebook' : 'AuthController.facebook',
  'GET /auth/facebook/callback' : 'AuthController.facebookCallback',
  'GET /auth/google' : 'AuthController.google',
  'GET /auth/google/callback' : 'AuthController.googleCallback',
  'GET /auth/linkedin' : 'AuthController.linkedin',
  'GET /auth/linkedin/callback' : 'AuthController.linkedinCallback',

  'GET /home' : 'HomeController.index',
  'GET /app'  : 'HomeController.app',
  
   
  'POST /project': "ProjectController.create",
  'GET /project': "ProjectController.get",
  'GET /project/:id': "ProjectController.getById",
  'DELETE /project/:id' : "ProjectController.delete",
  'PUT /project/:id' : "ProjectController.update",

};