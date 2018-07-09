global.ValidationException = function(msg,errors,code){
	var response = {};
	response.status = 400;
	if(code) response.code = code;
	if(msg) response.msg = msg;
   response.errors = errors;
	return response;
}