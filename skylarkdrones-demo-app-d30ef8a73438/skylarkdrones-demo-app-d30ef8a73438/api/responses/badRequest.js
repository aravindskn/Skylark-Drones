
module.exports = function badRequest(data, options) {

  var req = this.req;
  var res = this.res;
  var sails = req._sails;

  // Set status code
  res.status(400);
  delete data.status
  // Log error to console
  if (data !== undefined) {
    sails.log.verbose('Sending 400 ("Bad Request") response: \n',data);
  }
  else sails.log.verbose('Sending 400 ("Bad Request") response');

  if (req.wantsJSON || sails.config.hooks.views === false) {
    return res.jsonx(data);
  }

  options = (typeof options === 'string') ? { view: options } : options || {};

  var viewData = data;
  if (options.view) {
    return res.view(options.view, { data: viewData, title: 'Bad Request' });
  }else{ 
    return res.guessView({ data: viewData, title: 'Bad Request' }, 
            function couldNotGuessView () {
              return res.jsonx(data);
    });
  }
};

